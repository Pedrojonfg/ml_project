"""S4 linear regressors (mf-008..mf-015): preprocessing, solvers, alpha, alarm line, CV."""

import warnings

import numpy as np
import pandas as pd
import pytest
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import Lasso
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import average_precision_score

import src.models.linear as lin
from src.features import FEATURE_COLUMNS
from src.metrics import f2_score, kelvins_l, mse_hr
from src.models.linear import (
    choose_alarm_line,
    fit_predict_fold,
    make_model,
    make_preprocessor,
    run_linear_cv,
    select_alpha,
)
from src.protocol import make_folds

_RIDGE0, _LASSO0 = lin.RIDGE_ALPHAS, lin.LASSO_ALPHAS  # originals, before patching
NF = len(FEATURE_COLUMNS)  # 35: 30 numeric + 5 one-hot (mf-010)


@pytest.fixture(autouse=True)
def small_grids(monkeypatch):
    # 3-point grids keep the runtime small; module reads globals at call time
    monkeypatch.setattr(lin, "RIDGE_ALPHAS", np.array([1.0, 100.0, 1e4]))
    monkeypatch.setattr(lin, "LASSO_ALPHAS", np.array([1e-3, 1e-1, 1e1]))


def _xy(n=120, seed=0):
    rng = np.random.default_rng(seed)
    X = np.hstack([rng.normal(size=(n, 30)), np.eye(5)[rng.integers(0, 5, n)]])
    y = -8.0 + 1.5 * X[:, 0] + 0.5 * X[:, 1] + rng.normal(scale=0.5, size=n)
    return X, y


def _folds(y, seeds=(1, 2)):
    t = pd.DataFrame({"event_id": np.arange(len(y)), "y_hr": y >= -6.0})
    return t.event_id.to_numpy(), make_folds(t, seeds=seeds, n_splits=5)


# ---------------------------------------------------------------- (1) preprocessing

def test_preprocessor_scales_numeric_only_and_keeps_order():
    X, _ = _xy()
    Z = make_preprocessor().fit_transform(X)
    assert Z.shape == X.shape
    np.testing.assert_allclose(Z[:, :30].mean(0), 0, atol=1e-9)  # per mf-010
    np.testing.assert_allclose(Z[:, :30].std(0), 1, atol=1e-9)
    np.testing.assert_array_equal(Z[:, 30:], X[:, 30:])  # one-hot untouched


def test_preprocessor_imputes_with_train_median():
    X, _ = _xy()
    X[0, 3] = np.nan
    X[1, 31] = np.nan
    pipe = make_preprocessor().fit(X)
    Xv = np.full((1, NF), np.nan)
    Z = pipe.transform(Xv)
    assert not np.isnan(Z).any()
    med = np.nanmedian(X, axis=0)
    assert Z[0, 31] == med[31]  # one-hot NaN -> train median, unscaled


# ---------------------------------------------------------------- (2) no leakage

def test_transforming_validation_does_not_change_fitted_statistics():
    X, _ = _xy()
    pipe = make_preprocessor().fit(X[:80])
    before = pipe.transform(X[:80])
    Zv = pipe.transform(X[80:] * 100 + 7)
    np.testing.assert_array_equal(pipe.transform(X[:80]), before)
    mu, sd = X[:80, :30].mean(0), X[:80, :30].std(0)
    np.testing.assert_allclose(Zv[:, :30], (X[80:, :30] * 100 + 7 - mu) / sd)


@pytest.mark.parametrize("name", ["ridge", "lasso"])
def test_fold_alpha_and_t_ignore_validation_x(name):
    X, y = _xy()
    a = fit_predict_fold(name, X[:90], y[:90], X[90:])
    b = fit_predict_fold(name, X[:90], y[:90], X[90:] * 50 + 3)
    assert a["alpha"] == b["alpha"] and a["t"] == b["t"]


