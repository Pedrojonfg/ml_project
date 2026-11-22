"""S9 lead-time curve and leave-mission-out (pj-053..060, pj-077, pj-078)."""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from statistics import mode
from typing import Any

import numpy as np
import pandas as pd

from src.features import FEATURE_COLUMNS, build_features
from src.metrics import lrp_from_cdms
from src.models.linear import _rep_metrics, fit_predict_fold, metrics_pooled_from_oof, run_linear_cv
import src.models.trees as trees
from src.models.trees import (  # noqa: F401 — old names kept for test monkeypatches
    N_ESTIMATORS_GRID,
    W_GRID,
    _fit_variants,
    _predict_variants,
    _sw,
    floor_c,
    kelvins_pack,
    make_gbdt,
    run_nested_tree_cv,
    run_oof_cv,
    select_gbdt_n_estimators,
)
from src.protocol import build_event_table, make_folds

LEAD_TIME_CUTS = (2, 3, 4)  # pj-054
LINEAR_SLUGS = ("ols", "ridge", "lasso")  # pj-056, pj-059
LMO_REASON_ZERO_HR = "zero_hr_in_holdout"  # pj-060


def cohort_event_ids(cdm: pd.DataFrame, table: pd.DataFrame, t_cut: float) -> np.ndarray:
    """Events in table with >=1 CDM at time_to_tca >= t_cut (pj-054)."""
    in_table = set(table.event_id.astype(int))
    ok = (
        cdm.loc[cdm.event_id.isin(in_table)]
        .groupby("event_id", sort=False)
        .time_to_tca
        .apply(lambda s: (s >= t_cut).any())
    )
    return ok.loc[ok].index.to_numpy(dtype=np.int64)


def mission_ids_for_events(cdm: pd.DataFrame, event_ids: np.ndarray) -> pd.Series:
    first = cdm.groupby("event_id", sort=False).mission_id.first()
    return first.reindex(event_ids).astype(np.int64)


def lrp_array(cdm: pd.DataFrame, event_ids: np.ndarray, t_cut: float) -> np.ndarray:
    lut = lrp_from_cdms(cdm, ttc_min=t_cut)
    out = np.array([lut[int(e)] for e in event_ids], dtype=np.float64)
    if np.any(np.isnan(out)):
        raise RuntimeError("missing LRP for cohort event")
    return out


def gbdt_from_bakeoff(path_or_dict: Path | str | dict) -> dict[str, float]:
    """Top-level metrics from results/gbdt.json (pj-078)."""
    if isinstance(path_or_dict, (str, Path)):
        data = json.loads(Path(path_or_dict).read_text())
    else:
        data = path_or_dict
    return dict(data["metrics"] if "metrics" in data else data)


def _atomic_write_json(path: Path, obj: dict[str, Any]) -> None:
    # ponytail: temp + replace so a crash cannot leave a corrupt "done" checkpoint
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        try:
            os.close(fd)
        except OSError:
            pass
        Path(tmp).write_text(json.dumps(obj, indent=2, default=_json_default) + "\n")
        os.replace(tmp, path)
        tmp = ""
    finally:
        if tmp and os.path.exists(tmp):
            try:
                os.unlink(tmp)
            except OSError:
                pass


def _pick_linear_slug(
    X: np.ndarray, y: np.ndarray, eid: np.ndarray, folds: pd.DataFrame,
) -> tuple[str, dict[str, float]]:
    best_slug, best_m = None, None
    for slug in LINEAR_SLUGS:
        res = run_linear_cv(slug, X, y, eid, folds)
        pooled = metrics_pooled_from_oof(y, res.oof_r_hat, res.oof_p_hr)
        if best_m is None or _better_linear(pooled, best_m, slug, best_slug):
            best_slug, best_m = slug, pooled
    assert best_slug is not None and best_m is not None
    return best_slug, best_m


def _better_linear(
    cand: dict[str, float], incumbent: dict[str, float], slug: str, inc_slug: str,
) -> bool:
    """pj-056 tie-break: lower L_unclipped, then higher F2, then slug order."""
    lc, li = cand["L_unclipped"], incumbent["L_unclipped"]
    if lc < li:
        return True
    if lc > li:
        return False
    if cand["F2"] > incumbent["F2"]:
        return True
    if cand["F2"] < incumbent["F2"]:
        return False
    return slug < inc_slug


@dataclass
class LeadTimePoint:
    t_cut: int
    n_events: int
    n_hr: int
    models: dict[str, Any]


