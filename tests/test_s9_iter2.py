"""S9 iteration-2 GBDT protocol (pj-077) and t=2 bake-off reuse (pj-078)."""

from __future__ import annotations

import inspect
import json
import os
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest

import src.models.trees as trees
import src.s9 as s9
from src.protocol import TTC_MIN, build_event_table, make_folds
from src.s9 import run_leadtime_point, run_lmo

# Regression: S9 still wires GBDT through iteration-1 select_gbdt_n_estimators only.
_OLD_GBDT_SELECTOR = "select_gbdt_n_estimators"


def _mini_cdm():
  import pandas as pd

  rows = []
  eid = 100
  # Enough HR / non-HR for outer 3-fold and linear inner 5-fold; LRP≈last risk for floor_c.
  for i in range(24):
    mission_id = (i % 6) + 1
    is_hr = i < 12
    risk_final = -5.0 if is_hr else -8.0
    for ttc in (4.0, 3.0, 2.5, 1.0):
      rows.append(
          dict(
              event_id=eid,
              time_to_tca=ttc,
              risk=risk_final,
              mission_id=mission_id,
              miss_distance=1.0,
              relative_speed=1.0,
              t_weighted_rms=1.0,
              c_object_type="PAYLOAD",
          )
      )
    eid += 1
  return pd.DataFrame(rows)


def _mini_table_folds():
  cdm = _mini_cdm()
  table = build_event_table(cdm)
  folds = make_folds(table, n_splits=3, seeds=(42,))
  return cdm, table, folds


def _fake_bakeoff(l_unclipped: float = 1.111) -> dict:
  return {
      "model": "gbdt",
      "metrics": {
          "F2": 0.25,
          "MSE_HR_clipped": 0.5,
          "MSE_HR_unclipped": 0.55,
          "L_clipped": l_unclipped - 0.1,
          "L_unclipped": l_unclipped,
      },
  }


def _small_grids(monkeypatch, ws=(1, 2), ns=(3, 5)):
  monkeypatch.setattr(trees, "W_GRID", ws)
  monkeypatch.setattr(trees, "N_ESTIMATORS_GRID", ns)
  # keep S9 module aliases in sync with trees grids used by nested selection
  monkeypatch.setattr(s9, "W_GRID", ws)
  monkeypatch.setattr(s9, "N_ESTIMATORS_GRID", ns)


def _stub_linear(monkeypatch):
  """Avoid S4 nested α search on tiny synthetic X (contract under test is GBDT)."""

  def fake_pick(X, y, eid, folds):
    return "ols", {"L_unclipped": 1.0, "F2": 0.1}

  def fake_lin_cv(slug, X, y, eid, folds):
    class R:
      metrics = {"L_unclipped": 1.0, "F2": 0.1}
      oof_r_hat = np.full(len(y), -7.0)
      oof_p_hr = np.zeros(len(y))

    return R()

  def fake_fit_predict(slug, X_tr, y_tr, X_te):
    return {"r_hat_val": np.full(len(X_te), -7.0), "p_hr_val": np.zeros(len(X_te))}

  monkeypatch.setattr(s9, "_pick_linear_slug", fake_pick)
  monkeypatch.setattr(s9, "run_linear_cv", fake_lin_cv)
  monkeypatch.setattr(s9, "fit_predict_fold", fake_fit_predict)
  monkeypatch.setattr(s9, "metrics_pooled_from_oof", lambda y, r, p: {"L_unclipped": 1.0, "F2": 0.1})


def _small_folds(monkeypatch, n_splits=2):
  from src.protocol import make_folds as real_make_folds

  def _mk(table, seeds=(42,), n_splits=n_splits):
    return real_make_folds(table, seeds=seeds, n_splits=n_splits)

  monkeypatch.setattr(s9, "make_folds", _mk)


@pytest.fixture
def mini():
  return _mini_table_folds()


def test_gbdt_from_bakeoff_exposes_top_level_metrics(tmp_path):
  """Protects pj-078: helper reads results/gbdt.json-shaped top-level metrics."""
  assert hasattr(s9, "gbdt_from_bakeoff"), "gbdt_from_bakeoff path/dict helper required"
  path = tmp_path / "gbdt.json"
  bake = _fake_bakeoff(2.345)
  path.write_text(json.dumps(bake))
  got = s9.gbdt_from_bakeoff(path)
  assert got["L_unclipped"] == pytest.approx(2.345)
  got_dict = s9.gbdt_from_bakeoff(bake)
  assert got_dict["L_unclipped"] == pytest.approx(2.345)


