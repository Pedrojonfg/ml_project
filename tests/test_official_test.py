"""Official-test protocol (pj-081..pj-084): model set, event filter, train-only fit, seed 42.

Contract for src/official_test.py (module is written by the solver, not by this file):
  OFFICIAL_SLUGS: tuple[str, ...]                       # per pj-081
  filter_official_test_events(cdm) -> DataFrame         # column event_id; per pj-084
  official_test_cdms(cdm) -> DataFrame                  # only CDMs with ttc >= 2 of kept events; per pj-084
  run_official_baselines(y_true, lrp) -> {"CRP": m, "LRP": m}   # m has Kelvins metric keys
  fit_predict_slug(slug, X_train, y_train, X_test, *, lrp_train) -> {"r_hat", "p_hr"}  # per pj-082
Linear slugs delegate to src.models.linear.fit_predict_fold; tree slugs call
src.models.trees.select_by_inner_cv (module attribute) for re-selection (pj-083).
"""

import numpy as np
import pandas as pd
import pytest

import src.models.linear as lin
import src.models.trees as trees
from src.features import FEATURE_COLUMNS
from src.official_test import (
    OFFICIAL_SLUGS,
    filter_official_test_events,
    fit_predict_slug,
    official_test_cdms,
    run_official_baselines,
)

NF = len(FEATURE_COLUMNS)
METRIC_KEYS = ("F2", "MSE_HR_clipped", "L_clipped")


def _cdm(rows):
    # rows: (event_id, time_to_tca, risk)
    return pd.DataFrame(rows, columns=["event_id", "time_to_tca", "risk"])


def _train_xy(n=160, n_hr=24, seed=0):
    # Kelvins-like: ~15% HR (y >= -6), LRP = noisy copy of y so floor_c (pj-026) is solvable
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, NF))
    y = np.where(np.arange(n) < n_hr, -5.0, -9.0) + 0.5 * X[:, 0] + rng.normal(scale=0.3, size=n)
    lrp = y + rng.normal(scale=0.5, size=n)
    return X, y, lrp


# ---------------------------------------------------------------- pj-081

def test_model_set_list_matches_pj_081():
    expected = {
        "CRP", "LRP",
        "ols", "ridge", "lasso", "knn", "kernel_ridge", "rf", "gbdt", "mlp", "gru",
        "s6_stage1_lr_none", "s6_stage1_lr_l2", "s6_stage1_lr_l1",
        *(f"s6_{c}__{m}" for c in ("lr_none", "lr_l2", "lr_l1") for m in ("ols", "ridge", "lasso")),
    }
    assert len(OFFICIAL_SLUGS) == len(set(OFFICIAL_SLUGS))  # no duplicates
    assert set(OFFICIAL_SLUGS) == expected  # 2 + 9 + 3 + 9 = 23 rows
    assert not any("s9" in s.lower() for s in OFFICIAL_SLUGS)  # S9 excluded


# ---------------------------------------------------------------- pj-084

def test_filter_keeps_events_with_usable_cdm_drops_others():
    cdm = _cdm([
        (1, 5.0, -7.0), (1, 3.0, -6.5), (1, 0.5, -5.0),  # usable + post-2d CDM: kept
        (2, 1.9, -7.0), (2, 0.5, -7.0),                   # no ttc >= 2: dropped
        (3, 2.0, -8.0),                                   # boundary ttc == 2 counts as usable, last CDM ttc >= 2 still kept
        (4, 6.0, -9.0), (4, 2.5, -9.0),                   # last CDM ttc >= 2 (official test shape): kept, not pj-003
    ])
    kept = filter_official_test_events(cdm)
    assert sorted(kept["event_id"].tolist()) == [1, 3, 4]  # per pj-084


def test_official_inputs_use_only_ttc_ge_2_cdms():
    cdm = _cdm([(1, 5.0, -7.0), (1, 1.0, -3.0), (2, 0.5, -3.0), (3, 2.0, -8.0)])
    used = official_test_cdms(cdm)
    assert (used["time_to_tca"] >= 2.0).all()  # per pj-084: no near-TCA CDM leaks into inputs
    assert sorted(used["event_id"].unique().tolist()) == [1, 3]


# ---------------------------------------------------------------- baselines

