"""S6 stage 1: logistic classifiers, 1-SE choice of C, OOF scores, Platt calibration, Brier (mf-021..mf-039)."""

from __future__ import annotations

import warnings
from dataclasses import dataclass

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold

from src.metrics import HR_THRESHOLD_LOG10
from src.models.linear import INNER_SEED, INNER_SPLITS, choose_alarm_line, make_preprocessor

CLASSIFIERS = ("lr_none", "lr_l2", "lr_l1")  # per mf-021
C_GRIDS = {"lr_l2": np.logspace(-4, 4, 25), "lr_l1": np.logspace(-2, 4, 25)}  # per mf-026
REL_BINS = 10  # per mf-036


def make_logistic(name: str, C: float | None = None) -> LogisticRegression:
    # sklearn 1.9.1: penalty deprecated; L2 = (C, l1_ratio=0), L1 = (C, l1_ratio=1), none = C=inf
    common = dict(class_weight="balanced", max_iter=10000, tol=1e-4, warm_start=False,  # per mf-011, mf-030
                  fit_intercept=True, intercept_scaling=1, dual=False, n_jobs=None, verbose=0)  # per mf-030
    if name == "lr_none":
        return LogisticRegression(C=np.inf, l1_ratio=0.0, solver="lbfgs", random_state=None, **common)
    if name == "lr_l2":
        return LogisticRegression(C=C, l1_ratio=0.0, solver="lbfgs", random_state=None, **common)
    if name == "lr_l1":
        common["intercept_scaling"] = 100  # per mf-041
        return LogisticRegression(C=C, l1_ratio=1.0, solver="liblinear", random_state=0, **common)  # per mf-041
    raise ValueError(f"unknown classifier {name!r}")


