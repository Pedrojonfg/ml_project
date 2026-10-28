"""S5 tree models (pj-014..020): helpers, leakage, determinism."""

import numpy as np
import pandas as pd
import pytest

from src.features import FEATURE_COLUMNS
from src.models.trees import (
    feature_family,
    make_gbdt,
    make_imputer,
    make_rf,
    p_hr_from_r_hat,
    run_oof_cv,
    top_k_names,
)
from src.protocol import make_folds as protocol_make_folds


def test_p_hr_hard_threshold():
    r = np.array([-6.0, -6.1, -5.0])
    assert p_hr_from_r_hat(r).tolist() == [1.0, 0.0, 1.0]


def test_feature_family_buckets():
    assert feature_family("risk_snap_last") == "risk"
    assert feature_family("miss_distance_snap_first") == "geometry"
    assert feature_family("obj_DEBRIS") == "object"
    assert feature_family("n_cdm") == "metadata"


def test_imputer_fit_train_only_no_val_leakage():
    # ponytail: median on train must not use validation NaN placement
    imp = make_imputer()
    X_train = np.array([[1.0], [3.0], [np.nan]])
    X_val = np.array([[np.nan]])
    imp.fit(X_train)
    assert imp.transform(X_val)[0, 0] == 2.0  # median of 1,3 not val


def test_rf_deterministic_under_seed():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(80, len(FEATURE_COLUMNS)))
    y = X[:, 0] * 0.1 + rng.normal(scale=0.01, size=80)
    table = pd.DataFrame({
        "event_id": np.arange(80, dtype=np.int64),
        "y_hr": y >= np.median(y),
    })
    folds = protocol_make_folds(table, seeds=(42,), n_splits=5)
    eid = table.event_id.to_numpy()
    a = run_oof_cv(lambda rs: make_rf(10, rs), X, y, eid, folds, collect_importance=False)
    b = run_oof_cv(lambda rs: make_rf(10, rs), X, y, eid, folds, collect_importance=False)
    np.testing.assert_allclose(a.oof_pred, b.oof_pred)


def test_oof_keeps_every_repetition_and_averages_metrics():
    rng = np.random.default_rng(2)
    n = 100
    X = rng.normal(size=(n, len(FEATURE_COLUMNS)))
    y = np.where(rng.random(n) < 0.2, -5.0, -30.0)
    table = pd.DataFrame({"event_id": np.arange(n, dtype=np.int64), "y_hr": y >= -6})
    folds = protocol_make_folds(table, seeds=(42, 43, 44), n_splits=5)
    res = run_oof_cv(lambda rs: make_rf(5, rs), X, y, table.event_id.to_numpy(), folds,
                     collect_importance=False)
    assert res.oof_pred.shape == (3, n)
    assert len(res.metrics_per_rep) == 3
    assert res.metrics["F2"] == pytest.approx(np.mean([m["F2"] for m in res.metrics_per_rep]))


def test_top_k_names_order():
    imp = np.zeros(5)
    imp[2] = 3
    imp[0] = 1
    assert top_k_names(imp, 2) == [FEATURE_COLUMNS[2], FEATURE_COLUMNS[0]]


def test_importance_diagnostics_runs_tiny():
    rng = np.random.default_rng(1)
    n, p = 60, len(FEATURE_COLUMNS)
    X = rng.normal(size=(n, p))
    y = X[:, 0] * 0.2 + rng.normal(scale=0.05, size=n)
    table = pd.DataFrame({"event_id": np.arange(n, dtype=np.int64), "y_hr": y > 0})
    folds = protocol_make_folds(table, seeds=(42,), n_splits=5)
    eid = table.event_id.to_numpy()
    rf = run_oof_cv(lambda rs: make_rf(5, rs), X, y, eid, folds)
    gb = run_oof_cv(lambda rs: make_gbdt(5, rs), X, y, eid, folds)
    from src.models.trees import importance_diagnostics

    d = importance_diagnostics(rf.importances, gb.importances, X, y, folds, 5, 5)
    assert "reopen_required" in d


