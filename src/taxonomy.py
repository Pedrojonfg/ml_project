"""S2 jump taxonomy (mf-001..mf-005): labels from risk_final vs lrp, plus lead time."""

import numpy as np
import pandas as pd

from src.metrics import HR_THRESHOLD_LOG10
from src.protocol import TTC_MIN

JUMP_CUT = 1.0  # per mf-003


def label_events(event_table: pd.DataFrame, cdm: pd.DataFrame, cut: float = JUMP_CUT) -> pd.DataFrame:
    """Label each event by delta = risk_final - lrp, HR crossing, and lead time of the last usable CDM."""
    risk = event_table.risk_final.to_numpy(dtype="float64")
    lrp = event_table.lrp.to_numpy(dtype="float64")
    delta = risk - lrp
    hr = HR_THRESHOLD_LOG10
    jump_class = np.select(
        [delta >= cut, delta <= -cut, risk >= hr],  # per mf-003, mf-004
        ["jump-up", "jump-down", "stable-high"],
        default="stable-low",
    )
    hr_crossing = np.select(
        [(lrp < hr) & (hr <= risk), (lrp >= hr) & (hr > risk)],  # per mf-002
        ["up", "down"],
        default="none",
    )
    usable = cdm[cdm.time_to_tca >= TTC_MIN]  # per mf-005
    lead = usable.groupby("event_id").time_to_tca.min()
    return pd.DataFrame({
        "event_id": event_table.event_id.to_numpy(),
        "delta": delta,
        "jump_class": jump_class,
        "hr_crossing": hr_crossing,
        "lead_time": event_table.event_id.map(lead).to_numpy(dtype="float64"),  # per mf-005
    })
