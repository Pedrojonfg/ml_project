"""S6: calibrated two-stage (logistic + Platt, stored S4 regressors) vs LRP, CRP and S4 (mf-021..mf-041)."""
# ponytail: one-shot CLI. Stage 1 is slow, so it runs one repetition at a time (its 5 folds in parallel
# worker processes) and each repetition is checkpointed in data/s6_cache/ (gitignored): a rerun skips what
# is done. Each classifier is then saved (results/s6_stage1_<clf>.json + preds/s6_stage1_<clf>.parquet) and
# the report is assembled once the three exist.
# Usage: python scripts/run_s6_two_stage.py [lr_none lr_l2 lr_l1] [--jobs N] [--report-only] [--boot-b B]

import argparse
import json
import pickle
import sys
import time
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.evaluation import BOOT_B, bootstrap_compare  # noqa: E402
from src.features import FEATURE_COLUMNS, build_features  # noqa: E402
from src.metrics import HR_THRESHOLD_LOG10  # noqa: E402
from src.models.linear import _rep_metrics  # noqa: E402
from src.models.two_stage import CLASSIFIERS, reliability_diagram, run_stage1_cv  # noqa: E402
from src.protocol import build_event_table, make_folds  # noqa: E402

DATA = ROOT / "data/esa/Collision Avoidance Challenge - Dataset/kelvins_competition_data"
CACHE = ROOT / "data/s6_cache"
RESULTS = ROOT / "results"
PRED = ROOT / "preds"
REGRESSORS = ("ols", "ridge", "lasso")  # per mf-023


def _wide(frame: pd.DataFrame, col: str, eid: np.ndarray) -> np.ndarray:
    """(n_reps, n_events) matrix of `col`, columns in `eid` order."""
    return np.vstack([
        frame[frame.rep == k].set_index("event_id").loc[eid, col].to_numpy(dtype=np.float64)
        for k in sorted(frame.rep.unique())
    ])


