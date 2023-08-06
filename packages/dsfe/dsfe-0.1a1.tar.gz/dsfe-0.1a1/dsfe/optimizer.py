""" Optimization
"""

import numpy as np
from scipy.optimize import minimize


class MinimizeError(Exception):
    """ Error for failure of minimize
    """


def ss_any_line(c_s, x, y):
    """ Sum of squares cost function for simple regression

    Parameters
    ----------
    c_s : array, length 2
        Array containing intercept and slope values for proposed line.
    x : array
        x values we will use to predict the `y` values.
    y : array
        y values we are trying to predict using the `x` values and the line
        defined in `c_s`.

    Returns
    -------
    cost : float
        Cost function value; the sum of squared prediction errors.
    """
    predictions = c_s[0] + c_s[1] * x
    errors = y - predictions
    return np.sum(errors ** 2)


def ms_any_line(c_s, x, y):
    """ Mean squares cost function for simple regression

    Parameters
    ----------
    c_s : array, length 2
        Array containing intercept and slope values for proposed line.
    x : array
        x values we will use to predict the `y` values.
    y : array
        y values we are trying to predict using the `x` values and the line
        defined in `c_s`.

    Returns
    -------
    cost : float
        Cost function value; the mean squared prediction error.
    """
    return ss_any_line(c_s, x, y) / len(x)


def rmse_any_line(c_s, x, y):
    """ Root mean squares cost function for simple regression

    Parameters
    ----------
    c_s : array, length 2
        Array containing intercept and slope values for proposed line.
    x : array
        x values we will use to predict the `y` values.
    y : array
        y values we are trying to predict using the `x` values and the line
        defined in `c_s`.

    Returns
    -------
    cost : float
        Cost function value; the square root of the mean squared prediction
        errors.
    """
    return np.sqrt(ms_any_line(c_s, x, y))


def optimize(cost_function,
             starting_params,
             extra_args=(),
             method='Nelder-Mead'):
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

    `method` specifies the algorithm that ``minimize`` should use to search for
    the best parameters.  It default to a ``mimimize`` method called
    'Nelder-Mead' that works well for cost function values are not very stable.
    Use ``method=None`` to trigger Scipy's usual selection of method for
    ``minimize``, or specify some other method; see the documentation for
    ``scipy.optimize.minimize`` for the list of options.

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
    method : str or None, optional
        ``method`` to pass to ``minimize``.  This specifies the search
        algorithm that ``minimize`` will use to find the best (lowest cost)
        parameters.  Default is 'Nelder-Mead'.

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
    res = minimize(cost_function, starting_params, args=extra_args,
                   method=method)
    if not res.success:
        raise MinimizeError(f'Minimize with method {method} failed with '
                            f'message {res.message}')
    return res.x
