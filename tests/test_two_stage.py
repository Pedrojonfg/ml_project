"""S6 stage 1 (mf-021..mf-039): logistic classifiers, 1-SE C choice, OOF scores, Platt, Brier."""

import numpy as np
import pandas as pd
import pytest
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score

import src.models.two_stage as ts
from src.metrics import HR_THRESHOLD_LOG10
from src.models.linear import make_preprocessor
from src.models.two_stage import (
    C_GRIDS,
    CLASSIFIERS,
    _one_se_choice,
    brier,
    fit_platt,
    fit_predict_fold,
    make_logistic,
    oof_z,
    platt_p,
    reliability_diagram,
    run_stage1_cv,
    select_c,
)
from src.protocol import make_folds


def _xy(n=150, seed=0):
    # 30 numeric + 5 one-hot columns (mf-010 layout); y = risk_final, ~25% HR
    rng = np.random.default_rng(seed)
    X = np.hstack([rng.normal(size=(n, 30)), np.eye(5)[rng.integers(0, 5, n)]])
    y = -7.5 + 1.2 * X[:, 0] + 0.6 * X[:, 1] + rng.normal(scale=0.7, size=n)
    return X, y


@pytest.fixture
def small_grids(monkeypatch):
    # 3-point grids keep runtime small; module must read C_GRIDS at call time (as S4 precedent)
    monkeypatch.setattr(ts, "C_GRIDS", {"lr_l2": np.array([1e-2, 1.0, 1e2]),
                                        "lr_l1": np.array([1e-2, 1.0, 1e2])})


def _sigmoid(x):
    return 1 / (1 + np.exp(-x))


# ---------------------------------------------------------------- make_logistic / grids

def test_classifiers_names():
    assert CLASSIFIERS == ("lr_none", "lr_l2", "lr_l1")  # mf-021


@pytest.mark.parametrize("name,solver", [("lr_none", "lbfgs"), ("lr_l2", "lbfgs"), ("lr_l1", "liblinear")])
def test_make_logistic_registered_params(name, solver):
    m = make_logistic(name, None if name == "lr_none" else 1.0)
    p = m.get_params()
    assert p["solver"] == solver  # mf-030, mf-041 (L1 liblinear)
    assert p["max_iter"] == 10000 and p["tol"] == 1e-4
    assert p["class_weight"] == "balanced"  # mf-011
    assert p["fit_intercept"] is True and p["warm_start"] is False
    assert p["intercept_scaling"] == (100 if name == "lr_l1" else 1)  # mf-041 / mf-030
    assert p["dual"] is False
    if name == "lr_l1":
        assert p["random_state"] == 0 and p["l1_ratio"] == 1.0  # mf-041


def test_make_logistic_unknown_raises():
    with pytest.raises(ValueError):
        make_logistic("lr_elastic", 1.0)


def test_make_logistic_penalty_behavior():
    X, y = _xy(200)
    yh = y >= HR_THRESHOLD_LOG10
    Z = make_preprocessor().fit_transform(X)
    # L1 with small C gives exact zeros; L2 does not (mf-009)
    l1 = make_logistic("lr_l1", 0.02).fit(Z, yh)
    l2 = make_logistic("lr_l2", 0.02).fit(Z, yh)
    assert (l1.coef_ == 0).sum() > 0
    assert (l2.coef_ == 0).sum() == 0
    # unpenalized == L2 with a huge C
    none = make_logistic("lr_none").fit(Z, yh)
    big = make_logistic("lr_l2", 1e8).fit(Z, yh)
    np.testing.assert_allclose(none.coef_, big.coef_, atol=1e-3)


def test_c_grids_mf026():
    assert set(C_GRIDS) == {"lr_l2", "lr_l1"}
    g2, g1 = C_GRIDS["lr_l2"], C_GRIDS["lr_l1"]
    assert len(g2) == len(g1) == 25
    np.testing.assert_allclose([g2[0], g2[-1]], [1e-4, 1e4])
    np.testing.assert_allclose([g1[0], g1[-1]], [1e-2, 1e4])


# ---------------------------------------------------------------- 1-SE rule (pure helper)

