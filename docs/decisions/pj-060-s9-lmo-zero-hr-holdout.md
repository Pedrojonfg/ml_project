# pj-060. S9 LMO — held-out missions with zero HR events

- **Status:** accepted
- **Date:** 2026-11-14
- **Tags:** evaluation
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

On the internal cohort, six missions have no HR events among their events (`pj-058` EDA). For leave-one-mission-out, those folds have `n_hr_test = 0`. F₂ and L are not meaningful on a pure-negative test set for HR-focused metrics; MSE_HR is undefined (no HR events to score).

## Options considered

1. **Skip** the fold in summary statistics; still **record** a row with status `skipped` and reason.
2. Include the fold with F₂ = 0 and L = NA in aggregates.
3. Report magnitude metrics only on folds with `n_hr_test ≥ 1`.

## Decision

Chose **option 1**:

- Do **not** include skipped folds in means/medians or ranking summaries.
- **Do** write an explicit record per skipped `mission_id`: `status = skipped`, `reason = zero_hr_in_holdout`, plus `n_test` and `n_hr_test = 0`.
- Do not run model training for that fold if there is no HR signal to evaluate on the test side **and** metrics require HR events — implementation may still log LRP-only detection stats; if all HR metrics are undefined, skip training and record skip (implementation detail: at minimum, no bogus L/F₂ numbers in the summary table).

## Rationale (developer's own words)

Omit because there is no HR signal; it is important to keep a skipped row with the reason.

## Checks raised

- Skipped missions are still visible for reproducibility and oral Q&A (13 evaluable HR-bearing hold-outs remain).
- Train sets for other folds still use events from zero-HR missions (they contribute non-HR training data).

## Expected behavior and validation

- `results/s9_lmo.json` (or equivalent) lists 19 missions: 6 skipped + 13 with full metrics when `n_hr_test ≥ 1`.

## Consequences

- W2 LMO table footnote: folds skipped when hold-out has no HR events.