@pytest.mark.parametrize("name", ["ridge", "lasso"])
def test_cv_fold_alpha_and_t_ignore_validation_y(name):
    X, y = _xy()
    eid, folds = _folds(y)
    a = run_linear_cv(name, X, y, eid, folds)
    f0 = folds[(folds.rep == 0) & (folds.fold == 0)].event_id.to_numpy()
    y2 = y.copy()
    y2[f0] = -3.0  # change validation targets of rep 0 fold 0 only
    b = run_linear_cv(name, X, y2, eid, folds)
    ra, rb = a.fold_records[0], b.fold_records[0]
    assert (ra["rep"], ra["fold"]) == (0, 0)
    assert ra["alpha"] == rb["alpha"] and ra["t"] == rb["t"]


# ---------------------------------------------------------------- (3) solver agreement

def test_ols_matches_min_norm_lstsq_with_intercept():
    X, y = _xy()
    Z = make_preprocessor().fit_transform(X)
    m = make_model("ols").fit(Z, y)
    A = np.hstack([np.ones((len(y), 1)), Z])
    beta = np.linalg.lstsq(A, y, rcond=None)[0]
    np.testing.assert_allclose(m.predict(Z), A @ beta, atol=1e-8)


def test_ridge_matches_closed_form():
    X, y = _xy()
    Z = make_preprocessor().fit_transform(X)
    Zc, yc = Z - Z.mean(0), y - y.mean()
    alpha = 37.0
    coef = np.linalg.solve(Zc.T @ Zc + alpha * np.eye(NF), Zc.T @ yc)
    m = make_model("ridge", alpha).fit(Z, y)
    np.testing.assert_allclose(m.coef_, coef, atol=1e-8)


def test_lasso_all_zero_above_alpha_max():
    X, y = _xy()
    Z = make_preprocessor().fit_transform(X)
    Zc, yc = Z - Z.mean(0), y - y.mean()
    amax = np.abs(Zc.T @ yc).max() / len(y)
    m = make_model("lasso", 1.01 * amax).fit(Z, y)
    assert not m.coef_.any()


# ---------------------------------------------------------------- (4) select_alpha

def test_select_alpha_rejects_ols():
    X, y = _xy()
    with pytest.raises(ValueError):
        select_alpha("ols", X, y)


def test_select_alpha_tie_goes_to_highest(monkeypatch):
    X, y = _xy()
    # huge alphas -> constant predictions -> identical mean AP (mf-013)
    monkeypatch.setattr(lin, "LASSO_ALPHAS", np.array([1e3, 1e4, 1e5]))
    out = select_alpha("lasso", X, y)
    assert len(set(out["mean_ap"].values())) == 1
    assert out["alpha"] == 1e5


def test_select_alpha_matches_manual_inner_cv_seed_0():
    X, y = _xy()
    yhr = y >= -6.0
    out = select_alpha("ridge", X, y)
    manual = {}
    skf = StratifiedKFold(5, shuffle=True, random_state=0)  # per mf-015
    for a in lin.RIDGE_ALPHAS:
        aps = []
        for tr, va in skf.split(X, yhr):
            p = make_preprocessor().fit(X[tr])
            m = make_model("ridge", a).fit(p.transform(X[tr]), y[tr])
            aps.append(average_precision_score(yhr[va], m.predict(p.transform(X[va]))))
        manual[float(a)] = np.mean(aps)
    assert set(out["mean_ap"]) == set(manual)
    for a, v in manual.items():
        assert out["mean_ap"][a] == pytest.approx(v)
    assert out["alpha"] == max(manual, key=lambda a: (round(manual[a], 12), a))


def test_lasso_sweep_descending_one_object_per_inner_fold(monkeypatch):
    X, y = _xy()
    calls = []
    orig = Lasso.fit

    def rec(self, *a, **k):
        calls.append((id(self), self.alpha))
        return orig(self, *a, **k)

    monkeypatch.setattr(Lasso, "fit", rec)
    select_alpha("lasso", X, y)  # per mf-014
    assert len(calls) == 5 * 3
    for i in range(5):
        chunk = calls[3 * i: 3 * i + 3]
        assert len({c[0] for c in chunk}) == 1  # same object along the grid
        assert [c[1] for c in chunk] == sorted(lin.LASSO_ALPHAS, reverse=True)
    assert len({c[0] for c in calls}) == 5  # new object per inner fold


