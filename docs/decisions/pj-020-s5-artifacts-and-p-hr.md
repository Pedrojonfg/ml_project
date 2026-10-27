# pj-020. S5 outputs — artifact names, `p_hr`, imputer flags

- **Status:** accepted
- **Date:** 2026-10-27
- **Tags:** engineering | modeling
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

R1 contracts (`docs/dependencias-y-reuniones.md`) require `results/<modelo>.json` and `preds/<modelo>.parquet` with columns `event_id`, `fold`, `p_hr`, `r_hat`. S5 fits regressors on `risk_final` (pj-014); `p_hr` must be defined without a calibrated classifier.

## Decision

1. **Model slugs:** `rf` (Random Forest), `gbdt` (`GradientBoostingRegressor`).
2. **Paths:** `results/rf.json`, `results/gbdt.json`; `preds/rf.parquet`, `preds/gbdt.parquet` (schema per team contract; metrics per pj-006–007 when bootstrap is wired).
3. **`r_hat`:** continuous log₁₀ risk prediction from the regressor (`predict`).
4. **`p_hr`:** hard HR flag from the prediction: `1.0` if `r_hat >= -6.0`, else `0.0` (float), threshold per pj-001. Not a calibrated probability (S6).
5. **`SimpleImputer` (pj-015):** `strategy="median"`, `add_indicator=False`, `keep_empty_features=False`.

## Rationale (developer's own words)

Use hard threshold for `p_hr`; name files `rf` and `gbdt`; keep sklearn imputer defaults for indicator and empty features.

## Consequences

- Parquet and JSON writers use these slugs and column semantics.
- Report prose must not call `p_hr` a calibrated probability for S5 models.
