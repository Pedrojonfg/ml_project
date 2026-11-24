# pj-081. Official test — model set

- **Status:** accepted
- **Date:** 2026-11-24
- **Tags:** evaluation
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

R5 (`docs/dependencias-y-reuniones.md`) requires a single evaluation on the official Zenodo/Kelvins test with frozen models. W1 (`pj-035`) reported CRP/LRP only on that split for the Progress Report. The Final Report needs an explicit list of which learned rows appear on that one-shot pass.

## Mathematical framing

The official test is a fixed held-out event set. Models selected and trained under the internal S1 protocol are applied once; the test does not enter hyperparameter selection or model choice.

## Options considered

1. **All single-stage bake-off slugs + CRP/LRP** — one row per estimator with existing artifacts.
2. **Baselines only (CRP/LRP)** — same reporting stance as W1.
3. **A subset** (e.g. LRP + best linear + GBDT + two-stage) — fewer rows.
4. **Option 1 + all S6 stage-1 and paired combinations** — includes calibrated two-stage rows.
5. **Other / none**

## Decision

Chose **option 4**. The official-test evaluation includes:

- Baselines CRP and LRP.
- All single-stage bake-off slugs with artifacts: `ols`, `ridge`, `lasso`, `knn`, `kernel_ridge`, `rf`, `gbdt`, `mlp`, `gru`.
- All S6 stage-1 and paired combinations already produced under the S6 ADRs.

Not included: S9 lead-time / leave-mission-out (not a single model on this split).

## Rationale (developer's own words)

All of them, so we can have real data to report.

## Checks raised

- “All” does not include S9 → recorded; excluded.
- S6 rows expand the table; fit protocol still open → accepted.
- After seeing numbers, no retuning (R5) → recorded.
- W1 test table was CRP/LRP only (`pj-035`); including learned models changes Final Report reporting relative to W1, not the internal OOF bake-off → recorded.

## Expected behavior and validation

- Official-test artifacts list one result block (or row) per model in the set above.
- No S9 curve/LMO fold appears as an official-test model row under this ADR.

## Consequences

- Fit protocol, event filter on test, and reporting vs OOF remain later decisions on this agenda.
- Not doing: using the official test for selection; including S9 as a model row.
