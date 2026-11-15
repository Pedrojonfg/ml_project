"""S10 kernel ridge (mf-044..mf-053): constants, median distance, eigh solution, selection, CV."""

import numpy as np
import pytest
from sklearn.kernel_ridge import KernelRidge
from sklearn.model_selection import StratifiedKFold

import src.models.kernel_ridge as kr
from src.models.kernel_ridge import (
    C_GAMMA,
    LAMBDA_GRID,
    decompose,
    fit_predict_fold,
    median_sq_dist,
    predict,
    select_lambda,
)
from src.models.linear import INNER_SEED, INNER_SPLITS, make_preprocessor, run_linear_cv
from tests.test_linear import _folds, _xy

SMALL_GRID = np.array([1e-2, 1.0, 1e2])


@pytest.fixture
def small_grid(monkeypatch):
    # 3-value grid keeps runtime small; the module reads the global at call time
    monkeypatch.setattr(kr, "LAMBDA_GRID", SMALL_GRID)


def _brute_median(Z):
    d = [np.sum((Z[i] - Z[j]) ** 2) for i in range(len(Z)) for j in range(i + 1, len(Z))]
    return float(np.median(d))


# ---------------------------------------------------------------- (1) constants

def test_registered_constants():
    assert C_GAMMA == 10.0  # per mf-049
    assert len(LAMBDA_GRID) == 25
    np.testing.assert_array_equal(LAMBDA_GRID, np.logspace(-3, 3, 25))  # per mf-049


# ---------------------------------------------------------------- (2) median_sq_dist

def test_median_sq_dist_odd_number_of_pairs():
    # 3 points -> 3 pairs; squared distances 1, 4, 5 -> median 4  (per mf-050)
    Z = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 2.0]])
    d = sorted([1.0, 4.0, 1.0 + 4.0])
    assert median_sq_dist(Z) == pytest.approx(d[1])
    assert median_sq_dist(Z) == pytest.approx(_brute_median(Z))


def test_median_sq_dist_even_number_of_pairs_is_mean_of_central_pair():
    # 4 points, 6 pairs: squared distances 1, 9, 10, 16, 18, 25 -> median (10 + 16) / 2
    Z = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 3.0], [4.0, 3.0]])
    sq = sorted(np.sum((Z[i] - Z[j]) ** 2) for i in range(4) for j in range(i + 1, 4))
    assert len(sq) == 6
    assert sq[2] != sq[3]  # the two central values differ, so a wrong median is detected
    assert median_sq_dist(Z) == pytest.approx((sq[2] + sq[3]) / 2)  # per mf-050
    assert median_sq_dist(Z) == pytest.approx(_brute_median(Z))


def test_median_sq_dist_random_matches_brute_force():
    Z = np.random.default_rng(3).normal(size=(25, 4))
    assert median_sq_dist(Z) == pytest.approx(_brute_median(Z), rel=1e-12)


# ---------------------------------------------------------------- (3) agreement with sklearn

@pytest.mark.parametrize("lam", [1e-3, 1.0, 1e3])
def test_decompose_predict_matches_sklearn_kernel_ridge(lam):
    rng = np.random.default_rng(1)
    Z, Zn = rng.normal(size=(60, 5)), rng.normal(size=(20, 5))
    y = -8.0 + Z[:, 0] + rng.normal(scale=0.3, size=60)
    st = decompose(Z, y)
    assert st["mean"] == pytest.approx(y.mean())  # per mf-047
    assert st["m"] == pytest.approx(median_sq_dist(Z))  # per mf-050
    assert st["gamma"] == pytest.approx(C_GAMMA / median_sq_dist(Z))  # per mf-048, mf-049
    ref = KernelRidge(kernel="rbf", alpha=lam, gamma=st["gamma"]).fit(Z, y - y.mean())
    expected = ref.predict(Zn) + y.mean()
    np.testing.assert_allclose(predict(st, Zn, lam), expected, rtol=1e-6, atol=1e-8)  # per mf-052