# ---- pj-026: floor c, lrp-aware CV, floor diagnostics ----

def _synth(n=200, seed=0):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, len(FEATURE_COLUMNS)))
    u = rng.random(n)
    y = np.full(n, -30.0)
    hr = u < 0.10
    near = (u >= 0.10) & (u < 0.40)
    y[hr] = rng.uniform(-6.0, -4.0, hr.sum())
    y[near] = rng.uniform(-6.5, -6.01, near.sum())
    lrp = np.full(n, -30.0)
    det = hr & (rng.random(n) < 0.7)
    lrp[det] = y[det]
    fa = ~hr & (rng.random(n) < 0.05)
    lrp[fa] = -5.0
    table = pd.DataFrame({"event_id": np.arange(n, dtype=np.int64), "y_hr": y >= -6})
    return X, y, lrp, table


def _p_of_c(y, c):
    hr = y >= -6.0
    mu = y[hr].mean()
    m = np.maximum(y[~hr], c).mean()
    return (-6.0 - m) / (mu - m)


def test_floor_c_solves_calibration_equation():
    from src.metrics import f2_score
    from src.models.trees import floor_c

    _, y, lrp, _ = _synth()
    out = floor_c(y, lrp)
    assert {"c", "mu_hr", "sd_hr", "f_star", "p_star"} <= set(out)
    hr = y >= -6.0
    assert out["mu_hr"] == pytest.approx(y[hr].mean())
    assert out["sd_hr"] == pytest.approx(y[hr].std(ddof=1))
    assert out["f_star"] > 0
    assert out["f_star"] == pytest.approx(f2_score(y, lrp))
    assert out["p_star"] == pytest.approx(out["f_star"] / 5)
    assert -29.99 < out["c"] < -6.0005
    assert _p_of_c(y, out["c"]) == pytest.approx(out["p_star"], abs=1e-6)


def test_floor_c_raises_when_lrp_f2_is_zero():
    from src.models.trees import floor_c

    _, y, _, _ = _synth()
    with pytest.raises(ValueError):
        floor_c(y, np.full_like(y, -30.0))


def test_run_oof_cv_without_lrp_has_empty_floors():
    X, y, _, table = _synth(100, seed=3)
    folds = protocol_make_folds(table, seeds=(42,), n_splits=5)
    res = run_oof_cv(lambda rs: make_rf(5, rs), X, y, table.event_id.to_numpy(), folds,
                     collect_importance=False)
    assert res.floors == []


def test_run_oof_cv_with_lrp_floors_use_train_rows_only():
    from src.models.trees import _fold_masks, floor_c

    X, y, lrp, table = _synth()
    folds = protocol_make_folds(table, seeds=(42, 43), n_splits=5)
    res = run_oof_cv(lambda rs: make_rf(5, rs), X, y, table.event_id.to_numpy(), folds,
                     collect_importance=False, lrp=lrp)
    assert len(res.floors) == 2 * 5
    assert [(f["rep"], f["fold"]) for f in res.floors] == [
        (r, k) for r in range(2) for k in range(5)
    ]
    for f in res.floors:
        train_m, _ = _fold_masks(folds, f["rep"], f["fold"])
        ref = floor_c(y[train_m], lrp[train_m])
        assert {"c", "mu_hr", "sd_hr", "f_star", "p_star"} <= set(f)
        assert f["c"] == pytest.approx(ref["c"])
    # RF predictions average floored training targets, so none can fall below the lowest floor
    c_min = min(f["c"] for f in res.floors)
    assert c_min > -29.99
    assert res.oof_pred.min() >= c_min - 1e-9
    assert res.oof_pred.shape == (2, len(y))


