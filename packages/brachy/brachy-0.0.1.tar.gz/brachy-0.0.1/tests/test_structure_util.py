import jax
import numpy as np
from jax import numpy as jnp
from brachy import nn
from brachy import rng_util

from tempfile import TemporaryFile
# from jax.tree_util import tree_map, tree_reduce

from jax._src.typing import Array, ArrayLike, DType, DTypeLike
from typing import overload, Any, Callable, Literal, Optional, Sequence, Tuple, Union

import einops

import pprint
import torch

from brachy import structure_util as su


import unittest

def same_dicts(*to_compare, keys_to_exclude=[]):
    if len(to_compare) == 0:
        return True
    
    keys = set(to_compare[0].keys())

    for d in to_compare[1:]:
        if set(d.keys()) != keys:
            return False

    for key in keys:
        if key in keys_to_exclude:
            continue
        value = to_compare[0][key]

        for d in to_compare[1:]:
            comp_value = d[key]

            if type(value) != type(comp_value):
                return False

            if isinstance(value, Array) or isinstance(value, np.ndarray):
                if value.shape != comp_value.shape:
                    return False
                if not jnp.allclose(value, comp_value):
                    return False
                continue

            if not isinstance(value, dict):
                if value != comp_value:
                    return False
                continue
            
            if not same_dicts(value, comp_value, keys_to_exclude=keys_to_exclude):
                return False

    
    return True



def same_trees(*trees, keys_to_exclude=[]):
    for tree in trees:
        if not su.is_structure_tree(tree, recurse=True):
            return False

    return same_dicts(*trees,keys_to_exclude=keys_to_exclude)





def apply(tree, global_config, x, y):
    value = tree['params']['a'] + x -y
    split = tree.filter_keys(['params', 'buffers'])
    return tree, value

def apply_child(tree, global_config, x, y):
    value = 3*tree['params']['f'] + tree['buffers']['g'] + x -y
    split = tree.filter_keys(['params', 'buffers'])
    return tree, value

def apply_grand_child(tree, global_config, x, y):
    value = -1*tree['params']['f'] + tree['buffers']['g'] + x -y
    split = tree.filter_keys(['params', 'buffers'])
    return tree, value

grand_child = {
    'params': {
        'f': jnp.zeros((2,3)),
    },
    'buffers': {
        'g': jnp.array([[33,99,3],[5,6,7]])
    },
    'aux': {
        'comment': 'this is a grand child node',
    },
    'apply': apply_grand_child,
    'submodules': {}
}


child = {
    'params': {
        'f': jnp.zeros((1,3)),
    },
    'buffers': {
        'g': jnp.array([[1,99,3],[5,6,7]])
    },
    'aux': {
        'comment': 'this is a child node',
    },
    'apply': apply_child,
    'submodules': {
        'g': grand_child
    }
}

tree = {
    'params': {
        'a': jnp.ones(4),
        'b': jnp.zeros((1,2,1)),
    },
    'buffers': {
        'x': jnp.array([[1,2,3],[5,6,7]])
    },
    'aux': {
        'comment': 'this is some text',
        4: 234
    },
    'apply': apply,
    'submodules': {
        'c': child
    }
}

params = {
    'params': {
        'a': jnp.ones(4),
        'b': jnp.zeros((1,2,1)),
    },
    'submodules': {
        'c': {
            'params': {
                'f': jnp.zeros((1,3))
            },
            'submodules': {
                'g': {
                    'params': {
                        'f': jnp.zeros((2,3)),
                    },
                    'submodules': {}
                }
            }
        }
    }
}


buffers = {
    'buffers': {
        'x': jnp.array([[1,2,3],[5,6,7]])
    },
    'submodules': {
        'c': {
            'buffers': {
                'g': jnp.array([[1,99,3],[5,6,7]])
            },
            'submodules': {
                'g': {
                    'buffers': {
                        'g': jnp.array([[33,99,3],[5,6,7]])
                    },
                    'submodules': {}
                }
            }
        }
    }
}

apply_aux = {
    'apply': apply,
    'aux': {
        'comment': 'this is some text',
        4: 234
    },
    'submodules': {
        'c': {
            'apply': apply_child,
            'aux': {
                'comment': 'this is a child node',
            },
            'submodules': {
                'g': {
                    'apply': apply_grand_child,
                    'aux': {
                        'comment': 'this is a grand child node',
                    },
                    'submodules': {}
                }
            }
        }
    }
}


