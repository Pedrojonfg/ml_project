# pj-024. S5 relaxed tree regularization and `n_estimators` grids

- **Status:** accepted
- **Date:** 2026-10-27
- **Tags:** modeling | regularization
- **Decided by:** Pedro
- **AI involvement:** options + critique
- **Supersedes:** pj-016 / pj-017 depth and sample constraints; pj-018 candidate set

## Context

Run 0 (pj-021) with `max_depth` 4 and `min_samples_split` 4 yielded RF OOF F₂ = 0 (no `r_hat` ≥ −6). Compute budget allows larger grids (pj-021). Selection metric for grids is mean clipped L OOF (pj-022).

## Options considered

1. Keep pj-016/pj-017 regularization; only change selection metric (pj-022).
2. Relax depth and sample constraints; expand `n_estimators` grid; apply **same** constraints to RF and GBDT.
3. Different regularization per model family.

## Decision

Chose **option 2**. **Random Forest** and **GradientBoostingRegressor** share:

| Parameter | Value |
|-----------|-------|
| `max_depth` | 8 |
| `min_samples_split` | 2 |
| `min_samples_leaf` | 1 |

**`n_estimators` grids (both models):** {300, 500, 1000}.

For each model, run full OOF CV per candidate; select `n_estimators` with **lowest mean clipped L** (pj-022); tie → **smaller** `n_estimators`.

All other registered settings unchanged (pj-015 imputation, pj-016 bootstrap/`max_features`/criterion, pj-017 `learning_rate` 0.1, `subsample` 1.0, `random_state` 42 + rep index).

## Rationale (developer's own words)

Try max depth 8, min_samples_split 2, min_samples_leaf 1, and estimator grids 300, 500, and 1000; keep RF and GBDT the same for now.

## Checks raised

- Higher capacity may improve F₂ but can overfit rare HR events; monitor OOF F₂ and L clipped vs LRP.
- GBDT gains a search where pj-017 had fixed 200 estimators; runtime ≈ 3× per model vs single fit.
- If all grid points still have F₂ = 0, clipped L remains ∞ — pj-023 tie-break still open.

## Consequences

- Update `make_rf` / `make_gbdt` and both selection loops in S5 training script.
- Supersedes depth and sample rows in pj-016/pj-017 and grid in pj-018 for implementation; pj-022 unchanged.
