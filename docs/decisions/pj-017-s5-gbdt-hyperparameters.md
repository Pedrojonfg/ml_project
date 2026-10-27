# pj-017. S5 gradient boosting — `GradientBoostingRegressor` and hyperparameters

- **Status:** accepted
- **Date:** 2026-10-27
- **Tags:** modeling | regularization
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

Scope S5 second model: gradient boosting alongside RF, same targets and CV (pj-014, pj-004–005). pj-015 uses median imputation for both models. `HistGradientBoostingRegressor` remains a **revisit** option with pj-015 if NaNs become material or `GradientBoostingRegressor` is too slow.

Developer’s first GBDT for the project; hyperparameters may be revised after CV (new ADR). No `n_estimators` grid at launch (see Rationale).

## Options considered

1. `GradientBoostingRegressor` + shared imputer (current).
2. `HistGradientBoostingRegressor` + imputer or native NaN (deferred per pj-015 revisit).
3. `n_estimators` grid {100, 300, 500} parallel to RF (higher compute).

## Decision

Chose **option 1** with **fixed** boosting hyperparameters below (no multi-value `n_estimators` search unless results motivate a new ADR).

| Parameter | Value |
|-----------|-------|
| Estimator | `sklearn.ensemble.GradientBoostingRegressor` |
| `n_estimators` | 200 |
| `learning_rate` | 0.1 |
| `max_depth` | 4 |
| `min_samples_split` | 4 |
| `min_samples_leaf` | 2 |
| `subsample` | 1.0 |
| `max_features` | `"sqrt"` |
| `loss` | `"squared_error"` |
| `random_state` | `42 + repetition_index` (0…4 → 42…46) |
| `validation_fraction` | 0.1 (default; early stopping not enabled) |
| `n_iter_no_change` | `None` (default) |
| `tol` | `1e-4` (default) |
| `ccp_alpha` | `0.0` (default) |

## Rationale (developer's own words)

Stay with `GradientBoostingRegressor` while there are no NaNs and the dataset is not huge; switching to the faster histogram booster is overkill for now and tied to revisiting pj-015 if circumstances change. Use learning rate 0.1 and parallel the Random Forest depth and sample constraints (depth 4, min_samples_split 4, min_samples_leaf 2, sqrt features). Do not run the 100/300/500 search for boosting initially because it is more expensive in time unless early results are bad.

## Checks raised

- GBR trains trees sequentially; 200 estimators at 0.1 learning rate (developer update 2026-10-27) is not guaranteed optimal for Kelvins L.
- If RF search shows strong sensitivity to `n_estimators`, revisiting GBDT `n_estimators` or grid search is a follow-up decision, not automatic.

## Consequences

- Same imputer pipeline as RF (pj-015).
- Revisit triggers in pj-015 apply to this estimator class jointly.
- GBDT row in results uses `n_estimators=200` until a new ADR changes it.