def _cohort_xy(
    t_cut: float, cdm: pd.DataFrame, table: pd.DataFrame, folds: pd.DataFrame,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, pd.DataFrame, int]:
    ids = cohort_event_ids(cdm, table, float(t_cut))
    sub = table[table.event_id.isin(ids)].sort_values("event_id", ignore_index=True)
    sub_folds = folds[folds.event_id.isin(ids)].sort_values(["rep", "event_id"]).reset_index(drop=True)
    feats = build_features(sub, cdm, ttc_min=float(t_cut))
    merged = feats.merge(sub[["event_id", "risk_final", "y_hr"]], on="event_id")
    merged = merged.sort_values("event_id", ignore_index=True)
    eid = merged.event_id.to_numpy(dtype=np.int64)
    X = merged[list(FEATURE_COLUMNS)].to_numpy(dtype=np.float64)
    y = merged.risk_final.to_numpy(dtype=np.float64)
    lrp = lrp_array(cdm, eid, float(t_cut))
    return X, y, lrp, eid, sub_folds, int(sub.y_hr.sum())


def run_leadtime_point(
    t_cut: int,
    cdm: pd.DataFrame,
    table: pd.DataFrame,
    folds: pd.DataFrame,
    *,
    bakeoff_gbdt: dict | None = None,
    bakeoff_gbdt_path: Path | str | None = None,
    nest_cache_dir: Path | str | None = None,
) -> LeadTimePoint:
    X, y, lrp, eid, sub_folds, n_hr = _cohort_xy(t_cut, cdm, table, folds)
    lrp_m = kelvins_pack(y, lrp)
    lin_slug, lin_pooled = _pick_linear_slug(X, y, eid, sub_folds)
    lin_res = run_linear_cv(lin_slug, X, y, eid, sub_folds)
    lin_mean = lin_res.metrics
    lin_mean["L_unclipped_pooled_pick"] = lin_pooled["L_unclipped"]

    if t_cut == 2 and (bakeoff_gbdt is not None or bakeoff_gbdt_path is not None):
        # per pj-078: reuse bake-off GBDT; do not retrain
        src = bakeoff_gbdt if bakeoff_gbdt is not None else bakeoff_gbdt_path
        assert src is not None
        m = gbdt_from_bakeoff(src)
        gbdt_block: dict[str, Any] = {
            "metrics": m,
            "metrics_pooled": m,
            "source": "bakeoff",
            "reused_bakeoff": True,
        }
    else:
        # per pj-077: nested (w, n_estimators) + c(w) + HR weights
        nest = Path(nest_cache_dir) if nest_cache_dir is not None else None
        if nest is not None:
            nest.mkdir(parents=True, exist_ok=True)
        res = run_nested_tree_cv("gbdt", X, y, lrp, eid, sub_folds, cache_dir=nest)
        ws = [f["w"] for f in res.floors]
        ns = [int(f["n_estimators"]) for f in res.floors]
        gbdt_block = {
            "metrics": res.metrics,
            "metrics_pooled": res.metrics_pooled,
            "w": float(mode(ws)) if ws else float(W_GRID[0]),
            "n_estimators": int(mode(ns)) if ns else int(N_ESTIMATORS_GRID[0]),
            "fold_records": res.floors,
        }

    return LeadTimePoint(
        t_cut=t_cut,
        n_events=len(eid),
        n_hr=n_hr,
        models={
            "lrp": {"metrics": lrp_m, "metrics_pooled": lrp_m},
            "gbdt": gbdt_block,
            "linear": {
                "slug": lin_slug,
                "metrics": lin_mean,
                "metrics_pooled": metrics_pooled_from_oof(y, lin_res.oof_r_hat, lin_res.oof_p_hr),
            },
        },
    )


def _metric_block_l_unclipped(block: dict[str, Any]) -> float:
    return float(block["metrics_pooled"]["L_unclipped"])


def _curve_entry_from_models(p: dict[str, Any]) -> dict[str, Any]:
    return {
        "t_cut": p["t_cut"],
        "n_events": p["n_events"],
        "n_hr": p["n_hr"],
        "L_unclipped": {
            "lrp": _metric_block_l_unclipped(p["models"]["lrp"]),
            "gbdt": _metric_block_l_unclipped(p["models"]["gbdt"]),
            "linear": _metric_block_l_unclipped(p["models"]["linear"]),
        },
        "linear_slug": p["models"]["linear"]["slug"],
        "detail": p["models"],
    }