def test_select_n_estimators_pass_lrp_through(monkeypatch):
    import src.models.trees as trees

    seen = []

    class Stub:
        metrics_pooled = {"L_unclipped": 1.0}

    def spy(pipeline_factory, X, y, event_ids, folds, feature_names=FEATURE_COLUMNS,
            collect_importance=True, lrp=None):
        seen.append(lrp)
        return Stub()

    monkeypatch.setattr(trees, "run_oof_cv", spy)
    monkeypatch.setattr(trees, "N_ESTIMATORS_GRID", (3, 4))
    X, y, lrp, table = _synth(50, seed=4)
    folds = protocol_make_folds(table, seeds=(42,), n_splits=5)
    eid = table.event_id.to_numpy()
    for select in (trees.select_rf_n_estimators, trees.select_gbdt_n_estimators):
        seen.clear()
        select(X, y, eid, folds, lrp=lrp)
        assert len(seen) == 2 and all(s is lrp for s in seen)
        seen.clear()
        select(X, y, eid, folds)
        assert len(seen) == 2 and all(s is None for s in seen)


def test_importance_diagnostics_accepts_lrp_and_fits_on_floored_y(monkeypatch):
    import src.models.trees as trees
    from src.models.trees import _fold_masks, floor_c, importance_diagnostics

    X, y, lrp, table = _synth(150, seed=5)
    folds = protocol_make_folds(table, seeds=(42,), n_splits=5)
    eid = table.event_id.to_numpy()
    rf = run_oof_cv(lambda rs: make_rf(5, rs), X, y, eid, folds, lrp=lrp)
    gb = run_oof_cv(lambda rs: make_gbdt(5, rs), X, y, eid, folds, lrp=lrp)

    fitted = []

    def recording(factory):
        def make(n, rs):
            pipe = factory(n, rs)
            orig = pipe.fit

            def fit(Xf, yf, *a, **k):
                fitted.append(np.asarray(yf).copy())
                return orig(Xf, yf, *a, **k)

            pipe.fit = fit
            return pipe
        return make

    monkeypatch.setattr(trees, "make_rf", recording(trees.make_rf))
    monkeypatch.setattr(trees, "make_gbdt", recording(trees.make_gbdt))
    d = importance_diagnostics(rf.importances, gb.importances, X, y, folds, 5, 5, lrp=lrp)
    assert "reopen_required" in d
    train_m, _ = _fold_masks(folds, 0, 0)
    c = floor_c(y[train_m], lrp[train_m])["c"]
    assert len(fitted) == 2
    for yf in fitted:
        np.testing.assert_allclose(yf, np.maximum(y[train_m], c))


# floor_c_diagnostics on hand-built CvResult objects

def _floors(folds, c=-20.0, mu=-5.0, sd=0.5, f_star=0.5, by_fold=None):
    out = []
    for rep in sorted(folds.rep.unique()):
        for k in range(5):
            d = by_fold(int(rep), k) if by_fold else {}
            out.append({"rep": int(rep), "fold": k, "c": c, "mu_hr": mu, "sd_hr": sd,
                        "f_star": f_star, "p_star": f_star / 5, **d})
    return out


def _fake_res(y, oof_pred, folds, floors, metrics=None):
    from src.models.trees import CvResult, kelvins_pack

    oof = np.atleast_2d(np.asarray(oof_pred, dtype=np.float64))
    per_rep = [kelvins_pack(y, oof[i]) for i in range(oof.shape[0])]
    mean = {k: float(np.mean([m[k] for m in per_rep])) for k in per_rep[0]}
    pooled = kelvins_pack(np.tile(y, oof.shape[0]), oof.ravel())
    return CvResult(oof, metrics or mean, per_rep, pooled, [], np.zeros(len(FEATURE_COLUMNS)),
                    floors=floors)


def _diag_setup(y, n_reps=1):
    n = len(y)
    table = pd.DataFrame({"event_id": np.arange(n, dtype=np.int64), "y_hr": y >= -6})
    return protocol_make_folds(table, seeds=tuple(range(42, 42 + n_reps)), n_splits=5)