# ---------------------------------------------------------------- (5) alarm line

def _brute_t(r, y):
    hr = y >= -6.0
    cands = np.unique(r[hr])
    f = np.array([f2_score(y, np.where(r >= c, 0.0, -100.0)) for c in cands])
    return float(np.median(cands[np.isclose(f, f.max(), rtol=0, atol=1e-12)]))


def test_alarm_line_is_a_hr_candidate_and_matches_brute_force():
    rng = np.random.default_rng(3)
    y = np.where(rng.random(40) < 0.3, -5.0, -9.0)
    r = y + rng.normal(scale=2.0, size=40)
    t = choose_alarm_line(r, y)
    assert t == _brute_t(r, y)
    assert t in set(r[y >= -6.0])  # unique max here -> a candidate itself (mf-012)


def test_alarm_line_tiny_example():
    # HR r_hat 3 and 1; non-HR 2. c=3: P=1,R=.5 ; c=1: P=2/3,R=1 -> F2 higher at c=1
    r = np.array([3.0, 1.0, 2.0])
    y = np.array([-5.0, -5.0, -9.0])
    assert choose_alarm_line(r, y) == 1.0


def _tied(P, k):
    """HR candidates tie at max F2 for the last k HR events (F2 = 5tp/(4P+tp+fp))."""
    r, y, tied, v = [], [], [], 1000.0
    for _ in range(P - k + 1):
        r.append(v); y.append(-5.0); v -= 1
    tied.append(r[-1])
    for _ in range(k - 1):
        for _ in range(5):
            r.append(v); y.append(-9.0); v -= 1
        r.append(v); y.append(-5.0); tied.append(v); v -= 1
    return np.array(r), np.array(y), tied


@pytest.mark.parametrize("P,k", [(10, 3), (15, 4)])
def test_alarm_line_tie_median(P, k):
    r, y, tied = _tied(P, k)
    t = choose_alarm_line(r, y)
    assert t == np.median(tied)  # odd: central; even: mean of two central
    assert t == _brute_t(r, y)


# ---------------------------------------------------------------- (6) registered parameters

def test_make_model_registered_params():
    p = make_model("ols").get_params()
    assert (p["fit_intercept"], p["positive"], p["copy_X"]) == (True, False, True)  # mf-014
    p = make_model("ridge", 5.0).get_params()
    assert p["alpha"] == 5.0 and p["solver"] == "cholesky"  # mf-014
    assert (p["fit_intercept"], p["positive"], p["copy_X"]) == (True, False, True)
    p = make_model("lasso", 0.5).get_params()
    assert p["alpha"] == 0.5
    assert (p["max_iter"], p["tol"], p["selection"]) == (10000, 1e-4, "cyclic")  # mf-014
    assert (p["warm_start"], p["precompute"], p["positive"]) == (True, False, False)
    assert (p["fit_intercept"], p["copy_X"]) == (True, True)


def test_registered_constants():
    np.testing.assert_allclose(_RIDGE0, np.logspace(0, 6, 25))  # mf-013
    np.testing.assert_allclose(_LASSO0, np.logspace(-4, 2, 25))  # mf-013
    assert lin.INNER_SEED == 0 and lin.INNER_SPLITS == 5  # mf-015


# ---------------------------------------------------------------- (7) run_linear_cv

