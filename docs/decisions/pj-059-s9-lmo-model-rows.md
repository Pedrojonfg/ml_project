# pj-059. S9 LMO — model rows and training window

- **Status:** accepted
- **Date:** 2026-11-14
- **Tags:** evaluation | modeling
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

Leave-mission-out uses 19 folds (`pj-058`). The lead-time curve already fixes model rows and per-cut re-selection: LRP, GBDT, and the best among `{ols, ridge, lasso}` by pooled OOF **L unclipped**, with full hyperparameter selection at each `t_cut` (`pj-056`). LMO is the main internal bake-off at the standard input window (`time_to_tca ≥ 2`, `pj-003`).

## Options considered

**Model set per LMO fold**

1. **Same triad as the lead-time curve** — LRP + GBDT + best linear among `{ols, ridge, lasso}`.
2. **LRP + GBDT only** — drop the linear row.
3. **Full W1 Table-2 models** — every fold retrains all bake-off rows.

**Usable CDM threshold for LMO**

- **`t_cut = 2`** only (same as the primary bake-off).
- Run LMO at each lead-time cut (19×3 expensive).

## Decision

- **Models:** **option 1** — same triad and rules as `pj-056`:
  - LRP recomputed on train/test split per fold.
  - GBDT with full S5 grid selection (`pj-024`, `pj-025`) fit on train mission union, evaluated on held-out mission.
  - Train all three magnitude regressors `{ols, ridge, lasso}`; **report the candidate with lowest L unclipped on the held-out mission** (ties per `pj-056`).
  - Re-run selection on each LMO fold (no frozen hyperparameters from event-CV or from other missions).
- **Window:** **`t_cut = 2`** only for LMO (not the `{3, 4}` grid).

## Rationale (developer's own words)

Use the same triad; there is no reason to do otherwise.

## Checks raised

- Held-out missions can be small (minimum 4 events) or HR-free → selection unstable; zero-HR folds handled in `pj-060`.
- Train size varies (one mission removed); HR count on train drops when a high-HR mission is held out.
- Linear α selection still uses AP (`mf-013`); winning linear among three still by L on the held-out mission (as on the lead-time curve).

## Expected behavior and validation

- One JSON/table block per mission with metrics for LRP, GBDT, and winning linear slug (or skipped per `pj-060`).
- Optional summary across missions: only non-skipped folds.

## Consequences

- Primary metric for LMO presentation defaults to the same as the lead-time figure unless a later ADR overrides (`pj-057`: L unclipped, with F₂ revision trigger).
- Does not replace event-level repeated CV results in `results/*.json`.