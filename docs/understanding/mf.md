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

## S4: syllabus models vs LRP (logistic, ridge, lasso, bootstrap) — 2026-11-01

Verdict: skipped by Mario (2026-11-01). Mario stated he had covered logistic, lasso and ridge in class; KNN deferred out of this pass.

| Concept | Role | Status | Source | Evidence |
|---------|------|--------|--------|----------|
| Gaussian noise => MSE (MLE) | prerequisite | shaky | notes ch.2 (not opened; no PDF tooling) | Derived log-likelihood structure after teaching; computed per-point weights 1/(2 sigma_i^2) correctly; initially claimed plain MSE still maximizes likelihood under heteroscedastic noise |
| Bernoulli likelihood / cross-entropy | prerequisite | shaky | notes ch.3 (not opened) | Wrote log L = sum[y log p + (1-y) log(1-p)] after a hint on log rules; first attempt omitted the log; numeric comparison (p=0.9 vs 0.01) not answered |
| Logistic regression, ridge, lasso, regularization / bias-variance | core | not examined | notes ch.2, 3, 5; outside-notes: ESL 3.4 (lasso) | Skipped |
| Feature scaling for L1/L2, scaler fit on train only, nested CV for lambda/C | hazard | not examined | outside-notes: ESL 3.4, 7.10 | Skipped |
| Class imbalance in logistic loss, decision threshold vs F2 | hazard/core | not examined | outside-notes: Murphy PML ch.5 | Skipped (imbalance metrics were solid in S2 record, different regime) |
| Bootstrap over events | core | not examined | outside-notes: ESL 7.11 | Skipped |
| KNN | core if included | deferred | outside-notes: ESL ch.13 | Out of this pass by Mario |
