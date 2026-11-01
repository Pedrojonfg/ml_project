"""S2 EDA: events per mission, class imbalance, jump-class shares at cuts 0.5/1/2."""
# ponytail: one-shot CLI; no lead-time / latest_risk histograms (bins deferred, mf-005/mf-006)

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.eda.figures import CLASSES, plot_imbalance, plot_missions  # noqa: E402
from src.protocol import build_event_table  # noqa: E402
from src.taxonomy import JUMP_CUT, label_events  # noqa: E402

DATA = ROOT / "data/esa/Collision Avoidance Challenge - Dataset/kelvins_competition_data"
OUT = ROOT / "results/eda"
CUTS = (0.5, 1.0, 2.0)  # per mf-003 "Expected behavior and validation"


def main() -> None:
    cdm = pd.read_csv(DATA / "train_data.csv", usecols=["event_id", "time_to_tca", "mission_id", "risk"])
    table = build_event_table(cdm)
    OUT.mkdir(parents=True, exist_ok=True)

    # mission per event = first mission_id of the event's CDMs
    missions = cdm.groupby("event_id", as_index=False).mission_id.first()
    missions = missions[missions.event_id.isin(table.event_id)]
    plot_missions(missions, OUT / "missions.png")

    rows = []
    for cut in CUTS:
        labels = label_events(table, cdm, cut=cut)  # per mf-003
        counts = labels.jump_class.value_counts()
        for c in CLASSES:
            rows.append({"cut": cut, "jump_class": c, "n": int(counts.get(c, 0)),
                         "share": counts.get(c, 0) / len(labels)})
        if cut == JUMP_CUT:  # registered cut, per mf-003
            plot_imbalance(labels, table, OUT / "imbalance.png")
    shares = pd.DataFrame(rows)
    shares.to_csv(OUT / "jump_class_shares.csv", index=False)
    print(shares.to_string(index=False))
    print(table.y_hr.value_counts().to_string())


if __name__ == "__main__":
    main()
