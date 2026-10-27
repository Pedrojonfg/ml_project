# pj-018. S5 Random Forest — `n_estimators` search

- **Status:** accepted
- **Date:** 2026-10-27
- **Tags:** modeling | evaluation
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

Pedro’s first RF for the project. Training cost for ~8892 events and 35 features is moderate; exploring a small grid for tree count is acceptable. The same CV folds and repetitions used for the final comparison table are reused for selection (optimistic bias hazard noted in understanding record S5).

## Options considered

1. Single fixed `n_estimators` (e.g. 300).
2. Small grid **{100, 300, 500}**; pick one value for reporting.
3. Larger grid or nested CV (higher compute).

## Decision

Chose **option 2**: candidate set **`n_estimators` ∈ {100, 300, 500}**.

**Selection rule:** For each candidate, run the full S1 CV protocol (K=5 folds × R=5 repetitions) with pj-016 settings and pj-015 imputation. Aggregate **mean unclipped `L`** (pj-007) over all out-of-fold validation predictions (all folds and repetitions). Select the candidate with the **lowest** mean unclipped `L`. Use that `n_estimators` for the reported RF row, feature importances, and saved predictions for that model.

Ties: prefer the **smaller** `n_estimators` among tied candidates.

## Rationale (developer's own words)

A search over 100, 300, and 500 seems reasonable given the dataset size and avoids guessing a single tree count.

## Checks raised

- Selection on the same folds used for reporting inflates optimism slightly; acceptable for scope S5 if documented as a limitation.
- Total RF training ≈ 3× one pass over the CV grid.

## Consequences

- Implementation runs three full CV evaluations for RF before locking `n_estimators`.
- Parameter registry records the **chosen** value after the search (per run) or documents the grid + rule if the code auto-selects each time.
