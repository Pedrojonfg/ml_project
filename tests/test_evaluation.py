"""Tests for the S4 event-level bootstrap (``src/evaluation.py``).

Contract under test: bootstrap_indices, metric_pack_reps, bca_interval,
bootstrap_report and the constants BOOT_B, BOOT_SEED, BOOT_LEVEL,
L_CAP_FACTOR, F2_ZERO_MAX_SHARE. ``metric_pack_reps`` takes ``idx`` as ONE
resample (1-D event indices, shape (N,)) and returns arrays of shape (R,).
"""

from __future__ import annotations


import numpy as np
import pytest

from src.evaluation import (
    BOOT_B,
    BOOT_LEVEL,
    BOOT_SEED,
    F2_ZERO_MAX_SHARE,
    L_CAP_FACTOR,
    bca_interval,
    bootstrap_indices,
    bootstrap_report,
    metric_pack_reps,
)
from src.metrics import crp_constant_risk, f2_score, kelvins_l, mse_hr

KEYS = ("F2", "MSE_HR_clipped", "MSE_HR_unclipped", "L_clipped", "L_unclipped")
L_KEYS = ("L_clipped", "L_unclipped")
B = 200


def _data(n=40, reps=3, seed=0):
    rng = np.random.default_rng(seed)
    hr = rng.random(n) < 0.3
    y = np.where(hr, rng.uniform(-6, -3, n), rng.uniform(-9, -6.5, n))
    y[:3] = -5.0  # guarantee some HR events
    lrp = y + rng.normal(0, 0.7, n)
    r_hat = y + rng.normal(0, 0.8, (reps, n))
    return y, lrp, r_hat, (r_hat >= -6.0).astype(float)


def _few_hr():
    """30 events, 3 HR; model flags only event 0 -> F2 = 0 in many resamples."""
    n = 30
    y = np.full(n, -8.0)
    y[:3] = [-5.0, -4.5, -5.5]
    lrp = y + 0.3
    r_hat = np.tile(np.full(n, -8.0), (3, 1))
    r_hat[:, :3] = [-5.5, -4.0, -6.5]
    p_hr = np.zeros((3, n))
    p_hr[:, 0] = 1.0
    return y, lrp, r_hat, p_hr


def _all_finite(entry):
    return np.all(np.isfinite([entry["estimate"], *entry["ci"]]))


def test_constants():
    assert BOOT_B == 10000  # per pj-006
    assert BOOT_SEED == 2026  # per mf-016
    assert BOOT_LEVEL == 0.95  # per pj-006
    assert L_CAP_FACTOR == 10  # per mf-017
    assert F2_ZERO_MAX_SHARE == 0.025  # per mf-017


def test_bootstrap_indices_shape_range_and_rng_equivalence():
    idx = bootstrap_indices(25, B=B)
    assert idx.shape == (B, 25)
    assert np.issubdtype(idx.dtype, np.integer)
    assert idx.min() >= 0 and idx.max() < 25
    expected = np.random.default_rng(2026).integers(0, 25, size=(B, 25))  # per mf-016
    np.testing.assert_array_equal(idx, expected)
    np.testing.assert_array_equal(idx, bootstrap_indices(25, B=B, seed=2026))
    assert not np.array_equal(idx, bootstrap_indices(25, B=B, seed=7))


def test_metric_pack_reps_original_sample_matches_metrics():
    y, _, r_hat, p_hr = _data()
    out = metric_pack_reps(y, r_hat, p_hr)
    assert set(out) == set(KEYS)
    for k in KEYS:
        assert out[k].shape == (3,)
    for r in range(3):
        f2 = f2_score(y, np.where(p_hr[r] == 1.0, 0.0, -100.0))
        mc, mu = mse_hr(y, r_hat[r], clip_at=-6.001), mse_hr(y, r_hat[r], clip_at=None)
        assert out["F2"][r] == pytest.approx(f2)
        assert out["MSE_HR_clipped"][r] == pytest.approx(mc)
        assert out["MSE_HR_unclipped"][r] == pytest.approx(mu)
        assert out["L_clipped"][r] == pytest.approx(kelvins_l(mc, f2))
        assert out["L_unclipped"][r] == pytest.approx(kelvins_l(mu, f2))


def test_metric_pack_reps_resample_equals_materialized_resample():
    y, _, r_hat, p_hr = _data()
    idx = np.random.default_rng(5).integers(0, len(y), len(y))
    got = metric_pack_reps(y, r_hat, p_hr, idx=idx)
    want = metric_pack_reps(y[idx], r_hat[:, idx], p_hr[:, idx])
    for k in KEYS:
        np.testing.assert_allclose(got[k], want[k])


def test_metric_pack_reps_f2_zero_gives_infinite_l():
    y, _, r_hat, _ = _data()
    out = metric_pack_reps(y, r_hat, np.zeros_like(r_hat))
    assert np.all(out["F2"] == 0.0)
    assert np.all(np.isinf(out["L_clipped"])) and np.all(np.isinf(out["L_unclipped"]))


