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


# ---- iteration 2: HR sample weights (pj-072) + nested-CV selection of w (pj-073) ----

def test_iteration2_grid_constants():
    import src.models.trees as trees

    # pj-073: w grid capped at 10, 3 inner folds
    assert tuple(trees.W_GRID) == (1, 2, 5, 10)
    assert trees.INNER_SPLITS == 3


def test_hr_weights_weight_hr_events_only():
    from src.models.trees import hr_weights

    y = np.array([-6.0, -5.9, -6.01, -30.0, -4.0])
    out = hr_weights(y, 5)
    assert isinstance(out, np.ndarray) and out.dtype.kind == "f"
    assert out.tolist() == [5.0, 5.0, 1.0, 1.0, 5.0]  # -6.0 itself is HR (pj-001)
    assert hr_weights(y, 1).tolist() == [1.0] * 5


def _p_star_w(p_star, w):
    return w * p_star / (w * p_star + 1.0 - p_star)


def test_floor_c_w1_matches_unweighted_and_records_w():
    from src.models.trees import floor_c

    _, y, lrp, _ = _synth()
    base = floor_c(y, lrp)
    one = floor_c(y, lrp, w=1.0)
    assert one["c"] == base["c"]
    assert base["w"] == 1.0 and one["w"] == 1.0
    assert isinstance(base["w"], float)


@pytest.mark.parametrize("w", [2, 5, 10])
def test_floor_c_solves_weighted_calibration_equation(w):
    from src.metrics import f2_score
    from src.models.trees import floor_c

    _, y, lrp, _ = _synth()
    out = floor_c(y, lrp, w=w)
    assert out["w"] == float(w) and isinstance(out["w"], float)
    # p_star stays the unweighted F*/5; only the target of the equation is weighted
    assert out["f_star"] == pytest.approx(f2_score(y, lrp))
    assert out["p_star"] == pytest.approx(out["f_star"] / 5)
    assert out["mu_hr"] == pytest.approx(y[y >= -6.0].mean())  # unweighted mean
    assert -29.99 < out["c"] < -6.0005
    assert _p_of_c(y, out["c"]) == pytest.approx(_p_star_w(out["p_star"], w), abs=1e-6)
    assert _p_of_c(y, out["c"]) != pytest.approx(out["p_star"], abs=1e-3)


def test_floor_c_decreases_monotonically_in_w():
    from src.models.trees import floor_c

    _, y, lrp, _ = _synth()
    cs = [floor_c(y, lrp, w=w)["c"] for w in (1, 2, 5, 10)]
    assert all(a > b for a, b in zip(cs, cs[1:]))


def test_floor_c_diagnostics_r3_converts_weighted_probability_per_fold():
    from src.models.trees import floor_c_diagnostics

    y = np.where(np.arange(100) < 30, -5.0, -30.0)
    folds = _diag_setup(y)
    pred = np.where(y >= -6, -5.5, -30.0)  # p_w = 0.9 with c = -10, mu = -5
    ws = {0: 1.0, 1: 2.0, 2: 5.0, 3: 10.0, 4: 1.0}
    fl = _floors(folds, c=-10.0, mu=-5.0, by_fold=lambda r, k: {"w": ws[k]})
    d = floor_c_diagnostics(y, _fake_res(y, pred, folds, fl), folds)
    fold = folds[folds.rep == 0].fold.to_numpy()
    zone = pred >= -6
    p_w = 0.9
    p = np.array([p_w / (ws[k] - (ws[k] - 1.0) * p_w) for k in fold])
    assert d["R3"]["evaluable"]
    assert d["R3"]["ratio"] == pytest.approx(1.0 / p[zone].mean())
    assert d["R3"]["ratio"] != pytest.approx(1.0 / p_w)  # the unconverted ratio


def test_floor_c_diagnostics_r3_fires_only_after_conversion_with_large_w():
    from src.models.trees import floor_c_diagnostics

    y = np.where(np.arange(100) < 30, -5.0, -30.0)
    folds = _diag_setup(y)
    pred = np.where(y >= -6, -5.5, -30.0)
    # unconverted p_w = 0.9 -> ratio 1.11 (no fire); converted p = 0.9/1.9 -> ratio 2.11 (fires)
    fl = _floors(folds, c=-10.0, mu=-5.0, by_fold=lambda r, k: {"w": 10.0})
    d = floor_c_diagnostics(y, _fake_res(y, pred, folds, fl), folds)
    assert d["R3"]["ratio"] == pytest.approx(1.9 / 0.9)
    assert d["R3"]["fires"] and d["reopen_required"]


