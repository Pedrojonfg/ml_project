# mf-001. Purpose and scope of the jump taxonomy

- **Status:** accepted
- **Date:** 2026-10-31
- **Tags:** modeling | evaluation
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

S2 defines a jump taxonomy (stable-low / stable-high / jump-up / jump-down) from
Δ = y_final − latest_risk (log10 risk units). Δ uses y_final, which is not
available at prediction time t0 (last valid CDM, time_to_tca ≥ 2 d). Official
test is used once, at R5, with frozen models (docs/dependencias-y-reuniones.md).

## Mathematical framing

The label is a deterministic function of (latest_risk, y_final). It describes
the error of the LRP baseline (ŷ = latest_risk). Using it as a model input
would make y_final recoverable from the inputs (leakage).

## Options considered

1. **Analysis and reporting only** — label never enters X, targets or weights;
   metrics are reported per class.
2. **Analysis plus auxiliary prediction target** — a model predicts the class
   from t0 information; the label is a target, never an input.
3. **Analysis plus class weighting/resampling in training** — weights depend on
   y_final; valid only inside training folds.

Scope options: train only, official test only, both.

## Decision

Chose **option 1** (analysis and reporting only). Scope: **both train and
official test**: the label is computed on both, but the test taxonomy is only
inspected, never used for modeling decisions.

## Rationale (developer's own words)

The label can be used to analyze and present results, not to train, because it
comes from Δ, which uses y_final, and that would be leakage. It is computed on
both train and test so that events are always classified; the test labels are
only looked at, so they do not influence the model.

## Checks raised

- "Classify" was ambiguous (grouping for analysis vs. predicting the label) →
  clarified: grouping for analysis (option 1).
- Leakage argument applies to the label as an input, not as a target → noted;
  option 1 excludes both uses.
- Computing test labels could conflict with "test used once at R5" if inspected
  early → developer: computed on both, only looked at (not used for modeling).

## Expected behavior and validation

Per-class metric tables and the atlas are produced from labels; no label or
Δ-derived column appears in the feature columns of event_table. Check: assert
that no feature column is derived from y_final.

## Consequences

- No jump-class model, weights or resampling in this task.
- Labels on train depend on the S1 labeling rule (Pedro).
- Test taxonomy does not feed any model or tuning choice before R5.
