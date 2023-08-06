import numpy as np

from .io import write_numpy_file
from .linalg import column_updated_inverse


def training_and_error_computation(
    nb_exp, func, n_train, sigma, lambd, x_test, y_test, save_file, kernel, verbose=True
):
    error = np.empty(n_train - 1)
    for j in range(nb_exp):
        # training dataset
        x_train = 2 * np.random.rand(n_train, 2) - 1
        y_train = func(x_train)
        # kernels
        K = kernel(x_train, x_train, sigma=sigma)
        K += lambd * np.eye(n_train)
        K_test = kernel(x_test, x_train, sigma=sigma)

        K_inv = np.linalg.inv(K[0:1, 0:1])
        for i in range(1, n_train):
            # recursive inversion
            x = K[:i, i]
            b = K[i, i]
            K_inv = column_updated_inverse(K_inv, x, b)

            # prediction
            alpha = K_inv @ y_train[: i + 1]
            y_pred = K_test[:, : i + 1] @ alpha
            y_pred -= y_test
            y_pred **= 2

            # error
            error[i - 1] = np.mean(y_pred)

        write_numpy_file(error, save_file)
        if verbose:
            print(j, flush=True, end=",")
    if verbose:
        print()


def classif_training_and_error_computattion(
    nb_exp,
    func,
    n_train,
    sigma,
    x_test,
    y_test,
    weight_test,
    save_file,
    kernel,
    verbose=True,
    delta=None,
):
    error = np.empty(n_train - 1)
    for j in range(nb_exp):
        # training dataset
        x_train = 2 * np.random.rand(n_train) - 1
        if delta is not None:
            x_train += delta * np.sign(x_train)
            x_train /= 1 + delta
        y_train = np.sign(func(x_train) - 2 * np.random.rand(n_train) + 1)
        # y_train = func(x_train)

        # weights
        K_test = kernel(x_test, x_train, sigma=sigma)
        for i in range(1, n_train):
            # prediction
            eta_pred = K_test[:, : i + 1] @ y_train[: i + 1]
            eta_pred /= K_test[:, : i + 1].sum(axis=1)
            y_pred = np.sign(eta_pred)
            err = (y_pred != y_test).astype(float)
            err *= weight_test

            # error
            error[i - 1] = np.mean(err)

        write_numpy_file(error, save_file)
        if verbose:
            print(j, flush=True, end=",")
