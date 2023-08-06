"""
Created on Mon Jun 13 2022.

@author: mbaye diongue
"""
import numpy as np


def pava_python(x):
    """Compute the proximity operator of  the monotone Cone.

       S(j,k,:) = sum( x(j:k,:) ) / (k-j+1)

    for every 'j' and 'k' in {1,...,N}, where N = size(x,1).
    """
    N = np.size(x, 0)

    res = np.zeros(np.size(x))
    cum_sum = np.reshape(1 + np.arange(N**2) % N, (N, N))
    cum_sum = 1 + cum_sum - np.arange(1, N+1).reshape((N, 1))
    cum_sum = np.cumsum(x) / cum_sum
    for n in range(N):
        max_sum = -np.inf
        for j in range(n+1):
            min_sum = np.min( cum_sum, axis=1) 
            if min_sum > max_sum:
                max_sum = min_sum
        res[n] = max_sum
    return res
