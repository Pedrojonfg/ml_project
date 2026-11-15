# mf-053. Evaluation protocol of the kernel ridge row in S10

- **Status:** accepted
- **Date:** 2026-11-15
- **Tags:** evaluation
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

The S4 rows (OLS, ridge, lasso, KNN) use: 5-fold CV stratified on `y_hr`, shuffled, event-level (pj-004); R = 5 repetitions, seeds 42-46 (pj-005); F2, MSE_HR and L, MSE_HR and L both clipped (-6.001) and unclipped (pj-007); event bootstrap B = 10000, 95% BCa, joint resampling, per-repetition metrics averaged, paired differences vs LRP and CRP (pj-006, mf-016..mf-020). Cost of one kernel ridge repetition (5 outer folds): about 45 min measured/extrapolated (mf-052); five repetitions about 3.7 h. The experiment window closes on 2026-11-18 (docs/plan-reparto.md).

## Mathematical framing

Each repetition gives out-of-fold predictions for all events; the metric of a row is the mean of the per-repetition metrics, and the bootstrap resamples events. Fewer repetitions average over fewer fold assignments and give a less stable repetition spread.

## Options considered

1. **Unchanged: R = 5, seeds 42-46** — same protocol as the other S4 rows; about 3.7 h.
2. **Fewer repetitions (1 to 4, seeds from 42)** — about 45 min per repetition; the row averages over fewer repetitions than the others. Either keep the other rows with their 5 repetitions (a), or recompute them restricted to the same repetitions from the stored predictions, without refitting (b).
3. **Smaller bootstrap (for example B = 1000)** — not the bottleneck; noisier intervals.

## Decision

Chose **option 2** with **(a)**. Kernel ridge is run on **2 repetitions, seeds 42 and 43** of pj-005 (10 outer folds). Everything else is unchanged: pj-004, pj-006, pj-007, mf-016..mf-020 (bootstrap seed 2026, B = 10000, BCa, caps and unreliable flags). The other S4 rows keep their 5 repetitions and are not recomputed; the kernel ridge row of the table carries a note stating that it uses 2 repetitions.

## Rationale (developer's own words)

To save time: two repetitions. Option a is best because nothing needs to be recomputed.

## Checks raised

- The table mixes averages over 5 and over 2 repetitions, so the comparison between rows is not strictly fair and the intervals of this row may be wider.
- The repetition spread (supplementary in pj-006) is computed with only 2 values and is of little information.
- Seeds 42 and 43 give the same fold assignments as in S4; a fair comparison later (other rows recomputed on those two repetitions from `preds/*.parquet`, no refitting) remains possible.
- Estimated run time about 1.5 h.

## Expected behavior and validation

Stored: `results/kernel_ridge.json` (metrics, per-repetition metrics, per-fold selected lambda, t, m, gamma, bootstrap) and `preds/kernel_ridge.parquet` with the repetition of every prediction (reps 42 and 43 only).

## Consequences

- Not doing: R = 5 for this row, recomputing the other rows on 2 repetitions, a smaller bootstrap.
