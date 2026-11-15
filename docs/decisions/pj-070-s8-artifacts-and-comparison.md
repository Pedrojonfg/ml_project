# pj-070. S8 artifacts, slugs, and bake-off comparison

- **Status:** accepted
- **Date:** 2026-11-15
- **Tags:** evaluation | engineering
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

S5 defines slugs, `results/` + `preds/` layout, and `p_hr` from `r_hat` (`pj-020`). S8 shares the same task/alarm (`pj-062`) and should sit on the same bake-off protocol (`pj-006`, `pj-007`).

## Options considered

1. Mirror S5: slugs `mlp` / `gru`; `results/<slug>.json` + `preds/<slug>.parquet`; bootstrap BCa as S1/S4/S5; compare under the same metric dashboard vs LRP (and CRP where other tables do).
2. Different artifact schema or uncertainty protocol for S8 only.
3. Other / none.

## Decision

Chose **option 1** with slugs **`mlp`** (tabular) and **`gru`** (sequence).

| Item | Value |
|------|-------|
| Slugs | `mlp`, `gru` |
| Paths | `results/mlp.json`, `results/gru.json`, `preds/mlp.parquet`, `preds/gru.parquet` |
| Parquet columns | `event_id`, `fold`, `r_hat`, `p_hr` (contract as S5); repetition handled as in existing preds writers |
| `p_hr` | `1.0` if `r_hat >= -6.0` else `0.0` (`pj-062`) |
| Metrics | F₂, MSE_HR, L per `pj-007` |
| Uncertainty | same bootstrap / BCa protocol as other model rows (`pj-006` and S4/S5 wiring) |
| Comparison | same bake-off framing as other regressor rows vs LRP (and CRP when the table includes it) |

## Rationale (developer's own words)

OK to do it like S5 with the small slug/naming change proposed — consistency.

## Checks raised

- No protocol reason to treat S8 uncertainty differently — developer accepted consistency.
- Whether W2 prose puts MLP/GRU in the main table or an appendix is writing-scope, not this ADR.

## Expected behavior and validation

- Pred files joinable with S5 preds on `event_id` / fold schema.
- JSON metrics comparable side-by-side with `rf` / `gbdt` / linear rows.

## Consequences

- Auto-trivial engineering may place `src/models/` modules and `scripts/run_s8.py` without a further modeling ADR.
- Dependency: add `torch` to the environment with an explicit version in requirements when implementing (advise/dependencies — pin in the implementation commit).