def stage1(clf, X, y, eid, folds, jobs):
    """Stage 1 of one classifier, one repetition at a time, each one checkpointed."""
    CACHE.mkdir(parents=True, exist_ok=True)
    parts = []
    for rep in sorted(folds.rep.unique()):
        f = CACHE / f"{clf}_rep{rep}.pkl"
        if f.exists():
            print(clf, "rep", rep, "from checkpoint", flush=True)
        else:
            t0 = time.time()
            res = run_stage1_cv(clf, X, y, eid, folds[folds.rep == rep], n_jobs=jobs)
            f.write_bytes(pickle.dumps(res))
            print(clf, "rep", rep, round(time.time() - t0, 1), "s", flush=True)
        parts.append(pickle.loads(f.read_bytes()))
    per_rep = [b for p in parts for b in p.brier_per_rep]
    return {
        "brier_per_rep": per_rep, "brier": float(np.mean(per_rep)),
        "fold_records": [r for p in parts for r in p.fold_records],
        "fold_frames": [fr for p in parts for fr in p.fold_frames],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("classifiers", nargs="*", default=list(CLASSIFIERS))
    ap.add_argument("--jobs", type=int, default=5)  # processes for the folds of one repetition
    ap.add_argument("--report-only", action="store_true")  # skip stage 1, assemble from saved files
    ap.add_argument("--boot-b", type=int, default=BOOT_B)  # registered value (pj-006); lower only for smoke tests
    args = ap.parse_args()

    cdm = pd.read_csv(DATA / "train_data.csv")
    table = build_event_table(cdm)
    folds = make_folds(table)
    feats = build_features(table, cdm)
    merged = feats.merge(table[["event_id", "risk_final", "lrp"]], on="event_id")
    X = merged[list(FEATURE_COLUMNS)].to_numpy(dtype=np.float64)
    y = merged.risk_final.to_numpy(dtype=np.float64)
    lrp = merged.lrp.to_numpy(dtype=np.float64)
    eid = merged.event_id.to_numpy(dtype=np.int64)
    y_hr = y >= HR_THRESHOLD_LOG10

    RESULTS.mkdir(parents=True, exist_ok=True)
    PRED.mkdir(parents=True, exist_ok=True)
    for clf in [] if args.report_only else args.classifiers:
        t0 = time.time()
        res = stage1(clf, X, y, eid, folds, args.jobs)
        (RESULTS / f"s6_stage1_{clf}.json").write_text(json.dumps({
            "classifier": clf, "brier": res["brier"], "brier_per_rep": res["brier_per_rep"],
            "fold_records": res["fold_records"],  # C, C*, SE, tie size, edge flag, a, b, t, convergence flags
            "seconds": round(time.time() - t0, 1),
        }, indent=2, default=float) + "\n")
        pd.concat(res["fold_frames"], ignore_index=True).to_parquet(PRED / f"s6_stage1_{clf}.parquet", index=False)
        print(clf, round(time.time() - t0, 1), "s, Brier", res["brier"], flush=True)

    stage1_files = {c: PRED / f"s6_stage1_{c}.parquet" for c in CLASSIFIERS}
    if not all(p.exists() for p in stage1_files.values()):
        print("stage 1 incomplete; report not assembled")
        return

    # Rows: 9 S6 rows (classifier x S4 regressor, mf-024) and the 3 stored S4 rows (mf-034).
    s4 = {r: pd.read_parquet(PRED / f"{r}.parquet") for r in REGRESSORS}
    rows = {f"s4_{r}": (_wide(s4[r], "r_hat", eid), _wide(s4[r], "p_hr", eid)) for r in REGRESSORS}
    s1 = {c: pd.read_parquet(p) for c, p in stage1_files.items()}
    for c in CLASSIFIERS:
        alarm = _wide(s1[c], "alarm", eid)
        for r in REGRESSORS:
            rows[f"{c}__{r}"] = (rows[f"s4_{r}"][0], alarm)  # r_hat of stage 2 as it is, per mf-035

    # Pairs (mf-037): each S6 row vs its S4 regressor, plus the 18 pairs that change one stage only.
    pairs = [(f"{c}__{r}", f"s4_{r}") for c in CLASSIFIERS for r in REGRESSORS]
    pairs += [(f"{a}__{r}", f"{b}__{r}") for r in REGRESSORS for a, b in combinations(CLASSIFIERS, 2)]
    pairs += [(f"{c}__{a}", f"{c}__{b}") for c in CLASSIFIERS for a, b in combinations(REGRESSORS, 2)]
    t0 = time.time()
    cmp = bootstrap_compare(y, lrp, rows, pairs, B=args.boot_b)  # per mf-037: same bootstrap as S4
    print("bootstrap", round(time.time() - t0, 1), "s", flush=True)

    for c in CLASSIFIERS:
        info = json.loads((RESULTS / f"s6_stage1_{c}.json").read_text())
        for r in REGRESSORS:
            name = f"{c}__{r}"
            r_hat, alarm = rows[name]
            per_rep = [_rep_metrics(y, r_hat[i], alarm[i]) for i in range(len(r_hat))]
            out = {
                "model": name, "classifier": c, "regressor": r,
                "metrics": {k: float(np.mean([m[k] for m in per_rep])) for k in per_rep[0]},
                "metrics_per_rep": per_rep,
                "fold_records": info["fold_records"],
                "bootstrap": cmp["rows"][name],
                "paired": {k: v for k, v in cmp["pairs"].items() if name in k.split("|")},
            }
            (RESULTS / f"s6_{name}.json").write_text(json.dumps(out, indent=2, default=float) + "\n")
            frame = s1[c].rename(columns={"alarm": "p_hr"}).merge(
                s4[r][["event_id", "rep", "r_hat"]], on=["event_id", "rep"])  # contract: event_id, fold, p_hr, r_hat
            frame.to_parquet(PRED / f"s6_{name}.parquet", index=False)

    # Calibration (mf-036): Brier per classifier and the diagram, per repetition then averaged bin by bin.
    cal = {}
    for c in CLASSIFIERS:
        p = _wide(s1[c], "p_cal", eid)
        bins = [reliability_diagram(p[i], y_hr, k=10) for i in range(len(p))]
        cal[c] = {
            "brier": json.loads((RESULTS / f"s6_stage1_{c}.json").read_text())["brier"],
            "mean_p": np.mean([b[0] for b in bins], axis=0).tolist(),
            "observed_hr": np.mean([b[1] for b in bins], axis=0).tolist(),
        }
    cal["brier_constant_hr_rate"] = float(y_hr.mean() * (1 - y_hr.mean()))  # reference of mf-036
    (RESULTS / "s6_calibration.json").write_text(json.dumps(cal, indent=2) + "\n")
    (RESULTS / "s6_comparisons.json").write_text(json.dumps(cmp["pairs"], indent=2, default=float) + "\n")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharex=True, sharey=True)
    hi = max(max(cal[c]["mean_p"] + cal[c]["observed_hr"]) for c in CLASSIFIERS)
    for ax, c in zip(axes, CLASSIFIERS):
        ax.plot([0, hi], [0, hi], color="grey", lw=1)  # perfect calibration
        ax.plot(cal[c]["mean_p"], cal[c]["observed_hr"], "o-")
        ax.set_title(f"{c} (Brier {cal[c]['brier']:.5f})")
        ax.set_xlabel("mean predicted p")
    axes[0].set_ylabel("observed HR fraction")
    fig.tight_layout()
    fig.savefig(RESULTS / "s6_reliability.png", dpi=150)


if __name__ == "__main__":
    main()
