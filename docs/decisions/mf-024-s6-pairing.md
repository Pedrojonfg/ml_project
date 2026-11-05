# mf-024. Pairing of stage-1 and stage-2 variants in S6

- **Status:** accepted
- **Date:** 2026-11-04
- **Tags:** modeling
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

mf-021 chose three stage-1 classifiers (unpenalized, L2, L1 logistic); mf-023 chose three stage-2 regressors (unpenalized, ridge, lasso). The two stages are trained separately; the calibration depends only on the stage-1 classifier, so there are 3 calibrations whatever the pairing.

## Mathematical framing

The pairing fixes which (classifier, regressor) models are combined and evaluated. With separate training, every pair is a combination of pieces already fitted; the pairing changes the number of results rows and of bootstrap comparisons, not the training cost.

## Options considered

1. **A. All 9 combinations** — shows what each stage contributes separately; 9 rows; more paired bootstrap comparisons.
2. **B. Matched by penalty** — (unpenalized, OLS), (L2, ridge), (L1, lasso); 3 rows; a difference between rows mixes the effect of both stages with the penalty.
3. **C. A single pair** — 1 row; no comparison of variants inside S6.

## Decision

Chose **A**: all 9 combinations of the three stage-1 classifiers with the three stage-2 regressors.

## Rationale (developer's own words)

It is the best way to see what each stage contributes.

## Checks raised

- The AI corrected its own earlier statement: calibrations are per classifier (3), not per pair.
- Developer first added that A "helps to retrain"; after the AI's clarification (A does not need retraining, and is no easier to retrain than B or C) the developer removed it from the rationale.

## Expected behavior and validation

9 two-stage rows in the S6 results table, built from 3 stage-1 outputs and 3 stage-2 outputs.

## Consequences

- Reuse vs refit of the S4 regressor predictions is still to decide (queue).
- Bootstrap comparisons for 9 rows against LRP, CRP and the S4/S5 rows (mf-016..020) to be specified in the evaluation decision.
