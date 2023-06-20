from typing import Callable

import numpy as np


def metropolis_hastings(
    f: Callable, x_0: float = 0.0, n_samples: int = 10000
) -> np.ndarray:
    """Implements the metropolis-hastings algorithm with a normal distribution as proposal function.

    Args:
        f (Callable): An arbitrary probability density function
            that is used to calculate the acceptance ratio alpha=f(x_next)/f(x_t).
            f has to accept a single parameter x and return the function value for x.
        x_0 (float, optional): The first observation to start from.
        n_samples (int, optional): Number of samples to be drawn. Defaults to 10000.

    Returns:
        (np.ndarray): Drawn samples from the target distribution.
    """

    if n_samples < 1:
        raise ValueError("n_samples must be a positive integer")

    ## instantiate then assign
    results = np.empty(shape=(n_samples))
    results[0] = x_0
    for n in range(1, n_samples):
        x_t = results[n - 1]

        x_next = np.random.normal(loc=x_t)
        u = np.random.random()
        alpha = f(x_next) / f(x_t)

        results[n] = x_next if alpha >= u else x_t

    return results