def test_floor_c_diagnostics_r0_all_predictions_below_threshold():
    from src.models.trees import floor_c_diagnostics

    y = np.where(np.arange(100) < 20, -5.0, -30.0)
    folds = _diag_setup(y)
    res = _fake_res(y, np.full(100, -30.0), folds, _floors(folds))
    d = floor_c_diagnostics(y, res, folds)
    assert {"f_star_mean", "c_min", "c_max", "c_mean"} <= set(d)
    assert d["R0"]["evaluable"] and d["R0"]["fires"]
    assert d["reopen_required"]


def test_floor_c_diagnostics_summary_of_floors_and_clean_case():
    from src.models.trees import floor_c_diagnostics

    y = np.where(np.arange(100) < 20, -5.0, -30.0)
    folds = _diag_setup(y, n_reps=2)
    fl = _floors(folds, by_fold=lambda r, k: {"c": -10.0 - k - 5 * r,
                                              "f_star": 0.9 if k == 0 else 1.0})
    res = _fake_res(y, np.tile(y, (2, 1)), folds, fl)  # perfect predictions
    d = floor_c_diagnostics(y, res, folds)
    cs = [f["c"] for f in fl]
    assert d["c_min"] == pytest.approx(min(cs))
    assert d["c_max"] == pytest.approx(max(cs))
    assert d["c_mean"] == pytest.approx(np.mean(cs))
    assert d["f_star_mean"] == pytest.approx(np.mean([f["f_star"] for f in fl]))
    assert not d["R0"]["fires"]
    assert not d["R2"]["fires"]
    assert d["R3"]["evaluable"] and d["R3"]["ratio"] == pytest.approx(1.0)
    assert not d["R3"]["fires"]
    assert not d["R4"]["evaluable"]  # no HR events are missed
    assert d["R1"]["evaluable"] and not d["R1"]["fires"]  # F2 = 1 vs f_star_mean ~ 0.98
    assert d["reopen_required"] == any(d[k]["fires"] for k in ("R0", "R1", "R2", "R3", "R4"))


def test_floor_c_diagnostics_r1_band_around_f_star_mean():
    from src.models.trees import floor_c_diagnostics

    y = np.where(np.arange(100) < 20, -5.0, -30.0)
    folds = _diag_setup(y)
    fl = _floors(folds, f_star=0.5)
    base = _fake_res(y, y, folds, fl)
    for f2, fires in ((0.5, False), (0.2, True), (0.9, False), (1.2, True)):
        res = _fake_res(y, y, folds, fl, metrics={**base.metrics, "F2": f2})
        assert bool(floor_c_diagnostics(y, res, folds)["R1"]["fires"]) == fires


def test_floor_c_diagnostics_r2_fires_when_shifted_threshold_is_better():
    from src.models.trees import floor_c_diagnostics

    y = np.where(np.arange(100) < 20, -5.0, -30.0)
    folds = _diag_setup(y)
    pred = np.where(y >= -6, -6.5, -30.0)  # HR events sit just under the alarm threshold
    res = _fake_res(y, pred, folds, _floors(folds))
    d = floor_c_diagnostics(y, res, folds)
    assert d["R0"]["fires"]  # F2 at -6 is 0
    assert d["R2"]["evaluable"] and d["R2"]["fires"]
    assert d["R2"]["gain"] > 0.05
    assert d["R2"]["best_t"] <= -6.5 + 1e-9
    assert d["reopen_required"]


def test_floor_c_diagnostics_r2_keeps_truth_at_minus_six():
    from src.models.trees import floor_c_diagnostics

    # every event alarms; moving the truth line to -7 would wrongly turn F2 into 1
    y = np.where(np.arange(100) < 50, -5.5, -6.5)
    folds = _diag_setup(y)
    res = _fake_res(y, np.full(100, -5.5), folds, _floors(folds))
    d = floor_c_diagnostics(y, res, folds)
    assert d["R2"]["gain"] == pytest.approx(0.0)
    assert not d["R2"]["fires"]


