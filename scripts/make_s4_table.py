"""S4 table: OLS/ridge/lasso vs LRP, from results/*.json (no recomputation)."""

import json
from pathlib import Path

R = Path(__file__).resolve().parents[1] / "results"


def f(est, ci, d=3):
    return f"{est:.{d}f}" if ci is None else f"{est:.{d}f} [{ci[0]:.{d}f}, {ci[1]:.{d}f}]"


lrp = json.load(open(R / "s1_baselines.json"))["baselines"]["all"]["LRP"]
rows = [("LRP (baseline)", f"{lrp['F2']:.3f}", "-", f"{lrp['MSE_HR_clipped']:.3f}", f"{lrp['L_clipped']:.3f}", "-")]
for m in [m for m in ["ols", "ridge", "lasso", "knn"] if (R / f"{m}.json").exists()]:
    b = json.load(open(R / f"{m}.json"))["bootstrap"]
    F, M, L = b["F2"], b["MSE_HR_clipped"], b["L_clipped"]
    rows.append((
        m,
        f(F["estimate"], F["ci"]),
        f(F["paired_vs_LRP"]["estimate"], F["paired_vs_LRP"]["ci"]),
        f(M["estimate"], M["ci"]),
        f(L["estimate"], L["ci"]),
        f(L["paired_vs_LRP"]["estimate"], L["paired_vs_LRP"]["ci"]),
    ))
head = ["Model", "F2 (95% CI)", "F2 - LRP", "MSE_HR clipped", "L clipped", "L - LRP"]
md = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
md += ["| " + " | ".join(r) + " |" for r in rows]
out = "\n".join(md) + "\n"
(R / "s4_table.md").write_text(out)
print(out)
