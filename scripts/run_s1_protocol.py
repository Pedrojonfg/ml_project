"""S1: build event table + folds, score LRP/CRP on the filtered events (point estimates)."""
# ponytail: one-shot CLI; no bootstrap here (pj-006 lives in src/evaluation.py, S4)

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.metrics import crp_predictions, f2_score, kelvins_l, mse_hr  # noqa: E402
from src.protocol import build_event_table, make_folds  # noqa: E402

DATA = ROOT / "data/esa/Collision Avoidance Challenge - Dataset/kelvins_competition_data"
PROCESSED = ROOT / "data/processed"
RESULTS = ROOT / "results"
TEST_LRP_L = 0.694  # Uriot et al. 2020, official test (reference only)


def score(y: np.ndarray, pred: np.ndarray) -> dict:
    f2 = f2_score(y, pred)
    out = {"F2": f2}
    for name, clip in (("clipped", -6.001), ("unclipped", None)):  # per pj-007
        m = mse_hr(y, pred, clip_at=clip)
        out[f"MSE_HR_{name}"] = m
        out[f"L_{name}"] = kelvins_l(m, f2)
    return {k: round(float(v), 6) for k, v in out.items()}


def main() -> None:
    cdm = pd.read_csv(DATA / "train_data.csv", usecols=["event_id", "time_to_tca", "risk"])
    table = build_event_table(cdm)
    folds = make_folds(table)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(exist_ok=True)
    table.to_csv(PROCESSED / "event_table.csv", index=False)
    folds.to_csv(PROCESSED / "folds.csv", index=False)

    y = table.risk_final.to_numpy()
    subsets = {"all": np.ones(len(table), bool), "last_ttc<1 (X only)": (table.last_ttc < 1).to_numpy()}
    res = {
        "n_events": len(table),
        "n_hr": int(table.y_hr.sum()),
        "reference_test_LRP_L": TEST_LRP_L,
        "baselines": {},
    }
    for sub, m in subsets.items():
        res["baselines"][sub] = {
            "n_events": int(m.sum()),
            "n_hr": int(table.y_hr[m].sum()),
            "LRP": score(y[m], table.lrp.to_numpy()[m]),
            "CRP": score(y[m], crp_predictions(int(m.sum()))),
        }
    hr = folds.merge(table[["event_id", "y_hr"]], on="event_id").groupby(["rep", "fold"]).y_hr.sum()
    res["hr_per_fold_min_max"] = [int(hr.min()), int(hr.max())]
    (RESULTS / "s1_baselines.json").write_text(json.dumps(res, indent=2) + "\n")
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
