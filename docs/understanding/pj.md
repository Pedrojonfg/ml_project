# Understanding record — Pedro (PJ)

## S1 event protocol — 2026-10-24

Verdict: READY.

| Concept | Type | Status | Source | Notes |
|---|---|---|---|---|
| Group dependence / leakage across CDMs of one event | hazard | solid | ESL §7.10 | Predicted ~0 error for 1-NN under plain K-fold vs nonzero under GroupKFold; tied to test being unseen events |
| Temporal truncation / target leakage (inputs >= 2 d) | hazard | solid | Uriot et al. 2020 | The 0.5 d CDM carries the label and is unavailable at prediction time |
| F2 (precision, recall, beta) | core | solid | scripts/esa_kelvins_metrics.py | Mis-computed recall once (denominator must be true HR); later correct |
| Composition of L = MSE_HR / F2 | core | solid | same script | MSE_HR is computed only on true HR events; applied to CRP |
| Standard error of a mean, 1/sqrt(n) | core | solid | ESL §7.10 | SE=0.2 and n=400 to halve it |
| Train/test distribution shift, validity of model comparison | hazard | solid | covariate shift literature | Mission-mix example; ranking may or may not transfer |
| LRP / CRP baselines | core | solid | prelim_results.json | CRP = all-HR trivial model; `risk` is already log10 |
| Bias of K-fold CV vs K | core | solid | ESL §7.10.1 | Pessimistic bias for small K; bias vs variance reasoning mixed up once; miscounted HR per fold once |

Mistakes made (useful for the oral): recall denominator (true HR events), counting HR per fold (1/K, not (K-1)/K), believing `risk` was on a linear scale.

## S3 event features — 2026-10-27

Verdict: **READY**.

| Concept | Role | Status | Source | Evidence |
|---------|------|--------|--------|----------|
| Temporal rule (inputs only ttc ≥ 2 d) | prerequisite | solid | S1 / pj-002, pj-003 | Q1; Q4 |
| Target vs inputs (`risk_final`, `y_hr` vs `lrp`) | core | solid | pj-001, protocol | Retry: `lrp` in X; target = risk at min `time_to_tca` |
| CDM column examples for X | core | shaky | Kelvins CSV | Retry named location/temperature (not in schema); knows `lrp`; real fields e.g. `miss_distance`, `relative_position_*` exist in data |
| Deltas on usable CDMs (no leakage) | core | solid | pj-003 | Misread `risk_last` as y; confirmed delta between usable CDMs is not leakage |
| Leakage via global scaler before CV | hazard | shaky | outside-notes: ESL §7.10 | Named leakage; taught val-fold stats in scaler fit |
| Feature contract stub vs v1 | core | solid | plan-reparto §6 | Retry: stub few cols for Mario; v1 full engineering from CSV |

## S5 trees vs LRP — 2026-10-27

Verdict: **READY**.

| Concept | Role | Status | Source | Evidence |
|---------|------|--------|--------|----------|
| Continuous `risk_final` → F₂ / MSE_HR / L (same as LRP) | prerequisite | solid | S1 / metrics.py | Confirmed solid without re-exam |
| Repeated event-level CV (R=5, seeds 42–46) | prerequisite | solid | pj-004, pj-005 | Confirmed solid without re-exam |
| Regression tree leaves (mean) and split objective (SSE reduction) | core | shaky | notes ch. 8, ~p. 85–90 | Leaf mean −6 correct; once confused parent SSE (2) with post-split child SSE (0.5); retaught |
| Bagging / Random Forest (bootstrap, mean prediction, `max_features` per split) | core | solid | notes §8.4 | Bootstrap + subset per split; forest mean −6 from (−6,−5,−7); why RF vs one greedy tree |
| Gradient boosting (residuals, η, sequential trees) | core | solid | notes §8.5 | Ordered C→B→A→D; numeric residual chain; event 1 second-round residual −0.5 |
| Feature importance (impurity decrease summed over splits) | core | solid | notes §8 + sklearn docs | Summed over splits/trees, not first tree only |
| Imputation fit on train fold only | hazard | solid | pj-010, ESL §7.10 | Stated train-only per fold explicitly |
| HR rarity with direct risk regression | hazard | shaky | pj-001, class imbalance | Risk stated: ~1% HR; model predicts continuous risk; F₂ still threshold-based; may under-predict extremes unless trees capture tails |
| Tuning on same folds as final table | hazard | shaky | outside-notes: nested CV | Not examined; decision in ledger — optimistic bias if same folds used for pick and report |

### Addendum — floor c (2026-10-28)

| Concept | Role | Status | Source | Evidence |
|---------|------|--------|--------|----------|
| Metric clipping vs training-target transform | core | solid | pj-007, pj-026 | Asked the difference; then argued unclipped selection on his own (missed HR should weigh more once a floor exists) |
| Floor c ↔ implied HR-fraction alarm threshold p*(c) | core | solid | derivation in pj-026 | Followed derivation; chose theory-based c over CV for compute |
| F_β-optimal threshold p* = F*/(1+β²) | core | shaky | outside-notes: Lipton et al. 2014 | Taught, not derived by him; asked whether using LRP F₂ as F* is cheating (good leakage instinct) |
| Revocation checks R2–R4 (threshold sweep, calibration ratio, Cohen's d) | hazard | solid | pj-026 | Needed re-explanation; then answered two applied cases correctly (R3 band 12.5–50 % for 25 %; R2 gain 0.03 < 0.05) |
