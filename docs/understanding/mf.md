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

## S10: kernel ridge (RBF) — 2026-11-15

Verdict: READY. Tiny numeric examples (two points (1,2), (2,3), lambda = 5, then 0.01 and 1000). All sources outside-notes: Bishop PRML ch.6 and ESL ch.5/12, from memory, unverified; the notes PDF could not be opened (poppler missing), so syllabus chapters 5 and 6 are cited by name only.

| Concept | Role | Status | Source | Evidence |
|---------|------|--------|--------|----------|
| Ridge primal: closed form, effect of lambda | prerequisite | solid | notes ch.5; outside-notes: ESL 3.4 | Derived w = 8/(5+lambda) unaided, computed 1.6 (lambda 0) and 0.8 (lambda 5); lambda large gives w near 0 and a near-constant prediction (first said "predicts nothing"); with unpenalized intercept it predicts the training mean (chose B) |
| Dual form: w = sum alpha_i x_i, alpha_i = residual_i / lambda | core | solid | notes 6.2; outside-notes: Bishop PRML 6.1 | Computed alpha = (0.24, 0.28) and checked w = 0.8 |
| Kernel as similarity, Gram matrix K, alpha = (K + lambda I)^-1 y | core | solid | notes 6.3 | Computed f(3) with linear and RBF kernels; used K = I to get f(x_i) = y_i/(1+lambda) for lambda 5 and 0.01 |
| RBF kernel and gamma | core | solid | outside-notes: Bishop PRML 6.2 | Question 6c wrong (said small gamma memorizes); after teaching, answered correctly that large gamma with small lambda memorizes (7c, 11c) |
| lambda and gamma as bias-variance control (over/under-fit) | core | solid | notes ch.5 | Question 10b wrong (called small gamma over-fit); after teaching, classified train/validation error pairs correctly and mapped them to (gamma 100, lambda 0.01) and gamma 0.0001 |
| Scaling before distances, scaler on train only | hazard | solid | S4 addendum KNN (2026-11-12) | Not re-examined; carried from the KNN record, same distance-based regime |
| Memorizing model and the alarm line fitted on training predictions | hazard | solid | S4 mf-012 | Question 8 wrong (said B); 8b partly wrong. After teaching: with held-out predictions (4-event example) chose t = -6.8 and saw the alarm fire at r_hat = -6.5 (Q12a, b); first described the held-out events as validation data, then correctly said they come from the outer training fold and that using the outer validation fold would be leakage (Q13) |
| Cost: K is n x n, solve is O(n^3) | hazard | solid | outside-notes: ESL ch.12 | 7100^2 = 50.4 M entries, x4 and x8 when n doubles |
| Nested selection of two hyperparameters (grid x inner folds) | hazard | solid | outside-notes: ESL 7.10 | Question 10a wrong (175 combinations, forgot inner folds); after teaching 3 x 2 x 5 = 30 |

Not examined, carried to the ADR as open questions: kernel family (linear, polynomial, Laplacian) beyond RBF; sklearn `gamma` parametrization (exp(-gamma d^2) as used here); `KernelRidge` has no `fit_intercept` (checked in sklearn 1.9.1: parameters are alpha, kernel, gamma, degree, coef0, kernel_params), so centering y and the intercept must be decided; self-weight on the training diagonal for the alarm line (analogue of the KNN self-neighbour, mf-043).
