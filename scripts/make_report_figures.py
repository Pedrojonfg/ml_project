"""Clean, column-width versions of two figures for the Final Report.

Reads results/s6_calibration.json and results/s9_leadtime.json (no retraining).
Writes report/figures/fig_reliability.pdf and report/figures/fig_leadtime.pdf.
"""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "report" / "figures"
plt.rcParams.update({"font.size": 9, "axes.grid": True, "grid.alpha": 0.25})

# --- reliability: three calibrated stage-1 classifiers on one panel
cal = json.loads((ROOT / "results" / "s6_calibration.json").read_text())
names = {"lr_none": "unpenalised", "lr_l2": "L2", "lr_l1": "L1"}
fig, ax = plt.subplots(figsize=(3.3, 2.9))
ax.plot([0, 0.105], [0, 0.105], color="grey", lw=1, label="perfect")
for k, lab in names.items():
    ax.plot(cal[k]["mean_p"], cal[k]["observed_hr"], marker="o", ms=3.5, lw=1,
            label=f"{lab} (Brier {cal[k]['brier']:.4f})")
ax.set_xlabel("mean calibrated probability (decile bin)")
ax.set_ylabel("observed HR fraction")
ax.legend(fontsize=7, loc="upper left")
fig.tight_layout()
fig.savefig(OUT / "fig_reliability.pdf")
plt.close(fig)

# --- lead time: unclipped L on a log axis
lt = json.loads((ROOT / "results" / "s9_leadtime.json").read_text())["points"]
cuts = [p["t_cut"] for p in lt]
fig, ax = plt.subplots(figsize=(3.3, 2.7))
for key, lab, mk in [("lrp", "LRP", "o"), ("gbdt", "Gradient boosting", "s"),
                     ("linear", "Best linear model", "^")]:
    ax.plot(cuts, [p["L_unclipped"][key] for p in lt], marker=mk, lw=1.2, label=lab)
ax.set_yscale("log")
ax.set_xticks(cuts)
ax.set_xlabel("earliest usable CDM ($t_{cut}$, days before TCA)")
ax.set_ylabel("unclipped $L$ (log scale)")
for p in lt:
    ax.annotate(f"{p['n_hr']} HR", (p["t_cut"], p["L_unclipped"]["gbdt"]),
                textcoords="offset points", xytext=(0, -11), ha="center", fontsize=7)
ax.legend(fontsize=7, loc="center right")
fig.tight_layout()
fig.savefig(OUT / "fig_leadtime.pdf")
plt.close(fig)