def run_leadtime_curve(
    cdm: pd.DataFrame,
    table: pd.DataFrame | None = None,
    folds: pd.DataFrame | None = None,
    *,
    cache_dir: Path | str | None = None,
    bakeoff_gbdt_path: Path | str | None = None,
) -> dict[str, Any]:
    table = table if table is not None else build_event_table(cdm)
    folds = folds if folds is not None else make_folds(table)
    cache = Path(cache_dir) if cache_dir is not None else None
    if cache is not None:
        cache.mkdir(parents=True, exist_ok=True)
    bake = None
    if bakeoff_gbdt_path is not None:
        bake = json.loads(Path(bakeoff_gbdt_path).read_text())

    points: list[dict[str, Any]] = []
    for t in LEAD_TIME_CUTS:
        cp = cache / f"t{t}.json" if cache is not None else None
        if cp is not None and cp.is_file():
            points.append(_curve_entry_from_models(json.loads(cp.read_text())))
            continue
        nest = cache / f"gbdt_t{t}" if cache is not None else None
        pt = run_leadtime_point(
            t, cdm, table, folds,
            bakeoff_gbdt=bake if t == 2 else None,
            nest_cache_dir=nest,
        )
        raw = {"t_cut": pt.t_cut, "n_events": pt.n_events, "n_hr": pt.n_hr, "models": pt.models}
        if cp is not None:
            _atomic_write_json(cp, raw)
        points.append(_curve_entry_from_models(raw))

    return {
        "kind": "leadtime",
        "primary_metric": "L_unclipped",
        "points": points,
    }


def _lmo_eval_split(
    X_tr: np.ndarray,
    y_tr: np.ndarray,
    lrp_tr: np.ndarray,
    eid_tr: np.ndarray,
    folds_tr: pd.DataFrame,
    X_te: np.ndarray,
    y_te: np.ndarray,
    lrp_te: np.ndarray,
) -> dict[str, Any]:
    # per pj-077: nested select (w, n) on the LMO training part, then refit
    ns = tuple(N_ESTIMATORS_GRID)
    ws = tuple(W_GRID)
    tr = np.arange(len(y_tr), dtype=np.int64)
    rs = 42

    def fp(fit_idx, pred_idx, w):
        pipe, _ = _fit_variants("gbdt", X_tr, y_tr, lrp_tr, fit_idx, w, ns, rs)
        return _predict_variants("gbdt", pipe, X_tr[pred_idx], ns)

    (bw, bn), _scores = trees.select_by_inner_cv(fp, ws, tr, y_tr, rs)
    fc = floor_c(y_tr, lrp_tr, bw)
    gb = make_gbdt(int(bn), rs)
    gb.fit(X_tr, np.maximum(y_tr, fc["c"]), **_sw(y_tr, bw))
    r_gbdt = gb.predict(X_te)

    lin_slug, _ = _pick_linear_slug(X_tr, y_tr, eid_tr, folds_tr)
    lin = fit_predict_fold(lin_slug, X_tr, y_tr, X_te)
    r_lin = lin["r_hat_val"]
    p_lin = lin["p_hr_val"]

    return {
        "w": float(bw),
        "n_estimators": int(bn),
        "gbdt_n_estimators": int(bn),
        "linear_slug": lin_slug,
        "metrics": {
            "lrp": kelvins_pack(y_te, lrp_te),
            "gbdt": kelvins_pack(y_te, r_gbdt),
            "linear": _rep_metrics(y_te, r_lin, p_lin),
        },
    }


