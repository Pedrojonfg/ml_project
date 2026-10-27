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
