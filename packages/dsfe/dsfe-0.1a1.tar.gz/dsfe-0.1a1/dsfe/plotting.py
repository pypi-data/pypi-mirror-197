""" Plotting for DSFE
"""

import numpy as np

import matplotlib.pyplot as plt


def count_bar(arr, x_vals=None):
    """ Do bar plot of counts for integers in `arr`

    This function is a simple wrapper for ``np.bincount`` and ``plt.bar``.

    It assumes all the values in `arr` are all non-negative integers (such as
    counts), then counts how many times each integer occurs in `arr`, and makes
    a bar graph to display the counts.

    Parameters
    ----------
    arr : array-like
        A sequence that can be made into an array, such as an array or a list.
        The array must contain non-negative integers.
    x_vals : None or array-like, optional
        x values for bar plot.  If None, use the obvious integer array from 0
        through the maximum value in `arr`.  Otherwise, use `x_vals` as the x
        values, and select corresponding values from counts.

    Returns
    -------
    bc : BarContainer
        The Matplotlib container for a bar plot.
    """
    # Convert arr to integers if necessary.
    to_count = np.asarray(arr).astype(int)
    if x_vals is None:  # We didn't specify x_vals
        y_vals = np.bincount(to_count)  # Count numbers of each integer.
        x_vals = np.arange(len(y_vals))
    else:  # We specified x_vals
        # Make counts go up as far as we need for the x_vals indices.
        counts = np.bincount(to_count, minlength=np.max(x_vals) + 1)
        y_vals = counts[x_vals]
    out = plt.bar(x_vals, y_vals)
    plt.xticks(x_vals)
    return out
