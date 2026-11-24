"""S8: tabular MLP + masked GRU repeated CV vs LRP (pj-061..pj-070)."""
# ponytail: one-shot CLI, same layout as run_s4_linear.py / run_s5_trees.py

import argparse
import json
import multiprocessing as mp
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.evaluation import bootstrap_report  # noqa: E402
from src.features import FEATURE_COLUMNS, build_features  # noqa: E402
from src.models import neural as nn_s8  # noqa: E402
from src.models import trees  # noqa: E402
from src.models.trees import floor_c_diagnostics, p_hr_from_r_hat  # noqa: E402
from src.protocol import build_event_table, make_folds  # noqa: E402

DATA = ROOT / "data/esa/Collision Avoidance Challenge - Dataset/kelvins_competition_data"
RESULTS = ROOT / "results"
PRED = ROOT / "preds"
CACHE = ROOT / "data/cache_iter2"  # per-repetition checkpoints (idempotent restart)
_JOB = {}


def _one_rep(args):
    slug, r, cache = args
    j = _JOB
    nn_s8.run_neural_cv(slug, j["inputs"][slug](), j["y"], j["lrp"], j["eid"],
                        j["folds"][j["folds"].rep == r], cache_dir=cache)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*", default=["mlp", "gru"])
    ap.add_argument("--workers", type=int, default=5)
    ap.add_argument("--max-epochs", type=int, default=100)  # pj-074; 200 only if the GRU trigger fires
    args = ap.parse_args()
    names = args.names
    nn_s8.MAX_EPOCHS = args.max_epochs
    torch.set_num_threads(1)
    cdm = pd.read_csv(DATA / "train_data.csv")
    table = build_event_table(cdm)
    folds = make_folds(table)
    feats = build_features(table, cdm)
    merged = feats.merge(table[["event_id", "risk_final", "lrp"]], on="event_id")
    y = merged.risk_final.to_numpy(dtype=np.float64)
    lrp = merged.lrp.to_numpy(dtype=np.float64)
    eid = merged.event_id.to_numpy(dtype=np.int64)
    inputs = {
        "mlp": lambda: (merged[list(FEATURE_COLUMNS)].to_numpy(dtype=np.float64),),
        "gru": lambda: nn_s8.build_sequences(eid, cdm),
    }

    RESULTS.mkdir(parents=True, exist_ok=True)
    PRED.mkdir(parents=True, exist_ok=True)
    _JOB.update(inputs=inputs, y=y, lrp=lrp, eid=eid, folds=folds)
    for slug in names:
        t0 = time.time()
        suffix = "" if args.max_epochs == 100 else f"_e{args.max_epochs}"
        cache = CACHE / f"{slug}{suffix}"
        cache.mkdir(parents=True, exist_ok=True)
        # per pj-073: fill the per-rep cache in parallel (fork shares the data), then aggregate from cache
        with mp.get_context("fork").Pool(args.workers) as pool:
            pool.map(_one_rep, [(slug, int(r), cache) for r in sorted(folds.rep.unique())], chunksize=1)
        res = nn_s8.run_neural_cv(slug, inputs[slug](), y, lrp, eid, folds, cache_dir=cache)
        best_epochs = [f["best_epoch"] for f in res.floors]
        p_hr = np.stack([p_hr_from_r_hat(r) for r in res.oof_pred])
        out = {
            "model": slug,
            "metrics": res.metrics,
            "metrics_per_rep": res.metrics_per_rep,
            "fold_records": res.floors,  # floor c (pj-068) + early-stopping epoch per fold and repetition
            "floor_c_diagnostics": floor_c_diagnostics(y, res, folds),  # pj-068: same R0-R4 record as S5
            "hyperparameters": {
                "mlp_hidden": list(nn_s8.MLP_HIDDEN), "gru_hidden": nn_s8.GRU_HIDDEN,
                "gru_layers": nn_s8.GRU_LAYERS, "T": nn_s8.T_MAX, "seq_channels": list(nn_s8.SEQ_CHANNELS),
                "lr": nn_s8.LR, "betas": list(nn_s8.BETAS), "eps": nn_s8.EPS, "weight_decay": nn_s8.WEIGHT_DECAY,
                "batch_size": nn_s8.BATCH_SIZE, "max_epochs": nn_s8.MAX_EPOCHS, "patience": nn_s8.PATIENCE,
                "inner_val_frac": nn_s8.INNER_VAL_FRAC, "w_grid": list(trees.W_GRID),
                "inner_splits": trees.INNER_SPLITS, "loss": "weighted_mean", "monitor": "weighted_mse",
            },
            "median_best_epoch": float(np.median(best_epochs)),  # pj-074 trigger: > 90 on gru -> cap 200
            "trigger_200": bool(slug == "gru" and np.median(best_epochs) > 90),
            "bootstrap": bootstrap_report(y, lrp, res.oof_pred, p_hr),  # per pj-006, pj-070
            "seconds": round(time.time() - t0, 1),
        }
        (RESULTS / f"{slug}{suffix}.json").write_text(json.dumps(out, indent=2, default=float) + "\n")
        pd.concat(res.fold_frames, ignore_index=True).to_parquet(PRED / f"{slug}{suffix}.parquet", index=False)
        print(slug, out["seconds"], "s", json.dumps(res.metrics))


if __name__ == "__main__":
    main()
