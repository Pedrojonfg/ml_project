# pj-016. S5 Random Forest — fixed hyperparameters

- **Status:** accepted
- **Date:** 2026-10-27
- **Tags:** modeling | regularization
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

Scope S5 fits `RandomForestRegressor` on v1 features with per-fold median imputation (pj-015), regressing `risk_final` (pj-014), under repeated stratified event-level CV (pj-004, pj-005). This is the developer’s first Random Forest for the project; initial values may be revised after inspecting CV behaviour (record changes via a new or superseding ADR).

`n_estimators` is not fixed here; see pj-018.

## Options considered

Fixed depth, leaf, and split constraints vs deeper trees (`max_depth` 10 or `None`); various `min_samples_split`; `max_features` sqrt vs all features; model `random_state` fixed vs tied to repetition index.

## Decision

Use **scikit-learn** `RandomForestRegressor` with:

| Parameter | Value |
|-----------|-------|
| `max_depth` | 4 |
| `min_samples_split` | 4 |
| `min_samples_leaf` | 2 |
| `max_features` | `"sqrt"` |
| `bootstrap` | `True` |
| `max_samples` | `None` |
| `criterion` | `"squared_error"` |
| `random_state` | `42 + repetition_index` (repetition_index 0…4 → 42…46) |
| `n_jobs` | `-1` |
| `warm_start` | `False` (default) |
| `ccp_alpha` | `0.0` (default) |
| `max_leaf_nodes` | `None` (default) |
| `min_impurity_decrease` | `0.0` (default) |

## Rationale (developer's own words)

First time training a Random Forest; hyperparameters may change if results are weak or overfit. After reconsidering depth, use a smaller `max_depth` (4) and `min_samples_split` 4 to limit overfitting on a small HR tail. Keep sqrt feature subsampling and bootstrap. Tie model seed to repetition index (42 plus index). Use squared error as in class. Use all CPU cores.

## Checks raised

- ~80% of `risk_final` at −30: shallow trees may predict near the floor; F₂ still depends on the −6 threshold.
- `random_state` 42…46 matches fold seed integers but serves a different RNG (fold assignment vs forest bootstrap); document both in code comments.
- Re-tuning after poor results is expected; do not change registered values silently.

## Consequences

- Implement RF inside imputer pipeline (pj-015).
- Pass `random_state=42 + rep_idx` for each of the R=5 repetitions.
- `n_estimators` chosen per pj-018.