def test_one_se_exact_tie_takes_smallest_c_star_and_its_se():
    # mf-039: C* = smallest C among tied maxima; SE from C*'s five AUCs (mf-027, ddof=1)
    aucs = {
        1.0: [0.89] * 5,
        10.0: [0.88, 0.92, 0.90, 0.90, 0.90],     # small spread
        100.0: [0.70, 1.00, 0.90, 0.80, 1.00][:5],  # large spread, would widen the set
        1000.0: [0.5] * 5,
    }
    mean_auc = {1.0: 0.89, 10.0: 0.9, 100.0: 0.9, 1000.0: 0.5}
    r = _one_se_choice(mean_auc, aucs)
    se = np.std(aucs[10.0], ddof=1) / np.sqrt(5)
    assert se < 0.01  # so C=1 (0.89) is outside the tie set only if SE comes from C=10
    assert r["c_star"] == 10.0
    assert r["se"] == pytest.approx(se)
    assert r["tie_set"] == [10.0, 100.0]
    assert r["C"] == 10.0


def test_one_se_selects_smallest_of_tie_set():
    aucs = {1.0: [0.7] * 5, 10.0: [0.9] * 5, 100.0: [0.88, 0.92, 0.90, 0.90, 0.90], 1000.0: [0.5] * 5}
    mean_auc = {1.0: 0.7, 10.0: 0.895, 100.0: 0.9, 1000.0: 0.5}
    r = _one_se_choice(mean_auc, aucs)
    se = np.std(aucs[100.0], ddof=1) / np.sqrt(5)
    assert r["c_star"] == 100.0
    assert r["se"] == pytest.approx(se)
    assert r["tie_set"] == [10.0, 100.0]  # 0.895 >= 0.9 - se; 0.7 is out
    assert r["C"] == 10.0  # mf-027: smallest C of the tie set


# ---------------------------------------------------------------- select_c

@pytest.mark.parametrize("name", ["lr_l2", "lr_l1"])
def test_select_c_in_grid_deterministic_and_edge(name, small_grids):
    X, y = _xy(120)
    yh = y >= HR_THRESHOLD_LOG10
    r1, r2 = select_c(name, X, yh), select_c(name, X, yh)
    grid = list(ts.C_GRIDS[name])
    assert r1["C"] in grid
    assert r1 == r2  # mf-030: identical across runs
    assert set(r1["mean_auc"]) == set(grid)
    assert r1["edge"] == (r1["C"] in (grid[0], grid[-1]))  # mf-029
    assert r1["tie_set"] == sorted(r1["tie_set"]) and r1["C"] == min(r1["tie_set"])
    assert r1["c_star"] == min(c for c in grid if r1["mean_auc"][c] == max(r1["mean_auc"].values()))
    assert isinstance(r1["nonconverged"], list)


def test_select_c_single_point_grid_is_edge(monkeypatch):
    monkeypatch.setattr(ts, "C_GRIDS", {"lr_l2": np.array([1.0]), "lr_l1": np.array([1.0])})
    X, y = _xy(100)
    assert select_c("lr_l2", X, y >= HR_THRESHOLD_LOG10)["edge"] is True


def test_select_c_mean_auc_matches_independent_computation(small_grids):
    # mf-025, mf-028, mf-010: mean over 5 inner folds of AUC of decision_function, preprocessor refit per part
    X, y = _xy(120)
    yh = y >= HR_THRESHOLD_LOG10
    r = select_c("lr_l2", X, yh)
    skf = StratifiedKFold(5, shuffle=True, random_state=0)
    for C in ts.C_GRIDS["lr_l2"]:
        aucs = []
        for tr, va in skf.split(X, yh):
            pre = make_preprocessor().fit(X[tr])
            m = make_logistic("lr_l2", float(C)).fit(pre.transform(X[tr]), yh[tr])
            aucs.append(roc_auc_score(yh[va], m.decision_function(pre.transform(X[va]))))
        assert r["mean_auc"][C] == pytest.approx(np.mean(aucs))


# ---------------------------------------------------------------- oof_z

