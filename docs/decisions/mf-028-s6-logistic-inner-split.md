# mf-028. Inner split and seed of the logistic models in S6

- **Status:** accepted
- **Date:** 2026-11-04
- **Tags:** modeling
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

mf-025 selects C by inner CV inside each outer training fold. For the S4 regressors the inner split is `StratifiedKFold(n_splits=5, shuffle=True, random_state=0)`, for every outer training fold and repetition (mf-015). Outer protocol: K = 5, seeds 42..46 (pj-004, pj-005).

## Mathematical framing

The inner split fixes which events validate each C. The same split for S4 and S6 makes the inner-CV selection differ only through the model, not through the partition.

## Options considered

1. **Same as S4** — `StratifiedKFold(n_splits=5, shuffle=True, random_state=0)`.
2. **A different split or seed for the logistic models** — selection differs from S4 by the partition too.

## Decision

Chose **same as S4** (mf-015): `StratifiedKFold(n_splits=5, shuffle=True, random_state=0)` stratified by `y_hr`, for the inner split of every outer training fold, in every repetition.

## Rationale (developer's own words)

Using the same inner split avoids mixing two sources of variation when comparing S4 with S6.

## Checks raised

None raised.

## Expected behavior and validation

Inner folds of the logistic models equal those of the S4 regressors for the same outer training fold.

## Consequences

- Still to decide: treatment of an optimum at a grid edge, solver and library parameters.