def test_decompose_state_is_consistent():
    rng = np.random.default_rng(2)
    Z = rng.normal(size=(30, 4))
    y = rng.normal(size=30)
    st = decompose(Z, y)
    K = np.exp(-st["gamma"] * ((Z[:, None] - Z[None]) ** 2).sum(-1))
    np.testing.assert_allclose((st["U"] * st["w"]) @ st["U"].T, K, atol=1e-9)  # K = U diag(w) U^T
    np.testing.assert_allclose(st["b"], st["U"].T @ (y - y.mean()), atol=1e-9)  # per mf-052
    np.testing.assert_array_equal(st["Z"], Z)


def test_gamma_scale_invariance_of_kernel():
    # per mf-048: scaling the rows by s scales m by s^2 and gamma by 1/s^2, kernel unchanged
    rng = np.random.default_rng(4)
    Z, y = rng.normal(size=(30, 4)), rng.normal(size=30)
    a, b = decompose(Z, y), decompose(3.0 * Z, y)
    assert b["gamma"] == pytest.approx(a["gamma"] / 9.0)
    np.testing.assert_allclose(b["w"], a["w"], atol=1e-8)


# ---------------------------------------------------------------- (4) intercept behaviour

def test_huge_lambda_gives_training_mean():
    rng = np.random.default_rng(5)
    Z, Zn = rng.normal(size=(50, 4)), rng.normal(size=(15, 4))
    y = -20.0 + 3 * Z[:, 0]
    st = decompose(Z, y)
    np.testing.assert_allclose(predict(st, Zn, 1e12), y.mean(), atol=1e-6)  # per mf-047


def test_far_point_gets_training_mean_even_for_tiny_lambda():
    rng = np.random.default_rng(6)
    Z = rng.normal(size=(50, 4))
    y = -20.0 + 3 * Z[:, 0]
    st = decompose(Z, y)
    far = np.full((3, 4), 1e3)
    np.testing.assert_allclose(predict(st, far, 1e-3), y.mean(), atol=1e-6)  # per mf-047


# ---------------------------------------------------------------- (5) numerical stop

def test_predict_raises_when_eigenvalue_plus_lambda_not_positive():
    rng = np.random.default_rng(7)
    Z, y = rng.normal(size=(20, 3)), rng.normal(size=20)
    st = dict(decompose(Z, y))
    w = st["w"].copy()
    w[0] = -1.0
    st["w"] = w
    with pytest.raises(ValueError):
        predict(st, Z[:3], 1e-3)  # per mf-052: w + lam = -0.999 <= 0
    w[0] = -1e-3
    with pytest.raises(ValueError):
        predict(st, Z[:3], 1e-3)  # boundary: w + lam == 0 is also an error


# ---------------------------------------------------------------- (6) select_lambda

def test_select_lambda_output_in_grid(small_grid):
    X, y = _xy()
    sel = select_lambda(X, y)
    assert sel["lam"] in set(SMALL_GRID)
    assert set(sel["mean_ap"]) == set(SMALL_GRID)  # per mf-049
    assert all(0.0 <= v <= 1.0 for v in sel["mean_ap"].values())
    assert sel["mean_ap"][sel["lam"]] == max(sel["mean_ap"].values())


def test_select_lambda_is_deterministic(small_grid):
    X, y = _xy()
    a, b = select_lambda(X, y), select_lambda(X, y)
    assert a["lam"] == b["lam"] and a["mean_ap"] == b["mean_ap"]
    np.testing.assert_allclose(a["oof_r"], b["oof_r"], atol=1e-8)


def test_select_lambda_ties_go_to_the_largest_lambda(small_grid, monkeypatch):
    X, y = _xy()
    monkeypatch.setattr(kr, "average_precision_score", lambda *a, **k: 0.5)
    assert select_lambda(X, y)["lam"] == SMALL_GRID.max()  # per mf-049


def test_select_lambda_computes_one_ap_per_inner_fold_and_lambda(small_grid, monkeypatch):
    X, y = _xy()
    calls = {"n": 0}

    def fake_ap(y_true, r_hat):
        calls["n"] += 1
        return 0.1

    monkeypatch.setattr(kr, "average_precision_score", fake_ap)
    sel = select_lambda(X, y)
    # one AP per (inner fold, lambda)  per mf-049
    assert calls["n"] == INNER_SPLITS * len(SMALL_GRID)
    assert all(v == pytest.approx(0.1) for v in sel["mean_ap"].values())