def run_lmo(
    cdm: pd.DataFrame,
    table: pd.DataFrame | None = None,
    t_cut: float = 2.0,
    *,
    cache_dir: Path | str | None = None,
) -> dict[str, Any]:
    table = table if table is not None else build_event_table(cdm)
    ids = cohort_event_ids(cdm, table, t_cut)
    sub = table[table.event_id.isin(ids)].sort_values("event_id", ignore_index=True)
    feats = build_features(sub, cdm, ttc_min=t_cut)
    merged = feats.merge(sub[["event_id", "risk_final", "y_hr"]], on="event_id")
    missions = mission_ids_for_events(cdm, merged.event_id.to_numpy(dtype=np.int64))
    cache = Path(cache_dir) if cache_dir is not None else None
    if cache is not None:
        cache.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, Any]] = []
    for mid in sorted(missions.unique()):
        cp = cache / f"mission_{int(mid)}.json" if cache is not None else None
        if cp is not None and cp.is_file():
            rows.append(json.loads(cp.read_text()))
            continue

        test_m = missions.to_numpy() == mid
        n_test = int(test_m.sum())
        n_hr_test = int(sub.y_hr.to_numpy()[test_m].sum())
        if n_hr_test == 0:
            row: dict[str, Any] = {
                "mission_id": int(mid),
                "status": "skipped",
                "reason": LMO_REASON_ZERO_HR,
                "n_test": n_test,
                "n_hr_test": 0,
            }
            if cp is not None:
                _atomic_write_json(cp, row)
            rows.append(row)
            continue

        train_m = ~test_m
        sub_tr = merged.loc[train_m].reset_index(drop=True)
        sub_te = merged.loc[test_m].reset_index(drop=True)
        eid_tr = sub_tr.event_id.to_numpy(dtype=np.int64)
        eid_te = sub_te.event_id.to_numpy(dtype=np.int64)
        folds_tr = make_folds(sub_tr[["event_id", "y_hr"]])

        X_tr = sub_tr[list(FEATURE_COLUMNS)].to_numpy(dtype=np.float64)
        y_tr = sub_tr.risk_final.to_numpy(dtype=np.float64)
        lrp_tr = lrp_array(cdm, eid_tr, t_cut)
        X_te = sub_te[list(FEATURE_COLUMNS)].to_numpy(dtype=np.float64)
        y_te = sub_te.risk_final.to_numpy(dtype=np.float64)
        lrp_te = lrp_array(cdm, eid_te, t_cut)

        block = _lmo_eval_split(X_tr, y_tr, lrp_tr, eid_tr, folds_tr, X_te, y_te, lrp_te)
        row = {
            "mission_id": int(mid),
            "status": "ok",
            "n_test": n_test,
            "n_hr_test": n_hr_test,
            **block,
        }
        if cp is not None:
            _atomic_write_json(cp, row)
        rows.append(row)

    eval_rows = [r for r in rows if r.get("status") == "ok"]
    summary = {}
    if eval_rows:
        for key in ("lrp", "gbdt", "linear"):
            l_vals = [r["metrics"][key]["L_unclipped"] for r in eval_rows]
            l_fin = [x for x in l_vals if np.isfinite(x)]
            f2s = [r["metrics"][key]["F2"] for r in eval_rows if "F2" in r["metrics"][key]]
            summary[key] = {
                "L_unclipped_mean": float(np.mean(l_fin)) if l_fin else None,
                "L_unclipped_mean_n": len(l_fin),
                "F2_mean": float(np.mean(f2s)) if f2s else None,
            }

    return {
        "kind": "lmo",
        "t_cut": t_cut,
        "primary_metric": "L_unclipped",
        "n_missions_total": int(missions.nunique()),
        "n_missions_evaluated": len(eval_rows),
        "n_missions_skipped": len(rows) - len(eval_rows),
        "folds": rows,
        "summary": summary,
    }


def plot_leadtime(path: Path, lead: dict[str, Any]) -> None:
    import matplotlib.pyplot as plt

    pts = lead["points"]
    xs = [p["t_cut"] for p in pts]
    fig, ax = plt.subplots(figsize=(6, 4))
    for name, style in (("lrp", "o-"), ("gbdt", "s-"), ("linear", "^-")):
        ys = [p["L_unclipped"][name] for p in pts]
        ax.plot(xs, ys, style, label=name)
    for p in pts:
        ax.annotate(
            f"n={p['n_events']}, HR={p['n_hr']}",
            (p["t_cut"], p["L_unclipped"]["lrp"]),
            fontsize=7,
            xytext=(4, 4),
            textcoords="offset points",
        )
    ax.set_xlabel("t_cut (days before TCA)")
    ax.set_ylabel("L (unclipped)")
    ax.set_title("S9 lead-time skill (pj-057)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def _slim_leadtime(lead: dict[str, Any]) -> dict[str, Any]:
    if not lead.get("points"):
        return lead
    points = [{k: v for k, v in p.items() if k != "detail"} for p in lead["points"]]
    return {**lead, "points": points}


def write_leadtime(out_dir: Path, lead: dict[str, Any]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "s9_leadtime.json").write_text(
        json.dumps(_slim_leadtime(lead), indent=2, default=_json_default) + "\n"
    )
    if lead.get("points"):
        plot_leadtime(out_dir / "s9_leadtime.png", lead)


def write_lmo(out_dir: Path, lmo: dict[str, Any]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "s9_lmo.json").write_text(json.dumps(lmo, indent=2, default=_json_default) + "\n")


def write_results(out_dir: Path, lead: dict[str, Any], lmo: dict[str, Any]) -> None:
    if lead.get("points") or lead.get("kind") == "leadtime":
        write_leadtime(out_dir, lead)
    write_lmo(out_dir, lmo)


def leadtime_complete(lead: dict[str, Any] | None) -> bool:
    return bool(lead and lead.get("kind") == "leadtime" and len(lead.get("points", [])) == len(LEAD_TIME_CUTS))


def lmo_complete(lmo: dict[str, Any] | None) -> bool:
    return bool(lmo and lmo.get("kind") == "lmo" and lmo.get("n_missions_total"))


def _json_default(x: Any) -> Any:
    if isinstance(x, (np.floating, np.integer)):
        return float(x) if isinstance(x, np.floating) else int(x)
    if isinstance(x, np.ndarray):
        return x.tolist()
    raise TypeError(type(x))