def test_leadtime_point_accepts_bakeoff_kwarg():
  """Regression: run_leadtime_point must accept injected bake-off for t_cut=2."""
  params = inspect.signature(run_leadtime_point).parameters
  assert "bakeoff_gbdt" in params or "bakeoff_gbdt_path" in params


def test_leadtime_t2_reuses_bakeoff_without_old_gbdt_selector(mini, monkeypatch):
  """Protects pj-078: t_cut=2 GBDT metrics come from bake-off; no select_gbdt_n_estimators."""
  cdm, table, folds = mini
  bake = _fake_bakeoff(9.876)

  def _forbidden(*_a, **_k):
    raise AssertionError("t_cut=2 must not call iteration-1 GBDT n_estimators-only path")

  monkeypatch.setattr(s9, _OLD_GBDT_SELECTOR, _forbidden)
  monkeypatch.setattr(s9, "run_oof_cv", _forbidden)
  _stub_linear(monkeypatch)

  point = run_leadtime_point(2, cdm, table, folds, bakeoff_gbdt=bake)
  gbdt = point.models["gbdt"]
  assert gbdt["metrics_pooled"]["L_unclipped"] == pytest.approx(9.876)
  assert gbdt.get("source") == "bakeoff" or gbdt.get("reused_bakeoff") is True


@pytest.mark.parametrize("t_cut", [3, 4])
def test_leadtime_t34_gbdt_uses_nested_w_and_n_estimators(mini, monkeypatch, t_cut):
  """Protects pj-077: cuts 3–4 select (w, n_estimators) via trees.select_by_inner_cv."""
  cdm, table, folds = mini
  _small_grids(monkeypatch)
  inner_calls, old_calls = [], []

  real_select = trees.select_by_inner_cv

  def spy_select(*args, **kwargs):
    inner_calls.append({"args": args, "kwargs": kwargs})
    return real_select(*args, **kwargs)

  def spy_old(*_a, **_k):
    old_calls.append(True)
    raise AssertionError("iteration-1 select_gbdt_n_estimators must not run under pj-077")

  monkeypatch.setattr(trees, "select_by_inner_cv", spy_select)
  monkeypatch.setattr(s9, _OLD_GBDT_SELECTOR, spy_old)
  _stub_linear(monkeypatch)

  point = run_leadtime_point(t_cut, cdm, table, folds)
  assert inner_calls, "GBDT must use trees.select_by_inner_cv for iteration-2 nested selection"
  assert not old_calls
  gbdt = point.models["gbdt"]
  assert "w" in gbdt
  assert gbdt["w"] in trees.W_GRID
  assert gbdt["n_estimators"] in trees.N_ESTIMATORS_GRID


def test_lmo_gbdt_fold_uses_nested_selection_not_old_selector(mini, monkeypatch):
  """Protects pj-077: LMO GBDT folds use HR weights + nested (w, n_estimators)."""
  cdm, table, _ = mini
  _small_grids(monkeypatch)
  inner_calls, old_calls = [], []

  real_select = trees.select_by_inner_cv

  def spy_select(*args, **kwargs):
    inner_calls.append(True)
    return real_select(*args, **kwargs)

  def spy_old(*_a, **_k):
    old_calls.append(True)
    raise AssertionError("LMO must not use select_gbdt_n_estimators-only path")

  monkeypatch.setattr(trees, "select_by_inner_cv", spy_select)
  monkeypatch.setattr(s9, _OLD_GBDT_SELECTOR, spy_old)
  _small_folds(monkeypatch)
  _stub_linear(monkeypatch)

  out = run_lmo(cdm, table, t_cut=float(TTC_MIN))
  ok = [r for r in out["folds"] if r.get("status") == "ok"]
  assert ok, "need at least one evaluated LMO fold in synthetic cohort"
  assert inner_calls
  assert not old_calls
  for row in ok:
    assert "w" in row
    assert row["w"] in trees.W_GRID
    assert row["n_estimators"] in trees.N_ESTIMATORS_GRID


