"""S5 tree regressors: RF + GBDT vs LRP (pj-014..020)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterable

import numpy as np
import pandas as pd
from scipy.optimize import brentq
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.pipeline import Pipeline

from src.features import FEATURE_COLUMNS
from src.metrics import HR_THRESHOLD_LOG10, f2_score, kelvins_l, mse_hr
from src.protocol import N_SPLITS

N_ESTIMATORS_GRID = (300, 500, 1000)  # per pj-024
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
            max_depth=8,  # per pj-024
            min_samples_split=2,
            min_samples_leaf=1,
            max_features="sqrt",
            bootstrap=True,
            max_samples=None,
            criterion="squared_error",
            random_state=random_state,
            n_jobs=-1,
        )),
    ])


def make_gbdt(n_estimators: int, random_state: int) -> Pipeline:
    # per pj-017, pj-024
    return Pipeline([
        ("imputer", make_imputer()),
        ("model", GradientBoostingRegressor(
            n_estimators=n_estimators,
            learning_rate=0.1,
            max_depth=8,  # per pj-024
            min_samples_split=2,
            min_samples_leaf=1,
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
    oof_pred: np.ndarray  # shape (n_reps, n_events)
    metrics: dict[str, float]  # mean of per-repetition metrics, per pj-006
    metrics_per_rep: list[dict[str, float]]
    metrics_pooled: dict[str, float]  # all reps pooled, used for grid selection per pj-022
    fold_frames: list[pd.DataFrame]
    importances: np.ndarray  # mean over splits, shape (n_features,)
    floors: list[dict] = field(default_factory=list)  # per pj-026


def floor_c(y_train: np.ndarray, lrp_train: np.ndarray) -> dict:
    # per pj-026
    y_train = np.asarray(y_train, dtype=np.float64)
    lrp_train = np.asarray(lrp_train, dtype=np.float64)
    hr = y_train >= P_HR_THRESHOLD
    mu_hr = float(y_train[hr].mean())
    sd_hr = float(y_train[hr].std(ddof=1))
    f_star = float(f2_score(y_train, lrp_train))
    p_star = f_star / 5.0

    def m(c: float) -> float:
        return float(np.maximum(y_train[~hr], c).mean())

    def p(c: float) -> float:
        mc = m(c)
        return (-6.0 - mc) / (mu_hr - mc)

    c = brentq(lambda c: p(c) - p_star, -29.99, -6.0005)
    return {
        "c": float(c),
        "mu_hr": mu_hr,
        "sd_hr": sd_hr,
        "f_star": f_star,
        "p_star": float(p_star),
    }


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
    lrp: np.ndarray | None = None,
) -> CvResult:
    reps = sorted(folds.rep.unique())
    oof = np.full((len(reps), len(y)), np.nan, dtype=np.float64)
    imp_sum = np.zeros(len(FEATURE_COLUMNS), dtype=np.float64)
    n_imp = 0
    pred_rows: list[pd.DataFrame] = []
    floors: list[dict] = []

    for i, rep in enumerate(reps):
        rs = 42 + int(rep)  # per pj-016, pj-017
        pipe = pipeline_factory(rs)
        for fold_id in range(N_SPLITS):
            train_m, val_m = _fold_masks(folds, int(rep), fold_id)
            y_fit = y[train_m]
            if lrp is not None:
                fc = floor_c(y[train_m], lrp[train_m])
                y_fit = np.maximum(y[train_m], fc["c"])
                floors.append({"rep": int(rep), "fold": fold_id, **fc})
            pipe.fit(X[train_m], y_fit)
            pred = pipe.predict(X[val_m])
            oof[i, val_m] = pred
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
    per_rep = [kelvins_pack(y, oof[i]) for i in range(len(reps))]
    metrics = {k: float(np.mean([m[k] for m in per_rep])) for k in per_rep[0]}
    pooled = kelvins_pack(np.tile(y, len(reps)), oof.ravel())
    importances = imp_sum / max(n_imp, 1)
    return CvResult(oof, metrics, per_rep, pooled, pred_rows, importances, floors)


def _select_n_estimators(
    X: np.ndarray,
    y: np.ndarray,
    event_ids: np.ndarray,
    folds: pd.DataFrame,
    pipeline_factory: Callable[[int, int], Pipeline],
    lrp: np.ndarray | None = None,
) -> int:
    # per pj-024, pj-025
    best_n, best_l = None, float("inf")
    for n_est in N_ESTIMATORS_GRID:
        res = run_oof_cv(
            lambda rs, n=n_est: pipeline_factory(n, rs),
            X,
            y,
            event_ids,
            folds,
            collect_importance=False,
            lrp=lrp,
        )
        l = res.metrics_pooled["L_unclipped"]  # per pj-025
        if l < best_l or (l == best_l and (best_n is None or n_est < best_n)):
            best_l, best_n = l, n_est
    assert best_n is not None
    return int(best_n)


def select_rf_n_estimators(
    X: np.ndarray,
    y: np.ndarray,
    event_ids: np.ndarray,
    folds: pd.DataFrame,
    lrp: np.ndarray | None = None,
) -> int:
    return _select_n_estimators(X, y, event_ids, folds, make_rf, lrp=lrp)


def select_gbdt_n_estimators(
    X: np.ndarray,
    y: np.ndarray,
    event_ids: np.ndarray,
    folds: pd.DataFrame,
    lrp: np.ndarray | None = None,
) -> int:
    return _select_n_estimators(X, y, event_ids, folds, make_gbdt, lrp=lrp)


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
    gbdt_n_estimators: int,
    lrp: np.ndarray | None = None,
) -> dict:
    # mandatory B1 (rep 0, fold 0) and B3 — per pj-019
    rep, fold_id = 0, 0
    train_m, val_m = _fold_masks(folds, rep, fold_id)
    rs = 42
    y_train = y[train_m]
    if lrp is not None:
        fc = floor_c(y[train_m], lrp[train_m])
        y_train = np.maximum(y[train_m], fc["c"])

    def b1_for(pipe: Pipeline, global_imp: np.ndarray, label: str) -> dict:
        pipe.fit(X[train_m], y_train)
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
    gbdt_pipe = make_gbdt(gbdt_n_estimators, rs)
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


def _floor_per_prediction(
    y: np.ndarray,
    res: CvResult,
    folds: pd.DataFrame,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    reps = sorted(folds.rep.unique())
    r = len(reps)
    n = len(y)
    yt = np.tile(y, r)
    rp = res.oof_pred.ravel()
    ev = np.tile(np.arange(n), r)
    floor_map = {(int(f["rep"]), int(f["fold"])): f for f in res.floors}
    c_pp = np.empty(r * n, dtype=np.float64)
    mu_pp = np.empty(r * n, dtype=np.float64)
    for r_idx, rep in enumerate(reps):
        fcol = folds[folds.rep == rep].fold.to_numpy()
        for i in range(n):
            flo = floor_map[(int(rep), int(fcol[i]))]
            idx = r_idx * n + i
            c_pp[idx] = flo["c"]
            mu_pp[idx] = flo["mu_hr"]
    return yt, rp, ev, c_pp, mu_pp


def floor_c_diagnostics(y: np.ndarray, res: CvResult, folds: pd.DataFrame) -> dict:
    # per pj-026
    yt, rp, ev, c_pp, mu_pp = _floor_per_prediction(y, res, folds)
    f_stars = [float(f["f_star"]) for f in res.floors]
    f_star_mean = float(np.mean(f_stars)) if f_stars else 0.0
    cs = [float(f["c"]) for f in res.floors]
    c_min = float(min(cs)) if cs else 0.0
    c_max = float(max(cs)) if cs else 0.0
    c_mean = float(np.mean(cs)) if cs else 0.0
    sd_hr_mean = float(np.mean([float(f["sd_hr"]) for f in res.floors])) if res.floors else 0.0

    f2_pooled = float(res.metrics_pooled["F2"])
    r0 = {
        "evaluable": True,
        "fires": f2_pooled == 0.0,
        "value": f2_pooled,
    }

    f2_mean = float(res.metrics["F2"])
    r1 = {
        "evaluable": True,
        "fires": f2_mean < f_star_mean / 2.0 or f2_mean > 2.0 * f_star_mean,
        "value": f2_mean,
    }

    ts = np.round(np.arange(-7.0, -5.0 + 1e-9, 0.01), 2)
    # truth stays at -6; only the alarm line moves to t
    f2_by_t = [float(f2_score(yt, rp - t - 6.0)) for t in ts]
    f2_at_m6 = float(f2_score(yt, rp, threshold=-6.0))
    best_i = int(np.argmax(f2_by_t))
    gain = float(f2_by_t[best_i] - f2_at_m6)
    r2 = {
        "evaluable": True,
        "fires": gain > 0.05,
        "best_t": float(ts[best_i]),
        "gain": gain,
    }

    zone = rp >= -6.0
    hr_in_zone = zone & (yt >= -6.0)
    n_hr_ev_zone = len(np.unique(ev[hr_in_zone]))
    r3_eval = n_hr_ev_zone >= 10
    if r3_eval:
        p_hat = np.clip((rp - c_pp) / (mu_pp - c_pp), 0.0, 1.0)
        obs = float(np.mean(yt[zone] >= -6.0))
        mean_p = float(np.mean(p_hat[zone]))
        ratio = obs / mean_p if mean_p else 0.0
        r3_fires = ratio < 0.5 or ratio > 2.0
    else:
        ratio = None
        r3_fires = False
    r3 = {"evaluable": r3_eval, "fires": r3_fires, "ratio": ratio}

    hr = yt >= -6.0
    det = hr & (rp >= -6.0)
    mis = hr & (rp < -6.0)
    n_det = len(np.unique(ev[det]))
    n_mis = len(np.unique(ev[mis]))
    r4_eval = n_det >= 10 and n_mis >= 10
    if r4_eval:
        diff = float(abs(np.mean(yt[det]) - np.mean(yt[mis])))
        threshold = 0.8 * sd_hr_mean
        r4_fires = diff > threshold
    else:
        diff = None
        threshold = None
        r4_fires = False
    r4 = {
        "evaluable": r4_eval,
        "fires": r4_fires,
        "diff": diff,
        "threshold": threshold,
    }

    reopen = any(x["fires"] for x in (r0, r1, r2, r3, r4))
    return {
        "f_star_mean": f_star_mean,
        "c_min": c_min,
        "c_max": c_max,
        "c_mean": c_mean,
        "R0": r0,
        "R1": r1,
        "R2": r2,
        "R3": r3,
        "R4": r4,
        "reopen_required": bool(reopen),
    }
