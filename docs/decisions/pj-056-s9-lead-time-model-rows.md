# pj-056. S9 lead-time curve — model rows and re-selection

- **Status:** accepted
- **Date:** 2026-11-14
- **Tags:** evaluation | modeling
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

S9 lead-time curve at `t_cut ∈ {2, 3, 4}` (`pj-054`) with v1 features per cut (`pj-055`). W1 internal bake-off already reports LRP, S4 magnitude regressors, and S5 trees under S1 CV (`pj-035`, `pj-036`). S5 hyperparameter pick uses lowest pooled out-of-fold **L unclipped** (`pj-025`). S4 ridge/lasso α uses inner-CV AP (`mf-013`); row comparison still uses the same L / F₂ dashboard (`pj-007`).

## Options considered

**Rows on the curve**

1. **LRP + GBDT only**
2. **LRP + RF + GBDT**
3. **LRP + GBDT + one S4 magnitude regressor**
4. **Full W1 Table-2 set (no S6)**
5. **LRP only on the curve**

**Hyperparameters at `t_cut ∈ {3, 4}`**

- **Freeze** GBDT and S4 choices from the `t_cut = 2` run.
- **Re-run** the same selection protocols on each cut’s cohort and features.

**Which S4 regressor (if a single series)**

- Fixed slug (e.g. ridge).
- **Best at each cut** among a defined candidate set by the bake-off metric.

## Decision

- **Rows:** **LRP**, **GBDT**, and **one S4 magnitude regressor** — option 3.
- **S4 candidate set:** `{ols, ridge, lasso}` magnitude regressors only (same families as the W1 bake-off linears; KNN and logistic excluded from this selection).
- **S4 row shown at each `t_cut`:** the candidate with **lowest pooled OOF L unclipped** at that `t_cut` (same aggregation as `pj-025` / stored results). Caption or table notes **which slug won** at each point (the plotted “linear” series may switch family across cuts).
- **Hyperparameters:** **re-run** full selection on each cut — GBDT `n_estimators` grid and tree params per `pj-024`/`pj-025`; each linear candidate with `mf-013` α selection on that cut’s training folds. No carrying α or `n_estimators` from `t_cut = 2` to later cuts.

**Tie-break when two candidates share the same L unclipped (within float tie):** higher **F₂**; if still tied, lexicographic order of model slug.

## Rationale (developer's own words)

Use the linear row that performs best, and re-run selection at each cut to stay faithful to the data available at that lead time — not frozen settings from the 2-day window.

## Checks raised

- The lead-time figure is **three** series, but the winning linear slug may change between cuts → caption must name the slug per `t_cut`.
- Three linear full S4 runs per cut plus one GBDT run × 3 cuts = heavier than a single frozen slug; accepted for fidelity.
- RF is omitted from the curve (option C); RF numbers remain in the main bake-off only.
- S6 combinations are out of scope for this curve unless a later ADR adds them.

## Expected behavior and validation

- At `t_cut = 2`, cohort and protocol match the main internal bake-off (8 892 events); GBDT/LRP should be numerically consistent with existing `results/*.json` if code paths match.
- Store per-cut artifacts: `results/s9_leadtime_t{t}_*.json` (or equivalent) with winning S4 slug recorded.

## Consequences

- Implementation runs `protocol` cohort mask + features + S4/S5 pipelines with `ttc_min=t_cut`.
- Parameter registry updated for S9 model rows and re-selection policy.
- Next ADRs: primary y-axis metric, LMO scheme, W2 deliverables.