# select_by_inner_cv (pj-073)

def _inner_setup(n=120, seed=7):
    _, y, _, _ = _synth(n, seed=seed)
    tr = np.flatnonzero(np.arange(n) % 4 != 0)  # non-contiguous: positions != indices
    return y, tr


def _expected_inner_splits(y, tr, seed):
    from sklearn.model_selection import StratifiedKFold

    skf = StratifiedKFold(n_splits=3, shuffle=True, random_state=seed)
    return [(tr[a], tr[b]) for a, b in skf.split(np.zeros(len(tr)), y[tr] >= -6.0)]


def test_select_by_inner_cv_uses_stratified_seeded_splits_of_training_part():
    from src.models.trees import select_by_inner_cv

    y, tr = _inner_setup()
    calls = []

    def fp(fit_idx, pred_idx, w):
        calls.append((w, np.asarray(fit_idx).copy(), np.asarray(pred_idx).copy()))
        return {0: np.full(len(pred_idx), -30.0)}

    select_by_inner_cv(fp, (1, 5), tr, y, 43)
    assert len(calls) == 2 * 3  # one fit per (w, inner split); variants share it
    exp = _expected_inner_splits(y, tr, 43)
    got = {(w, frozenset(f.tolist()), frozenset(p.tolist())) for w, f, p in calls}
    want = {(w, frozenset(f.tolist()), frozenset(p.tolist())) for w in (1, 5) for f, p in exp}
    assert got == want
    tr_set = set(tr.tolist())
    for w in (1, 5):
        parts = [p for ww, _, p in calls if ww == w]
        pooled = np.concatenate(parts)
        assert sorted(pooled.tolist()) == sorted(tr_set)  # held-out parts partition tr
        n_hr = [int(np.sum(y[p] >= -6.0)) for p in parts]
        assert min(n_hr) >= 1 and max(n_hr) - min(n_hr) <= 1  # stratified by HR
    for _, f, p in calls:
        assert set(f.tolist()) | set(p.tolist()) == tr_set  # nothing outside tr is touched
        assert not set(f.tolist()) & set(p.tolist())

    # same seed -> same splits; another seed -> other splits
    again = []
    select_by_inner_cv(lambda f, p, w: (again.append(frozenset(np.asarray(p).tolist())),
                                        {0: np.full(len(p), -30.0)})[1], (1,), tr, y, 43)
    assert set(again) == {frozenset(p.tolist()) for _, p in exp}
    other = []
    select_by_inner_cv(lambda f, p, w: (other.append(frozenset(np.asarray(p).tolist())),
                                        {0: np.full(len(p), -30.0)})[1], (1,), tr, y, 44)
    assert set(other) != set(again)


def test_select_by_inner_cv_scores_pooled_l_not_mean_of_parts():
    from src.models.trees import kelvins_pack, select_by_inner_cv

    y, tr = _inner_setup()
    first = int(tr.min())
    parts = {}

    def fp(fit_idx, pred_idx, w):
        pred_idx = np.asarray(pred_idx)
        # the held-out part holding tr.min() misses every HR event (F2 = 0 there)
        pred = np.full(len(pred_idx), -30.0) if first in pred_idx else y[pred_idx] + 0.3
        parts.setdefault(w, []).append((pred_idx, pred))
        return {0: pred}

    best, scores = select_by_inner_cv(fp, (1,), tr, y, 42)
    idx = np.concatenate([p for p, _ in parts[1]])
    pr = np.concatenate([q for _, q in parts[1]])
    pooled = kelvins_pack(y[idx], pr)["L_unclipped"]
    per_part = [kelvins_pack(y[p], q)["L_unclipped"] for p, q in parts[1]]
    assert np.isinf(np.mean(per_part)) and np.isfinite(pooled)  # the two rules disagree
    assert scores[(1, 0)] == pytest.approx(pooled)
    assert best == (1, 0)


