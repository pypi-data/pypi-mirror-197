import jax
import numpy as np
from jax import numpy as jnp
import nn


import torch

import unittest


def allclose(a, b):
    return jnp.allclose(a,b)#, atol=1e-4, rtol=1e-4)



class MyModule:
    def __new__(cls, vocab, embed, dim1, dim2, dim3=1, return_torch=False):

        with nn.set_return_torch(return_torch):
            organizer = nn.StateOrganizer()

            organizer.embed = nn.Embedding(vocab, embed)
            organizer.seq = nn.Sequential(nn.Linear(embed, dim1), nn.Linear(dim1, dim2))

            t_mul = torch.normal(torch.ones(dim2))
            j_mul = t_mul.numpy()
            organizer.register_buffer('mul', j_mul, t_mul)

            organizer.fc2 = nn.Linear(dim2, dim3)

        return organizer.create_module(cls, MyTModule(organizer), return_torch)



    def apply(module, state, x):

        module = module(state)

        x = module.embed(x)
        x = module.seq(x)
        x = module.mul * x
        x = module.fc2(x)

        return x


class MyTModule(nn.TModule):

    def forward(self, x):
        x = self.embed(x)
        x = self.seq(x)
        x = self.mul * x
        x = self.fc2(x)
        return x




class NextModule:

    def __new__(cls, vocab, embed, dim_next, dim_out, return_torch=False):

        organizer = nn.StateOrganizer()

        organizer.trunk = MyModule(vocab, embed, 10, 20, dim_next, return_torch=return_torch)

        t_bias = torch.normal(torch.zeros(dim_next))
        t_bias.requires_grad = True
        j_bias = t_bias.detach().numpy()
        
        organizer.register_parameter('next_bias', j_bias, t_bias)

        organizer.head = nn.Linear(dim_next, dim_out, return_torch=return_torch)

        return organizer.create_module(cls, NextTModule(organizer), return_torch)



    def apply(module, state, x):
        module = module(state)


        x = module.trunk(x)
        x = jax.nn.relu(x)
        x = module.next_bias + x
        x = jax.nn.relu(x)
        x = module.head(x)

        return x


class NextTModule(nn.TModule):

    def forward(self, x):
        x = self.trunk(x)
        x = torch.nn.functional.relu(x)
        x = self.next_bias + x
        x = torch.nn.functional.relu(x)
        x = self.head(x)

        return x


class TestNN(unittest.TestCase):



    def test_identity(self):
        state, apply, t_state, t_module = nn.Identity(return_torch=True)

        x = jnp.array([[1,2,3],[5,6,6],[7,8,9]], dtype=float)
        x_t = torch.tensor(np.array(x))

        y = apply(state, x)

        y_t = t_module(x_t).numpy()

        self.assertTrue(allclose(y_t, y))



    def test_linear(self):
        state, apply, t_state, t_module = nn.Linear(3, 2, bias=False, return_torch=True)

        x = jnp.array([[1,2,3],[5,6,6],[7,8,9]], dtype=jnp.float32)
        x_t = torch.tensor(np.array(x))

        y = apply(state, x)
        y_t = t_module(x_t).detach().numpy()

        self.assertTrue(allclose(y_t, y))


    def test_conv2d(self):
        state, apply, t_state, t_module = nn.Conv2d(3, 4, 5, padding='same', bias=True, return_torch=True)

        x = jnp.array(np.random.normal(np.ones((2, 3, 6,7))), dtype=jnp.float32)
        x_t = torch.tensor(np.array(x))

        y = apply(state, x)
        y_t = t_module(x_t).detach().numpy()

        self.assertTrue(allclose(y_t, y))



    def test_embedding(self):
        state, apply, t_state, t_module = nn.Embedding(30, 10, return_torch=True)

        x = jnp.array([0, 2, 29, 7, 4])
        x_t = torch.tensor(np.array(x))

        y = apply(state, x)

        y_t = t_module(x_t).detach().numpy()


        self.assertTrue(allclose(y_t, y))

    def test_sequential(self):
        chain = [
            nn.Linear(3, 10, return_torch=True),
            nn.Linear(10,20, bias=False, return_torch=True),
            nn.Linear(20,3, return_torch=True)
        ]
        state, apply, t_state, t_module = nn.Sequential(*chain, return_torch=True)

        x = jnp.array([[1,2,3],[5,6,6],[7,8,9]], dtype=float)
        x_t = torch.tensor(np.array(x))

        y = apply(state, x)

        y_t = t_module(x_t).detach().numpy()


        self.assertTrue(jnp.allclose(y_t, y))

        
    def test_layer_norm(self):
        state, apply, t_state, t_module = nn.LayerNorm(3, return_torch=True)


        x = jnp.array([[1,2,3],[5,6,6],[7,8,9]], dtype=float)
        x_t = torch.tensor(np.array(x))

        y = apply(state, x)

        y_t = t_module(x_t).detach().numpy()


        self.assertTrue(jnp.allclose(y_t, y))      


    def test_nested_modules(self):

        state, _, t_state, t_module = NextModule(5, 10, 20, 2, return_torch=True)

        _, apply = NextModule(5, 10, 20, 2, return_torch=False)

        x = jnp.ones(10, dtype=int)
        x_t = torch.tensor(np.array(x))

        y = apply(state, x)

        y_t = t_module(x_t).detach().numpy()


        self.assertTrue(jnp.allclose(y_t, y))  



if __name__ == 'main':
    unittest.main()

