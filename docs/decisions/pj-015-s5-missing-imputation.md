# pj-015. S5 missing values — per-fold median imputation (shared pipeline)

- **Status:** accepted
- **Date:** 2026-10-27
- **Tags:** modeling | data
- **Decided by:** Pedro
- **AI involvement:** options + critique; factual data check (train v1 feature matrix: 0% NaN cells)

## Context

pj-010 leaves non-`std` NaNs in S3 features for per-fold handling in S4/S5. `RandomForestRegressor` does not accept NaN inputs in scikit-learn. `HistGradientBoostingRegressor` can treat NaN natively. Scope S5 trains RF and a gradient-boosting regressor on the same `X` under the same CV protocol.

## Options considered

1. **Shared `Pipeline`**: `SimpleImputer(strategy="median")` fit on training fold only, then both tree models on imputed `X`.
2. **Split pipelines**: imputer + RF; `HistGradientBoostingRegressor` on raw `X` with native NaN handling.
3. **No imputer**: forbid NaNs in `build_features` via extra S3 rules (extends pj-010).
4. **Other imputation** (mean, mode, iterative, etc.).

## Decision

Chose **option 1**: median imputation in a single shared preprocessing path for both S5 tree regressors.

## Rationale (developer's own words)

Unless native NaN handling in GBDT gives a large advantage, median imputation for both models is conventional and harmless given the project decisions so far suggest there will be no NaNs; a single pipeline avoids maintaining two paths.

## Mathematical framing

For each CV fold, imputation statistics (per-column median) are computed on training events only and applied to validation events. Tree models are fit on the imputed feature matrix; targets remain `risk_final` (pj-014).

## Checks raised

- On current Kelvins train after `build_features`, NaN rate is 0%; imputation is a protocol safeguard for test/edge cases, not a train-set correction today.
- Native NaN splits can matter when missingness is frequent and informative; with near-zero missing rate, empirical gain over median is expected to be small.
- Mario may adopt the same imputer in S4 for comparability; not required by this ADR.

## Consequences

- S5 implementation uses one sklearn `Pipeline` pattern: imputer (median, fold-fit) → regressor.
- Parameter registry must still list imputer `strategy` and any `SimpleImputer` options explicitly.
- If missing rate becomes material later, revisiting option 2 or 4 requires a new ADR.

## Revisit trigger (developer request)

Reopen **this ADR together with** the S5 gradient-boosting estimator choice (pj-017) if any of the following hold:

1. **Material NaNs in `X` at evaluation time** (held-out or competition test): seriously consider **option 2** — RF keeps median imputation; GBDT switches to `HistGradientBoostingRegressor` on raw `X` with native NaN splits (median imputer not applied on that path).
2. **`GradientBoostingRegressor` is too slow** for the repeated-CV workload: consider `HistGradientBoostingRegressor` for speed (still paired with median imputation unless trigger 1 applies).

While S5 uses `GradientBoostingRegressor`, trigger 1 cannot be satisfied without changing the booster class; do not treat “revisit imputation only” as sufficient — class + pipeline must be updated in one decision pass. Record supersession in new ADR(s) if adopted.
