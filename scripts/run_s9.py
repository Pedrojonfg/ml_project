"""S9: lead-time curve + leave-mission-out (pj-053..060)."""
# ponytail: one-shot CLI; full train — long on kelvins train

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.protocol import build_event_table, make_folds  # noqa: E402
from src.s9 import (  # noqa: E402
    leadtime_complete,
    lmo_complete,
    run_leadtime_curve,
    run_lmo,
    write_leadtime,
    write_lmo,
)

DATA = ROOT / "data/esa/Collision Avoidance Challenge - Dataset/kelvins_competition_data"
OUT = ROOT / "results"
LEAD_PATH = OUT / "s9_leadtime.json"
LMO_PATH = OUT / "s9_lmo.json"


def _load(path: Path) -> dict | None:
    if not path.is_file():
        return None
    return json.loads(path.read_text())


def main() -> None:
    args = sys.argv[1:]
    only = set(args) if args else set()
    resume = "resume" in only or (
        not only and (LEAD_PATH.is_file() or LMO_PATH.is_file())
    )
    only.discard("resume")

    cdm = pd.read_csv(DATA / "train_data.csv")
    table = build_event_table(cdm)
    folds = make_folds(table)

    lead: dict = {"skipped": True}
    lmo: dict = {"skipped": True}

    do_lead = not only or "leadtime" in only
    do_lmo = not only or "lmo" in only

    if do_lead:
        cached = _load(LEAD_PATH) if resume else None
        if leadtime_complete(cached):
            print(f"lead-time: reuse {LEAD_PATH}")
            lead = cached  # type: ignore[assignment]
        else:
            print("S9 lead-time curve (cuts 2,3,4) …", flush=True)
            lead = run_leadtime_curve(cdm, table, folds)
            write_leadtime(OUT, lead)
            print("lead-time written", flush=True)

    if do_lmo:
        cached = _load(LMO_PATH) if resume else None
        if lmo_complete(cached):
            print(f"LMO: reuse {LMO_PATH}")
            lmo = cached  # type: ignore[assignment]
        else:
            print("S9 leave-mission-out …", flush=True)
            lmo = run_lmo(cdm, table, t_cut=2.0)
            write_lmo(OUT, lmo)
            print("LMO written", flush=True)

    print(json.dumps({
        "leadtime": [{"t_cut": p["t_cut"], "L_unclipped": p["L_unclipped"]} for p in lead.get("points", [])],
        "lmo_summary": lmo.get("summary"),
        "lmo_skipped": lmo.get("n_missions_skipped"),
    }, indent=2))


if __name__ == "__main__":
    main()