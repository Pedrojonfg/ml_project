# pj-083. Official test — hyperparameter re-selection on full train

- **Status:** accepted
- **Date:** 2026-11-24
- **Tags:** modeling | evaluation
- **Decided by:** Pedro
- **AI involvement:** options + critique; opinion requested (common practice in papers)

## Context

`pj-082` requires one fit per learned slug on the full filtered training set, then predict the official test. Internal OOF stores a different selected hyperparameter vector per outer fold/repetition, so there is no single frozen value to reuse. Selection must not use the official test (R5).

## Mathematical framing

Hyperparameter selection is part of the training procedure. Treating the full filtered train as the sole outer training part and applying the same inner/nested rule as in the bake-off yields one hyperparameter vector per slug; the final estimator is then fit on that full train and evaluated on test.

## Options considered

1. **Re-selection** with each family’s existing nested/inner rule on the full filtered train as outer train.
2. **Mode / median** of the 25 OOF fold choices — no new search.
3. **Fixed ADR point** without search where a grid existed.
4. **Other / none**

## Decision

Chose **option 1**. For each learned slug in `pj-081`, before the single fit of `pj-082`:

1. Re-run that family’s existing selection procedure with the full filtered training set (`pj-003`) as the outer training part.
2. Inner/nested seeds that depended on the outer repetition index use **42** (aligned with nested repetition 0 under `pj-073`).
3. After selection: fit preprocessing (imputer/scaler as applicable), training-target floor `c(w)` where the family uses it, and alarm line `t` where applicable, on the full filtered train only.
4. Fit the model and predict the official test. The test does not enter selection, preprocessing statistics, `c(w)`, or `t`.

## Rationale (developer's own words)

Re-selection because it is the process that best fits our way of training. Seed 42 aligned with nested rep 0.

## Checks raised

- OOF had per-fold choices; a single fit needs one vector → re-selection supplies it → accepted.
- Full-train nested has no outer `r`; seed 42 vs S4 inner seed 0 (`mf-015`) → different families already used different seeds → accepted.
- Preprocessing / `c(w)` / alarm `t` on full train after selection → included in this ADR.
- Compute: one nested pass per slug → recorded.
- Common-practice considerations were requested; developer still chose in their own words → recorded as opinion requested.

## Expected behavior and validation

- Official-test artifacts store the selected hyperparameters (and `t`, `c`, `w` as applicable) for the full-train run.
- No test `event_id` appears in any selection or fitting step.
- Re-running with seed 42 reproduces the same selected values and test predictions (up to documented non-determinism for torch if any).

## Consequences

- Parameter registry: official-test hyperparameter freeze = re-selection on full train, inner seed 42 where rep-indexed.
- Supersedes the deferred freeze row under `pj-082`.
- Event filter on test and reporting vs OOF remain later on the agenda.
- Not doing: mode-of-folds freeze; using the test inside selection.
