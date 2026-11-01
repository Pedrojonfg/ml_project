# mf-012. Alarm line for the S4 regressors

- **Status:** accepted
- **Date:** 2026-11-01
- **Tags:** modeling | evaluation
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

mf-008 (reopened and confirmed) keeps the regressor target `risk_final` untransformed. Check run in the ledger session (ridge, alpha = 1.0, repetition 0): r_hat never reaches -6 (0 of 8892), so F2 at the protocol alarm line is 0 and L infinite, although the AUC of r_hat for y_hr is 0.92. Protocol F2 (pj-007, ADR 018) alarms at -6.

## Mathematical framing

For each model, training fold and repetition, an alarm line t is chosen and an event alarms if r_hat >= t. F2 is a step function of t; it changes only when t crosses a prediction, and its maximum is attained at the r_hat value of a true HR event (lowering t below that value adds non-HR events and no HR). t is chosen on in-sample predictions of the training fold, which fit the training HR better than validation HR; this biases t upward.

## Options considered

1. **Maximize F2 on the training-fold predictions.**
2. **Maximize F2 on inner out-of-fold predictions within the training fold.** Check: pooled OOF F2 of 0.262 (option 1) vs 0.264 (option 2), 3 repetitions, one ridge, 5x the cost.
3. **Rank rule:** alarm the top k % of r_hat, with k set in the training fold.
4. **Smoothed criterion:** t at the centre of the plateau near the maximum.

## Decision

Chose **option 1**. In each training fold, for each model and repetition:

- Candidates: the r_hat values of the HR events of the training fold (about 74).
- Criterion: t maximizing F2 (beta = 2) on the training-fold predictions.
- Ties: the median of the tied candidates (for an even number, the mean of the two central values).
- t is recomputed for each model, fold and repetition; t and its variability across folds are stored as part of the results.

MSE_HR (clipped and unclipped, pj-007) is computed on the true HR events with r_hat, independent of t. L = MSE_HR / F2 with that F2.

## Rationale (developer's own words)

Maximize F2 on the training fold because F2 is the metric evaluated; a proxy would be arbitrary. Option 2 performs the same (0.262 vs 0.264) at 5x the cost; options 3 and 4 add parameters without evidence of improvement. Candidates are the r_hat values of the training HR: they are where one more HR enters or leaves the alarm, covering the relevant zone without wasted evaluations. Ties by the median: the most robust point of the plateau, equidistant from the edges, without bias to more or fewer alarms. The variability of t per fold is kept as a diagnostic to understand the gap.

## Checks raised

- The loss of about 0.16 pooled F2 against the oracle (one global t chosen looking at the validation, 0.420) is a hypothesis, not a result: the cause may be noise of the step function with about 74 HR or a shift of the r_hat scale across folds; the oracle is optimistic by construction (selected on the same 93 HR). To be contrasted with the stored t per fold.
- The training predictions fit the training HR, so the maximizing t is biased upward; option 2 did not improve in the check.
- t is chosen in the training fold only, so the OOF evaluation has no leakage; the noise of t appears as a lower and more variable F2, not as a bias.
- This changes the definition of F2 for these models with respect to the protocol (alarm at -6). LRP and the S5 trees alarm at -6 (pj-001, pj-020); the regressors get one extra degree of freedom. Comparison stays on F2, MSE_HR and L. To be documented in the results table.
- The check ran on one untuned ridge (3 repetitions, 300-quantile grid, central-value tie rule); candidates and tie rule here differ from that grid.

## Expected behavior and validation

For every model, fold and repetition t is in the range of the r_hat values of the training HR; the stored t vary across folds. Out-of-fold F2 above 0 for the regressors (an F2 of 0 in all folds would revoke this ADR).

## Consequences

- The three S4 rows (unpenalized, ridge, lasso) use t, not -6, for F2.
- Alarm thresholds of S5 (hard threshold at -6) are not changed.
- Not doing: inner-CV threshold, rank rule, plateau smoothing.
