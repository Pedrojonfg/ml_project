"""S4 regressors: OLS, ridge, lasso (mf-008..mf-015) and KNN (mf-021) on risk_final."""

from __future__ import annotations

import warnings
from dataclasses import dataclass
from fractions import Fraction

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.metrics import average_precision_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.metrics import HR_THRESHOLD_LOG10, f2_score, kelvins_l, mse_hr
from src.models.trees import make_imputer

N_NUMERIC = 30  # numeric columns 0..29 scaled, 30..34 one-hot unscaled, per mf-010
RIDGE_ALPHAS = np.logspace(0, 6, 25)  # per mf-013
LASSO_ALPHAS = np.logspace(-4, 2, 25)  # per mf-013
K_GRID = (5, 10, 20, 50, 100, 200, 400)  # per mf-021
INNER_SEED = 0  # per mf-015
INNER_SPLITS = 5  # per mf-015
SURROGATE_ALARM, SURROGATE_QUIET = 0.0, -100.0  # maps p_hr to the -6 protocol F2


def make_preprocessor() -> Pipeline:
    # per mf-010: median imputer (reused from trees: same registered params), scaler on numeric only
    scaler = ColumnTransformer(
        [("scale", StandardScaler(with_mean=True, with_std=True), list(range(N_NUMERIC)))],
        remainder="passthrough",
    )
    return Pipeline([("imputer", make_imputer()), ("scaler", scaler)])


def make_model(name: str, alpha: float | None = None, k: int | None = None):
    # per mf-014 (linear) and mf-021 (knn)
    if name == "knn":
        return KNeighborsRegressor(
            n_neighbors=k, weights="uniform", algorithm="auto", leaf_size=30,
            p=2, metric="minkowski", metric_params=None, n_jobs=None,
        )
    if name == "ols":
        return LinearRegression(fit_intercept=True, positive=False, copy_X=True)
    if name == "ridge":
        return Ridge(alpha=alpha, fit_intercept=True, solver="cholesky", positive=False, copy_X=True)
    if name == "lasso":
        return Lasso(
            alpha=alpha, fit_intercept=True, precompute=False, copy_X=True,
            max_iter=10000, tol=1e-4, warm_start=True, positive=False, selection="cyclic",
        )
    raise ValueError(f"unknown model {name!r}")