def test_select_by_inner_cv_ties_go_to_smallest_w_then_variant():
    from src.models.trees import select_by_inner_cv

    y, tr = _inner_setup()

    def same(fit_idx, pred_idx, w):
        p = y[np.asarray(pred_idx)] + 0.3
        return {8: p, 3: p.copy()}

    best, scores = select_by_inner_cv(same, (5, 1, 2), tr, y, 42)
    assert set(scores) == {(w, v) for w in (1, 2, 5) for v in (3, 8)}
    assert len(set(scores.values())) == 1
    assert best == (1, 3)

    def none(fit_idx, pred_idx, w):
        p = np.full(len(pred_idx), -30.0)
        return {8: p, 3: p.copy()}

    best, scores = select_by_inner_cv(none, (5, 1, 2), tr, y, 42)
    assert all(np.isinf(v) for v in scores.values())
    assert best == (1, 3)


def test_select_by_inner_cv_picks_strictly_lowest_pooled_l():
    from src.models.trees import select_by_inner_cv

    y, tr = _inner_setup()

    def fp(fit_idx, pred_idx, w):
        yy = y[np.asarray(pred_idx)]
        if w == 1:
            return {3: np.full(len(yy), -30.0), 8: np.full(len(yy), -30.0)}  # L = inf
        return {3: yy + 0.3, 8: yy + (0.01 if w == 2 else 0.3)}

    best, scores = select_by_inner_cv(fp, (1, 2, 5), tr, y, 42)
    assert set(scores) == {(w, v) for w in (1, 2, 5) for v in (3, 8)}
    assert np.isinf(scores[(1, 3)]) and np.isinf(scores[(1, 8)])
    assert scores[(2, 8)] < scores[(2, 3)] == pytest.approx(scores[(5, 8)])
    assert best == (2, 8)


# run_nested_tree_cv (pj-072 + pj-073)

def _nested_data(n=200, seed=0, reps=1):
    X, y, lrp, table = _synth(n, seed=seed)
    folds = protocol_make_folds(table, seeds=tuple(range(42, 42 + reps)), n_splits=5)
    return X, y, lrp, table.event_id.to_numpy(), folds


def _small_grids(monkeypatch, ws=(1, 5), ns=(3, 5)):
    import src.models.trees as trees

    monkeypatch.setattr(trees, "W_GRID", ws)
    monkeypatch.setattr(trees, "N_ESTIMATORS_GRID", ns)


def _explicit_fit(kind, n, rs, X, y, lrp, fit_idx, pred_idx, w):
    # w == 1 fits without sample_weight: in scikit-learn >= 1.9 RandomForestRegressor
    # bootstraps differently with explicit unit weights than with None, and w = 1 must
    # reproduce the unweighted pj-026 pipeline (run_oof_cv) exactly.
    import src.models.trees as trees

    c = trees.floor_c(y[fit_idx], lrp[fit_idx], w)["c"]
    pipe = (trees.make_rf if kind == "rf" else trees.make_gbdt)(n, rs)
    kw = {} if w == 1 else {"model__sample_weight": trees.hr_weights(y[fit_idx], w)}
    pipe.fit(X[fit_idx], np.maximum(y[fit_idx], c), **kw)
    return pipe.predict(X[pred_idx]), pipe


def _choice_from_inner_l(inner_l):
    best, best_l = None, None
    for key in sorted(inner_l, key=lambda s: tuple(int(t) for t in s.split("|"))):
        if best is None or inner_l[key] < best_l:
            best, best_l = key, inner_l[key]
    w, n = best.split("|")
    return int(w), int(n)


def test_run_nested_tree_cv_rejects_unknown_kind():
    from src.models.trees import run_nested_tree_cv

    X, y, lrp, eid, folds = _nested_data(100)
    with pytest.raises(ValueError):
        run_nested_tree_cv("xgb", X, y, lrp, eid, folds)


