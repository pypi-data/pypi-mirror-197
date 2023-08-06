
import numpy as np

from ..auxillary import dist_computer


def exp_kernel(x1, x2, sigma=1):
    K = dist_computer(x1, x2)
    K[K <= 0] = 0
    np.sqrt(K, out=K)
    K /= -sigma
    np.exp(K, out=K)
    return K


def rbf_kernel(x1, x2, sigma=0.1):
    if len(x1.shape) == 1:
        x1 = x1[:, np.newaxis]
    if len(x2.shape) == 1:
        x2 = x2[:, np.newaxis]
    K = dist_computer(x1, x2)
    K /= - sigma**2
    np.exp(K, out=K)
    return K


def rbf_periodic(x1, x2, sigma=0.1):
    if len(x1.shape) == 1:
        x1 = x1[:, np.newaxis]
    if len(x2.shape) == 1:
        x2 = x2[:, np.newaxis]
    tmp = x1[:, np.newaxis, :] - x2[np.newaxis, :, :]
    tmp %= 2
    tmp = np.minimum(tmp, 2 - tmp)
    tmp **= 2
    K = np.sum(tmp, axis=-1)
    K *= -1
    K /= sigma**2
    np.exp(K, out=K)
    return K
