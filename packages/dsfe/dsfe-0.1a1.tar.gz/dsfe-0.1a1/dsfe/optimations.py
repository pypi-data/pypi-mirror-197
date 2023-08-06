""" Optimization
"""

import numpy as np
from scipy import minimize


class MinimizeError(Exception):
    """ Error for failure of minimize
    """


def rsme_any_line(c_s, x, y):
    predictions = c_s[0] + c_s[1] * x
    errors = y - predictions
    return np.sqrt(np.mean(errors ** 2))


def optimize(cost_function,
             starting_params,
             extra_args=(),
             noisy=True):
    """ Optimize wrapper for calling Scipy ``minimize``

    This function passes arguments to ``scipy.optimize.minimize`.  In
    particular, we pass it the `cost_function` (a callable, such as a
    function), starting parameters `starting_params` and any extra arguments to
    go to the function `extra_args`.

    Assume that `extra_args` stays at its default (empty). Then the routine
    will be doing multiple calls of form ``fun = cost_function(params)`` in
    order to choose the values in the array `params` that give the lowest value
    (cost) from `cost_function`.   The routine will use `starting_params` as
    the initial argument to `cost_function`, as it begins its search.

    If `extra_args` is not default, and not empty, it contains extra arguments
    that should be passed along to the `cost_function`.  For example, if the
    `cost_function` takes three arguments, of which the first must be the
    `params` array, then you can pass in the second and third arguments, by
    setting `extra_args` to contain them.  For example, if we need to call
    `cost_function` like this: ``fun = cost_function(params, arg1, arg2)`` then
    you would pass in the values for ``arg1`` and ``arg2`` to this routine with
    ``extra_args=(arg1, arg2)``.

    `noisy` defaults to True, and triggers the use of a standard mimimize
    method called 'Nelder-Mead' that works well for cost function values are
    not very stable.  Use ``noisy=False`` to trigger Scipy's usual selection
    of method for ``minimize``.

    Parameters
    ----------
    cost_function : callable
        A callable (for example, a function), that we will call to get *values*
        of the cost function.  We are trying to find the values for the
        *parameters* that minimize the value from `cost_function`, when we call
        the `cost_function` as ``cost_function(params)``.
    starting_params : array-like
        Something that can be made into an array, such as an array or a list,
        that contains the starting parameters that `cost_function` should try
        first.
    extra_args : sequence, optional
        A sequence of second, third, etc arguments to be passed to
        `cost_function` after the obligatory ``params`` argument.  Default is
        empty, meaning the routine passes only the obligatory ``params``
        argument.

    Returns
    -------
    minimizing_params : array
        Array of parameters such that ``cost_function(minimizing_params)`` (or
        ``cost_function(minimizing_params, extra_args[0], extra_args[1] ...)``
        if `extra_args` not empty) gives the smallest value of any potential
        choice of `params`.

    Raises
    ------
    MinimizeError
        If the result of ``minimize` does not record ``success``.
    """
    if extra_args:
        extra_args = tuple(extra_args)
    method = None  # The default for scipy.optimize.minimize
    if noisy:  # Set method that works well for noisy data.
        method = 'Nelder-Mead'
    res = minimize(cost_function, starting_params, args=extra_args,
                   method=method)
    if not res.success:
        raise MinimizeError(f'Minimize with method {method} failed with '
                            f'message {res.message}')
    return res.x