@pytest.mark.parametrize("name,C", [("lr_none", None), ("lr_l2", 1.0)])
def test_oof_z_shape_determinism_and_independent_recompute(name, C):
    X, y = _xy(120)
    yh = y >= HR_THRESHOLD_LOG10
    z, nonconv = oof_z(name, C, X, yh)
    z2, _ = oof_z(name, C, X, yh)
    assert z.shape == (len(y),) and np.isfinite(z).all()
    np.testing.assert_array_equal(z, z2)
    assert isinstance(nonconv, bool)
    # mf-032/mf-038: z of each row from a model trained on the other 4 inner folds, preprocessor refit
    exp = np.empty(len(y))
    for tr, va in StratifiedKFold(5, shuffle=True, random_state=0).split(X, yh):
        pre = make_preprocessor().fit(X[tr])
        m = make_logistic(name, C).fit(pre.transform(X[tr]), yh[tr])
        exp[va] = m.decision_function(pre.transform(X[va]))
    np.testing.assert_allclose(z, exp, atol=1e-9)


def test_oof_z_lr_none_ignores_c():
    X, y = _xy(100)
    yh = y >= HR_THRESHOLD_LOG10
    np.testing.assert_array_equal(oof_z("lr_none", None, X, yh)[0], oof_z("lr_none", 123.0, X, yh)[0])


# ---------------------------------------------------------------- Platt

def test_fit_platt_recovers_known_logit():
    rng = np.random.default_rng(0)
    z = rng.normal(scale=2.0, size=20000)
    y = rng.random(20000) < _sigmoid(1.0 * z - 2.0)  # imbalanced: class_weight=None keeps b near -2 (mf-033)
    r = fit_platt(z, y)
    assert r["a"] == pytest.approx(1.0, abs=0.1)
    assert r["b"] == pytest.approx(-2.0, abs=0.15)
    assert r["converged"] is True


def test_platt_p_is_sigmoid_and_monotone():
    z = np.linspace(-5, 5, 11)
    p = platt_p(z, 0.7, 0.3)
    np.testing.assert_allclose(p, _sigmoid(0.7 * z + 0.3))
    assert (np.diff(p) > 0).all()


# ---------------------------------------------------------------- fit_predict_fold

KEYS = {"C", "c_star", "se", "tie_size", "edge", "a", "b", "a_nonpositive", "t",
        "z_val", "p_val", "alarm_val", "platt_converged", "final_converged"}


@pytest.mark.parametrize("name", ["lr_none", "lr_l2"])
def test_fit_predict_fold_contract(name, small_grids):
    X, y = _xy(150)
    Xtr, ytr, Xva = X[:110], y[:110], X[110:]
    r = fit_predict_fold(name, Xtr, ytr, Xva)
    assert KEYS <= set(r)
    assert r["z_val"].shape == r["p_val"].shape == r["alarm_val"].shape == (40,)
    assert r["alarm_val"].dtype == np.float64
    np.testing.assert_array_equal(r["alarm_val"], (r["p_val"] >= r["t"]).astype(np.float64))
    np.testing.assert_allclose(r["p_val"], platt_p(r["z_val"], r["a"], r["b"]))
    assert r["a_nonpositive"] == (r["a"] <= 0)  # mf-031
    if name == "lr_none":
        assert r["C"] is None  # mf-032: no C
    else:
        assert r["C"] in list(ts.C_GRIDS[name]) and r["tie_size"] >= 1
    # mf-035: t is the calibrated p of one of the training HR events (out-of-fold)
    yh = ytr >= HR_THRESHOLD_LOG10
    z, _ = oof_z(name, r["C"], Xtr, yh)
    cands = platt_p(z, r["a"], r["b"])[yh]
    assert np.isclose(cands, r["t"], rtol=0, atol=1e-12).any()


def test_fit_predict_fold_no_validation_leakage(small_grids):
    X, y = _xy(150)
    Xtr, ytr = X[:110], y[:110]
    r1 = fit_predict_fold("lr_l2", Xtr, ytr, X[110:])
    r2 = fit_predict_fold("lr_l2", Xtr, ytr, np.random.default_rng(9).normal(size=(40, 35)) * 50)
    for k in ("C", "c_star", "se", "a", "b", "t"):
        assert r1[k] == r2[k]  # mf-032: nothing from the validation fold enters C, (a, b) or t


