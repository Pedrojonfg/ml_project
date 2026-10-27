# pj-010. Missing values in S3 features

- **Status:** accepted
- **Date:** 2026-10-27
- **Tags:** modeling | preprocessing | data
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

pj-009 defines tabular v1 features from usable CDMs. sklearn models in S4/S5 need a policy for undefined or missing numeric values. Train usable rows show no NaNs in the four snapshot variables; policy still applies to test, edge cases, and future columns.

## Options considered

1. **S3 never imputes; all NaNs deferred to S4** with per-fold fit.
2. **S3 global imputation** (e.g. train median) — requires careful leakage control.
3. **S3 explicit edge-case rules only; other NaNs deferred to S4** (hybrid).
4. **Drop or omit columns when undefined** — breaks fixed schema.

## Decision

Chose **hybrid (3) + (1) for the remainder**:

- **`std(risk)` over usable CDMs:** if `n_usable_cdms == 1`, set **`0`** (no within-window variation).
- **All other NaNs** in v1 feature columns: **leave as NaN in S3**; **S4/S5** handle imputation (or equivalent) with fit on training fold only.

No other S3 imputation rules in v1 unless added by a later ADR.

## Rationale (developer's own words)

Use zero for single-usable std because it is mathematically coherent (no observed variability). For anything else, do not impute in S3; let the training pipeline handle missing values per fold.

## Checks raised

- NaN `std` with single point would be misread after median imputation in S4 → avoided by using 0.
- Rare NaNs in raw CSV cells may still appear → S4 must define imputer; out of scope for S3 except passing NaNs through.

## Expected behavior and validation

- After `build_features`, single-usable events have `std_usable_risk == 0` (or the documented column name).
- Tests on synthetic one-usable event.

## Consequences

- S4 owns default imputation strategy for remaining NaNs.
- Parameter registry updated with single-usable std rule.
