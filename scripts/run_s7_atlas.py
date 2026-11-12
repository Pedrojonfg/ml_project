"""S7 failure atlas: select C1–C8/O1–O3 cases, record empty pools, plot CDM timelines."""
# ponytail: one-shot CLI; selection logic lives in src/atlas/selection.py

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.atlas.selection import ORDER, S4, S6_SLUGS, select_atlas_slots  # noqa: E402
from src.atlas.t_raw import (  # noqa: E402
    compute_t_raw_by_clf,
    t_raw_from_jsonable,
    t_raw_to_jsonable,
)
from src.features import FEATURE_COLUMNS, build_features  # noqa: E402
from src.protocol import TTC_MIN, build_event_table, make_folds  # noqa: E402
from src.taxonomy import label_events  # noqa: E402

DATA = ROOT / "data/esa/Collision Avoidance Challenge - Dataset/kelvins_competition_data"
RESULTS = ROOT / "results"
PRED = ROOT / "preds"
FIG = RESULTS / "atlas"


def _range_risk(cdm: pd.DataFrame, event_ids: np.ndarray) -> pd.Series:
    usable = cdm[cdm.time_to_tca >= TTC_MIN]
    g = usable.groupby("event_id")["risk"]
    rr = g.max() - g.min()
    return rr.reindex(event_ids).astype("float64")


def _load_preds() -> dict[str, pd.DataFrame]:
    slugs = ["rf", "gbdt", *S4, *S6_SLUGS]
    out = {}
    for s in slugs:
        out[s] = pd.read_parquet(PRED / f"{s}.parquet")
    return out


def _load_or_compute_t_raw(X, y, eid, folds, n_jobs: int, force: bool) -> dict:
    cache = RESULTS / "atlas_t_raw.json"
    if cache.exists() and not force:
        return t_raw_from_jsonable(json.loads(cache.read_text())["rows"])
    t_raw = compute_t_raw_by_clf(X, y, eid, folds, RESULTS, n_jobs=n_jobs)
    cache.write_text(json.dumps({"rows": t_raw_to_jsonable(t_raw)}, indent=2) + "\n")
    return t_raw


def _caption(slot: str, asg: dict, table: pd.DataFrame, labels: pd.DataFrame) -> str:
    eid = asg.get("event_id")
    if eid is None:
        return f"{slot}: empty pool (pj-052)."
    row = table.set_index("event_id").loc[int(eid)]
    lab = labels.set_index("event_id").loc[int(eid)]
    return (
        f"{slot}: event_id={eid}, k={asg.get('k')}/5, "
        f"risk_final={float(row.risk_final):.4f}, y_hr={bool(row.y_hr)}, "
        f"lrp={float(row.lrp):.4f}, jump={lab.jump_class}, delta={float(lab.delta):.4f}"
    )


def _plot_event(eid: int, cdm: pd.DataFrame, title: str, path: Path) -> None:
    sub = cdm[cdm.event_id == eid].sort_values("time_to_tca", ascending=False)
    fig, ax = plt.subplots(figsize=(6, 3.2))
    ax.plot(sub.time_to_tca, sub.risk, marker="o", ms=3, lw=1)
    ax.axhline(-6.0, color="0.4", ls="--", lw=0.8)
    ax.set_xlabel("time_to_tca (days)")
    ax.set_ylabel("risk (log10)")
    ax.set_title(title)
    ax.invert_xaxis()
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--force-t-raw", action="store_true")
    ap.add_argument("--skip-t-raw", action="store_true", help="leave O2 empty (no t_raw)")
    args = ap.parse_args()

    cdm = pd.read_csv(DATA / "train_data.csv")
    table = build_event_table(cdm)
    folds = make_folds(table)
    labels = label_events(table, cdm)
    feats = build_features(table, cdm)
    merged = feats.merge(table[["event_id", "risk_final"]], on="event_id")
    X = merged[list(FEATURE_COLUMNS)].to_numpy(dtype=np.float64)
    y = merged.risk_final.to_numpy(dtype=np.float64)
    eid = merged.event_id.to_numpy(dtype=np.int64)
    rr = _range_risk(cdm, eid)

    RESULTS.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)

    preds = _load_preds()
    if args.skip_t_raw:
        t_raw = None
    else:
        t_raw = _load_or_compute_t_raw(X, y, eid, folds, args.jobs, args.force_t_raw)

    result = select_atlas_slots(table, labels, preds, range_risk=rr, t_raw_by_clf=t_raw)
    captions = {s: _caption(s, result["assignments"][s], table, labels) for s in ORDER}

    payload = {
        "order": result["order"],
        "empty": result["empty"],
        "assignments": {
            s: {
                "event_id": a["event_id"],
                "k": a["k"],
                "caption": captions[s],
                "meta": a.get("meta") or {},
            }
            for s, a in result["assignments"].items()
        },
    }
    (RESULTS / "atlas_selection.json").write_text(json.dumps(payload, indent=2) + "\n")
    (RESULTS / "atlas_empty.json").write_text(
        json.dumps({"empty": result["empty"], "policy": "pj-052"}, indent=2) + "\n"
    )
    (RESULTS / "atlas_captions.md").write_text(
        "\n".join(f"- {captions[s]}" for s in ORDER) + "\n"
    )

    for slot in ORDER:
        asg = result["assignments"][slot]
        eid_s = asg.get("event_id")
        if eid_s is None:
            continue
        _plot_event(int(eid_s), cdm, captions[slot], FIG / f"{slot}.png")

    print(json.dumps({"empty": result["empty"], "assignments": {
        s: result["assignments"][s]["event_id"] for s in ORDER
    }}, indent=2))


if __name__ == "__main__":
    main()
