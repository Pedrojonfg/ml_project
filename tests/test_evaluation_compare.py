"""Tests for the S6 paired-comparison bootstrap ``bootstrap_compare`` (mf-037, mf-040).

Rows are (r_hat (R, N), p_hr (R, N)); a pair (A, B) means A minus B, key "A|B".
"""

from __future__ import annotations

import numpy as np
import pytest

from src.evaluation import (
    F2_ZERO_MAX_SHARE,
    bca_interval,
    bootstrap_compare,
    bootstrap_indices,
    bootstrap_report,
    metric_pack_reps,
)

KEYS = ("F2", "MSE_HR_clipped", "MSE_HR_unclipped", "L_clipped", "L_unclipped")
L_KEYS = ("L_clipped", "L_unclipped")
B = 300
N = 240


def _data():
    rng = np.random.default_rng(0)
    hr = rng.random(N) < 0.3
    y = np.where(hr, rng.uniform(-6, -3, N), rng.uniform(-9, -6.5, N))
    y[:5] = -5.0  # guarantee HR events
    lrp = y + rng.normal(0, 0.7, N)
    rows = {}
    for name, seed in (("A", 1), ("B", 2), ("C", 3)):
        r = y + np.random.default_rng(seed).normal(0, 0.8, (2, N))
        rows[name] = (r, (r >= -6.0).astype(float))
    return y, lrp, rows


def _same(a, b):
    if a is None or b is None:
        assert a is None and b is None
    elif isinstance(a, dict):
        assert a.keys() == b.keys()
        for k in a:
            _same(a[k], b[k])
    elif isinstance(a, (bool, np.bool_)):
        assert a == b
    else:
        np.testing.assert_allclose(a, b)


def test_rows_equal_bootstrap_report():  # mf-037: same procedure per row
    y, lrp, rows = _data()
    out = bootstrap_compare(y, lrp, rows, [("A", "B")], B=B, seed=7)
    assert set(out) == {"rows", "pairs"} and set(out["rows"]) == set(rows)
    for name, (r, p) in rows.items():
        _same(out["rows"][name], bootstrap_report(y, lrp, r, p, B, 7))


def test_pair_estimate_is_difference_and_antisymmetric():
    y, lrp, rows = _data()
    out = bootstrap_compare(y, lrp, rows, [("A", "B"), ("B", "A")], B=B)
    ab, ba = out["pairs"]["A|B"], out["pairs"]["B|A"]
    for k in KEYS:
        want = out["rows"]["A"][k]["estimate"] - out["rows"]["B"][k]["estimate"]
        np.testing.assert_allclose(ab[k]["estimate"], want)
        np.testing.assert_allclose(ba[k]["estimate"], -want)
        assert set(ab[k]) >= {"estimate", "ci", "bca_not_computable"}
    for k in L_KEYS:
        assert "reliable" in ab[k]


def test_pair_ci_uses_same_resamples_and_jackknife_difference():  # mf-016, mf-018
    y, lrp, rows = _data()
    Bs, seed = 60, 11
    out = bootstrap_compare(y, lrp, rows, [("A", "B")], B=Bs, seed=seed)["pairs"]["A|B"]
    (ra, pa), (rb, pb) = rows["A"], rows["B"]

    def diff(key, idx=None, drop=None):
        if drop is not None:
            idx = np.delete(np.arange(N), drop)
        d = metric_pack_reps(y, ra, pa, idx)[key].mean() - metric_pack_reps(y, rb, pb, idx)[key].mean()
        return d

    for key in ("F2", "MSE_HR_unclipped"):
        boot = np.array([diff(key, i) for i in bootstrap_indices(N, Bs, seed)])
        jack = np.array([diff(key, drop=i) for i in range(N)])
        est = diff(key)
        np.testing.assert_allclose(out[key]["estimate"], est)
        np.testing.assert_allclose(out[key]["ci"], bca_interval(est, boot, jack))