def test_run_leadtime_curve_resumes_per_cut_checkpoint(mini, tmp_path, monkeypatch):
  """Protects per-cut cache: existing cache_dir/t{t}.json skips recomputation."""
  assert "cache_dir" in inspect.signature(s9.run_leadtime_curve).parameters
  cdm, table, folds = mini
  cached_t2 = {
      "t_cut": 2,
      "n_events": 1,
      "n_hr": 1,
      "models": {
          "lrp": {"metrics_pooled": {"L_unclipped": 0.0}},
          "gbdt": {"metrics_pooled": {"L_unclipped": 7.7}, "source": "bakeoff"},
          "linear": {"metrics_pooled": {"L_unclipped": 0.0}, "slug": "ols"},
      },
  }
  (tmp_path / "t2.json").write_text(json.dumps(cached_t2))

  calls = []

  def counting_point(t_cut, *args, **kwargs):
    calls.append(t_cut)
    return run_leadtime_point(t_cut, *args, **kwargs)

  monkeypatch.setattr(s9, "run_leadtime_point", counting_point)
  _small_grids(monkeypatch)
  _stub_linear(monkeypatch)
  bake_path = tmp_path / "gbdt_bake.json"
  bake_path.write_text(json.dumps(_fake_bakeoff(1.0)))

  curve = s9.run_leadtime_curve(
      cdm,
      table,
      folds,
      cache_dir=tmp_path,
      bakeoff_gbdt_path=bake_path,
  )
  assert 2 not in calls, "t_cut=2 must load from cache, not re-enter run_leadtime_point"
  assert set(calls) == {3, 4}
  t2 = next(p for p in curve["points"] if p["t_cut"] == 2)
  assert t2["L_unclipped"]["gbdt"] == pytest.approx(7.7)


def test_run_lmo_resumes_per_mission_checkpoint(mini, tmp_path, monkeypatch):
  """Protects per-mission cache: mission_{id}.json skips _lmo_eval_split for that mission."""
  assert "cache_dir" in inspect.signature(s9.run_lmo).parameters
  cdm, table, _ = mini

  cached = {
      "mission_id": 1,
      "status": "ok",
      "n_test": 1,
      "n_hr_test": 1,
      "w": 1,
      "n_estimators": 3,
      "gbdt_n_estimators": 3,
      "linear_slug": "ridge",
      "metrics": {
          "lrp": {"L_unclipped": 1.0},
          "gbdt": {"L_unclipped": 2.5},
          "linear": {"L_unclipped": 1.5},
      },
  }
  (tmp_path / "mission_1.json").write_text(json.dumps(cached))

  splits = []

  real_split = s9._lmo_eval_split

  def counting_split(*args, **kwargs):
    splits.append(True)
    return real_split(*args, **kwargs)

  monkeypatch.setattr(s9, "_lmo_eval_split", counting_split)
  _small_grids(monkeypatch)
  _small_folds(monkeypatch)
  _stub_linear(monkeypatch)

  out = s9.run_lmo(cdm, table, t_cut=float(TTC_MIN), cache_dir=tmp_path)
  m1 = next(r for r in out["folds"] if r["mission_id"] == 1)
  assert m1["metrics"]["gbdt"]["L_unclipped"] == pytest.approx(2.5)
  assert len(splits) < out["n_missions_evaluated"], "cached mission must not call _lmo_eval_split"


def test_atomic_write_json_leaves_valid_file_on_replace_failure(tmp_path):
  """Protects atomic checkpoint writes: failed replace must not corrupt the target."""
  assert hasattr(s9, "_atomic_write_json")
  target = tmp_path / "t3.json"
  target.write_text(json.dumps({"t_cut": 3, "stale": True}))

  with patch("os.replace", side_effect=OSError("simulated crash")):
    with pytest.raises(OSError):
      s9._atomic_write_json(target, {"t_cut": 3, "fresh": True})

  assert json.loads(target.read_text()) == {"t_cut": 3, "stale": True}
  leftovers = [p.name for p in tmp_path.iterdir() if p.name.startswith(".") or p.suffix == ".tmp"]
  assert not leftovers, f"no corrupt partial checkpoint files: {leftovers}"


def test_atomic_write_json_uses_temp_then_replace(tmp_path):
  """Protects atomic checkpoint writes: happy path uses mkstemp + os.replace."""
  assert hasattr(s9, "_atomic_write_json")
  target = tmp_path / "mission_2.json"
  payload = {"mission_id": 2, "status": "ok"}
  replaced = []

  real_replace = os.replace

  def track_replace(src, dst):
    replaced.append((Path(src), Path(dst)))
    return real_replace(src, dst)

  with patch("tempfile.mkstemp", return_value=(99, str(tmp_path / "_part.json"))):
    with patch("os.replace", side_effect=track_replace):
      s9._atomic_write_json(target, payload)

  assert json.loads(target.read_text()) == payload
  assert replaced and replaced[0][1] == target