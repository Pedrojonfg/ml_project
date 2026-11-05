# mf-034. Source of the stage-2 predictions in S6

- **Status:** accepted
- **Date:** 2026-11-04
- **Tags:** modeling
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

mf-022 and mf-023 fix the stage-2 models: the three S4 regressors trained on all events. Their out-of-fold predictions exist in `preds/{ols,ridge,lasso}.parquet` and metrics in `results/{ols,ridge,lasso}.json`, both tracked in git, produced with the S1 protocol (K = 5, seeds 42..46) and the S4 decisions (mf-008..mf-020).

## Mathematical framing

The stage-2 prediction r_hat of each event is out-of-fold, so it can be reused as the second stage of S6 without refitting, as long as the protocol and the S4 decisions stay as they were when the files were produced.

## Options considered

1. **A. Reuse the S4 predictions** — S6 depends on the stored files; no refit.
2. **B. Refit the regressors inside the S6 pipeline** — one script produces everything; the numbers equal the S4 ones if nothing changes.

## Decision

Chose **A**: the stage-2 predictions of S6 are the stored S4 predictions.

## Rationale (developer's own words)

I reuse them; it is the most coherent with S4.

## Checks raised

- If S4 is rerun or its decisions change, the S6 results using these files must be recomputed → none, developer keeps A.
- How the 5 repetitions are stored in the parquet files is checked at implementation.

## Expected behavior and validation

For every event, fold and repetition of S6, r_hat equals the value stored in the S4 file of the same regressor.

## Consequences

- Still to decide: how the two stages are combined, the alarm line, and the evaluation.