def test_oof_r_matches_manual_refit_on_inner_training_part(small_grid):
    X, y = _xy()
    sel = select_lambda(X, y)
    oof = sel["oof_r"]
    assert oof.shape == (len(y),) and not np.isnan(oof).any()
    y_hr = y >= -6.0
    skf = StratifiedKFold(INNER_SPLITS, shuffle=True, random_state=INNER_SEED)  # per mf-015
    for tr, va in skf.split(X, y_hr):
        pre = make_preprocessor().fit(X[tr])  # per mf-045: refit on the inner training part
        st = decompose(pre.transform(X[tr]), y[tr])  # own mean, m, gamma (mf-047, mf-050)
        expected = predict(st, pre.transform(X[va]), sel["lam"])
        np.testing.assert_allclose(oof[va], expected, rtol=1e-6, atol=1e-8)  # per mf-051


# ---------------------------------------------------------------- (7) fit_predict_fold

def test_fit_predict_fold_keys_and_consistency(small_grid):
    X, y = _xy()
    res = fit_predict_fold(X[:90], y[:90], X[90:])
    for key in ("alpha", "lam", "gamma", "m", "t", "r_hat_val", "p_hr_val",
                "final_converged", "nonconverged_alphas", "mean_ap"):
        assert key in res
    assert res["alpha"] is None
    assert res["final_converged"] is True and res["nonconverged_alphas"] == []
    assert res["lam"] in set(SMALL_GRID)
    assert res["r_hat_val"].shape == (30,)
    np.testing.assert_array_equal(res["p_hr_val"], (res["r_hat_val"] >= res["t"]).astype(np.float64))
    assert res["p_hr_val"].dtype == np.float64
    Z = make_preprocessor().fit_transform(X[:90])  # per mf-045: refit on the whole outer training part
    assert res["m"] == pytest.approx(median_sq_dist(Z))  # per mf-050
    assert res["gamma"] == pytest.approx(C_GAMMA / median_sq_dist(Z))  # per mf-048, mf-049


def test_fit_predict_fold_r_hat_val_is_final_model_prediction(small_grid):
    X, y = _xy()
    res = fit_predict_fold(X[:90], y[:90], X[90:])
    pre = make_preprocessor().fit(X[:90])
    st = decompose(pre.transform(X[:90]), y[:90])
    expected = predict(st, pre.transform(X[90:]), res["lam"])
    np.testing.assert_allclose(res["r_hat_val"], expected, rtol=1e-6, atol=1e-8)  # per mf-051, mf-052


def test_alarm_line_uses_oof_predictions(small_grid):
    from src.models.linear import choose_alarm_line
    X, y = _xy()
    res = fit_predict_fold(X[:90], y[:90], X[90:])
    sel = select_lambda(X[:90], y[:90])
    assert res["lam"] == sel["lam"]
    assert res["t"] == choose_alarm_line(sel["oof_r"], y[:90])  # per mf-051


def test_fit_predict_fold_ignores_validation_rows(small_grid):
    # no leakage (mf-050, mf-051): lam, m, gamma, t depend on the training part only
    X, y = _xy()
    a = fit_predict_fold(X[:90], y[:90], X[90:])
    b = fit_predict_fold(X[:90], y[:90], X[90:] * 50 + 3)
    for key in ("lam", "m", "gamma", "t"):
        assert a[key] == b[key]


# ---------------------------------------------------------------- (8) CV wiring

def test_run_linear_cv_kernel_ridge(small_grid):
    X, y = _xy()
    eid, folds = _folds(y)
    res = run_linear_cv("kernel_ridge", X, y, eid, folds, reps=[0, 1])
    assert res.oof_r_hat.shape == (2, len(y)) and res.oof_p_hr.shape == (2, len(y))
    assert not np.isnan(res.oof_r_hat).any() and not np.isnan(res.oof_p_hr).any()
    assert len(res.fold_records) == 10  # 2 reps x 5 folds
    for rec in res.fold_records:
        assert rec["lam"] in set(SMALL_GRID)
        assert rec["gamma"] > 0 and rec["m"] > 0
        assert np.isfinite(rec["t"])
