"""S10 kernel ridge (RBF) on risk_final (mf-044..mf-053): one eigh per fit, all lambda from it."""

from __future__ import annotations

import numpy as np
from sklearn.metrics import average_precision_score
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.model_selection import StratifiedKFold

from src.metrics import HR_THRESHOLD_LOG10
from src.models.linear import INNER_SEED, INNER_SPLITS, choose_alarm_line, make_preprocessor

C_GAMMA = 10.0  # gamma = C_GAMMA / m, fixed, not tuned, per mf-049
LAMBDA_GRID = np.logspace(-3, 3, 25)  # per mf-049


def _sq_dists(A: np.ndarray, B: np.ndarray | None = None) -> np.ndarray:
    # squared Euclidean distances in float64, per mf-052 (never float32)
    A = np.asarray(A, dtype=np.float64)
    B = None if B is None else np.asarray(B, dtype=np.float64)
    return euclidean_distances(A, B, squared=True)


def _median_upper(d2: np.ndarray) -> float:
    # per mf-050: median over all distinct pairs (upper triangle), no subsample, no seed.
    # Row slices avoid the index arrays of np.triu_indices (memory).
    v = np.concatenate([d2[i, i + 1:] for i in range(len(d2) - 1)])
    return float(np.median(v, overwrite_input=True))


def median_sq_dist(Z: np.ndarray) -> float:
    """m of mf-050 for the preprocessed training rows Z."""
    return _median_upper(_sq_dists(Z))


def decompose(Z: np.ndarray, y: np.ndarray) -> dict:
    """Fit state for every lambda: K = U diag(w) U^T, b = U^T (y - mean)  (mf-052)."""
    Z = np.asarray(Z, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    mean = float(y.mean())  # centering with the mean of this training part, per mf-047
    K = _sq_dists(Z)  # squared distances, overwritten below by the kernel
    m = _median_upper(K)  # per mf-050
    gamma = C_GAMMA / m  # per mf-048, mf-049
    K *= -gamma
    np.exp(K, out=K)  # RBF kernel exp(-gamma * d2), per mf-046
    w, U = np.linalg.eigh(K, UPLO="L")  # float64, eigenvalues used as computed, per mf-052
    del K
    return {"Z": Z, "mean": mean, "m": m, "gamma": gamma, "w": w, "U": U, "b": U.T @ (y - mean)}


def _alpha(st: dict, lam: float) -> np.ndarray:
    d = st["w"] + lam
    if np.any(d <= 0):  # stop, no clipping, per mf-052
        raise ValueError(f"eigenvalue + lambda <= 0 (min {d.min()!r}, lambda {lam!r})")
    return st["U"] @ (st["b"] / d)  # alpha = U diag(1/(w + lam)) U^T (y - mean), per mf-052


def _kernel_new(st: dict, Z_new: np.ndarray) -> np.ndarray:
    K = _sq_dists(Z_new, st["Z"])  # rectangular, small
    K *= -st["gamma"]
    return np.exp(K, out=K)


def predict(st: dict, Z_new: np.ndarray, lam: float) -> np.ndarray:
    """K(Z_new, train) alpha + mean  (mf-047, mf-052)."""
    return _kernel_new(st, Z_new) @ _alpha(st, lam) + st["mean"]


def select_lambda(X_train: np.ndarray, y_train: np.ndarray) -> dict:
    """Inner 5-fold selection of lambda by mean AP (mf-049); held-out r_hat for the alarm line (mf-051)."""
    grid = [float(lam) for lam in LAMBDA_GRID]  # read at call time; fixed, never extended (mf-049)
    y_hr = y_train >= HR_THRESHOLD_LOG10
    skf = StratifiedKFold(INNER_SPLITS, shuffle=True, random_state=INNER_SEED)  # per mf-015
    aps = {lam: [] for lam in grid}
    oof = np.full((len(grid), len(y_train)), np.nan)
    for tr, va in skf.split(X_train, y_hr):
        pre = make_preprocessor().fit(X_train[tr])  # per mf-045, refit per inner training part
        st = decompose(pre.transform(X_train[tr]), y_train[tr])  # own mean, m, gamma (mf-047, mf-050)
        Kva = _kernel_new(st, pre.transform(X_train[va]))
        for i, lam in enumerate(grid):  # all lambda from the same decomposition, per mf-052
            oof[i, va] = Kva @ _alpha(st, lam) + st["mean"]
            aps[lam].append(average_precision_score(y_hr[va], oof[i, va]))  # per mf-013
        del st, Kva
    mean_ap = {lam: float(np.mean(aps[lam])) for lam in grid}
    best = max(mean_ap.values())
    lam = max(l for l in grid if mean_ap[l] == best)  # exact ties to the highest lambda, per mf-049
    return {"lam": lam, "mean_ap": mean_ap, "oof_r": oof[grid.index(lam)]}


def fit_predict_fold(X_train: np.ndarray, y_train: np.ndarray, X_val: np.ndarray) -> dict:
    sel = select_lambda(X_train, y_train)
    t = choose_alarm_line(sel["oof_r"], y_train)  # mf-012 on inner held-out r_hat, per mf-051
    pre = make_preprocessor().fit(X_train)  # per mf-045, mf-049: refit on the whole outer training fold
    st = decompose(pre.transform(X_train), y_train)
    r_val = predict(st, pre.transform(X_val), sel["lam"])  # selected lambda only, per mf-052
    m, gamma = st["m"], st["gamma"]
    del st
    return {
        "alpha": None, "lam": sel["lam"], "gamma": gamma, "m": m, "t": t,
        "n_oof": int(len(sel["oof_r"])),  # held-out predictions used for t, per mf-051
        "r_hat_val": r_val,
        "p_hr_val": (r_val >= t).astype(np.float64),  # alarm if r_hat >= t, per mf-051
        "final_converged": True, "nonconverged_alphas": [], "mean_ap": sel["mean_ap"],
    }