def test_floor_c_diagnostics_r3_not_evaluable_with_few_distinct_hr_in_zone():
    from src.models.trees import floor_c_diagnostics

    y = np.where(np.arange(100) < 20, -5.0, -30.0)
    folds = _diag_setup(y, n_reps=2)
    pred = np.full(100, -30.0)
    pred[:6] = -5.0  # 6 distinct events, 12 pooled predictions
    res = _fake_res(y, np.tile(pred, (2, 1)), folds, _floors(folds))
    d = floor_c_diagnostics(y, res, folds)
    assert not d["R3"]["evaluable"] and not d["R3"]["fires"]


def test_floor_c_diagnostics_r3_fires_on_overconfident_zone():
    from src.models.trees import floor_c_diagnostics

    y = np.where(np.arange(100) < 15, -5.0, -30.0)
    folds = _diag_setup(y)
    pred = np.full(100, -30.0)
    pred[:60] = -5.0  # 15 true HR + 45 false alarms; p_hat = 1 (mu_hr = -5)
    res = _fake_res(y, pred, folds, _floors(folds))
    d = floor_c_diagnostics(y, res, folds)
    assert d["R3"]["evaluable"]
    assert d["R3"]["ratio"] == pytest.approx(0.25)
    assert d["R3"]["fires"] and d["reopen_required"]


def test_floor_c_diagnostics_r3_uses_floor_of_each_prediction_fold():
    from src.models.trees import floor_c_diagnostics

    y = np.where(np.arange(100) < 30, -5.0, -30.0)
    folds = _diag_setup(y)
    pred = np.where(y >= -6, -5.5, -30.0)
    cs = {k: -8.0 - 4 * k for k in range(5)}
    mus = {k: -5.0 + 0.1 * k for k in range(5)}
    fl = _floors(folds, by_fold=lambda r, k: {"c": cs[k], "mu_hr": mus[k]})
    d = floor_c_diagnostics(y, _fake_res(y, pred, folds, fl), folds)
    fold = folds[folds.rep == 0].fold.to_numpy()
    zone = pred >= -6
    p_hat = np.array([np.clip((-5.5 - cs[k]) / (mus[k] - cs[k]), 0, 1) for k in fold])
    assert d["R3"]["ratio"] == pytest.approx(1.0 / p_hat[zone].mean())


def test_floor_c_diagnostics_r4_not_evaluable_with_few_events_in_a_group():
    from src.models.trees import floor_c_diagnostics

    y = np.where(np.arange(100) < 23, -5.0, -30.0)
    folds = _diag_setup(y)
    pred = np.full(100, -30.0)
    pred[:20] = -5.0  # 20 detected, 3 missed
    d = floor_c_diagnostics(y, _fake_res(y, pred, folds, _floors(folds)), folds)
    assert not d["R4"]["evaluable"] and not d["R4"]["fires"]


def test_floor_c_diagnostics_r4_fires_when_missed_hr_are_much_lower():
    from src.models.trees import floor_c_diagnostics

    y = np.full(100, -30.0)
    y[:15] = -4.0   # detected
    y[15:30] = -5.9  # missed
    folds = _diag_setup(y)
    pred = np.where(np.arange(100) < 15, -5.0, -30.0)
    d = floor_c_diagnostics(y, _fake_res(y, pred, folds, _floors(folds, sd=0.5)), folds)
    assert d["R4"]["evaluable"]
    assert d["R4"]["diff"] == pytest.approx(1.9)
    assert d["R4"]["threshold"] == pytest.approx(0.4)
    assert d["R4"]["fires"] and d["reopen_required"]
    d2 = floor_c_diagnostics(y, _fake_res(y, pred, folds, _floors(folds, sd=3.0)), folds)
    assert d2["R4"]["threshold"] == pytest.approx(2.4)
    assert not d2["R4"]["fires"]