@pytest.mark.parametrize("kind", ["rf", "gbdt"])
def test_run_nested_tree_cv_structure_and_refit_on_outer_training_part(monkeypatch, kind):
    import src.models.trees as trees
    from src.models.trees import _fold_masks, floor_c, kelvins_pack, run_nested_tree_cv

    _small_grids(monkeypatch)
    X, y, lrp, eid, folds = _nested_data(reps=2)
    res = run_nested_tree_cv(kind, X, y, lrp, eid, folds)
    n = len(y)

    assert res.oof_pred.shape == (2, n) and not np.isnan(res.oof_pred).any()
    for fr in res.fold_frames:
        assert list(fr.columns) == ["event_id", "rep", "fold", "r_hat", "p_hr"]
    allf = pd.concat(res.fold_frames, ignore_index=True)
    assert len(allf) == 2 * n
    for rep in (0, 1):
        sub = allf[allf.rep == rep].sort_values("event_id")
        assert sub.event_id.tolist() == eid.tolist()  # every event exactly once per rep
        np.testing.assert_array_equal(sub.r_hat.to_numpy(), res.oof_pred[rep])
        np.testing.assert_array_equal(sub.fold.to_numpy(),
                                      folds[folds.rep == rep].sort_values("event_id").fold)
    np.testing.assert_array_equal(allf.p_hr.to_numpy(), (allf.r_hat >= -6.0).astype(float))

    assert [(f["rep"], f["fold"]) for f in res.floors] == [(r, k) for r in range(2) for k in range(5)]
    imps = []
    for f in res.floors:
        need = {"rep", "fold", "c", "mu_hr", "sd_hr", "f_star", "p_star", "w",
                "n_estimators", "inner_L"}
        assert need <= set(f)
        assert f["w"] in trees.W_GRID and f["n_estimators"] in trees.N_ESTIMATORS_GRID
        assert set(f["inner_L"]) == {f"{w}|{m}" for w in (1, 5) for m in (3, 5)}
        assert all(isinstance(v, float) for v in f["inner_L"].values())
        assert _choice_from_inner_l(f["inner_L"]) == (f["w"], f["n_estimators"])
        train_m, val_m = _fold_masks(folds, f["rep"], f["fold"])
        tr, va = np.flatnonzero(train_m), np.flatnonzero(val_m)
        assert f["c"] == pytest.approx(floor_c(y[tr], lrp[tr], f["w"])["c"])
        pred, pipe = _explicit_fit(kind, f["n_estimators"], 42 + f["rep"], X, y, lrp, tr, va,
                                   f["w"])
        np.testing.assert_allclose(res.oof_pred[f["rep"], va], pred, rtol=1e-10, atol=1e-10)
        imps.append(pipe.named_steps["model"].feature_importances_)

    assert res.importances.shape == (len(FEATURE_COLUMNS),)
    np.testing.assert_allclose(res.importances, np.mean(imps, axis=0), rtol=1e-8, atol=1e-12)
    for i in range(2):
        assert res.metrics_per_rep[i] == pytest.approx(kelvins_pack(y, res.oof_pred[i]))
    assert res.metrics == pytest.approx(
        {k: np.mean([m[k] for m in res.metrics_per_rep]) for k in res.metrics_per_rep[0]})
    assert res.metrics_pooled == pytest.approx(kelvins_pack(np.tile(y, 2), res.oof_pred.ravel()))


def test_run_nested_tree_cv_forced_large_w_reaches_the_refit(monkeypatch):
    from src.models.trees import _fold_masks, run_nested_tree_cv

    _small_grids(monkeypatch, ws=(5,), ns=(5,))
    X, y, lrp, eid, folds = _nested_data()
    res = run_nested_tree_cv("rf", X, y, lrp, eid, folds)
    assert all(f["w"] == 5 for f in res.floors)
    train_m, val_m = _fold_masks(folds, 0, 0)
    tr, va = np.flatnonzero(train_m), np.flatnonzero(val_m)
    weighted, _ = _explicit_fit("rf", 5, 42, X, y, lrp, tr, va, 5)
    c5 = res.floors[0]["c"]
    from src.models.trees import make_rf

    unweighted = make_rf(5, 42).fit(X[tr], np.maximum(y[tr], c5)).predict(X[va])
    assert not np.allclose(weighted, unweighted)  # the data make weights matter
    np.testing.assert_allclose(res.oof_pred[0, va], weighted, rtol=1e-10, atol=1e-10)