def test_bca_normal_mean_matches_normal_theory():
    rng = np.random.default_rng(1)
    x = rng.normal(0, 1, 100)
    boot = x[rng.integers(0, 100, (2000, 100))].mean(axis=1)
    jack = np.array([np.delete(x, i).mean() for i in range(100)])
    lo, hi = bca_interval(x.mean(), boot, jack)
    se = x.std(ddof=1) / 10
    assert lo < x.mean() < hi
    assert lo == pytest.approx(x.mean() - 1.96 * se, abs=0.3 * se)
    assert hi == pytest.approx(x.mean() + 1.96 * se, abs=0.3 * se)


def test_bca_reduces_to_percentile_when_a_and_z0_zero():
    boot = np.arange(1000, dtype=float)
    jack = np.array([-1.0, 1.0] * 10)  # zero third moment -> a = 0
    lo, hi = bca_interval(500.0, boot, jack)  # exactly half below -> z0 = 0
    assert lo == pytest.approx(np.quantile(boot, 0.025))
    assert hi == pytest.approx(np.quantile(boot, 0.975))


def test_bca_infinite_upper_tail_stays_finite_when_percentile_finite():
    rng = np.random.default_rng(2)
    finite = rng.normal(0, 1, 980)
    boot = np.concatenate([finite, np.full(20, np.inf)])  # top 2 % infinite
    jack = np.array([-1.0, 1.0] * 10)
    lo, hi = bca_interval(float(np.median(finite)), boot, jack)
    assert np.isfinite(lo) and np.isfinite(hi) and lo < hi


def test_report_structure_and_estimates():
    y, lrp, r_hat, p_hr = _data()
    rep = bootstrap_report(y, lrp, r_hat, p_hr, B=B)
    orig = metric_pack_reps(y, r_hat, p_hr)
    for k in KEYS:
        e = rep[k]
        assert e["estimate"] == pytest.approx(float(np.mean(orig[k])))
        assert len(e["ci"]) == 2
        for pair in ("paired_vs_LRP", "paired_vs_CRP"):
            assert set(e[pair]) >= {"estimate", "ci"}
            assert len(e[pair]["ci"]) == 2
    assert {"n_f2_zero_resamples", "f2_zero_share", "L_reliable"} <= set(rep)


def test_report_deterministic():
    y, lrp, r_hat, p_hr = _data()
    assert bootstrap_report(y, lrp, r_hat, p_hr, B=B) == bootstrap_report(y, lrp, r_hat, p_hr, B=B)


def test_report_model_identical_to_lrp_has_zero_paired_difference():
    # Only possible exactly if model and LRP share the same resample indices (mf-016).
    y, lrp, _, _ = _data()
    r_hat, p_hr = np.tile(lrp, (3, 1)), np.tile((lrp >= -6.0).astype(float), (3, 1))
    rep = bootstrap_report(y, lrp, r_hat, p_hr, B=B)
    for k in KEYS:
        assert rep[k]["paired_vs_LRP"]["estimate"] == 0.0
        assert list(rep[k]["paired_vs_LRP"]["ci"]) == [0.0, 0.0]


def test_report_perfect_predictor():
    y, lrp, _, _ = _data()
    r_hat, p_hr = np.tile(y, (3, 1)), np.tile((y >= -6.0).astype(float), (3, 1))
    rep = bootstrap_report(y, lrp, r_hat, p_hr, B=B)
    for k, v in (("F2", 1.0), ("MSE_HR_clipped", 0.0), ("MSE_HR_unclipped", 0.0)):
        assert rep[k]["estimate"] == pytest.approx(v)
        assert list(rep[k]["ci"]) == pytest.approx([v, v])
    assert rep["n_f2_zero_resamples"] == 0


def test_report_all_reliable_when_no_f2_zero():
    y, lrp, _, _ = _data()
    r_hat, p_hr = np.tile(y, (3, 1)), np.tile((y >= -6.0).astype(float), (3, 1))
    rep = bootstrap_report(y, lrp, r_hat, p_hr, B=B)
    assert rep["n_f2_zero_resamples"] == 0 and rep["f2_zero_share"] == 0.0
    assert rep["L_reliable"] is True
    for k in L_KEYS:
        assert rep[k].get("reliable", True) is True


def test_report_f2_zero_cap_and_unreliable_flag():
    y, lrp, r_hat, p_hr = _few_hr()
    rep = bootstrap_report(y, lrp, r_hat, p_hr, B=B)

    # Independent recomputation of the per-resample, per-repetition metrics.
    idx = bootstrap_indices(len(y), B=B)
    packs = [metric_pack_reps(y, r_hat, p_hr, idx=i) for i in idx]
    f2 = np.array([p["F2"] for p in packs])  # (B, R)
    n_zero = int(np.sum((f2 == 0).any(axis=1)))
    assert n_zero > 0
    assert rep["n_f2_zero_resamples"] == n_zero
    assert rep["f2_zero_share"] == pytest.approx(n_zero / B)

    # Cap per mf-017: 10 x largest finite per-repetition L, clipped/unclipped apart.
    assert rep["f2_zero_share"] > F2_ZERO_MAX_SHARE
    assert rep["L_reliable"] is False
    for k in L_KEYS:
        ls = np.array([p[k] for p in packs])
        cap = L_CAP_FACTOR * ls[np.isfinite(ls)].max()
        e = rep[k]
        assert e["reliable"] is False
        # all repetitions are identical, so capped resamples average to exactly the cap
        assert e["ci"][1] == pytest.approx(cap)
        for entry in (e, e["paired_vs_LRP"], e["paired_vs_CRP"]):
            assert _all_finite(entry)

    # F2 and MSE_HR are not affected by the flag.
    for k in ("F2", "MSE_HR_clipped", "MSE_HR_unclipped"):
        assert rep[k].get("reliable", True) is True
        assert _all_finite(rep[k])


