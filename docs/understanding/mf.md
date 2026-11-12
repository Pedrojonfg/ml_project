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
| KNN (superseded 2026-11-12: examined below) | core if included | see KNN rows | outside-notes: ESL ch.13 | Mario reopened KNN on 2026-11-12 (mf-043 on merge; only the KNN part of this record was done) |

### S4 addendum: KNN — 2026-11-12

Verdict: READY for the KNN decisions. The rest of the S4 record stays skipped. 5-point examples with small numbers; all sources are outside-notes (ESL ch.13 and Murphy PML ch.5, from memory, unverified; no notes page opened).

| Concept | Role | Status | Source | Evidence |
|---------|------|--------|--------|----------|
| KNN prediction: K nearest neighbours, vote | core | solid | outside-notes: ESL ch.13 | Found the 3 nearest of 5 points for x=3.4 (C, D, B); predicted HR for K=3 and K=1 |
| Choice of K (variance vs bias) | core | solid | outside-notes: ESL ch.13 | x=7: K=1 no HR, K=3 HR; K=5 (all points) predicts the majority class for any x |
| Class imbalance and the vote threshold | hazard | solid | outside-notes: Murphy PML ch.5 | Majority vote with K=5 needs 3 HR neighbours (answered 3); said "at least 1 of 5" raises alarms. Needed a question first about whether lowering the threshold "touches the results"; accepted that it is a decision rule fixed on training data, not on test (cf. mf-012, mf-013) |
| Feature scaling for distance | hazard | solid | outside-notes: ESL ch.13 | Chose Q (unscaled) then P (after dividing by std): the large-unit feature dominates raw distance |
| Scaler fit on train only inside each fold | hazard | solid | outside-notes: ESL 7.10 | Answered "training data only" |

Not examined for KNN: distance metric choice, curse of dimensionality with the S3 feature count, regression variant (average of neighbours' risk_final), ties. Carry to the KNN ADR as open questions.

## S6: calibrated two-stage (calibration, Platt, isotonic, stage combination) — 2026-11-04

Verdict: READY

| Concept | Role | Status | Source | Evidence |
|---------|------|--------|--------|----------|
| Calibrated probability = observed frequency; calibration vs discrimination | prerequisite | solid | outside-notes: Niculescu-Mizil & Caruana 2005 (from memory, unverified) | Expected n*p HR (4 of 5); judged 0.8 vs 2/5 as overestimate; stated a constant 0.5 model is calibrated but useless for ranking |
| Bernoulli likelihood, log-likelihood, cross-entropy | prerequisite | solid | notes ch.3 (not opened; no PDF tooling) | Confused independence with exclusivity and dropped 1-p for y=0 until corrected; then derived y log p + (1-y) log(1-p) unaided and its y=1 / y=0 cases |
| Reliability diagram (bins, diagonal, over/under side) | core | solid | outside-notes: Niculescu-Mizil & Caruana 2005 | Computed bin coordinates; first read points above the diagonal as overestimate, then placed (0.9, 0.6) below the diagonal as overestimate; knew the diagram shows calibration, not discrimination |
| Platt scaling, p = sigma(a*s + b), monotone for a>0 | core | solid | outside-notes: Platt 1999 (from memory, unverified); notes ch.3 for sigmoid | Computed p for given a, b, s; needed the monotonicity argument taught; with a<0 saw the order reverse and stated a must be positive |
| Isotonic regression (pool adjacent violators, ties) | core | solid | outside-notes: Zadrozny & Elkan 2002 (from memory, unverified) | First attempt pooled a non-violating pair; second attempt pooled blocks with original labels correctly ([0,1/3,1/3,1/3,1]); stated tied events cannot be ranked |
| Combining stages: E[r] = p*m_HR + (1-p)*m_low | core | solid | outside-notes: law of total expectation (Murphy PML) | Wrote the formula unaided; computed -7.4 and -6.5 for a miscalibrated p; the error scaling (p_hat - p)*(m_HR - m_low) was supplied by the AI |
| Calibrating on the data the model trained on, and with few HR | hazard | solid | outside-notes: Niculescu-Mizil & Caruana 2005 (unverified) | After teaching: saw memorized training scores give p=1.0 vs 0.6 on new events (overestimate); explained that few events per step make estimates unstable via 1/3 vs 1/30 shift and 6 vs 600 events. Earlier rated shaky: first answers computed the shifts wrongly and called the estimate with the higher value "more reliable" |
| Stage-2 regressor trained on HR events only (selection effect) | hazard | solid | outside-notes: selection bias (ESL ch.7 context) | Predicted the output for a true risk of -9 lands above -9 because training risks were all >= -6; extrapolation behavior of the chosen model family not examined |

Notes: calibration is not in the course notes by the index (not grepped; poppler/pypdf missing, notes pages not opened). All external references are from memory and unverified. Open for Stage 2: calibration method (Platt vs isotonic vs other), data used to calibrate, how the two stages combine (the formula above is one option, not chosen), what the stage-2 regressor is trained on, number of bins for the reliability diagram, calibration metrics (not examined).
