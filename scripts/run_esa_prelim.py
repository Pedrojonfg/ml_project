"""Reproduce proposal prelim: CRP/LRP on Zenodo test + 3 figures + JSON."""
# ponytail: one-shot CLI; paths fixed to repo layout

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.metrics import (  # noqa: E402
    HR_THRESHOLD_LOG10,
    crp_predictions,
    f2_score,
    kelvins_l,
    lrp_from_cdms,
    mse_hr,
)

DATA = ROOT / "data/esa/Collision Avoidance Challenge - Dataset/kelvins_competition_data"
FIG = ROOT / "presentations/proposal/figures"
OUT = ROOT / "presentations/proposal"


def main() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    test = pd.read_csv(DATA / "test_data.csv", usecols=["event_id", "time_to_tca", "risk"])
    priv = pd.read_csv(DATA / "test_data_private.csv", usecols=["event_id", "true_risk"])
    train = pd.read_csv(DATA / "train_data.csv", usecols=["event_id", "time_to_tca", "risk"])

    y_true_df = priv.sort_values("event_id")
    event_ids = y_true_df["event_id"].to_numpy()
    y_true = y_true_df["true_risk"].to_numpy(dtype=np.float64)
    lrp_map = lrp_from_cdms(
        {
            "event_id": test["event_id"].to_numpy(),
            "time_to_tca": test["time_to_tca"].to_numpy(dtype=np.float64),
            "risk": test["risk"].to_numpy(dtype=np.float64),
        }
    )
    y_lrp = np.array([lrp_map[int(e)] for e in event_ids], dtype=np.float64)
    y_crp = crp_predictions(len(y_true))

    def pack(name: str, y_pred: np.ndarray) -> dict:
        f2 = f2_score(y_true, y_pred)
        m = mse_hr(y_true, y_pred)
        return {
            "name": name,
            "F2": round(float(f2), 6),
            "MSE_HR": round(float(m), 6),
            "L": round(float(kelvins_l(m, f2)), 6),
            "n_events": int(len(y_true)),
            "n_hr": int(np.sum(y_true >= HR_THRESHOLD_LOG10)),
        }

    crp, lrp = pack("CRP", y_crp), pack("LRP", y_lrp)

    idx = train.groupby("event_id")["time_to_tca"].idxmin()
    train_final = train.loc[idx, "risk"].to_numpy()

    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    bins = np.linspace(-30.5, 0.5, 62)
    ax.hist(train_final, bins=bins, alpha=0.65, label=f"train finals (n={len(train_final)})", color="#5dade2", density=True)
    ax.hist(y_true, bins=bins, alpha=0.65, label=f"test finals (n={len(y_true)})", color="#e74c3c", density=True)
    ax.axvline(-6.0, color="black", ls="--", lw=1.2, label="HR threshold (log10 = −6)")
    ax.set_xlabel("final risk (log$_{10}$)")
    ax.set_ylabel("density")
    ax.set_title("Class imbalance: most events end far below high-risk")
    ax.legend(fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(FIG / "fig_risk_distribution.pdf", bbox_inches="tight")
    fig.savefig(FIG / "fig_risk_distribution.png", dpi=160, bbox_inches="tight")
    plt.close(fig)

    # schematic timeline is separate static asset; regenerate if missing
    timeline = FIG / "fig_cdm_timeline.pdf"
    if not timeline.exists():
        raise SystemExit("missing fig_cdm_timeline.pdf — regenerate schematic first")

    fig, ax = plt.subplots(figsize=(5.8, 3.2))
    x = np.arange(3)
    w = 0.35
    crp_vals = [crp["L"], crp["MSE_HR"], crp["F2"]]
    lrp_vals = [lrp["L"], lrp["MSE_HR"], lrp["F2"]]
    ax.bar(x - w / 2, crp_vals, w, label="CRP", color="#85929e")
    ax.bar(x + w / 2, lrp_vals, w, label="LRP", color="#1a5276")
    ax.axhline(0.694, color="#c0392b", ls=":", lw=1.2, label=r"paper LRP $L\approx0.694$")
    ax.set_xticks(x)
    ax.set_xticklabels(["$L$ (↓)", "MSE$_{HR}$ (↓)", "$F_2$ (↑)"])
    ax.set_title("Official test baselines (Zenodo; risk clipped at −6.001 for MSE)")
    for i, (a, b) in enumerate(zip(crp_vals, lrp_vals)):
        ax.text(i - w / 2, a, f"{a:.3f}", ha="center", va="bottom", fontsize=7)
        ax.text(i + w / 2, b, f"{b:.3f}", ha="center", va="bottom", fontsize=7)
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "fig_baseline_metrics.pdf", bbox_inches="tight")
    fig.savefig(FIG / "fig_baseline_metrics.png", dpi=160, bbox_inches="tight")
    plt.close(fig)

    results = {
        "protocol": "official Zenodo test; LRP=min ttc among ttc>=2; y=true_risk private; MSE_HR clips at -6.001",
        "doi": "10.5281/zenodo.4463683",
        "counts": {
            "train_events": int(train.event_id.nunique()),
            "train_cdms": int(len(train)),
            "test_events": int(len(y_true)),
            "test_cdms_public": int(len(test)),
            "test_hr": int(np.sum(y_true >= -6)),
            "test_hr_rate": float(np.mean(y_true >= -6)),
            "train_hr_rate_approx": float(np.mean(train_final >= -6)),
        },
        "baselines": {"CRP": crp, "LRP": lrp},
        "paper_lrp_reference": {"L": 0.694, "MSE_HR": 0.513, "F2": 0.739},
        "figures": [
            "figures/fig_risk_distribution.pdf",
            "figures/fig_cdm_timeline.pdf",
            "figures/fig_baseline_metrics.pdf",
        ],
    }
    (OUT / "prelim_results.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results["baselines"], indent=2))


if __name__ == "__main__":
    main()
