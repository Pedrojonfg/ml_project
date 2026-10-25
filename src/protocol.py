"""S1 event protocol: event table (pj-001..003) and repeated stratified folds (pj-004, pj-005)."""

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold

from src.metrics import HR_THRESHOLD_LOG10

SEEDS = (42, 43, 44, 45, 46)  # per pj-005
N_SPLITS = 5  # per pj-004
TTC_MIN = 2  # days; usable CDMs have time_to_tca >= 2 (per pj-002, pj-003)


def build_event_table(cdm: pd.DataFrame) -> pd.DataFrame:
    d = cdm[["event_id", "time_to_tca", "risk"]].astype(
        {"event_id": "int64", "time_to_tca": "float64", "risk": "float64"}
    )
    d = d.sort_values(["event_id", "time_to_tca"], ignore_index=True)
    # per event: first row = min time_to_tca (last CDM before TCA), first row of usable CDMs = LRP
    last = d.groupby("event_id").head(1).set_index("event_id")
    usable = d[d.time_to_tca >= TTC_MIN].groupby("event_id").head(1).set_index("event_id")
    g = d.groupby("event_id")
    t = pd.DataFrame({
        "risk_final": last.risk,  # pj-001, unclipped
        "lrp": usable.risk,  # pj-001 / pj-003: latest CDM with ttc >= 2
        "first_ttc": g.time_to_tca.max(),
        "last_ttc": g.time_to_tca.min(),
        "n_cdm": g.size().astype("int64"),
    })
    # keep rule (pj-002, pj-003): >= 1 usable CDM and last CDM ttc < 2
    t = t[t.lrp.notna() & (t.last_ttc < TTC_MIN)].reset_index()
    t["y_hr"] = t.risk_final >= HR_THRESHOLD_LOG10  # pj-001
    return t[["event_id", "risk_final", "y_hr", "lrp", "first_ttc", "last_ttc", "n_cdm"]].astype(
        {"event_id": "int64", "risk_final": "float64", "y_hr": "bool", "lrp": "float64",
         "first_ttc": "float64", "last_ttc": "float64", "n_cdm": "int64"}
    )


def make_folds(event_table: pd.DataFrame, seeds=SEEDS, n_splits=N_SPLITS) -> pd.DataFrame:
    t = event_table[["event_id", "y_hr"]].sort_values("event_id", ignore_index=True)
    parts = []
    for rep, seed in enumerate(seeds):
        skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)  # per pj-004, pj-005
        fold = np.empty(len(t), dtype="int64")
        for k, (_, test) in enumerate(skf.split(t, t.y_hr)):
            fold[test] = k
        parts.append(pd.DataFrame({
            "event_id": t.event_id.to_numpy(), "rep": rep, "seed": seed, "fold": fold,
        }))
    return pd.concat(parts, ignore_index=True).astype("int64")