# --- mf-018: BCa not computable when z0 is infinite; mf-019: no finite L at all ---

_JACK = np.array([-1.0, 1.0] * 10)


def test_bca_none_when_share_below_is_zero_or_one():  # mf-018, no clipping
    boot = np.arange(1.0, 101.0)
    assert bca_interval(0.5, boot, _JACK) is None  # share below = 0
    assert bca_interval(1.0, boot, _JACK) is None  # ties are not "below": still 0
    assert bca_interval(101.0, boot, _JACK) is None  # share below = 1


def test_bca_all_boot_equal_estimate_is_zero_width_interval():  # mf-018
    assert bca_interval(2.5, np.full(50, 2.5), _JACK) == (2.5, 2.5)


def test_bca_finite_z0_unchanged():  # mf-018: share 0.3 -> finite z0, same as before
    boot = np.arange(1000, dtype=float)
    lo, hi = bca_interval(300.0, boot, _JACK)
    assert lo < 300.0 < hi and np.isfinite([lo, hi]).all()


def _expected_none(y, lrp, r_hat, p_hr, B, seed):
    """Independent z0-infinite check for F2/MSE entries (no L cap involved)."""
    idx = bootstrap_indices(len(y), B=B, seed=seed)
    crp = np.full(len(y), crp_constant_risk())
    args = {
        "model": (r_hat, p_hr),
        "LRP": (lrp[None], (lrp >= -6.0)[None]),
        "CRP": (crp[None], (crp >= -6.0)[None]),
    }
    mean = lambda n, i: {k: v.mean() for k, v in metric_pack_reps(y, *args[n], idx=i).items()}
    boot = {n: [mean(n, i) for i in idx] for n in args}
    orig = {n: mean(n, None) for n in args}
    out = {}
    for k in ("F2", "MSE_HR_clipped", "MSE_HR_unclipped"):
        b = {n: np.array([d[k] for d in boot[n]]) for n in args}
        for name, bb, t in [("self", b["model"], orig["model"][k])] + [
            (f"paired_vs_{n}", b["model"] - b[n], orig["model"][k] - orig[n][k]) for n in ("LRP", "CRP")
        ]:
            share = np.mean(bb < t)
            out[k, name] = (share in (0.0, 1.0)) and not np.all(bb == t)
    return out


def test_report_flags_only_entries_with_infinite_z0():  # mf-018
    y, lrp, r_hat, p_hr = _data()
    # tiny B, seed 4: the F2 estimate is the minimum of its bootstrap values (share below = 0)
    rep = bootstrap_report(y, lrp, r_hat, p_hr, B=5, seed=4)
    exp = _expected_none(y, lrp, r_hat, p_hr, 5, 4)
    assert any(exp.values()) and not all(exp.values())
    for (k, name), none in exp.items():
        e = rep[k] if name == "self" else rep[k][name]
        assert e["bca_not_computable"] is none
        assert (e["ci"] is None) == none and np.isfinite(e["estimate"])
        assert none or len(e["ci"]) == 2
    for k in L_KEYS:  # L entries carry the flag too
        assert isinstance(rep[k]["bca_not_computable"], bool)


def test_report_model_never_alarms_has_no_finite_l():  # mf-019: no raise, L not computable
    y, lrp, r_hat, _ = _data()
    rep = bootstrap_report(y, lrp, r_hat, np.zeros_like(r_hat), B=B)
    assert rep["L_reliable"] is False and rep["n_f2_zero_resamples"] == B
    for k in L_KEYS:
        for e in (rep[k], rep[k]["paired_vs_LRP"], rep[k]["paired_vs_CRP"]):
            assert e["ci"] is None and e["bca_not_computable"] is True and e["reliable"] is False
    for k in ("F2", "MSE_HR_clipped", "MSE_HR_unclipped"):  # unaffected
        for e in (rep[k], rep[k]["paired_vs_LRP"], rep[k]["paired_vs_CRP"]):
            assert np.isfinite(e["estimate"])
            assert (e["ci"] is None) == e["bca_not_computable"]
            assert e["ci"] is None or np.isfinite(e["ci"]).all()
    assert rep["F2"]["estimate"] == 0.0 and list(rep["F2"]["ci"]) == [0.0, 0.0]