@pytest.mark.parametrize("kind", ["rf", "gbdt"])
def test_nested_inner_variants_equal_separate_weighted_fits(monkeypatch, kind):
    import src.models.trees as trees
    from src.models.trees import _fold_masks, run_nested_tree_cv

    _small_grids(monkeypatch, ws=(1, 5), ns=(3, 5, 8))
    X, y, lrp, eid, folds = _nested_data()
    seen = {}

    class _Stop(Exception):
        pass

    def spy(fit_predict, ws, tr, y_, seed):
        seen.update(fit_predict=fit_predict, ws=ws, tr=np.asarray(tr), y=y_, seed=seed)
        raise _Stop

    monkeypatch.setattr(trees, "select_by_inner_cv", spy)
    with pytest.raises(_Stop):
        run_nested_tree_cv(kind, X, y, lrp, eid, folds)

    train_m, _ = _fold_masks(folds, 0, 0)
    tr = np.flatnonzero(train_m)
    assert list(seen["ws"]) == [1, 5]
    np.testing.assert_array_equal(seen["tr"], tr)
    assert seen["seed"] == 42
    fit_idx, pred_idx = _expected_inner_splits(y, tr, 42)[0]
    for w in (1, 5):
        out = seen["fit_predict"](fit_idx, pred_idx, w)
        assert set(out) == {3, 5, 8}
        for n_est in (3, 5, 8):
            ref, _ = _explicit_fit(kind, n_est, 42, X, y, lrp, fit_idx, pred_idx, w)
            np.testing.assert_allclose(out[n_est], ref, rtol=1e-10, atol=1e-10)


def test_run_nested_tree_cv_never_reads_official_validation_fold(monkeypatch):
    from src.models.trees import _fold_masks, run_nested_tree_cv

    _small_grids(monkeypatch)
    X, y, lrp, eid, folds = _nested_data()
    a = run_nested_tree_cv("gbdt", X, y, lrp, eid, folds)

    _, val_m = _fold_masks(folds, 0, 0)
    y2, lrp2 = y.copy(), lrp.copy()
    hr_val = val_m & (y >= -6.0)
    y2[hr_val] = -10.0 - y[hr_val]  # still HR, other values
    y2[val_m & (y < -6.0) & (y > -7.0)] = -30.0
    lrp2[val_m] = np.random.default_rng(9).permutation(lrp[val_m])
    b = run_nested_tree_cv("gbdt", X, y2, lrp2, eid, folds)

    fa, fb = a.floors[0], b.floors[0]
    for key in ("c", "w", "n_estimators", "inner_L"):
        assert fa[key] == fb[key]
    np.testing.assert_array_equal(a.oof_pred[0, val_m], b.oof_pred[0, val_m])
    assert all(a.floors[k]["mu_hr"] != b.floors[k]["mu_hr"] for k in range(1, 5))
    assert any(a.floors[k]["c"] != b.floors[k]["c"] for k in range(1, 5))


def test_run_nested_tree_cv_deterministic(monkeypatch):
    from src.models.trees import run_nested_tree_cv

    _small_grids(monkeypatch)
    X, y, lrp, eid, folds = _nested_data(seed=1)
    a = run_nested_tree_cv("rf", X, y, lrp, eid, folds)
    b = run_nested_tree_cv("rf", X, y, lrp, eid, folds)
    np.testing.assert_allclose(a.oof_pred, b.oof_pred, rtol=1e-12)
    assert [(f["w"], f["n_estimators"], f["c"]) for f in a.floors] == \
        [(f["w"], f["n_estimators"], f["c"]) for f in b.floors]


@pytest.mark.parametrize("kind", ["rf", "gbdt"])
def test_run_nested_tree_cv_with_w1_only_reproduces_unweighted_pipeline(monkeypatch, kind):
    import src.models.trees as trees
    from src.models.trees import run_nested_tree_cv

    _small_grids(monkeypatch, ws=(1,), ns=(5,))
    X, y, lrp, eid, folds = _nested_data(reps=2)
    res = run_nested_tree_cv(kind, X, y, lrp, eid, folds)
    factory = trees.make_rf if kind == "rf" else trees.make_gbdt
    ref = run_oof_cv(lambda rs: factory(5, rs), X, y, eid, folds, lrp=lrp)
    np.testing.assert_allclose(res.oof_pred, ref.oof_pred, rtol=1e-10, atol=1e-10)
    assert [f["c"] for f in res.floors] == pytest.approx([f["c"] for f in ref.floors])
    assert all(f["w"] == 1 and f["n_estimators"] == 5 for f in res.floors)


