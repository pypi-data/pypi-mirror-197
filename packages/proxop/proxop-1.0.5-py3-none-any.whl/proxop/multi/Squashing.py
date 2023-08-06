"""
Version : 1.0 (08-09-2022).

Author  : Mbaye DIONGUE

Copyright (C) 2022

This file is part of the codes provided at http://proximity-operator.net

By downloading and/or using any of these files, you implicitly agree to
all the terms of the license CeCill-B (available online).
"""

from typing import Optional
import numpy as np


class Squashing:
    r"""Compute the proximity operator of the Squashing activation function.

    The squashing activation function is definded as:

           /  mu*arctan(sqrt(||x||/(mu - ||x||))-sqrt(||x|(mu-||x||) - x^2  if ||x||<mu
    f(x)= |  mu*( pi - mu )/2                                               if ||x||=mu
          \  +INF                                                           otherwise

        with mu = 8/(3*sqrt(3))

    Note: The proximity operator of this function f is the squashing function
    defined as:

            Squashing(y) = ( mu * ||y||/(1 +||y||) ) y

     INPUTS
    ========
     x     - ND array (np.ndarray)

     axis      - None or int, axis of block-wise processing [default: axis=None]
                  axis = None --> 'x' is processed as a single vector [DEFAULT] In this
                  case 'gamma' must be a scalar.
                  axis >=0   --> 'x' is processed block-wise along the specified axis
                  (0 -> rows, 1-> columns ect. In this case, 'gamma' must be singleton
                  along 'axis'.
    """

    def __init__(self, axis: Optional[int] = None):
        self.mu = 8 / (3 * np.sqrt(3))
        self.axis = axis

    def prox(self, x: np.ndarray) -> np.ndarray:
        mu = self.mu
        shape_sum = np.array(np.shape(x), dtype=int)
        shape_sum[self.axis] = 1
        l2_x = np.linalg.norm(x, ord=2, axis=self.axis).reshape(tuple(shape_sum))
        prox_x = (mu * l2_x / (1 + l2_x ** 2)) * x
        return prox_x

    def __call__(self, x: np.ndarray) -> float:
        if np.size(x) <= 1:
            x = np.reshape(x, (-1))
        mu = self.mu
        shape_sum = np.array(np.shape(x), dtype=int)
        shape_sum[self.axis] = 1
        l2_x = np.linalg.norm(x, ord=2, axis=self.axis).reshape(tuple(shape_sum))

        fun_x = mu * (np.pi - mu) / 2 * np.ones(np.shape(l2_x))
        fun_x[l2_x > mu] = np.inf
        mask = l2_x < mu
        fun_x[mask] = (
                mu * np.arctan(np.sqrt(l2_x[mask]) / (mu - l2_x[mask]))
                - np.sqrt(l2_x[mask] * (mu - l2_x[mask]))
                - 0.5 * l2_x[mask] ** 2
        )
        return np.sum(fun_x)