def test_a_nonpositive_flag_kept_not_forced(small_grids, monkeypatch):
    # mf-031: anti-informative OOF scores -> a <= 0, fit kept as is
    X, y = _xy(150)
    yh = y[:110] >= HR_THRESHOLD_LOG10
    rng = np.random.default_rng(1)
    anti = -(2.0 * yh - 1) + rng.normal(scale=0.3, size=110)
    monkeypatch.setattr(ts, "oof_z", lambda name, C, Xt, yt: (anti, False))
    r = fit_predict_fold("lr_l2", X[:110], y[:110], X[110:])
    assert r["a"] < 0 and r["a_nonpositive"] is True


# ---------------------------------------------------------------- Brier / reliability

def test_brier_hand_value():
    assert brier(np.array([0.8, 0.2, 0.5]), np.array([1, 0, 0])) == pytest.approx((0.04 + 0.04 + 0.25) / 3)


def test_reliability_diagram_hand_case():
    # mf-036: sort by p, np.array_split into k groups (7 -> 3,2,2)
    p = np.array([0.7, 0.1, 0.4, 0.2, 0.6, 0.3, 0.5])
    y = np.array([1, 0, 0, 0, 1, 1, 0])
    mp, obs = reliability_diagram(p, y, k=3)
    # sorted p: .1 .2 .3 | .4 .5 | .6 .7 ; sorted y: 0 0 1 | 0 0 | 1 1
    np.testing.assert_allclose(mp, [0.2, 0.45, 0.65])
    np.testing.assert_allclose(obs, [1 / 3, 0.0, 1.0])


# ---------------------------------------------------------------- run_stage1_cv

def test_run_stage1_cv_shapes_and_brier(small_grids):
    X, y = _xy(150)
    yh = y >= HR_THRESHOLD_LOG10
    table = pd.DataFrame({"event_id": np.arange(len(y)) + 100, "y_hr": yh})
    folds = make_folds(table, seeds=(1, 2), n_splits=5)
    res = run_stage1_cv("lr_l2", X, y, table.event_id.to_numpy(), folds)
    for a in (res.oof_z, res.oof_p, res.oof_alarm):
        assert a.shape == (2, 150) and not np.isnan(a).any()
    assert set(np.unique(res.oof_alarm)) <= {0.0, 1.0}
    assert len(res.brier_per_rep) == 2
    for i in range(2):
        assert res.brier_per_rep[i] == pytest.approx(brier(res.oof_p[i], yh))
    assert res.brier == pytest.approx(np.mean(res.brier_per_rep))  # mf-036: mean over repetitions
    assert len(res.fold_records) == len(res.fold_frames) == 10
    assert {(r["rep"], r["fold"]) for r in res.fold_records} == {(i, k) for i in range(2) for k in range(5)}
    assert list(res.fold_frames[0].columns) == ["event_id", "rep", "fold", "z", "p_cal", "alarm"]


# ---------------------------------------------------------------- run_stage1_cv parallelism (engineering only)

def test_run_stage1_cv_n_jobs_default_is_one():
    import inspect
    assert inspect.signature(run_stage1_cv).parameters["n_jobs"].default == 1


def _assert_parallel_equals_sequential(name):
    X, y = _xy(150)
    yh = y >= HR_THRESHOLD_LOG10
    table = pd.DataFrame({"event_id": np.arange(len(y)) + 100, "y_hr": yh})
    folds = make_folds(table, seeds=(1, 2), n_splits=5)
    ids = table.event_id.to_numpy()
    s = run_stage1_cv(name, X, y, ids, folds, n_jobs=1)
    p = run_stage1_cv(name, X, y, ids, folds, n_jobs=2)
    for f in ("oof_z", "oof_p", "oof_alarm"):
        assert np.array_equal(getattr(s, f), getattr(p, f))
    assert s.brier_per_rep == p.brier_per_rep and s.brier == p.brier
    assert s.fold_records == p.fold_records  # same content and order (rep-major, fold ascending)
    assert len(s.fold_frames) == len(p.fold_frames)
    for a, b in zip(s.fold_frames, p.fold_frames):
        pd.testing.assert_frame_equal(a, b)


def test_run_stage1_cv_parallel_identical_to_sequential():
    _assert_parallel_equals_sequential("lr_none")


def test_run_stage1_cv_parallel_identical_lr_l2_real_grid():
    # real 25-point C_GRIDS, no monkeypatch: workers import the real module (select_c / grid path)
    assert len(ts.C_GRIDS["lr_l2"]) == 25
    _assert_parallel_equals_sequential("lr_l2")
