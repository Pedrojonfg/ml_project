"""S3 event features (pj-009..pj-013): build X from usable CDMs and event_table metadata."""

import numpy as np
import pandas as pd

from src.protocol import TTC_MIN

SNAPSHOT_QUANTILES = (25, 50, 75)  # per pj-009
SNAPSHOT_VARS = ("risk", "miss_distance", "relative_speed", "t_weighted_rms")
OBJECT_TYPES = ("DEBRIS", "UNKNOWN", "PAYLOAD", "ROCKET BODY", "TBA")  # per pj-011
EVENT_META = ("n_cdm", "first_ttc", "last_ttc")  # per pj-009
RISK_AGG_COLS = (
    "n_usable_cdms",
    "ttc_span_usable",
    "risk_agg_min",
    "risk_agg_max",
    "risk_agg_range",
    "risk_agg_mean",
    "risk_agg_std",
)


def _snapshot_column_names() -> list[str]:
    cols = []
    for var in SNAPSHOT_VARS:
        cols.extend(
            [
                f"{var}_snap_first",
                f"{var}_snap_last",
                f"{var}_snap_p25",
                f"{var}_snap_p50",
                f"{var}_snap_p75",
            ]
        )
    return cols


def _object_type_column_names() -> list[str]:
    return [f"obj_{t.replace(' ', '_')}" for t in OBJECT_TYPES]


FEATURE_COLUMNS: tuple[str, ...] = tuple(
    _snapshot_column_names() + list(RISK_AGG_COLS) + list(EVENT_META) + _object_type_column_names()
)

_CDM_USECOLS = (
    "event_id",
    "time_to_tca",
    "risk",
    "miss_distance",
    "relative_speed",
    "t_weighted_rms",
    "c_object_type",
)


def _snapshots_for_usable(usable: pd.DataFrame) -> dict[str, float]:
    """First = farthest TCA (max ttc); last = closest usable (min ttc). per pj-009."""
    out: dict[str, float] = {}
    ttc = usable["time_to_tca"].to_numpy(dtype="float64")
    n = len(ttc)
    for var in SNAPSHOT_VARS:
        y = usable[var].to_numpy(dtype="float64")
        if n == 1:
            v = float(y[0])
            out[f"{var}_snap_first"] = v
            out[f"{var}_snap_last"] = v
            out[f"{var}_snap_p25"] = v
            out[f"{var}_snap_p50"] = v
            out[f"{var}_snap_p75"] = v
            continue
        order = np.argsort(ttc)
        ttc_s, y_s = ttc[order], y[order]
        out[f"{var}_snap_last"] = float(y_s[0])
        out[f"{var}_snap_first"] = float(y_s[-1])
        for q in SNAPSHOT_QUANTILES:
            t_q = float(np.percentile(ttc, q))
            out[f"{var}_snap_p{q}"] = float(np.interp(t_q, ttc_s, y_s))
    return out


def _risk_aggregates(usable: pd.DataFrame) -> dict[str, float]:
    risk = usable["risk"].to_numpy(dtype="float64")
    n = len(risk)
    ttc = usable["time_to_tca"].to_numpy(dtype="float64")
    std = 0.0 if n == 1 else float(np.std(risk, ddof=1))  # per pj-010
    return {
        "n_usable_cdms": float(n),
        "ttc_span_usable": float(ttc.max() - ttc.min()) if n else np.nan,
        "risk_agg_min": float(risk.min()),
        "risk_agg_max": float(risk.max()),
        "risk_agg_range": float(risk.max() - risk.min()),
        "risk_agg_mean": float(risk.mean()),
        "risk_agg_std": std,
    }


def _object_type_dummies(last_type: str) -> dict[str, float]:
    d = {f"obj_{t.replace(' ', '_')}": 0.0 for t in OBJECT_TYPES}
    if last_type in OBJECT_TYPES:
        d[f"obj_{last_type.replace(' ', '_')}"] = 1.0
    return d


def _features_one_event(usable: pd.DataFrame) -> dict[str, float]:
    usable = usable.sort_values("time_to_tca", ascending=True)
    row = {**_snapshots_for_usable(usable), **_risk_aggregates(usable)}
    last = usable.iloc[0]  # min time_to_tca among usable (per pj-011)
    row.update(_object_type_dummies(str(last["c_object_type"])))
    return row


def build_features(event_table: pd.DataFrame, cdm: pd.DataFrame) -> pd.DataFrame:
    """One row per event_id in event_table; columns match FEATURE_COLUMNS."""
    ids = event_table["event_id"].to_numpy()
    cdm = cdm.loc[cdm["event_id"].isin(ids), list(_CDM_USECOLS)].copy()
    usable = cdm[cdm["time_to_tca"] >= TTC_MIN]

    feats = usable.groupby("event_id", sort=False).apply(
        _features_one_event, include_groups=False
    )
    if isinstance(feats, pd.Series):
        feat_df = pd.DataFrame(feats.tolist(), index=feats.index)
    else:
        feat_df = feats

    meta = event_table.set_index("event_id")[list(EVENT_META)]
    out = meta.join(feat_df, how="left").reset_index()
    out = out[["event_id"] + list(FEATURE_COLUMNS)]
    return out.astype({c: "float64" for c in FEATURE_COLUMNS} | {"event_id": "int64"})
