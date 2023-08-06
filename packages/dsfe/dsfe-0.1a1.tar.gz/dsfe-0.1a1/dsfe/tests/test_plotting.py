""" Test plotting routines
"""

import numpy as np

from dsfe.plotting import count_bar


def test_plot_square2():
    arr = [0, 1, 1, 1, 2, 3, 4, 3, 4, 5]
    bar0 = count_bar(arr)
    out_counts = np.bincount(arr)
    assert np.all(bar0.datavalues == out_counts)
    assert np.all(out_counts == [p.get_height() for p in bar0.patches])
    # Restrict x axis
    x_vals = [1, 2, 5, 6, 8]
    bar_res = count_bar(arr, x_vals)
    exp_counts = [3, 1, 1, 0, 0]
    assert np.all(bar_res.datavalues == exp_counts)
    assert np.all(exp_counts == [p.get_height() for p in bar_res.patches])
    x_vals = [0, 1, 4]
    bar_res2 = count_bar(arr, x_vals)
    exp_counts2 = [1, 3, 2]
    assert np.all(bar_res2.datavalues == exp_counts2)
    assert np.all(exp_counts2 == [p.get_height() for p in bar_res2.patches])
