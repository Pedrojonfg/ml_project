"""S5 tree regressors: RF + GBDT vs LRP (pj-014..020)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.pipeline import Pipeline

from src.features import FEATURE_COLUMNS
from src.metrics import HR_THRESHOLD_LOG10, f2_score, kelvins_l, mse_hr
from src.protocol import N_SPLITS

RF_N_ESTIMATORS_GRID = (100, 300, 500)  # per pj-018
P_HR_THRESHOLD = HR_THRESHOLD_LOG10  # per pj-020, pj-001


def feature_family(name: str) -> str:
    """Feature family labels for pj-019 B3."""
    if name.startswith("risk_"):
        return "risk"
    if name.startswith(("miss_distance_", "relative_speed_", "t_weighted_rms_")):
        return "geometry"
    if name.startswith("obj_"):
        return "object"
    return "metadata"


def make_imputer() -> SimpleImputer:
    # per pj-015, pj-020
    return SimpleImputer(strategy="median", add_indicator=False, keep_empty_features=False)


def make_rf(n_estimators: int, random_state: int) -> Pipeline:
    # per pj-016
    return Pipeline([
        ("imputer", make_imputer()),
        ("model", RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=4,
            min_samples_split=4,
            min_samples_leaf=2,
            max_features="sqrt",
            bootstrap=True,
            max_samples=None,
            criterion="squared_error",
            random_state=random_state,
            n_jobs=-1,
        )),
    ])


def make_gbdt(random_state: int) -> Pipeline:
    # per pj-017
    return Pipeline([
        ("imputer", make_imputer()),
        ("model", GradientBoostingRegressor(
            n_estimators=200,
            learning_rate=0.1,
            max_depth=4,
            min_samples_split=4,
            min_samples_leaf=2,
            subsample=1.0,
            max_features="sqrt",
            loss="squared_error",
            random_state=random_state,
            validation_fraction=0.1,
        )),
    ])


def p_hr_from_r_hat(r_hat: np.ndarray) -> np.ndarray:
    # per pj-020
    return (np.asarray(r_hat, dtype=np.float64) >= P_HR_THRESHOLD).astype(np.float64)


def kelvins_pack(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    # per pj-007
    f2 = f2_score(y_true, y_pred)
    m_clip = mse_hr(y_true, y_pred, clip_at=-6.001)
    m_raw = mse_hr(y_true, y_pred, clip_at=None)
    return {
        "F2": float(f2),
        "MSE_HR_clipped": float(m_clip),
        "MSE_HR_unclipped": float(m_raw),
        "L_clipped": float(kelvins_l(m_clip, f2)),
        "L_unclipped": float(kelvins_l(m_raw, f2)),
    }


@dataclass
class CvResult:
    oof_pred: np.ndarray
    metrics: dict[str, float]
    fold_frames: list[pd.DataFrame]
    importances: np.ndarray  # mean over splits, shape (n_features,)


def _fold_masks(folds: pd.DataFrame, rep: int, fold_id: int) -> tuple[np.ndarray, np.ndarray]:
    sub = folds[folds.rep == rep]
    fold = sub.fold.to_numpy()
    val = fold == fold_id
    train = ~val
    return train, val


def run_oof_cv(
    pipeline_factory: Callable[[int], Pipeline],
    X: np.ndarray,
    y: np.ndarray,
    event_ids: np.ndarray,
    folds: pd.DataFrame,
    feature_names: Iterable[str] = FEATURE_COLUMNS,
    collect_importance: bool = True,
) -> CvResult:
    n = len(y)
    oof = np.full(n, np.nan, dtype=np.float64)
    imp_sum = np.zeros(len(FEATURE_COLUMNS), dtype=np.float64)
    n_imp = 0
    pred_rows: list[pd.DataFrame] = []

    names = list(feature_names)
    for rep in sorted(folds.rep.unique()):
        rs = 42 + int(rep)  # per pj-016, pj-017
        pipe = pipeline_factory(rs)
        for fold_id in range(N_SPLITS):
            train_m, val_m = _fold_masks(folds, int(rep), fold_id)
            pipe.fit(X[train_m], y[train_m])
            pred = pipe.predict(X[val_m])
            oof[val_m] = pred
            if collect_importance:
                imp_sum += pipe.named_steps["model"].feature_importances_
                n_imp += 1
            eid = event_ids[val_m]
            pred_rows.append(pd.DataFrame({
                "event_id": eid,
                "rep": int(rep),
                "fold": fold_id,
                "r_hat": pred,
                "p_hr": p_hr_from_r_hat(pred),
            }))

    if np.any(np.isnan(oof)):
        raise RuntimeError("incomplete OOF predictions")
    metrics = kelvins_pack(y, oof)
    importances = imp_sum / max(n_imp, 1)
    return CvResult(oof, metrics, pred_rows, importances)


def select_rf_n_estimators(
    X: np.ndarray,
    y: np.ndarray,
    event_ids: np.ndarray,
    folds: pd.DataFrame,
) -> int:
    # per pj-018
    best_n, best_l = None, float("inf")
    for n_est in RF_N_ESTIMATORS_GRID:
        res = run_oof_cv(
            lambda rs, n=n_est: make_rf(n, rs),
            X,
            y,
            event_ids,
            folds,
            collect_importance=False,
        )
        l = res.metrics["L_unclipped"]
        if l < best_l or (l == best_l and (best_n is None or n_est < best_n)):
            best_l, best_n = l, n_est
    assert best_n is not None
    return int(best_n)


def top_k_names(importances: np.ndarray, k: int = 5) -> list[str]:
    idx = np.argsort(importances)[::-1][:k]
    return [FEATURE_COLUMNS[i] for i in idx]


def importance_diagnostics(
    rf_imp: np.ndarray,
    gbdt_imp: np.ndarray,
    X: np.ndarray,
    y: np.ndarray,
    folds: pd.DataFrame,
    rf_n_estimators: int,
) -> dict:
    # mandatory B1 (rep 0, fold 0) and B3 — per pj-019
    rep, fold_id = 0, 0
    train_m, val_m = _fold_masks(folds, rep, fold_id)
    rs = 42

    def b1_for(pipe: Pipeline, global_imp: np.ndarray, label: str) -> dict:
        pipe.fit(X[train_m], y[train_m])
        perm = permutation_importance(
            pipe,
            X[val_m],
            y[val_m],
            n_repeats=5,
            random_state=42,
            scoring="neg_mean_squared_error",
        )
        imp_top = top_k_names(global_imp, 5)
        perm_top = top_k_names(perm.importances_mean, 5)
        overlap = len(set(imp_top) & set(perm_top))
        rank1_match = imp_top[0] == perm_top[0]
        fail = overlap < 3 or not rank1_match
        return {
            "model": label,
            "impurity_top5": imp_top,
            "permutation_top5": perm_top,
            "overlap": overlap,
            "rank1_match": rank1_match,
            "fail": fail,
        }

    rf_pipe = make_rf(rf_n_estimators, rs)
    gbdt_pipe = make_gbdt(rs)
    b1_rf = b1_for(rf_pipe, rf_imp, "rf")
    b1_gbdt = b1_for(gbdt_pipe, gbdt_imp, "gbdt")

    rf_r1, gb_r1 = top_k_names(rf_imp, 1)[0], top_k_names(gbdt_imp, 1)[0]
    fam_rf, fam_gb = feature_family(rf_r1), feature_family(gb_r1)
    b3_fail = rf_r1 != gb_r1 and fam_rf != fam_gb

    top10 = np.argsort(rf_imp)[::-1][:10]
    sub = X[:, top10]
    corr = np.corrcoef(sub, rowvar=False) if sub.shape[1] > 1 else np.ones((1, 1))
    max_abs_r = float(np.max(np.abs(corr - np.eye(corr.shape[0])))) if corr.size > 1 else 0.0

    reopen = b1_rf["fail"] or b1_gbdt["fail"] or b3_fail
    return {
        "b1_rf": b1_rf,
        "b1_gbdt": b1_gbdt,
        "b3": {
            "rf_rank1": rf_r1,
            "gbdt_rank1": gb_r1,
            "rf_family": fam_rf,
            "gbdt_family": fam_gb,
            "fail": b3_fail,
        },
        "max_pairwise_abs_r_top10_rf": max_abs_r,
        "reopen_required": reopen,
    }
