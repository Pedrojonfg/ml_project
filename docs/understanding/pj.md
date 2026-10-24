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