def _fit_flag(model, Z, y) -> bool:
    """Fit; return True if a ConvergenceWarning was raised (mf-014)."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        model.fit(Z, y)
    return any(issubclass(x.category, ConvergenceWarning) for x in w)


def select_alpha(name: str, X_train: np.ndarray, y_train: np.ndarray) -> dict:
    if name not in ("ridge", "lasso"):
        raise ValueError("select_alpha is only for ridge and lasso")
    grid = [float(a) for a in (RIDGE_ALPHAS if name == "ridge" else LASSO_ALPHAS)]
    order = sorted(grid, reverse=True) if name == "lasso" else grid  # per mf-014
    y_hr = y_train >= HR_THRESHOLD_LOG10
    skf = StratifiedKFold(INNER_SPLITS, shuffle=True, random_state=INNER_SEED)  # per mf-015
    aps = {a: [] for a in grid}
    nonconv = set()
    for tr, va in skf.split(X_train, y_hr):
        pre = make_preprocessor().fit(X_train[tr])  # per mf-010, refit per inner training part
        Ztr, Zva = pre.transform(X_train[tr]), pre.transform(X_train[va])
        model = make_model(name, order[0])  # one object per inner fold, reused along the grid (mf-014)
        for a in order:
            model.set_params(alpha=a)
            if _fit_flag(model, Ztr, y_train[tr]):
                nonconv.add(a)
            aps[a].append(average_precision_score(y_hr[va], model.predict(Zva)))  # per mf-013
    mean_ap = {a: float(np.mean(aps[a])) for a in grid}
    best = max(mean_ap.values())
    alpha = max(a for a in grid if mean_ap[a] == best)  # exact ties to the highest alpha, per mf-013
    return {"alpha": alpha, "mean_ap": mean_ap, "nonconverged": sorted(nonconv)}


def select_k(X_train: np.ndarray, y_train: np.ndarray) -> dict:
    # per mf-021: same inner CV and criterion as select_alpha (mf-013), grid K_GRID, ties to the largest K
    grid = [int(k) for k in K_GRID]
    y_hr = y_train >= HR_THRESHOLD_LOG10
    skf = StratifiedKFold(INNER_SPLITS, shuffle=True, random_state=INNER_SEED)  # per mf-015
    aps = {k: [] for k in grid}
    for tr, va in skf.split(X_train, y_hr):
        if max(grid) > len(tr):
            raise ValueError("K grid larger than the inner training part")
        pre = make_preprocessor().fit(X_train[tr])  # per mf-010, refit per inner training part
        Ztr, Zva = pre.transform(X_train[tr]), pre.transform(X_train[va])
        idx = make_model("knn", k=max(grid)).fit(Ztr, y_train[tr]).kneighbors(Zva)[1]  # sorted by distance
        for k in grid:  # mean of the k nearest = KNeighborsRegressor(k).predict with uniform weights
            aps[k].append(average_precision_score(y_hr[va], y_train[tr][idx[:, :k]].mean(axis=1)))
    mean_ap = {k: float(np.mean(aps[k])) for k in grid}
    best = max(mean_ap.values())
    return {"k": max(k for k in grid if mean_ap[k] == best), "mean_ap": mean_ap}


def _fit_predict_knn(X_train: np.ndarray, y_train: np.ndarray, X_val: np.ndarray) -> dict:
    sel = select_k(X_train, y_train)
    pre = make_preprocessor().fit(X_train)  # per mf-021, preprocessing refit on the outer train fold
    Ztr, Zva = pre.transform(X_train), pre.transform(X_val)
    model = make_model("knn", k=sel["k"]).fit(Ztr, y_train)
    idx = model.kneighbors(None)[1]  # X=None: each training event excludes itself (mf-021)
    t = choose_alarm_line(y_train[idx].mean(axis=1), y_train)
    r_val = model.predict(Zva)
    return {
        "alpha": None, "k": sel["k"], "t": t, "r_hat_val": r_val,
        "p_hr_val": (r_val >= t).astype(np.float64),  # per mf-012
        "final_converged": True, "nonconverged_alphas": [], "mean_ap": sel["mean_ap"],
    }


def choose_alarm_line(r_hat_train: np.ndarray, y_train: np.ndarray) -> float:
    # per mf-012: candidates = r_hat of training HR; exact F2 = 5tp/(4P+tp+fp); ties -> median
    r = np.asarray(r_hat_train, dtype=np.float64)
    hr = np.asarray(y_train) >= HR_THRESHOLD_LOG10
    r_hr, r_non = np.sort(r[hr]), np.sort(r[~hr])
    cands = np.unique(r_hr)
    P = len(r_hr)
    tp = P - np.searchsorted(r_hr, cands, side="left")
    fp = len(r_non) - np.searchsorted(r_non, cands, side="left")
    f2 = [Fraction(5 * int(t), 4 * P + int(t) + int(f)) for t, f in zip(tp, fp)]
    best = max(f2)
    tied = cands[[v == best for v in f2]]
    return float(np.median(tied))


def fit_predict_fold(name: str, X_train: np.ndarray, y_train: np.ndarray, X_val: np.ndarray) -> dict:
    if name == "knn":
        return _fit_predict_knn(X_train, y_train, X_val)
    alpha, nonconv_alphas, mean_ap = None, [], None
    if name != "ols":
        sel = select_alpha(name, X_train, y_train)
        alpha, nonconv_alphas, mean_ap = sel["alpha"], sel["nonconverged"], sel["mean_ap"]
    pre = make_preprocessor().fit(X_train)  # per mf-013, preprocessing refit on the outer train fold
    Ztr, Zva = pre.transform(X_train), pre.transform(X_val)
    model = make_model(name, alpha)  # new object, cold start (mf-014)
    final_nonconv = _fit_flag(model, Ztr, y_train)
    r_train = model.predict(Ztr)
    t = choose_alarm_line(r_train, y_train)
    r_val = model.predict(Zva)
    return {
        "alpha": alpha, "t": t, "r_hat_val": r_val,
        "p_hr_val": (r_val >= t).astype(np.float64),  # per mf-012
        "final_converged": not final_nonconv, "nonconverged_alphas": nonconv_alphas,
        "mean_ap": mean_ap,
    }


@dataclass
class LinearCvResult:
    oof_r_hat: np.ndarray  # (n_reps, n_events)
    oof_p_hr: np.ndarray
    metrics: dict[str, float]  # mean of per-repetition metrics
    metrics_per_rep: list[dict[str, float]]
    fold_frames: list[pd.DataFrame]
    fold_records: list[dict]


def _rep_metrics(y: np.ndarray, r_hat: np.ndarray, p_hr: np.ndarray) -> dict[str, float]:
    # per mf-012: F2 from the alarms, MSE_HR from r_hat (pj-007 clip variants)
    f2 = f2_score(y, np.where(p_hr == 1.0, SURROGATE_ALARM, SURROGATE_QUIET))
    m_clip = mse_hr(y, r_hat, clip_at=-6.001)
    m_raw = mse_hr(y, r_hat, clip_at=None)
    return {
        "F2": float(f2), "MSE_HR_clipped": float(m_clip), "MSE_HR_unclipped": float(m_raw),
        "L_clipped": float(kelvins_l(m_clip, f2)), "L_unclipped": float(kelvins_l(m_raw, f2)),
    }


def run_linear_cv(name: str, X: np.ndarray, y: np.ndarray, event_ids: np.ndarray,
                  folds: pd.DataFrame) -> LinearCvResult:
    reps = sorted(folds.rep.unique())
    oof_r = np.full((len(reps), len(y)), np.nan)
    oof_p = np.full((len(reps), len(y)), np.nan)
    frames, records = [], []
    for i, rep in enumerate(reps):
        sub = folds[folds.rep == rep]
        fold_of = pd.Series(sub.fold.to_numpy(), index=sub.event_id.to_numpy()).reindex(event_ids).to_numpy()
        for k in sorted(sub.fold.unique()):
            val = fold_of == k
            res = fit_predict_fold(name, X[~val], y[~val], X[val])
            oof_r[i, val], oof_p[i, val] = res["r_hat_val"], res["p_hr_val"]
            frames.append(pd.DataFrame({
                "event_id": event_ids[val], "rep": int(rep), "fold": int(k),
                "r_hat": res["r_hat_val"], "p_hr": res["p_hr_val"],
            }))
            records.append({
                "rep": int(rep), "fold": int(k), "alpha": res["alpha"], "k": res.get("k"), "t": res["t"],
                "final_converged": res["final_converged"],
                "nonconverged_alphas": res["nonconverged_alphas"],
            })
    if np.isnan(oof_r).any():
        raise RuntimeError("incomplete OOF predictions")
    per_rep = [_rep_metrics(y, oof_r[i], oof_p[i]) for i in range(len(reps))]
    metrics = {k: float(np.mean([m[k] for m in per_rep])) for k in per_rep[0]}
    return LinearCvResult(oof_r, oof_p, metrics, per_rep, frames, records)
