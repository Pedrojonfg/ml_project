"""Tests for the S2 jump taxonomy (mf-001..mf-005): labels from y_final vs latest_risk."""

import numpy as np
import pandas as pd

from src.metrics import HR_THRESHOLD_LOG10
from src.taxonomy import JUMP_CUT, label_events

OUT_COLUMNS = ["event_id", "delta", "jump_class", "hr_crossing", "lead_time"]
CLASSES = {"jump-up", "jump-down", "stable-high", "stable-low"}


def table(pairs):
    """pairs: [(lrp, risk_final), ...] -> event table with event_ids 1..n."""
    n = len(pairs)
    return pd.DataFrame({
        "event_id": np.arange(1, n + 1, dtype="int64"),
        "risk_final": [p[1] for p in pairs],
        "y_hr": [p[1] >= HR_THRESHOLD_LOG10 for p in pairs],
        "lrp": [p[0] for p in pairs],
        "first_ttc": 6.0,
        "last_ttc": 1.0,
        "n_cdm": 3,
    }).astype({"risk_final": "float64", "lrp": "float64"})


def cdms(events):
    """events: {event_id: [time_to_tca, ...]} -> CDM frame."""
    rows = [(e, t) for e, lst in events.items() for t in lst]
    df = pd.DataFrame(rows, columns=["event_id", "time_to_tca"])
    return df.astype({"event_id": "int64", "time_to_tca": "float64"})


def label(pairs, cut=None):
    t = table(pairs)
    c = cdms({i: [3.0, 1.0] for i in t.event_id})
    return label_events(t, c) if cut is None else label_events(t, c, cut)


def test_jump_cut_default():
    assert JUMP_CUT == 1.0  # per mf-003


def test_output_columns_dtypes_shape_order():
    t = table([(-5.0, -4.0), (-7.0, -7.0), (-4.0, -8.0)])
    t = t.iloc[[2, 0, 1]].reset_index(drop=True)  # non-sorted order must be kept
    out = label_events(t, cdms({1: [3.0], 2: [3.0], 3: [3.0]}))
    assert out.columns.tolist() == OUT_COLUMNS
    assert len(out) == len(t)
    assert out.event_id.tolist() == t.event_id.tolist()
    assert out.delta.dtype == "float64" and out.lead_time.dtype == "float64"
    np.testing.assert_allclose(out.delta, t.risk_final - t.lrp)


def test_four_classes():
    out = label([(-5.5, -4.0), (-4.0, -6.5), (-5.5, -5.2), (-7.5, -7.2)])
    assert out.jump_class.tolist() == ["jump-up", "jump-down", "stable-high", "stable-low"]


def test_inclusive_boundaries():  # per mf-003
    out = label([(-5.0, -4.0), (-4.0, -5.0)])  # delta exactly +1 and -1
    assert out.delta.tolist() == [1.0, -1.0]
    assert out.jump_class.tolist() == ["jump-up", "jump-down"]


def test_stable_threshold_boundary():  # per mf-004
    out = label([(-6.0, -6.0), (-6.5, -6.25)])  # -6.0 -> high; -6.25 -> low
    assert out.jump_class.tolist() == ["stable-high", "stable-low"]


def test_every_event_one_valid_class():
    rng = np.random.default_rng(0)
    pairs = list(zip(rng.uniform(-9, -2, 100), rng.uniform(-9, -2, 100)))
    out = label(pairs)
    assert out.jump_class.notna().all()
    assert set(out.jump_class) <= CLASSES


def test_hr_crossing_cases():  # per mf-002
    out = label([
        (-6.1, -5.9),  # up, but not a jump
        (-5.9, -6.1),  # down, not a jump
        (-5.5, -4.4),  # jump, no crossing
        (-6.0, -5.5),  # lrp exactly at threshold is already high -> none
        (-7.0, -6.0),  # lands exactly on threshold -> up
        (-6.0, -6.5),  # leaves threshold -> down
    ])
    assert out.hr_crossing.tolist() == ["up", "down", "none", "none", "up", "down"]


def test_class_and_crossing_independent():
    out = label([(-6.1, -5.9), (-5.5, -4.4), (-8.0, -4.0), (-4.0, -8.0)])
    assert out.jump_class.tolist() == ["stable-high", "jump-up", "jump-up", "jump-down"]
    assert out.hr_crossing.tolist() == ["up", "none", "up", "down"]


def test_lead_time_is_last_valid_cdm():  # per mf-005
    t = table([(-5.0, -4.0), (-5.0, -4.0), (-5.0, -4.0)])
    c = cdms({1: [6.5, 3.0, 2.0, 1.2, 0.4], 2: [5.0, 2.1, 0.3], 3: [1.5, 0.5]})
    out = label_events(t, c)
    assert out.lead_time.iloc[0] == 2.0
    assert out.lead_time.iloc[1] == 2.1
    assert np.isnan(out.lead_time.iloc[2])  # no usable CDM


def test_lead_time_ignores_ttc_below_2():
    t = table([(-5.0, -4.0)])
    out = label_events(t, cdms({1: [1.99, 0.1, 4.0]}))
    assert out.lead_time.iloc[0] == 4.0


def test_deterministic():
    t = table([(-5.0, -4.0), (-7.0, -7.0)])
    c = cdms({1: [3.0, 1.0], 2: [4.0]})
    pd.testing.assert_frame_equal(label_events(t, c), label_events(t, c))


def test_inputs_not_mutated():
    t = table([(-5.0, -4.0), (-7.0, -7.0)])
    c = cdms({1: [3.0, 1.0], 2: [4.0]})
    t0, c0 = t.copy(), c.copy()
    label_events(t, c)
    pd.testing.assert_frame_equal(t, t0)
    pd.testing.assert_frame_equal(c, c0)


def test_no_leakage_columns():  # per mf-001
    t = table([(-5.0, -4.0)])
    out = label_events(t, cdms({1: [3.0]}))
    for col in ["risk_final", "lrp", "y_hr", "first_ttc", "last_ttc", "n_cdm"]:
        assert col not in out.columns
    for col in ["delta", "jump_class", "hr_crossing", "lead_time"]:
        assert col not in t.columns  # input table stays label-free


def test_cut_argument():  # per mf-003
    pairs = [(-5.0, -4.1), (-5.0, -3.9)]  # delta 0.9 and 1.1
    assert label(pairs).jump_class.tolist() == ["stable-high", "jump-up"]
    assert label(pairs, cut=0.5).jump_class.tolist() == ["jump-up", "jump-up"]
    assert label(pairs, cut=2.0).jump_class.tolist() == ["stable-high", "stable-high"]


def test_extra_cdm_columns_accepted():
    t = table([(-5.0, -4.0)])
    c = cdms({1: [3.0, 2.5]})
    c["mission_id"] = 7
    c["risk"] = -5.0
    out = label_events(t, c)
    assert out.lead_time.iloc[0] == 2.5
