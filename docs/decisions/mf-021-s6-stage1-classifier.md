# mf-021. Stage-1 classifier of S6

- **Status:** accepted
- **Date:** 2026-11-04
- **Tags:** modeling
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

S4 kept the three logistic models for S6 (mf-007, mf-009, mf-011): trained on all events with target `y_hr`, `class_weight='balanced'`. They were not run in S4. Regularization selection and solver decisions of S4 (mf-013, mf-014) cover the regressors only.

## Mathematical framing

Stage 1 of S6 produces a score s per event, which a later decision calibrates into P(HR). With `class_weight='balanced'` the HR events weigh more in the loss, so the raw output is not a calibrated probability.

## Options considered

1. **A. Unpenalized logistic** — assumes the coefficients can be estimated freely; the maximum does not exist under perfect separation.
2. **B. Logistic with L2** — adds lambda * ||w||^2; shrinks without zeroing; needs lambda.
3. **C. Logistic with L1** — adds lambda * ||w||_1; zeroes some coefficients; needs lambda.
4. **D. All three at once** — three sets of scores, calibrations and results rows; multiplies later decisions by three.
5. **E. Another family** (e.g. boosted trees as classifier) — new model, not built in S4 or S5.

## Decision

Chose **D**: the three logistic variants (unpenalized, L2, L1) are the stage-1 classifiers of S6.

## Rationale (developer's own words)

Having all three seems the most versatile; it would help the comparison of results.

## Checks raised

- D triples the downstream decisions (calibration, calibration data, evaluation) → developer keeps D.
- `class_weight='balanced'` makes the raw output not a calibrated probability → left to the calibration decisions.

## Expected behavior and validation

Three sets of stage-1 scores per fold and repetition, one per variant.

## Consequences

- Regularization selection and solver of the logistic models are still to decide (queue item 5).
- Each later S6 decision applies to the three variants unless it says otherwise.
