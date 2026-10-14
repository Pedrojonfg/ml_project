"""Tests for Kelvins Collision Avoidance metrics (Uriot et al.).

Production implementations live in ``esa_kelvins_metrics.py`` (same directory).
Assumed public API (implementer may add helpers; these names are the contract
under test):

- ``HR_THRESHOLD_LOG10`` == -6.0
- ``is_high_risk(risk: float) -> bool``  — true when risk >= -6.0 (log10 space)
- ``f2_score(y_true, y_pred, threshold=HR_THRESHOLD_LOG10) -> float``
- ``mse_hr(y_true, y_pred, threshold=HR_THRESHOLD_LOG10) -> float``
- ``kelvins_l(mse_hr: float, f2: float) -> float`` — MSE_HR / F2; F2==0 => +inf
- ``crp_constant_risk()`` -> float  — always -5.0
- ``crp_predictions(n_events: int) -> np.ndarray`` — shape (n,) filled with CRP risk
- ``lrp_from_cdms(cdm_table) -> dict[int, float] | np.ndarray``

``cdm_table`` for LRP: mapping with numpy arrays ``event_id``, ``time_to_tca``,
``risk``. One row per CDM. LRP per event = ``risk`` at the row with *minimum*
``time_to_tca`` among rows with ``time_to_tca >= 2.0`` (latest known early CDM).
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pytest

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from esa_kelvins_metrics import (  # noqa: E402
    HR_THRESHOLD_LOG10,
    crp_constant_risk,
    crp_predictions,
    f2_score,
    is_high_risk,
    kelvins_l,
    lrp_from_cdms,
    mse_hr,
)


def _cdm_table(
    event_id: list[int],
    time_to_tca: list[float],
    risk: list[float],
) -> dict[str, np.ndarray]:
    return {
        "event_id": np.asarray(event_id, dtype=np.int64),
        "time_to_tca": np.asarray(time_to_tca, dtype=np.float64),
        "risk": np.asarray(risk, dtype=np.float64),
    }


def _f2_manual(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    threshold: float = -6.0,
    beta: float = 2.0,
) -> float:
    """Reference F-beta (beta=2) for binary HR labels derived from log10 risk."""
    t_pos = y_true >= threshold
    p_pos = y_pred >= threshold
    tp = int(np.sum(t_pos & p_pos))
    fp = int(np.sum(~t_pos & p_pos))
    fn = int(np.sum(t_pos & ~p_pos))
    if tp == 0 and fp == 0 and fn == 0:
        return 1.0
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    if precision + recall == 0.0:
        return 0.0
    b2 = beta * beta
    return (1.0 + b2) * precision * recall / (b2 * precision + recall)


# --- threshold / HR ---


def test_hr_threshold_constant() -> None:
    assert HR_THRESHOLD_LOG10 == -6.0


def test_is_high_risk_boundary_and_examples() -> None:
    assert is_high_risk(-6.0) is True
    assert is_high_risk(-5.0) is True
    assert is_high_risk(-6.0001) is False
    assert is_high_risk(-10.0) is False


# --- F2 ---


def test_f2_perfect_all_non_hr() -> None:
    y = np.array([-7.0, -8.0, -6.5])
    assert f2_score(y, y) == pytest.approx(1.0)
    assert f2_score(y, y) == pytest.approx(_f2_manual(y, y))


def test_f2_perfect_all_hr() -> None:
    y = np.array([-5.0, -6.0, -4.0])
    assert f2_score(y, y) == pytest.approx(1.0)


def test_f2_false_negative_lowers_recall() -> None:
    y_true = np.array([-5.0, -5.0, -8.0])
    y_pred = np.array([-5.0, -7.0, -8.0])
    expected = _f2_manual(y_true, y_pred)
    assert expected == pytest.approx(5.0 * 1.0 * 0.5 / (4.0 * 1.0 + 0.5))
    assert f2_score(y_true, y_pred) == pytest.approx(expected)


def test_f2_false_positive_lowers_precision() -> None:
    y_true = np.array([-8.0, -8.0])
    y_pred = np.array([-5.0, -8.0])
    expected = _f2_manual(y_true, y_pred)
    assert f2_score(y_true, y_pred) == pytest.approx(expected)
    assert expected < 1.0


def test_f2_all_wrong_hr_predictions_gives_zero() -> None:
    y_true = np.array([-5.0, -5.0])
    y_pred = np.array([-8.0, -8.0])
    assert f2_score(y_true, y_pred) == pytest.approx(0.0)


def test_f2_empty_arrays() -> None:
    empty = np.array([], dtype=np.float64)
    # ponytail: paper does not define empty-event F2; expect 0.0 or NaN — pick 0.0
    assert f2_score(empty, empty) == pytest.approx(0.0)


# --- MSE_HR ---


def test_mse_hr_only_true_high_risk_events() -> None:
    y_true = np.array([-5.0, -7.0, -5.5])
    y_pred = np.array([0.0, 100.0, 1.0])
    # HR mask: first and third only; -7 is not HR
    expected = np.mean([(-5.0 - 0.0) ** 2, (-5.5 - 1.0) ** 2])
    assert mse_hr(y_true, y_pred) == pytest.approx(expected)


def test_mse_hr_no_true_hr_is_nan_or_zero() -> None:
    y_true = np.array([-7.0, -8.0])
    y_pred = np.array([-5.0, -5.0])
    result = mse_hr(y_true, y_pred)
    # ponytail: undefined when no HR events — accept nan or 0.0
    assert result == 0.0 or math.isnan(result)


def test_mse_hr_single_hr_event() -> None:
    y_true = np.array([-6.0])
    y_pred = np.array(-5.5)
    assert mse_hr(y_true, y_pred) == pytest.approx(0.25)


# --- L = MSE_HR / F2 ---


def test_kelvins_l_combines_mse_hr_and_f2() -> None:
    y_true = np.array([-5.0, -5.0, -8.0])
    y_pred = np.array([-5.0, -6.5, -8.0])
    f2 = f2_score(y_true, y_pred)
    m = mse_hr(y_true, y_pred)
    assert kelvins_l(m, f2) == pytest.approx(m / f2)


def test_kelvins_l_zero_f2_is_positive_infinity() -> None:
    assert kelvins_l(1.0, 0.0) == math.inf
    assert kelvins_l(0.513, 0.0) == math.inf


def test_kelvins_l_perfect_f2_zero_mse_is_zero() -> None:
    assert kelvins_l(0.0, 1.0) == pytest.approx(0.0)


# --- CRP ---


def test_crp_constant_risk_is_minus_five() -> None:
    assert crp_constant_risk() == pytest.approx(-5.0)


def test_crp_predictions_vector() -> None:
    preds = crp_predictions(4)
    assert preds.shape == (4,)
    assert np.all(preds == pytest.approx(-5.0))


def test_crp_on_synthetic_events_matches_manual_l() -> None:
    y_true = np.array([-5.0, -7.0, -6.0, -8.0])
    y_pred = crp_predictions(len(y_true))
    f2 = f2_score(y_true, y_pred)
    m = mse_hr(y_true, y_pred)
    assert kelvins_l(m, f2) == pytest.approx(m / f2)


# --- LRP ---


def test_lrp_picks_min_time_to_tca_among_at_least_two_days() -> None:
    # paper r_{-2}: latest known among ttc>=2 == smallest ttc in that set
    table = _cdm_table(
        event_id=[1, 1, 1, 2, 2],
        time_to_tca=[3.0, 2.5, 1.0, 2.0, 5.0],
        risk=[-7.0, -6.5, -5.0, -8.0, -9.0],
    )
    out = lrp_from_cdms(table)
    if isinstance(out, dict):
        assert out[1] == pytest.approx(-6.5)
        assert out[2] == pytest.approx(-8.0)
    else:
        out = np.asarray(out)
        assert out[0] == pytest.approx(-6.5)
        assert out[1] == pytest.approx(-8.0)


def test_lrp_tie_on_time_to_tca_ambiguity() -> None:
    """If two CDMs share min time_to_tca >= 2, behavior is implementation-defined."""
    table = _cdm_table(
        event_id=[10, 10],
        time_to_tca=[4.0, 4.0],
        risk=[-6.0, -5.0],
    )
    out = lrp_from_cdms(table)
    risk = out[10] if isinstance(out, dict) else out[0]
    assert risk in (-6.0, -5.0)


def test_lrp_event_with_no_cdm_at_least_two_days() -> None:
    table = _cdm_table(
        event_id=[3, 3],
        time_to_tca=[1.5, 0.5],
        risk=[-4.0, -3.0],
    )
    out = lrp_from_cdms(table)
    if isinstance(out, dict):
        assert 3 not in out or math.isnan(out[3])
    else:
        # ponytail: single-event array may be nan or raise — nan acceptable
        val = float(np.asarray(out).ravel()[0])
        assert math.isnan(val) or val == pytest.approx(-4.0)  # if fallback to any CDM


def test_lrp_multiple_events_independent() -> None:
    table = _cdm_table(
        event_id=[1, 2, 1, 2],
        time_to_tca=[2.0, 3.0, 5.0, 2.0],
        risk=[-10.0, -11.0, -9.0, -12.0],
    )
    out = lrp_from_cdms(table)
    r1 = out[1] if isinstance(out, dict) else out[0]
    r2 = out[2] if isinstance(out, dict) else out[1]
    assert r1 == pytest.approx(-10.0)  # ttc 2.0 beats 5.0
    assert r2 == pytest.approx(-12.0)  # ttc 2.0 beats 3.0


# --- paper reference targets (soft) ---


@pytest.mark.parametrize(
    "name,target",
    [
        ("lrp_L", 0.694),
        ("lrp_mse_hr", 0.513),
        ("lrp_f2", 0.739),
        ("crp_L", 2.5),
    ],
)
def test_official_test_paper_targets(name: str, target: float) -> None:
    # ponytail: requires official test labels + CDM table on disk; not downloaded here
    pytest.skip(
        f"soft check {name}≈{target} — load official test fixtures when available"
    )


def test_lrp_metric_pipeline_self_consistent_on_toy_cdm() -> None:
    """End-to-end: LRP preds + per-event truths -> L matches components."""
    table = _cdm_table(
        event_id=[1, 1, 2, 2],
        time_to_tca=[3.0, 1.0, 2.5, 2.5],
        risk=[-6.0, -4.0, -7.0, -8.0],
    )
    lrp = lrp_from_cdms(table)
    if isinstance(lrp, dict):
        y_pred = np.array([lrp[1], lrp[2]])
    else:
        y_pred = np.asarray(lrp, dtype=np.float64)
    y_true = np.array([-5.5, -7.5])
    f2 = f2_score(y_true, y_pred)
    m = mse_hr(y_true, y_pred)
    assert kelvins_l(m, f2) == pytest.approx(m / f2)
