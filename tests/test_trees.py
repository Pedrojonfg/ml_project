"""S5 tree models (pj-014..020): helpers, leakage, determinism."""

import numpy as np
import pandas as pd

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
    gb = run_oof_cv(make_gbdt, X, y, eid, folds)
    from src.models.trees import importance_diagnostics

    d = importance_diagnostics(rf.importances, gb.importances, X, y, folds, 5)
    assert "reopen_required" in d