def _fit_flag(model, Z, y) -> bool:
    """Fit; return True if a ConvergenceWarning was raised (mf-030)."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        model.fit(Z, y)
    return any(issubclass(x.category, ConvergenceWarning) for x in w)


def _one_se_choice(mean_auc: dict, aucs: dict) -> dict:
    best = max(mean_auc.values())
    c_star = min(c for c in mean_auc if mean_auc[c] == best)  # per mf-039
    se = float(np.std(aucs[c_star], ddof=1) / np.sqrt(5))  # per mf-027
    tie_set = sorted(c for c in mean_auc if mean_auc[c] >= best - se)
    return {"C": min(tie_set), "c_star": c_star, "se": se, "tie_set": tie_set}


def select_c(name: str, X_train: np.ndarray, y_hr: np.ndarray) -> dict:
    if name not in ("lr_l2", "lr_l1"):
        raise ValueError("select_c is only for lr_l2 and lr_l1")
    grid = [float(c) for c in C_GRIDS[name]]  # read at call time
    skf = StratifiedKFold(INNER_SPLITS, shuffle=True, random_state=INNER_SEED)  # per mf-028
    aucs = {c: [] for c in grid}
    nonconv = set()
    for tr, va in skf.split(X_train, y_hr):
        pre = make_preprocessor().fit(X_train[tr])  # per mf-010, refit per inner training part
        Ztr, Zva = pre.transform(X_train[tr]), pre.transform(X_train[va])
        for c in grid:
            model = make_logistic(name, c)
            if _fit_flag(model, Ztr, y_hr[tr]):
                nonconv.add(c)
            aucs[c].append(roc_auc_score(y_hr[va], model.decision_function(Zva)))  # per mf-025
    mean_auc = {c: float(np.mean(aucs[c])) for c in grid}
    r = _one_se_choice(mean_auc, aucs)
    r.update(mean_auc=mean_auc, edge=bool(r["C"] in (grid[0], grid[-1])),  # per mf-029
             nonconverged=sorted(nonconv))
    return r


def oof_z(name: str, C: float | None, X_train: np.ndarray, y_hr: np.ndarray):
    # per mf-032, mf-038: OOF log-odds from the inner 5 folds with the selected C
    z = np.empty(len(y_hr))
    nonconv = False
    skf = StratifiedKFold(INNER_SPLITS, shuffle=True, random_state=INNER_SEED)  # per mf-028
    for tr, va in skf.split(X_train, y_hr):
        pre = make_preprocessor().fit(X_train[tr])  # per mf-010
        model = make_logistic(name, C)
        nonconv |= _fit_flag(model, pre.transform(X_train[tr]), y_hr[tr])
        z[va] = model.decision_function(pre.transform(X_train[va]))
    return z, bool(nonconv)


def fit_platt(z: np.ndarray, y_hr: np.ndarray) -> dict:
    # per mf-033: no penalty, no weights, 0/1 targets, lbfgs; partial solution kept (mf-031: a <= 0 kept)
    m = LogisticRegression(
        C=np.inf, l1_ratio=0.0, class_weight=None, solver="lbfgs", max_iter=10000, tol=1e-4,
        fit_intercept=True, random_state=None, warm_start=False, n_jobs=None, verbose=0,
        dual=False, intercept_scaling=1,
    )
    nonconv = _fit_flag(m, np.asarray(z).reshape(-1, 1), np.asarray(y_hr).astype(int))
    return {"a": float(m.coef_[0, 0]), "b": float(m.intercept_[0]), "converged": not nonconv}


def platt_p(z: np.ndarray, a: float, b: float) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-(a * np.asarray(z, dtype=np.float64) + b)))


def fit_predict_fold(name: str, X_train: np.ndarray, y_train: np.ndarray, X_val: np.ndarray) -> dict:
    y_hr = y_train >= HR_THRESHOLD_LOG10
    C = c_star = se = tie_size = edge = None
    sel_nonconv = []
    if name != "lr_none":
        sel = select_c(name, X_train, y_hr)
        C, c_star, se, edge = sel["C"], sel["c_star"], sel["se"], sel["edge"]
        tie_size, sel_nonconv = len(sel["tie_set"]), sel["nonconverged"]
    z_oof, oof_nonconv = oof_z(name, C, X_train, y_hr)
    platt = fit_platt(z_oof, y_hr)
    a, b = platt["a"], platt["b"]
    t = choose_alarm_line(platt_p(z_oof, a, b), y_train)  # per mf-035
    pre = make_preprocessor().fit(X_train)  # per mf-010, refit on the whole outer training fold
    model = make_logistic(name, C)
    final_nonconv = _fit_flag(model, pre.transform(X_train), y_hr)
    z_val = model.decision_function(pre.transform(X_val))
    p_val = platt_p(z_val, a, b)
    return {
        "C": C, "c_star": c_star, "se": se, "tie_size": tie_size, "edge": edge,
        "a": a, "b": b, "a_nonpositive": bool(a <= 0), "t": t,  # per mf-031
        "z_val": z_val, "p_val": p_val, "alarm_val": (p_val >= t).astype(np.float64),
        "platt_converged": platt["converged"], "final_converged": not final_nonconv,
        "select_nonconverged": sel_nonconv, "oof_nonconverged": oof_nonconv,
    }


@dataclass
class Stage1CvResult:
    oof_z: np.ndarray  # (n_reps, n_events)
    oof_p: np.ndarray
    oof_alarm: np.ndarray
    brier_per_rep: list[float]
    brier: float
    fold_records: list[dict]
    fold_frames: list[pd.DataFrame]


def brier(p: np.ndarray, y_hr: np.ndarray) -> float:
    return float(np.mean((np.asarray(p, dtype=np.float64) - np.asarray(y_hr, dtype=np.float64)) ** 2))


def reliability_diagram(p: np.ndarray, y_hr: np.ndarray, k: int = REL_BINS):
    # per mf-036: equal-count bins of events sorted by p (stable), np.array_split
    order = np.argsort(p, kind="stable")
    ps, ys = np.asarray(p, dtype=np.float64)[order], np.asarray(y_hr, dtype=np.float64)[order]
    idx = np.array_split(np.arange(len(ps)), k)
    return np.array([ps[i].mean() for i in idx]), np.array([ys[i].mean() for i in idx])


def run_stage1_cv(name: str, X: np.ndarray, y: np.ndarray, event_ids: np.ndarray,
                  folds: pd.DataFrame, n_jobs: int = 1) -> Stage1CvResult:
    reps = sorted(folds.rep.unique())
    oof_z_ = np.full((len(reps), len(y)), np.nan)
    oof_p = np.full((len(reps), len(y)), np.nan)
    oof_a = np.full((len(reps), len(y)), np.nan)
    frames, records = [], []
    tasks = []  # (i, rep, k, val mask), repetition-major, fold ascending
    for i, rep in enumerate(reps):
        sub = folds[folds.rep == rep]
        fold_of = pd.Series(sub.fold.to_numpy(), index=sub.event_id.to_numpy()).reindex(event_ids).to_numpy()
        for k in sorted(sub.fold.unique()):
            tasks.append((i, rep, k, fold_of == k))
    if n_jobs == 1:
        results = [fit_predict_fold(name, X[~v], y[~v], X[v]) for _, _, _, v in tasks]
    else:  # ponytail: joblib default loky backend; results come back in task order
        results = Parallel(n_jobs=n_jobs)(delayed(fit_predict_fold)(name, X[~v], y[~v], X[v])
                                          for _, _, _, v in tasks)
    for (i, rep, k, val), res in zip(tasks, results):
        oof_z_[i, val], oof_p[i, val], oof_a[i, val] = res["z_val"], res["p_val"], res["alarm_val"]
        frames.append(pd.DataFrame({
            "event_id": event_ids[val], "rep": int(rep), "fold": int(k),
            "z": res["z_val"], "p_cal": res["p_val"], "alarm": res["alarm_val"],
        }))
        records.append({
            "rep": int(rep), "fold": int(k),
            **{key: res[key] for key in ("C", "c_star", "se", "tie_size", "edge", "a", "b",
                                         "a_nonpositive", "t", "platt_converged", "final_converged",
                                         "select_nonconverged", "oof_nonconverged")},
        })
    if np.isnan(oof_z_).any():
        raise RuntimeError("incomplete OOF predictions")
    y_hr = y >= HR_THRESHOLD_LOG10
    per_rep = [brier(oof_p[i], y_hr) for i in range(len(reps))]  # per mf-036
    return Stage1CvResult(oof_z_, oof_p, oof_a, per_rep, float(np.mean(per_rep)), records, frames)