def test_baselines_crp_lrp_shapes():
    y = np.array([-7.0, -5.5, -8.0, -5.2, -9.0])
    lrp = np.array([-7.5, -5.1, -8.5, -6.5, -9.5])
    out = run_official_baselines(y, lrp)
    assert set(out) == {"CRP", "LRP"}
    for name in ("CRP", "LRP"):
        for k in METRIC_KEYS:
            assert k in out[name], (name, k)
            assert np.isscalar(out[name][k]) or np.ndim(out[name][k]) == 0
    # CRP predicts -5 everywhere: all alarms -> tp=2, fp=3, fn=0 -> F2 = 5*P*R/(4P+R), P=0.4, R=1
    assert out["CRP"]["F2"] == pytest.approx(5 * 0.4 / (4 * 0.4 + 1))
    # LRP: one HR event caught (-5.1), one missed (-6.5), no false alarm
    assert out["LRP"]["F2"] == pytest.approx(5 * 1.0 * 0.5 / (4 * 1.0 + 0.5))


# ---------------------------------------------------------------- pj-082 / pj-083

def test_train_fit_excludes_test_ids(monkeypatch):
    # test rows carry a sentinel in feature 0 (event_id marker); no helper may ever see it
    X, y, lrp = _train_xy(n=100, n_hr=15)
    X_test = np.random.default_rng(9).normal(size=(12, NF))
    X_test[:, 0] = 1e6 + np.arange(12)  # per pj-083: test never in selection or fit
    monkeypatch.setattr(lin, "RIDGE_ALPHAS", np.array([1.0, 100.0, 1e4]))
    seen = {"fold": [], "alpha": [], "alarm": []}

    def spy(key, real):
        def wrapper(*args, **kw):
            seen[key].append([np.asarray(a) for a in args if isinstance(a, np.ndarray)])
            return real(*args, **kw)
        return wrapper

    monkeypatch.setattr(lin, "fit_predict_fold", spy("fold", lin.fit_predict_fold))
    monkeypatch.setattr(lin, "select_alpha", spy("alpha", lin.select_alpha))
    monkeypatch.setattr(lin, "choose_alarm_line", spy("alarm", lin.choose_alarm_line))

    out = fit_predict_slug("ridge", X, y, X_test, lrp_train=lrp)

    assert len(seen["fold"]) == 1  # per pj-082: one fit on full train, no fold ensemble
    assert seen["fold"][0][0].shape == X.shape  # full filtered train is the outer train
    for key in ("fold", "alpha", "alarm"):
        assert seen[key], f"{key} helper never called"
        for call in seen[key]:
            for arr in call[:1] if key != "fold" else call[:2]:  # X_train (and y_train for fold)
                assert not (arr.ndim == 2 and (arr[:, 0] >= 1e5).any()), key
    # alarm line t and alpha come from train-only arrays: lengths never exceed n_train
    for call in seen["alarm"]:
        assert all(len(a) <= len(y) for a in call)
    assert np.asarray(out["r_hat"]).shape == (12,)
    assert np.asarray(out["p_hr"]).shape == (12,)


@pytest.mark.parametrize("kind", ["rf", "gbdt"])
def test_nested_seed_42(monkeypatch, kind):
    # per pj-083: inner/nested seed 42 for rep-indexed selection, full train as outer train
    X, y, lrp = _train_xy(n=100, n_hr=15)
    X_test = np.random.default_rng(3).normal(size=(10, NF))
    calls = []

    def fake_select(fit_predict, ws, tr, y_arg, seed):
        calls.append({"seed": seed, "tr": np.asarray(tr)})
        return (ws[0], 5), {(ws[0], 5): 0.0}

    monkeypatch.setattr(trees, "select_by_inner_cv", fake_select)
    import src.official_test as ot
    monkeypatch.setattr(ot, "select_by_inner_cv", fake_select, raising=False)

    out = fit_predict_slug(kind, X, y, X_test, lrp_train=lrp)

    assert calls, "tree path must re-select via select_by_inner_cv"
    assert all(c["seed"] == 42 for c in calls)
    for c in calls:
        np.testing.assert_array_equal(np.sort(c["tr"]), np.arange(len(y)))  # full train only
    assert np.asarray(out["r_hat"]).shape == (10,)
