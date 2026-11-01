# mf-007. Logistic task and target (S4)

- **Status:** accepted
- **Date:** 2026-11-01
- **Tags:** modeling | evaluation
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

S4 compares syllabus models against LRP under the S1 protocol (pj-004..pj-007) on the 8892 events of `event_table` (pj-003). `y_hr = risk_final >= -6.0` (pj-001).

## Mathematical framing

Binary classification: y_hr ~ Bernoulli(p(x)), with `predict_proba` returning the estimated probability of HR per event. The training loss is the Bernoulli negative log-likelihood (cross-entropy).

## Options considered

1. **Classification on all events, target `y_hr`, `predict_proba`.**
2. **Classification on a subset of events.**
3. **Regress `risk_final` and threshold at -6** (S5 formulation, pj-014).

## Decision

Chose **option 1**: the logistic model is trained on all 8892 events with target `y_hr` and outputs `predict_proba`, the estimated HR probability per event.

## Rationale (developer's own words)

The protocol evaluates all models with F2, MSE_HR and L on the same 8892 events. Logistic regression on `y_hr` is the natural classification formulation: it produces a probability per event, and it replicates the task LRP already performs.

## Checks raised

- A probability alone gives F2 (through an alarm rule) but not MSE_HR or L, which need a continuous `r_hat`; open, closed by the magnitude-regressor decision and the alarm/`r_hat` decision.
- Log-loss is not among the registered metrics (pj-007); not added here.
- Calibration of the probabilities is not guaranteed by the loss alone, especially with a penalty or class imbalance; calibration is S6's objective.
- Trees (S5) regress `risk_final` with a hard 0/1 `p_hr` (pj-014, pj-020), so models are compared on F2, MSE_HR and L, not on a shared probability.

## Expected behavior and validation

`predict_proba` returns values in (0, 1) for every event of `event_table`; one prediction per event and repetition.

## Consequences

- Does not decide the magnitude target, the alarm rule or the penalty (later decisions).
- Not doing: training on a subset, or regressing the label.

## Scope note — 2026-11-01

After the alarm-rule decision (mf-012), the developer decided that the three logistic models are kept for S6 and do not enter the S4 table. The S4 table has three rows, one per regressor (unpenalized, ridge, lasso). This decision stays accepted but is not implemented in S4; solver and selection decisions of S4 (mf-013, mf-014, mf-015) cover the regressors only.
