# pj-065. S8 preprocessing — median impute + StandardScaler (fold-fit)

- **Status:** accepted
- **Date:** 2026-11-15
- **Tags:** modeling | data | preprocessing
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

S8 tabular MLP and masked GRU (`pj-061`, `pj-064`) take numeric inputs where column scales differ sharply (`mf-010` notes miss_distance / relative_speed vs risk floors). S5 uses per-fold median imputation only (`pj-015`); trees do not require scaling. S4 linear models use median imputation plus `StandardScaler` on the 30 numeric columns, leaving one-hot `c_object_type` unscaled (`mf-010`).

## Mathematical framing

For each CV training fold, per-column medians are estimated and applied, then numeric features are standardized to zero mean and unit variance using training-fold statistics only. Validation (and any inner-val split) is transformed with those frozen statistics — no leakage. One-hot columns stay in {0, 1}. The same fold-fit impute+scale discipline applies to sequence channels (statistics from training-fold observations only).

## Options considered

1. **S5-literal:** median per-fold, no scaler — full tree consistency; raw scales into the net.
2. **S5 impute + S4-style StandardScaler** — shared missing-value rule plus scaled numerics for gradient-based models.
3. **Different pipelines per arm**
4. **Other / none**

## Decision

Chose **option 2**: both S8 arms use **median imputation** (`pj-015` spirit) and **`StandardScaler` on numeric columns only** (`mf-010` spirit), fit on the training fold only.

## Rationale (developer's own words)

B — consistency, but a good result for these models.

## Checks raised

- Literal S5 has no scaler; choosing B prioritizes NN-friendly scales while keeping the median imputer — developer accepted.
- Exact sequence-channel statistic aggregation (per CDM step vs per event) must not peek at validation events — implementation detail bound by this ADR's no-leakage rule.
- Library kwargs to pin later if not listed: e.g. `SimpleImputer(strategy="median")`, `StandardScaler(with_mean=True, with_std=True)` as in `mf-010`.

## Expected behavior and validation

- No NaNs reach MLP/GRU inputs after the fold pipeline.
- After scaling, training-fold numeric columns have mean ≈ 0 and variance ≈ 1; one-hots remain {0, 1}.
- Validation folds never influence imputer/scaler fits.

## Consequences

- Parameter registry inherits imputer/scaler choices aligned with `pj-015` / `mf-010`.
- Training and architecture ADRs still fix network and optimizer values.
