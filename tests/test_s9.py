"""S9 cohort + LMO skip rules (pj-054, pj-060)."""

import numpy as np
import pandas as pd

from src.features import build_features
from src.protocol import TTC_MIN, build_event_table
from src.s9 import LMO_REASON_ZERO_HR, cohort_event_ids, run_lmo


def _mini_cdm():
  rows = []
  eid = 100
  for mission_id, ttcs in [(1, [4.0, 2.5, 1.0]), (2, [3.0, 2.0, 0.5])]:
    for ttc in ttcs:
      rows.append(
          dict(
              event_id=eid,
              time_to_tca=ttc,
              risk=ttc * 0.01 - 7.0,
              mission_id=mission_id,
              miss_distance=1.0,
              relative_speed=1.0,
              t_weighted_rms=1.0,
              c_object_type="PAYLOAD",
          )
      )
    eid += 1
  rows.append(
      dict(
          event_id=eid,
          time_to_tca=2.0,
          risk=-8.0,
          mission_id=3,
          miss_distance=1.0,
          relative_speed=1.0,
          t_weighted_rms=1.0,
          c_object_type="PAYLOAD",
      )
  )
  return pd.DataFrame(rows)


def test_cohort_event_ids_respects_cut():
  cdm = _mini_cdm()
  table = build_event_table(cdm)
  at2 = cohort_event_ids(cdm, table, float(TTC_MIN))
  at3 = cohort_event_ids(cdm, table, 3.0)
  assert set(at3).issubset(set(at2))
  assert len(at3) <= len(at2)


def test_build_features_ttc_min_changes_snapshots():
  cdm = _mini_cdm()
  table = build_event_table(cdm)
  f2 = build_features(table.iloc[:1], cdm, ttc_min=2.0)
  f3 = build_features(table.iloc[:1], cdm, ttc_min=3.0)
  assert f2.risk_snap_last.iloc[0] != f3.risk_snap_last.iloc[0]


def test_lmo_skips_zero_hr_mission():
  cdm = _mini_cdm()
  table = build_event_table(cdm)
  out = run_lmo(cdm, table, t_cut=2.0)
  skipped = [r for r in out["folds"] if r.get("status") == "skipped"]
  assert any(r["reason"] == LMO_REASON_ZERO_HR for r in skipped)
  assert out["n_missions_skipped"] == len(skipped)