def test_identical_rows_give_zero_difference():
    y, lrp, rows = _data()
    out = bootstrap_compare(y, lrp, rows, [("A", "A")], B=B)["pairs"]["A|A"]
    for k in KEYS:
        assert out[k]["estimate"] == 0
        assert list(out[k]["ci"]) == [0, 0]


def test_shared_regressor_gives_zero_mse_difference_and_shared_alarms_zero_f2():  # mf-037 checks
    y, lrp, rows = _data()
    r = rows["A"][0]
    rows["same_r"] = (r, (r >= -4.0).astype(float))  # same r_hat, different alarms
    rows["same_p"] = (r + 0.3, rows["A"][1])  # same alarms, different r_hat
    out = bootstrap_compare(y, lrp, rows, [("A", "same_r"), ("A", "same_p")], B=B)["pairs"]
    for k in ("MSE_HR_clipped", "MSE_HR_unclipped"):
        assert out["A|same_r"][k]["estimate"] == 0
        assert list(out["A|same_r"][k]["ci"]) == [0, 0]
    assert out["A|same_p"]["F2"]["estimate"] == 0
    assert list(out["A|same_p"]["F2"]["ci"]) == [0, 0]
    assert out["A|same_r"]["F2"]["estimate"] != 0  # the alarms really differ


def _rel_data():
    """200 events, HR = events 0..9. Row A detects only events 0..3, B only 4..7,
    C and D detect all 10 (F2 = 0 essentially never)."""
    n = 200
    y = np.full(n, -8.0)
    y[:10] = -5.0
    lrp = y + 0.2

    def row(detected, shift):
        p = np.zeros((2, n))
        p[:, detected] = 1.0
        return np.tile(y + shift, (2, 1)), p

    rows = {"A": row(slice(0, 4), 0.5), "B": row(slice(4, 8), -0.5),
            "C": row(slice(0, 10), 0.3), "D": row(slice(0, 10), -0.3)}
    return y, lrp, rows


def test_pair_l_reliability_uses_either_share_mf040():
    y, lrp, rows = _rel_data()
    Bs, seed = 1000, 2026
    idx = bootstrap_indices(len(y), Bs, seed)
    # A resample with no HR event at all has F2 = 1 by the registered convention (all-negative perfect,
    # as in bootstrap_report), so it is not an F2 = 0 resample.
    has_hr = (idx < 10).any(axis=1)
    zero_a = ~(idx < 4).any(axis=1) & has_hr  # HR present but none detected by A -> TP = 0 -> F2 = 0
    zero_b = ~((idx >= 4) & (idx < 8)).any(axis=1) & has_hr
    either = zero_a | zero_b
    # Preconditions of the scenario: each alone passes, together they fail.
    assert zero_a.mean() <= F2_ZERO_MAX_SHARE and zero_b.mean() <= F2_ZERO_MAX_SHARE
    assert either.mean() > F2_ZERO_MAX_SHARE

    out = bootstrap_compare(y, lrp, rows, [("A", "B"), ("C", "D"), ("A", "C")], B=Bs, seed=seed)
    # each row alone is reliable (mf-017) ...
    for name in ("A", "B"):
        assert out["rows"][name]["L_reliable"] is True
    # ... but the pair is not (mf-040 option 1, not option 2)
    ab = out["pairs"]["A|B"]
    assert ab["n_f2_zero_either"] == int(either.sum())
    np.testing.assert_allclose(ab["f2_zero_either_share"], either.mean())
    for k in L_KEYS:
        assert ab[k]["reliable"] is False

    # low shares -> reliable
    cd = out["pairs"]["C|D"]
    assert cd["n_f2_zero_either"] == 0 and cd["f2_zero_either_share"] == 0
    for k in L_KEYS:
        assert cd[k]["reliable"] is True

    # one row alone <= 2.5% and the other 0: either share equals that row's share
    ac = out["pairs"]["A|C"]
    assert ac["n_f2_zero_either"] == int(zero_a.sum())


def test_unknown_row_name_raises():
    y, lrp, rows = _data()
    with pytest.raises((KeyError, ValueError)):
        bootstrap_compare(y, lrp, rows, [("A", "nope")], B=50)
