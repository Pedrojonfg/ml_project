"""S4 KNN regressor (mf-043): self-exclusion, K selection, alarm line, CV."""

import numpy as np
import pytest

import src.models.linear as lin
from src.features import FEATURE_COLUMNS
from src.models.linear import fit_predict_fold, make_model, make_preprocessor, run_linear_cv, select_k
from tests.test_linear import _folds, _xy

NF = len(FEATURE_COLUMNS)


@pytest.fixture(autouse=True)
def small_grid(monkeypatch):
    monkeypatch.setattr(lin, "K_GRID", (1, 3, 10))  # small data: 1 allowed here to test self-exclusion


def test_make_model_registered_params():
    m = make_model("knn", k=7)
    assert (m.n_neighbors, m.weights, m.p, m.metric) == (7, "uniform", 2, "minkowski")


def test_training_predictions_exclude_the_event_itself():
    X, y = _xy()
    Z = make_preprocessor().fit_transform(X)
    m = make_model("knn", k=1).fit(Z, y)
    idx = m.kneighbors(None)[1]
    assert (idx[:, 0] != np.arange(len(y))).all()  # nobody is their own neighbour
    assert not np.allclose(y[idx[:, 0]], y)  # K=1 does not reproduce own risk_final
    # same result brute force, by hand: nearest other event
    d = np.linalg.norm(Z[:, None] - Z[None], axis=2)
    np.fill_diagonal(d, np.inf)
    np.testing.assert_array_equal(idx[:, 0], d.argmin(1))


def test_select_k_ties_go_to_the_largest_k(monkeypatch):
    X, y = _xy()
    monkeypatch.setattr(lin, "average_precision_score", lambda *a, **k: 0.5)
    assert select_k(X, y)["k"] == 10


def test_select_k_returns_grid_value_and_mean_ap_for_each_k():
    X, y = _xy()
    sel = select_k(X, y)
    assert sel["k"] in (1, 3, 10) and set(sel["mean_ap"]) == {1, 3, 10}


def test_select_k_rejects_grid_larger_than_inner_training(monkeypatch):
    X, y = _xy(n=40)
    monkeypatch.setattr(lin, "K_GRID", (5, 100))
    with pytest.raises(ValueError):
        select_k(X, y)


def test_fold_output_and_alarm_rule():
    X, y = _xy()
    res = fit_predict_fold("knn", X[:90], y[:90], X[90:])
    assert res["k"] in (1, 3, 10) and res["alpha"] is None
    np.testing.assert_array_equal(res["p_hr_val"], (res["r_hat_val"] >= res["t"]).astype(float))


def test_fold_k_and_t_ignore_validation_x():
    X, y = _xy()
    a = fit_predict_fold("knn", X[:90], y[:90], X[90:])
    b = fit_predict_fold("knn", X[:90], y[:90], X[90:] * 50 + 3)
    assert a["k"] == b["k"] and a["t"] == b["t"]


def test_cv_runs_and_records_k():
    X, y = _xy()
    eid, folds = _folds(y)
    res = run_linear_cv("knn", X, y, eid, folds)
    assert res.oof_r_hat.shape == (2, len(y)) and not np.isnan(res.oof_r_hat).any()
    assert all(r["k"] in (1, 3, 10) for r in res.fold_records)