def grandchild_module():
    global_config = {
        'test_override': 'grandchild',
        'test_override_grandchild': 'g',
        'unique_grandchild': 'g',
    }


    params = {
        'w': jnp.array([1,2,3,4,5])
    }
    buffers = {
        'g': jnp.array([-1,-1,-1,-1,3])
    }
    aux = {
        'description': 'grandchild module'
    }

    tree = {
        'params': params,
        'buffers': buffers,
        'aux': aux,
        'apply': grandchild_apply,
        'submodules': {}
    }

    return tree, global_config

def grandchild_apply(tree, global_config, x):
    w = tree['params']['w']
    g = tree['buffers']['g']

    y = x*w + g

    assert global_config['test_override'] == 'root'
    assert global_config['unique_child'] == 'c'

    return su.filter_keys(tree), y


def child_module(p):
    global_config = {
        'test_override': 'child',
        'unique_child': 'c'
    }

    organizer = su.StateOrganizer(global_config=global_config)

    organizer.update_global_config({'test_override_grandchild': 'c'})

    organizer.gc = grandchild_module()

    organizer.w = jnp.array([p])

    return organizer.create_module(child_apply)


def child_apply(tree, global_config, x):

    organizer = su.StateOrganizer(tree, global_config)

    assert organizer.get_global_config('unique_grandchild') == 'g'
    assert organizer.get_global_config('test_override') == 'root'

    y = organizer.gc(x)

    y = y * organizer.w

    return organizer.get_state(), y


def root_module():

    organizer = su.StateOrganizer()
    organizer.update_global_config('test_override', 'root')
    organizer.register_buffer('a', jnp.array([1,1,1,3,3]))

    for k in range(1,4):
        organizer.register_submodule(k, child_module(k))

    return organizer.create_module(root_apply)

def root_apply(tree, global_config, x):

    organizer = su.StateOrganizer(tree, global_config)

    assert organizer.get_global_config('test_override_grandchild') ==  'c'

    y1 = organizer[1](x)
    y2 = organizer[2](y1)
    y3 = organizer[3](x)

    y_final = y1+y2+y3 + organizer.a

    organizer.a = jnp.array([1,1,1,2,2])

    return organizer.get_state(), y_final

def alt_root_apply(tree, global_config, x):

    organizer = su.StateOrganizer(tree, global_config)

    assert organizer.get_global_config('test_override_grandchild') ==  'c'

    y1 = organizer[1](x)
    y2 = organizer[2](y1)
    y3 = organizer[3](x)

    y_final = y1+y2+y3 + organizer.a

    return organizer.get_state(), y_final

    
    

