"""
Version : 1.0 ( 08-09-2022).

Author  : Mbaye Diongue

Copyright (C) 2022

This file is part of the codes provided at http://proximity-operator.net

By downloading and/or using any of these files, you implicitly agree to
all the terms of the license CeCill-B (available online).
"""

from typing import Optional
import numpy as np


class SoftmaxActi:
    r"""Compute the proximity operator of the softmax activation function.

    The softmax activation function is defined as:

               / \sum_{k=1}^{N}( x_k log(x_k) - x_k^2/2 ) if (x_1,...,x_N) \in [0,1]^N
         f(x)=|                                           and \sum_{k=1}^{N} x_k =1
              \  + inf                                    otherwise

    Note: The proximity operator of this function f is the (shifted) softmax function
    defined as:

        softmax(x) = ( exp(x_k) / ( \sum_{k=1}^{N}exp(x_k) )_{1<=k<=N) - u

    where u = (1,...,1).T a vector which have all components equal to 1

     INPUTS
    ========
     x         - ND array

     axis    - None or int, axis of block-wise processing [default: axis=None]
                  axis = None --> 'x' is processed as a single vector [DEFAULT] In this
                  case 'gamma' must be a scalar.
                  axis >=0   --> 'x' is processed block-wise along the specified axis
                  (0 -> rows, 1-> columns ect. In this case, 'gamma' must be singleton
                  along 'axis'.

     tol   - float, default: tol=1e-10
            Precision tolerance (for example if |x_i| < tol x_i is assumed
            to be null)
     """

    def __init__(self, axis: Optional[int] = None, tol: float = 1e-10):
        self.axis = axis
        self.tol = tol

    def prox(self, x: np.ndarray) -> np.ndarray:
        exp_x = np.exp(x - np.max(x))  # for numerical stability purpose
        shape_x = np.shape(x)
        shape_sum = np.array(shape_x, dtype=int)
        shape_sum[self.axis] = 1
        prox_x = exp_x / exp_x.sum(axis=self.axis).reshape(shape_sum) - np.ones(shape_x)
        return prox_x

    def __call__(self, x: np.ndarray) -> float:
        if np.size(x) <= 1:
            x = np.reshape(x, (-1))

        def fun_phi(t):
            if np.any(t > 1) or np.any(t < 0) or \
                    np.any(np.abs(np.sum(t, self.axis) - 1) > self.tol):
                return np.inf
            phi_t = np.zeros(np.shape(t))
            mask = t > 0
            phi_t[mask] = t[mask] * np.log(t[mask])
            return np.sum(phi_t - 0.5 * t ** 2, axis=self.axis)

        fun_x = fun_phi(x + 1.0) + np.sum(x, self.axis)
        return np.sum(fun_x)
