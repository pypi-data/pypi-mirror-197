""" Test optimizer
"""

from pathlib import Path

import numpy as np
from scipy.stats import linregress

import dsfe.optimizer as dso

import pytest

HERE = Path(__file__).parent


def test_optimize():
    bad_start = [2.25, 0.47]
    x, y = np.loadtxt(HERE / 'xy.csv', delimiter=',').T
    lr_res = linregress(x, y)
    best_params = [lr_res.intercept, lr_res.slope]
    for cost_func in (dso.ss_any_line, dso.ms_any_line, dso.rmse_any_line):
        params = dso.optimize(cost_func, bad_start, extra_args=[x, y])
        assert np.allclose(params, best_params, 1e-4)
    params = dso.optimize(dso.rmse_any_line,
                          bad_start,
                          extra_args=[x, y],
                          method=None)
    assert np.allclose(params, best_params, 1e-4)

    hgb, pcv = np.loadtxt(HERE / 'hgb_pcv.csv', delimiter=',').T
    maths_slope = [np.sum(hgb * pcv) / np.sum(hgb ** 2)]

    def ss(s):
        return np.sum((pcv - s[0] * hgb) ** 2)

    out_s = dso.optimize(ss, [2.25])
    assert np.allclose(out_s, maths_slope, 1e-4)

    with pytest.raises(dso.MinimizeError):
        dso.optimize(ss, [2.25], method=None)
