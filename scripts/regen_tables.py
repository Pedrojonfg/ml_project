"""Regenerate markdown tables/figures from existing results/ (no retrain)."""
# per pj-080: regen entrypoint; replays artifacts, does not refit models

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
OFFICIAL = RESULTS / "official"


def _s4() -> None:
    subprocess.check_call([sys.executable, str(ROOT / "scripts" / "make_s4_table.py")], cwd=ROOT)


def _official_table() -> None:
    # per pj-085: separate official-test table (not mixed with OOF)
    if not OFFICIAL.exists():
        print("skip official table: results/official/ missing")
        return
    rows = []
    for path in sorted(OFFICIAL.glob("*.json")):
        if path.name == "summary.json":
            continue
        d = json.loads(path.read_text())
        m = d.get("metrics") or {}
        if "F2" not in m:
            continue
        rows.append((
            d.get("model", path.stem),
            f"{m['F2']:.3f}",
            f"{m.get('MSE_HR_clipped', float('nan')):.3f}",
            f"{m.get('L_clipped', float('nan')):.3f}",
        ))
    if not rows:
        print("skip official table: no model metrics yet")
        return
    head = ["Model", "F2", "MSE_HR clipped", "L clipped"]
    md = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    md += ["| " + " | ".join(r) + " |" for r in rows]
    out = "\n".join(md) + "\n"
    (RESULTS / "official_table.md").write_text(out)
    print(out)


def main() -> None:
    _s4()
    _official_table()
    print("regen done (tables from results/; figures already in results/)")


if __name__ == "__main__":
    main()
