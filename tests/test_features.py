"""S3 feature builder (pj-009..pj-013)."""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.features import FEATURE_COLUMNS, OBJECT_TYPES, build_features
from src.protocol import TTC_MIN, build_event_table

DATA = (
    Path(__file__).resolve().parents[1]
    / "data/esa/Collision Avoidance Challenge - Dataset/kelvins_competition_data/train_data.csv"
)
USECOLS = [
    "event_id",
    "time_to_tca",
    "risk",
    "miss_distance",
    "relative_speed",
    "t_weighted_rms",
    "c_object_type",
]


def _cdm_frame(rows):
    return pd.DataFrame(rows, columns=USECOLS).astype(
        {
            "event_id": "int64",
            "time_to_tca": "float64",
            "risk": "float64",
            "miss_distance": "float64",
            "relative_speed": "float64",
            "t_weighted_rms": "float64",
        }
    )


def test_feature_columns_match_build_output():
    cdm = pd.read_csv(DATA, usecols=USECOLS, nrows=50000)
    table = build_event_table(cdm[["event_id", "time_to_tca", "risk"]])
    table = table.head(200)
    x = build_features(table, cdm)
    assert list(x.columns) == ["event_id"] + list(FEATURE_COLUMNS)
    assert len(x) == len(table)


def test_no_targets_in_features():
    cdm = _cdm_frame([
        (1, 5.0, -7.0, 100.0, 1.0, 0.01, "DEBRIS"),
        (1, 3.0, -6.5, 90.0, 1.0, 0.02, "DEBRIS"),
        (1, 0.5, -5.0, 80.0, 1.0, 0.03, "DEBRIS"),
    ])
    table = build_event_table(cdm[["event_id", "time_to_tca", "risk"]])
    x = build_features(table, cdm)
    for bad in ("risk_final", "y_hr", "lrp"):
        assert bad not in x.columns


def test_last_usable_risk_matches_lrp():
    cdm = _cdm_frame([
        (10, 6.0, -8.0, 100.0, 1.0, 0.01, "PAYLOAD"),
        (10, 4.0, -7.0, 90.0, 1.0, 0.02, "PAYLOAD"),
        (10, 2.5, -6.0, 80.0, 1.0, 0.03, "PAYLOAD"),
        (10, 0.3, -5.0, 70.0, 1.0, 0.04, "PAYLOAD"),
    ])
    table = build_event_table(cdm[["event_id", "time_to_tca", "risk"]])
    x = build_features(table, cdm)
    assert x.iloc[0]["risk_snap_last"] == table.iloc[0]["lrp"]


def test_single_usable_std_zero_and_snapshots_equal():
    cdm = _cdm_frame([
        (20, 3.0, -6.0, 50.0, 2.0, 0.05, "UNKNOWN"),
        (20, 0.4, -5.0, 40.0, 2.0, 0.06, "UNKNOWN"),
    ])
    table = build_event_table(cdm[["event_id", "time_to_tca", "risk"]])
    x = build_features(table, cdm)
    row = x.iloc[0]
    assert row["risk_agg_std"] == 0.0
    assert row["risk_snap_first"] == row["risk_snap_last"] == row["risk_snap_p50"]


def test_object_type_one_hot_last_usable():
    cdm = _cdm_frame([
        (30, 5.0, -7.0, 100.0, 1.0, 0.01, "DEBRIS"),
        (30, 2.2, -6.0, 90.0, 1.0, 0.02, "ROCKET BODY"),
        (30, 0.5, -5.0, 80.0, 1.0, 0.03, "ROCKET BODY"),
    ])
    table = build_event_table(cdm[["event_id", "time_to_tca", "risk"]])
    x = build_features(table, cdm)
    assert x.iloc[0]["obj_ROCKET_BODY"] == 1.0
    assert x.iloc[0]["obj_DEBRIS"] == 0.0


def test_contract_md_lists_same_columns():
    contract = (
        Path(__file__).resolve().parents[1] / "docs/contracts.md"
    ).read_text(encoding="utf-8")
    for col in FEATURE_COLUMNS:
        assert col in contract
