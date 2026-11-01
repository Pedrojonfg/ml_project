# Understanding record — Mario (mf)

## S2: jump definition (stable-low/stable-high/jump-up/jump-down) — 2026-10-31

Verdict: READY

| Concept | Role | Status | Source | Evidence |
|---------|------|--------|--------|----------|
| `risk` = log10(Pc), HR threshold -6 | prerequisite | solid | outside-notes: Uriot et al. 2020 (not in repo, unverified) | After teaching: computed 10^2 = 100x between -4 and -6 and 10^1.4 ≈ 25.1x for Δ=1.4; initially shaky (could not say why a tiny probability counts as high) |
| Event vs CDM; `event_table` one row per event | prerequisite | solid | docs/plan-reparto.md; ADR 018 | Gave 500 rows for 10 000 CDMs from 500 events |
| Threshold rule on Δ = y_final - latest_risk; sensitivity to cut | core | solid | outside-notes (ties to logistic regression, notes ch.3) | Labeled 3 events correctly at cuts 0.5/1/2; stated direction of change in jump count; asked on his own whether up/down cuts must be symmetric |
| Class imbalance and metrics (accuracy vs recall/precision) | core | solid | outside-notes (not in notes index) | Computed recall/precision/accuracy for a 10-of-1000 case after one arithmetic slip; explained why 99% accuracy misleads |
| Regression to the mean | core | solid | outside-notes: Stigler 1997 (from memory, unverified) | Predicted negative mean Δ for very high latest_risk and positive for very low, with reason; initially misapplied the numeric example |
| Leakage (feature availability at t0), target-dependent splits, stratification | hazard | solid | outside-notes: ESL ch.7, Kaufman et al. 2012 (unverified) | Classified 5 columns by availability at t0; reasoned that all-large-Δ validation biases metrics; justified stratifying by y_hr with 10 HR events / 5 folds. Initially stated the wrong rule (independence from target) and called Δ in validation split "not leakage" |
| Variable lead time of the last valid CDM | hazard | solid | docs/plan-reparto.md (S9) | Argued equal Δ is more surprising with less time; named time_to_tca of last valid CDM as the data to check |

Notes: all concepts rated outside-notes; course-notes.pdf pages could not be opened (poppler missing), so no notes page citations. Several external references are from memory and unverified. Open design questions surfaced for Stage 2: symmetric vs asymmetric cuts; jump by Δ only vs also by HR crossing (event B: crosses -6 with Δ=0.2, labeled stable-high); lead-time dependence of Δ.
