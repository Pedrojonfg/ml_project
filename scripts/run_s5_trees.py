"""S5: RF + GBDT repeated CV, importances, diagnostics (pj-014..020)."""
# ponytail: one-shot CLI; bootstrap per pj-006 deferred to evaluation.py

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.features import FEATURE_COLUMNS, build_features  # noqa: E402
from src.models.trees import (  # noqa: E402
    importance_diagnostics,
    make_gbdt,
    make_rf,
    run_oof_cv,
    select_rf_n_estimators,
)
from src.protocol import build_event_table, make_folds  # noqa: E402

DATA = ROOT / "data/esa/Collision Avoidance Challenge - Dataset/kelvins_competition_data"
RESULTS = ROOT / "results"
PRED = ROOT / "preds"


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
    merged = feats.merge(table[["event_id", "risk_final"]], on="event_id")
    X = merged[list(FEATURE_COLUMNS)].to_numpy(dtype=np.float64)
    y = merged.risk_final.to_numpy(dtype=np.float64)
    eid = merged.event_id.to_numpy(dtype=np.int64)

    RESULTS.mkdir(parents=True, exist_ok=True)
    PRED.mkdir(parents=True, exist_ok=True)

    rf_n = select_rf_n_estimators(X, y, eid, folds)
    rf_res = run_oof_cv(lambda rs: make_rf(rf_n, rs), X, y, eid, folds)
    gbdt_res = run_oof_cv(make_gbdt, X, y, eid, folds)

    diag = importance_diagnostics(rf_res.importances, gbdt_res.importances, X, y, folds, rf_n)
    imp_table = pd.DataFrame({
        "feature": list(FEATURE_COLUMNS),
        "rf_mean": rf_res.importances,
        "gbdt_mean": gbdt_res.importances,
    }).sort_values("rf_mean", ascending=False)
    imp_table.to_csv(RESULTS / "importance_means.csv", index=False)

    _plot_importance(rf_res.importances, RESULTS / "importance_rf.png", f"RF (n_estimators={rf_n})")
    _plot_importance(gbdt_res.importances, RESULTS / "importance_gbdt.png", "GBDT")

    for slug, res, extra in (
        ("rf", rf_res, {"n_estimators": rf_n, "n_estimators_grid": list((100, 300, 500))}),
        ("gbdt", gbdt_res, {"n_estimators": 200, "learning_rate": 0.1}),
    ):
        out = {"model": slug, "metrics": res.metrics, **extra}
        (RESULTS / f"{slug}.json").write_text(json.dumps(out, indent=2) + "\n")
        pd.concat(res.fold_frames, ignore_index=True).to_parquet(PRED / f"{slug}.parquet", index=False)

    (RESULTS / "importance_diagnostics.json").write_text(json.dumps(diag, indent=2) + "\n")
    print(json.dumps({"rf_n_estimators": rf_n, "reopen_required": diag["reopen_required"]}, indent=2))


if __name__ == "__main__":
    main()