def _fit_recorder(monkeypatch):
    from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor

    seen = []
    for cls in (RandomForestRegressor, GradientBoostingRegressor):
        orig = cls.fit

        def fit(self, *a, _orig=orig, **k):
            seen.append(self.random_state)
            return _orig(self, *a, **k)

        monkeypatch.setattr(cls, "fit", fit)
    return seen


def _assert_same_result(a, b):
    np.testing.assert_array_equal(a.oof_pred, b.oof_pred)
    assert a.floors == b.floors
    assert a.metrics == b.metrics and a.metrics_pooled == b.metrics_pooled
    assert a.metrics_per_rep == b.metrics_per_rep
    np.testing.assert_array_equal(a.importances, b.importances)
    assert len(a.fold_frames) == len(b.fold_frames)
    for fa, fb in zip(a.fold_frames, b.fold_frames):
        pd.testing.assert_frame_equal(fa.reset_index(drop=True), fb.reset_index(drop=True))


def test_run_nested_tree_cv_cache_reuses_and_completes_reps(monkeypatch, tmp_path):
    import os

    from src.models.trees import run_nested_tree_cv

    _small_grids(monkeypatch)
    X, y, lrp, eid, folds = _nested_data(reps=2)
    first = run_nested_tree_cv("gbdt", X, y, lrp, eid, folds, cache_dir=tmp_path)
    assert sorted(os.listdir(tmp_path)) == ["rep0.pkl", "rep1.pkl"]  # no temp leftovers

    seen = _fit_recorder(monkeypatch)
    again = run_nested_tree_cv("gbdt", X, y, lrp, eid, folds, cache_dir=tmp_path)
    assert seen == []  # fully cached: no model is fitted
    _assert_same_result(first, again)

    os.remove(tmp_path / "rep1.pkl")
    part = run_nested_tree_cv("gbdt", X, y, lrp, eid, folds, cache_dir=tmp_path)
    assert seen and set(seen) == {43}  # only rep 1 (seed 43) is recomputed
    _assert_same_result(first, part)
    assert sorted(os.listdir(tmp_path)) == ["rep0.pkl", "rep1.pkl"]


def test_importance_diagnostics_uses_model_specific_w(monkeypatch):
    import src.models.trees as trees
    from src.models.trees import _fold_masks, floor_c, hr_weights, importance_diagnostics

    X, y, lrp, table = _synth(150, seed=5)
    folds = protocol_make_folds(table, seeds=(42,), n_splits=5)
    eid = table.event_id.to_numpy()
    rf = run_oof_cv(lambda rs: make_rf(5, rs), X, y, eid, folds, lrp=lrp)
    gb = run_oof_cv(lambda rs: make_gbdt(5, rs), X, y, eid, folds, lrp=lrp)

    fitted = {}

    def recording(factory, label):
        def make(n, rs):
            pipe = factory(n, rs)
            orig = pipe.fit

            def fit(Xf, yf, *a, **k):
                fitted[label] = (np.asarray(yf).copy(), k.get("model__sample_weight"))
                return orig(Xf, yf, *a, **k)

            pipe.fit = fit
            return pipe
        return make

    monkeypatch.setattr(trees, "make_rf", recording(trees.make_rf, "rf"))
    monkeypatch.setattr(trees, "make_gbdt", recording(trees.make_gbdt, "gbdt"))
    d = importance_diagnostics(rf.importances, gb.importances, X, y, folds, 5, 5, lrp=lrp,
                               rf_w=2.0, gbdt_w=10.0)
    assert "reopen_required" in d
    train_m, _ = _fold_masks(folds, 0, 0)
    for label, w in (("rf", 2.0), ("gbdt", 10.0)):
        yf, sw = fitted[label]
        c = floor_c(y[train_m], lrp[train_m], w)["c"]
        np.testing.assert_allclose(yf, np.maximum(y[train_m], c))
        assert sw is not None
        np.testing.assert_array_equal(np.asarray(sw), hr_weights(y[train_m], w))
    assert fitted["rf"][0].min() > fitted["gbdt"][0].min()  # different c per model
