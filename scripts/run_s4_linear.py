"""S4: OLS, ridge, lasso repeated nested CV vs LRP (mf-008..mf-015)."""
# ponytail: one-shot CLI; bootstrap per pj-006, mf-016..mf-019 (src/evaluation.py)

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.evaluation import bootstrap_report  # noqa: E402
from src.features import FEATURE_COLUMNS, build_features  # noqa: E402
from src.models.linear import INNER_SEED, INNER_SPLITS, LASSO_ALPHAS, RIDGE_ALPHAS, run_linear_cv  # noqa: E402
from src.protocol import build_event_table, make_folds  # noqa: E402

DATA = ROOT / "data/esa/Collision Avoidance Challenge - Dataset/kelvins_competition_data"
RESULTS = ROOT / "results"
PRED = ROOT / "preds"


def main() -> None:
    names = sys.argv[1:] or ["ols", "ridge", "lasso"]
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
    for slug in names:
        t0 = time.time()
        res = run_linear_cv(slug, X, y, eid, folds)
        out = {
            "model": slug,
            "metrics": res.metrics,
            "metrics_per_rep": res.metrics_per_rep,
            "fold_records": res.fold_records,  # alpha and alarm line t per fold and repetition, per mf-012, mf-013
            "alpha_grid": (list(RIDGE_ALPHAS) if slug == "ridge" else list(LASSO_ALPHAS) if slug == "lasso" else None),
            "inner_seed": INNER_SEED,
            "inner_splits": INNER_SPLITS,
            "bootstrap": bootstrap_report(y, lrp, res.oof_r_hat, res.oof_p_hr),  # per pj-006, mf-016..mf-019
            "seconds": round(time.time() - t0, 1),
        }
        (RESULTS / f"{slug}.json").write_text(json.dumps(out, indent=2, default=float) + "\n")
        pd.concat(res.fold_frames, ignore_index=True).to_parquet(PRED / f"{slug}.parquet", index=False)
        print(slug, out["seconds"], "s", json.dumps(res.metrics))


if __name__ == "__main__":
    main()