@pytest.mark.parametrize("name", ["ols", "ridge", "lasso"])
def test_cv_shapes_coverage_consistency_determinism(name):
    X, y = _xy()
    eid, folds = _folds(y)
    res = run_linear_cv(name, X, y, eid, folds)
    R, N = 2, len(y)
    assert res.oof_r_hat.shape == (R, N) and res.oof_p_hr.shape == (R, N)
    assert not np.isnan(res.oof_r_hat).any()  # every event predicted once per rep
    assert len(res.fold_frames) == len(res.fold_records) == R * 5
    for rep in range(R):
        fr = pd.concat([f for f in res.fold_frames if (f.rep == rep).all()])
        assert len(fr) == N and fr.event_id.is_unique
    for fr, rec in zip(res.fold_frames, res.fold_records):
        assert (fr.p_hr.to_numpy() == (fr.r_hat.to_numpy() >= rec["t"]).astype(float)).all()
        assert (fr.rep.iloc[0], fr.fold.iloc[0]) == (rec["rep"], rec["fold"])
    again = run_linear_cv(name, X, y, eid, folds)
    np.testing.assert_array_equal(res.oof_r_hat, again.oof_r_hat)
    np.testing.assert_array_equal(res.oof_p_hr, again.oof_p_hr)
    if name == "ols":
        assert all(r["alpha"] is None for r in res.fold_records)


# ---------------------------------------------------------------- (8) non-converged path

def test_nonconverged_alpha_flagged_not_dropped(monkeypatch):
    X, y = _xy()
    orig = Lasso.fit
    bad = float(lin.LASSO_ALPHAS[0])

    def noisy(self, *a, **k):
        if self.alpha == bad:
            warnings.warn("no convergence", ConvergenceWarning)
        return orig(self, *a, **k)

    monkeypatch.setattr(Lasso, "fit", noisy)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        out = select_alpha("lasso", X, y)
    assert bad in out["nonconverged"]
    assert bad in out["mean_ap"] and np.isfinite(out["mean_ap"][bad])  # kept (mf-014)


def test_final_fit_nonconvergence_reported(monkeypatch):
    X, y = _xy()
    orig = Lasso.fit

    def noisy(self, *a, **k):
        warnings.warn("no convergence", ConvergenceWarning)
        return orig(self, *a, **k)

    monkeypatch.setattr(Lasso, "fit", noisy)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        res = fit_predict_fold("lasso", X[:90], y[:90], X[90:])
    assert res["final_converged"] is False
    assert sorted(res["nonconverged_alphas"]) == sorted(float(a) for a in lin.LASSO_ALPHAS)
    assert len(res["r_hat_val"]) == 30


# ---------------------------------------------------------------- (9) metrics

def test_metric_keys_and_f2_from_alarms_not_r_hat():
    rng = np.random.default_rng(5)
    n = 300
    X = np.hstack([rng.normal(size=(n, 30)), np.eye(5)[rng.integers(0, 5, n)]])
    y = np.where(X[:, 0] > 1.64, -5.9, -10.0)  # rare HR; linear r_hat stays far below -6
    eid, folds = _folds(y, seeds=(1, 2))
    res = run_linear_cv("ols", X, y, eid, folds)
    assert set(res.metrics) == {"F2", "MSE_HR_clipped", "MSE_HR_unclipped", "L_clipped", "L_unclipped"}
    assert len(res.metrics_per_rep) == 2
    assert (res.oof_r_hat < -6.0).all() and res.oof_p_hr.sum() > 0
    assert res.metrics["F2"] > 0  # would be 0 if F2 used r_hat >= -6
    for rep, m in enumerate(res.metrics_per_rep):
        p = res.oof_p_hr[rep]
        f2 = f2_score(y, np.where(p == 1.0, 0.0, -100.0))
        assert m["F2"] == pytest.approx(f2)
        assert m["MSE_HR_clipped"] == pytest.approx(mse_hr(y, res.oof_r_hat[rep], clip_at=-6.001))
        assert m["MSE_HR_unclipped"] == pytest.approx(mse_hr(y, res.oof_r_hat[rep], clip_at=None))
        assert m["L_clipped"] == pytest.approx(kelvins_l(m["MSE_HR_clipped"], f2))
        assert m["L_unclipped"] == pytest.approx(kelvins_l(m["MSE_HR_unclipped"], f2))
    assert res.metrics["F2"] == pytest.approx(np.mean([m["F2"] for m in res.metrics_per_rep]))
