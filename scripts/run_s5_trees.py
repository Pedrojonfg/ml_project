"""S5: RF + GBDT repeated CV, importances, diagnostics (pj-014..020, pj-026)."""
# ponytail: one-shot CLI; bootstrap per pj-006 deferred to evaluation.py

import json
import multiprocessing as mp
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.features import FEATURE_COLUMNS, build_features  # noqa: E402
from src.models.trees import (  # noqa: E402
    floor_c_diagnostics,
    importance_diagnostics,
    INNER_SPLITS,
    N_ESTIMATORS_GRID,
    W_GRID,
    run_nested_tree_cv,
)
from src.protocol import build_event_table, make_folds  # noqa: E402

DATA = ROOT / "data/esa/Collision Avoidance Challenge - Dataset/kelvins_competition_data"
RESULTS = ROOT / "results"
PRED = ROOT / "preds"
CACHE = ROOT / "data/cache_iter2"  # per-repetition checkpoints (idempotent restart)
WORKERS = int(sys.argv[1]) if len(sys.argv) > 1 else 5
_JOB = {}


def _one_rep(args):
    kind, r = args
    X, y, lrp, eid, folds = (_JOB[k] for k in ("X", "y", "lrp", "eid", "folds"))
    run_nested_tree_cv(kind, X, y, lrp, eid, folds[folds.rep == r], cache_dir=CACHE / kind)


def _run(kind, X, y, lrp, eid, folds):
    # per pj-073: fill the per-rep cache in parallel (fork shares the data), then aggregate from cache
    (CACHE / kind).mkdir(parents=True, exist_ok=True)
    _JOB.update(X=X, y=y, lrp=lrp, eid=eid, folds=folds)
    with mp.get_context("fork").Pool(WORKERS) as pool:
        pool.map(_one_rep, [(kind, int(r)) for r in sorted(folds.rep.unique())], chunksize=1)
    return run_nested_tree_cv(kind, X, y, lrp, eid, folds, cache_dir=CACHE / kind)


def _plot_importance(imp: np.ndarray, path: Path, title: str) -> None:
    order = np.argsort(imp)[::-1]
    names = [FEATURE_COLUMNS[i] for i in order]
    vals = imp[order]
    k = 10
    while k < min(15, len(vals)) and vals[k] >= 0.95 * vals[9]:
        k += 1
    names, vals = names[:k], vals[:k]
    fig, ax = plt.subplots(figsize=(7, max(3, 0.35 * len(names))))
    ax.barh(names[::-1], vals[::-1])
    ax.set_title(title)
    ax.set_xlabel("mean impurity importance (25 fits)")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    cdm = pd.read_csv(DATA / "train_data.csv")
    table = build_event_table(cdm)
    folds = make_folds(table)
    feats = build_features(table, cdm)
    merged = feats.merge(table[["event_id", "risk_final", "lrp"]], on="event_id")
    X = merged[list(FEATURE_COLUMNS)].to_numpy(dtype=np.float64)
    y = merged.risk_final.to_numpy(dtype=np.float64)
    lrp = merged.lrp.to_numpy(dtype=np.float64)
    eid = merged.event_id.to_numpy(dtype=np.int64)

    RESULTS.mkdir(parents=True, exist_ok=True)
    PRED.mkdir(parents=True, exist_ok=True)

    rf_res = _run("rf", X, y, lrp, eid, folds)
    gbdt_res = _run("gbdt", X, y, lrp, eid, folds)
    rf_n, rf_w = rf_res.floors[0]["n_estimators"], rf_res.floors[0]["w"]  # rep 0, fold 0 choice for B1
    gbdt_n, gbdt_w = gbdt_res.floors[0]["n_estimators"], gbdt_res.floors[0]["w"]

    diag = importance_diagnostics(
        rf_res.importances, gbdt_res.importances, X, y, folds, rf_n, gbdt_n, lrp=lrp,
        rf_w=rf_w, gbdt_w=gbdt_w,
    )
    floor_diag = {
        "rf": {**floor_c_diagnostics(y, rf_res, folds), "floors": rf_res.floors},
        "gbdt": {**floor_c_diagnostics(y, gbdt_res, folds), "floors": gbdt_res.floors},
    }
    (RESULTS / "floor_c_diagnostics.json").write_text(json.dumps(floor_diag, indent=2) + "\n")
    imp_table = pd.DataFrame({
        "feature": list(FEATURE_COLUMNS),
        "rf_mean": rf_res.importances,
        "gbdt_mean": gbdt_res.importances,
    }).sort_values("rf_mean", ascending=False)
    imp_table.to_csv(RESULTS / "importance_means.csv", index=False)

    _plot_importance(rf_res.importances, RESULTS / "importance_rf.png", "RF (nested n_estimators, w)")
    _plot_importance(
        gbdt_res.importances, RESULTS / "importance_gbdt.png", "GBDT (nested n_estimators, w)",
    )

    extra = {"n_estimators_grid": list(N_ESTIMATORS_GRID), "w_grid": list(W_GRID), "inner_splits": INNER_SPLITS}
    for slug, res in (("rf", rf_res), ("gbdt", gbdt_res)):
        out = {"model": slug, "metrics": res.metrics, "metrics_per_rep": res.metrics_per_rep,
               "fold_records": res.floors, **extra}  # chosen w, n_estimators, c and inner L per fold (pj-073)
        (RESULTS / f"{slug}.json").write_text(json.dumps(out, indent=2, default=float) + "\n")
        pd.concat(res.fold_frames, ignore_index=True).to_parquet(PRED / f"{slug}.parquet", index=False)

    (RESULTS / "importance_diagnostics.json").write_text(json.dumps(diag, indent=2) + "\n")
    print(json.dumps({
        "rf_n_estimators": rf_n,
        "gbdt_n_estimators": gbdt_n,
        "reopen_required": diag["reopen_required"],
        "reopen_floor_c_rf": floor_diag["rf"]["reopen_required"],
        "reopen_floor_c_gbdt": floor_diag["gbdt"]["reopen_required"],
    }, indent=2))


if __name__ == "__main__":
    main()