class TestStructureUtils(unittest.TestCase):


    def test_submodule_access(self):
        @su.organized_init
        def mutating_state(organizer, n):
            organizer.foo = jnp.array(range(n))
            return organizer.set_apply(mutating_apply)

        @su.organized_apply
        def mutating_apply(organizer, x):
            # organizer = su.StateOrganizer(tree, global_config)
            y = x * organizer.foo

            organizer.foo = 2 + organizer.foo

            # return organizer.get_state(), y
            return y

        @su.organized_init_with_rng
        def outer(organizer, rng=None):
            organizer.bar = jnp.ones(5)
            organizer.register_aux('random', rng_util.uniform(shape=(2,2)))
            organizer.submodule = mutating_state(5)

            organizer.set_forward(outer_apply)
        
        @su.organized_apply
        def outer_apply(organizer, x):
            # organizer = su.StateOrganizer(tree, global_config)
            y = x + organizer.bar
            y = organizer.submodule(y)
            y = organizer.submodule.foo + y

            return y

        rng_util.init_rng(0)
        tree, global_config = outer()

        rng0 = jax.random.PRNGKey(0)

        _, subkey = jax.random.split(rng0)
        _, subkey = jax.random.split(subkey)


        assert jnp.allclose(tree['aux']['random'], jax.random.uniform(subkey, shape=(2,2)))

        state, apply = su.bind_module(tree, global_config)

        x = jnp.zeros(5)

        state, y = apply(state, x)

        state, y2 = apply(state, x)

        assert jnp.allclose(y, jnp.array([2, 4, 6, 8, 10]))

        assert jnp.allclose(y2, jnp.array([6, 8, 10, 12, 14]))
        


    def test_organizer_update(self):
        tree, g_config = root_module()
        tree['apply'] = alt_root_apply

        organizer = su.StateOrganizer(tree, g_config)

        x = jnp.ones(5)

        y = organizer(x)

        new_tree = organizer.get_state()

        assert jnp.allclose(y, jnp.array([-1, 7, 19, 37, 121]))
        assert same_trees(tree, new_tree, keys_to_exclude=['apply'])


    def test_empty_tree(self):
        emptied_tree_ref = {
            'params': {},
            'buffers': {},
            'aux': {},
            'apply': lambda t, g, x: x,
            'submodules': {
                'c': {
                    'params': {},
                    'buffers': {},
                    'aux': {},
                    'apply': lambda t, g, x: x,
                    'submodules': {
                        'g': {
                            'params': {},
                            'buffers': {},
                            'aux': {},
                            'apply': lambda t, g, x: x,
                            'submodules': {},
                        }

                    }
                }
            }
        }

        emptied_tree = su.empty_tree(tree)

        assert same_trees(emptied_tree, emptied_tree_ref, keys_to_exclude=['apply']), f"reference empty tree:\n{emptied_tree_ref}\nReturned empty tree:\n{emptied_tree}"


        min_empty_ref = {
            'params': {},
            'buffers': {},
            'aux': {},
            'apply': lambda t, g, x: x,
            'submodules': {}
        }
        min_empty = su.empty_tree()
        assert same_trees(min_empty, min_empty_ref, keys_to_exclude=['apply']), f"reference empty tree:\n{min_empty_ref}\nReturned empty tree:\n{min_empty}"

    def test_map_params_buffers(self):
        tree = {
            'params': {
                'a': {'p': jnp.array(0)},
                'b': jnp.array([1,2])
            },
            'buffers': {'p': jnp.array(0)},
            'aux': {},
            'apply': None,
            'submodules': {
                'k': {
                    'params': {
                        'b': {'l': jnp.array([4,3])}
                    },
                    'buffers': {'l': jnp.array(3)},
                    'aux': {},
                    'apply': None,
                    'submodules': {}
                }
            }
        }

        expected = {
            'params': {
                'a': {'p': jnp.array(1)},
                'b': jnp.array([2,3])
            },
            'buffers': {'p': jnp.array(1)},
            'aux': {},
            'apply': None,
            'submodules': {
                'k': {
                    'params': {
                        'b': {'l': jnp.array([5,4])}
                    },
                    'buffers': {'l': jnp.array(4)},
                    'aux': {},
                    'apply': None,
                    'submodules': {}
                }
            }
        }

        mapped = su.map_params_buffers(lambda x: x+1, tree)

        assert same_dicts(mapped,  expected)



    def test_tree_alteration(self):
        # this will probably fail if test_organizer fails because I am lazy.
        tree, g_config = root_module()

        tree_2, g_config_2 = root_module()

        tree['submodules'][3] = tree_2

        params, module = su.bind_module(tree, g_config)
        module = jax.jit(module)

        reconstructed_tree, _ = su.unbind_module(params, module)

        assert same_trees(tree, reconstructed_tree)

        x = jnp.ones(5)

        next_params, y_first = module(params, x)

        next_params, y_second = module(next_params, x)

        assert jnp.allclose(y_first, jnp.array([-2, 11, 32, 65, 218]))

        assert jnp.allclose(y_second, jnp.array([-2, 11, 32, 63, 216]))


    def test_jit_autostatic(self):


        trace_count = 0
        jit  = su.improved_static(jax.jit)

        @jit
        def foo(x,y):
            nonlocal trace_count
            trace_count += 1
            if x['q'] == 'go ahead!':
                return {'a': x['a'], 'b': y['b']}
            else:
                return {'a': 2*y['a'], 'b': y['b']}

        x = {
            'q': 'stop',
            'a': jnp.ones(3)
        }
        y = {
            'a': jnp.ones(5),
            'b': ['hello', 'friend']
        }

        z = foo(x,y)
        x['a'] = jnp.zeros(3)
        w = foo(x,y)

        assert jnp.allclose(z['a'], jnp.array([2.0,2.0,2.0,2.0,2.0]))
        assert z['b'][0] == 'hello'
        assert z['b'][1] == 'friend'
        assert trace_count == 1

    def test_jit_tree(self):

        trace_count = 0

        @su.improved_static(jax.jit)
        def func(tree, global_config, x):
            nonlocal trace_count
            trace_count += 1
            organizer = su.StateOrganizer(tree, global_config)
            y = jnp.matmul(x, organizer.weight)+ organizer.bias
            return organizer.get_state(), y

        lin, global_config = nn.Linear(5,5, rng=jax.random.PRNGKey(0))
        global_config['foo'] = 'hihihi'
        lin['params']['weight'] = jnp.eye(5)
        lin['params']['bias'] = jnp.ones(5)
        x = jnp.ones(5)


        lin, y = func(lin, global_config, x)
        lin, y = func(lin, global_config, x)

        assert jnp.allclose(y, 2*jnp.ones(5)), f"y was: {y}"
        assert trace_count == 1, f"trace count was: {trace_count}"

        def loss(tree, global_config, x):
            state, y = func(tree, global_config, x)
            return state, jnp.sum(y**2)

        loss = su.jit(loss, static_argnums=1)


        value_and_grad = su.tree_value_and_grad(loss)
        (lin, value), grad = value_and_grad(lin, global_config, x)

        assert jnp.allclose(value, 20)
        assert jnp.allclose(grad['params']['bias'], 2*2*jnp.ones(5)), f"bias: {grad['params']['bias']}"
        assert jnp.allclose(grad['params']['weight'], 2*2*jnp.ones((5,5))), f"bias: {grad['params']['bias']}"


        def non_jittable_loss(tree, global_config, x):
            organizer = su.StateOrganizer(tree, global_config)
            y = jnp.matmul(x, organizer.weight)+ organizer.bias
            return organizer.get_state(), jnp.sum(y**2)

        value_and_grad = su.tree_value_and_grad(non_jittable_loss)
        (update, value), grad = value_and_grad(lin, global_config, x)

        assert jnp.allclose(value, 20)
        assert jnp.allclose(grad['params']['bias'], 2*2*jnp.ones(5)), f"bias: {grad['params']['bias']}"
        assert jnp.allclose(grad['params']['weight'], 2*2*jnp.ones((5,5))), f"bias: {grad['params']['bias']}"

    def test_jit_static_return(self):

        trace_count = 0

        def func(tree, global_config, x, z):
            nonlocal trace_count
            trace_count += 1
            organizer = su.StateOrganizer(tree, global_config)
            y = jnp.matmul(x, organizer.weight)+ organizer.bias
            return organizer.get_state(), global_config, z

        j_func = su.jit(func, static_argnums=3, static_returns=2)

        lin, global_config = nn.Linear(5,5, rng=jax.random.PRNGKey(0))
        lin['aux'] = {
            'number': 10
        }
        global_config['foo'] = 'hihihi'
        lin['params']['weight'] = jnp.eye(5)
        lin['params']['bias'] = jnp.ones(5)
        x = jnp.ones(5)
        z= {'f': 0, 'g': False}

        state, y, z = j_func(lin, global_config, x, z)
        # state, y, z = j_func(lin, global_config, x, z)

        assert state['aux']['number'] == 10
        assert not isinstance(state['aux']['number'], Array)

        assert z['g'] == False
        assert z['f'] == 0
        assert not isinstance(z['f'], Array)



    def test_jit_notree(self):

        trace_count = 0

        def func(x, y, z, w, q):
            nonlocal trace_count
            trace_count += 1
            if z['x']['y']:
                return x + w[3] + q
            else:
                if y['a']:
                    return -x - w[1] - q
                else:
                    return x
        jit = su.improved_static(jax.jit)
        j_func = jit(func, static_argnums=1, static_argnames=('z','w'))

        x = jnp.ones(1)
        other_x = jnp.zeros(1)
        q = jnp.ones(1)
        other_q = jnp.zeros(1)
        y = {
            'a': True
        }
        z = {
            'x': {
                'y': True
            }
        }
        w = [1,2,3,4]

        a = j_func(x, y, z, w, q)
        assert jnp.allclose(a, 6), f"a value: {a}"
        assert trace_count == 1, f"trace count: {trace_count}"

        a = j_func(other_x, y, z, w, other_q)
        assert jnp.allclose(a, 4), f"a value: {a}"
        assert trace_count == 1, f"trace count: {trace_count}"

        z['x']['y'] = False

        a = j_func(other_x, y, z, w, other_q)
        assert jnp.allclose(a, -2), f"a value: {a}"
        assert trace_count == 2, f"trace count: {trace_count}"

        other_y = {
            'a': True
        }

        other_z ={
            'x': {
                'y': False
            }
        }

        a = j_func(other_x, other_y, other_z, w, other_q)
        assert jnp.allclose(a, -2), f"a value: {a}"
        assert trace_count == 2, f"trace count: {trace_count}"

        other_z['p'] = 5
        a = j_func(other_x, other_y, other_z, w, other_q)
        assert jnp.allclose(a, -2), f"a value: {a}"
        assert trace_count == 3, f"trace count: {trace_count}"

        a = j_func(other_x, other_y, z=other_z, w=w, q=other_q)
        assert jnp.allclose(a, -2), f"a value: {a}"
        assert trace_count == 4, f"trace count: {trace_count}"

        other_y['a'] = False
        a = j_func(other_x, other_y, z=other_z, w=w, q=other_q)
        assert jnp.allclose(a, 0), f"a value: {a}"
        assert trace_count == 5, f"trace count: {trace_count}"


        other_y = {
            'a': False
        }
        a = j_func(x, other_y, z=other_z, w=w, q=other_q)
        assert jnp.allclose(a, 1), f"a value: {a}"
        assert trace_count == 5, f"trace count: {trace_count}"



    def test_is_jax_tree(self):
        complex_no = {'p': jax.tree_util.Partial(su.is_jax_tree), 'l': {'p': jax.random.PRNGKey(8), 'm': jax.numpy.array([1,2,3,4]), 'o': 'p'}, 'p': 0}
        complex_yes = {'p': jax.tree_util.Partial(su.is_jax_tree), 'l': {'p': jax.random.PRNGKey(8), 'm': jax.numpy.array([1,2,3,4]), 'o': False}, 'p': 0, 'n': None}
        simple_no = 'p'
        simple_yes = jnp.array([1])

        assert not su.is_jax_tree(complex_no)
        assert not su.is_jax_tree(simple_no)
        assert su.is_jax_tree(complex_yes)
        assert su.is_jax_tree(simple_yes)

    def test_organizer(self):
        tree, g_config = root_module()

        x = jnp.ones(5)

        params, module = su.bind_module(tree, g_config)

        module = jax.jit(module)

        reconstructed_tree, _ = su.unbind_module(params, module)

        assert same_trees(tree, reconstructed_tree)

        next_params, y_first = module(params, x)


        next_params, y_second = module(next_params, x)

        assert jnp.allclose(y_first, jnp.array([-1, 7, 19, 37, 121]))

        assert jnp.allclose(y_second, jnp.array([-1, 7, 19, 36, 120]))



    def test_split_merge_filter(self):

        s_params, s_buffers, s_apply_aux = su.split_tree(tree, ['params', 'buffers', ['apply', 'aux']])

        merged = su.merge_trees(s_params, s_buffers, s_apply_aux)

        limited_merged = su.merge_trees(s_params, s_buffers, s_apply_aux, keys_to_merge=['params', 'buffers'])
        filtered = su.filter_keys(tree)



        def new_apply(tree, global_config, x, y):
            value = tree['params']['b'] * x / y
            split = tree.filter_keys(['params', 'buffers'])
            return split, value

        def new_child_apply(tree, global_config, x, y):
            value = tree['params']['f'] * x / y
            split = tree.filter_keys(['params', 'buffers'])
            return split, value

        def new_grand_child_apply(tree, global_config, x, y):
            value = tree['buffers']['g'] * x / y
            split = tree.filter_keys(['params', 'buffers'])
            return split, value

        


        self.assertTrue(same_dicts(params, s_params))
        self.assertTrue(same_dicts(buffers, s_buffers))
        self.assertTrue(same_dicts(apply_aux, s_apply_aux))

        self.assertTrue(same_trees(merged, tree))

        self.assertTrue(same_dicts(limited_merged, filtered))


    def test_checkpoint_save(self):

        fp = TemporaryFile()

        tree, global_config = root_module()

        su.checkpoint.save(tree, global_config, fp)

        fp.seek(0)

        l_tree, l_global_config = su.checkpoint.load(fp)

        fp.close()

        x = jnp.ones(5)

        update, y = su.apply_tree(tree, global_config, x)
        tree = su.merge_trees(tree, update)

        update, l_y = su.apply_tree(l_tree, global_config, x)
        l_tree = su.merge_trees(l_tree, update)



        update, y = su.apply_tree(tree, global_config, x)
        tree = su.merge_trees(tree, update)

        update, l_y = su.apply_tree(l_tree, global_config, x)
        l_tree = su.merge_trees(l_tree, update)

        
        assert jnp.allclose(y, l_y)
        assert same_trees(tree, l_tree, keys_to_exclude=['apply'])

    def test_organizer_multiple_return_values(self):

        organizer = su.StateOrganizer()

        organizer.set_apply(lambda t, g, x: (t, x, 1,2,3))

        x,y,z, w = organizer(4)

        assert x==4
        assert y==1
        assert z==2
        assert w==3
