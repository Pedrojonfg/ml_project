"""S9: lead-time curve + leave-mission-out (pj-053..060, pj-077, pj-078)."""
# ponytail: fine-grained cache under data/cache_s9 — safe to kill and resume

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.protocol import build_event_table, make_folds  # noqa: E402
from src.s9 import run_leadtime_curve, run_lmo, write_leadtime, write_lmo  # noqa: E402

DATA = ROOT / "data/esa/Collision Avoidance Challenge - Dataset/kelvins_competition_data"
OUT = ROOT / "results"
CACHE = ROOT / "data/cache_s9"
BAKEOFF = OUT / "gbdt.json"


def main() -> None:
    args = set(sys.argv[1:])
    do_lead = not args or "leadtime" in args
    do_lmo = not args or "lmo" in args

    cdm = pd.read_csv(DATA / "train_data.csv")
    table = build_event_table(cdm)
    folds = make_folds(table)

    lead: dict = {"skipped": True}
    lmo: dict = {"skipped": True}

    if do_lead:
        print("S9 lead-time (cache=%s, bakeoff=%s) …" % (CACHE / "leadtime", BAKEOFF), flush=True)
        lead = run_leadtime_curve(
            cdm, table, folds,
            cache_dir=CACHE / "leadtime",
            bakeoff_gbdt_path=BAKEOFF,
        )
        write_leadtime(OUT, lead)
        print("lead-time written", flush=True)

    if do_lmo:
        print("S9 LMO (cache=%s) …" % (CACHE / "lmo"), flush=True)
        lmo = run_lmo(cdm, table, t_cut=2.0, cache_dir=CACHE / "lmo")
        write_lmo(OUT, lmo)
        print("LMO written", flush=True)

    print(json.dumps({
        "leadtime": [
            {"t_cut": p["t_cut"], "L_unclipped": p["L_unclipped"]}
            for p in lead.get("points", [])
        ],
        "lmo_summary": lmo.get("summary"),
        "lmo_skipped": lmo.get("n_missions_skipped"),
    }, indent=2))


if __name__ == "__main__":
    main()
