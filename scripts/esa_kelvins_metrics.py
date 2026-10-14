"""Kelvins Collision Avoidance scoring helpers (Uriot et al.)."""
# ponytail: numpy only; pure functions for tests + proposal baselines

from __future__ import annotations

import math
from typing import Mapping

import numpy as np

HR_THRESHOLD_LOG10 = -6.0
CRP_RISK = -5.0


def is_high_risk(risk: float, threshold: float = HR_THRESHOLD_LOG10) -> bool:
    return float(risk) >= threshold


def f2_score(
    y_true,
    y_pred,
    threshold: float = HR_THRESHOLD_LOG10,
    beta: float = 2.0,
) -> float:
    y_true = np.asarray(y_true, dtype=np.float64).ravel()
    y_pred = np.asarray(y_pred, dtype=np.float64).ravel()
    if y_true.size == 0:
        return 0.0
    t_pos = y_true >= threshold
    p_pos = y_pred >= threshold
    tp = int(np.sum(t_pos & p_pos))
    fp = int(np.sum(~t_pos & p_pos))
    fn = int(np.sum(t_pos & ~p_pos))
    # ponytail: all-negative perfect → F=1 (sklearn zero_division=1 style)
    if tp == 0 and fp == 0 and fn == 0:
        return 1.0
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    if precision + recall == 0.0:
        return 0.0
    b2 = beta * beta
    return (1.0 + b2) * precision * recall / (b2 * precision + recall)


def mse_hr(
    y_true,
    y_pred,
    threshold: float = HR_THRESHOLD_LOG10,
    clip_at: float | None = -6.001,
) -> float:
    """MSE on true HR events. Kelvins/paper clip risk at -6.001 for this term."""
    y_true = np.asarray(y_true, dtype=np.float64).ravel()
    y_pred = np.asarray(y_pred, dtype=np.float64).ravel()
    mask = y_true >= threshold
    if not np.any(mask):
        return 0.0
    yt = y_true[mask]
    yp = y_pred[mask]
    if clip_at is not None:
        # ponytail: match Uriot et al. Table 3 footnote / scoring note
        yt = np.maximum(yt, clip_at)
        yp = np.maximum(yp, clip_at)
    d = yt - yp
    return float(np.mean(d * d))


def kelvins_l(mse_hr_value: float, f2: float) -> float:
    if f2 == 0.0:
        return math.inf
    return float(mse_hr_value) / float(f2)


def crp_constant_risk() -> float:
    return CRP_RISK


def crp_predictions(n_events: int) -> np.ndarray:
    return np.full(int(n_events), CRP_RISK, dtype=np.float64)


def lrp_from_cdms(cdm_table: Mapping[str, np.ndarray]) -> dict[int, float]:
    """Latest Risk Prediction: risk at smallest time_to_tca among CDMs with ttc >= 2.

    (Paper r_{-2}: latest known risk still at least 2 days before TCA.)
    """
    event_id = np.asarray(cdm_table["event_id"])
    ttc = np.asarray(cdm_table["time_to_tca"], dtype=np.float64)
    risk = np.asarray(cdm_table["risk"], dtype=np.float64)
    out: dict[int, float] = {}
    for eid in np.unique(event_id):
        m = (event_id == eid) & (ttc >= 2.0)
        if not np.any(m):
            continue
        # among eligible, latest in time = closest to TCA = min time_to_tca
        idx = np.where(m)[0]
        j = idx[np.argmin(ttc[idx])]
        out[int(eid)] = float(risk[j])
    return out
