# mf-010. Preprocessing for S4 linear models

- **Status:** accepted
- **Date:** 2026-11-01
- **Tags:** modeling | data
- **Decided by:** Mario
- **AI involvement:** opinion requested

## Context

pj-010 left remaining feature NaNs to S4 per-fold imputation. L1 and L2 penalties (mf-009) depend on feature scale. v1 has 35 columns in `FEATURE_COLUMNS` order: 30 numeric and 5 one-hot `c_object_type` (pj-011). Profiling the 8892 events found 0 NaN in all 35 columns; non-risk features are not log10 (`miss_distance` 19..66828, `relative_speed` 49..17018, `t_weighted_rms` 0.5..2.9); risk features have 6-61 % of events at the -30 floor in several columns.

## Mathematical framing

Per training fold: impute each column with its training-fold median, then standardize the 30 numeric columns to zero mean and unit variance using training-fold statistics; the 5 one-hot columns stay in {0, 1}. Validation data is only transformed with those training statistics. With unit variance on all numeric columns, an L1 or L2 penalty weights their coefficients on a common scale.

## Options considered

1. **Imputation:** median, mean or constant, missing indicator, dropping events.
2. **Scaling:** StandardScaler, robust scaling (median, IQR), min-max, none; with or without scaling the one-hot columns.
3. **Transformations:** none, or log / other on non-log10 columns.

## Decision

- Imputation: `SimpleImputer`, strategy `median`, fit on the training fold, applied to all 35 columns (safeguard; 0 NaN observed).
- Scaling: `StandardScaler`, fit on the training fold, applied to the 30 numeric columns only; the 5 one-hot columns are left unscaled.
- Transformations: none.
- Library parameters set explicitly: `StandardScaler(with_mean=True, with_std=True)`; `SimpleImputer(add_indicator=False, keep_empty_features=False)`.

## Rationale (developer's own words)

Median imputation as a safeguard, because it is robust to outliers and skew. StandardScaler on the 30 numeric columns gives a uniform scale across columns, so L1 and L2 penalize coefficients equitably. No transformations, because there is no hypothesis justifying added complexity. `with_mean` and `with_std` True because that is the reason to use StandardScaler. `add_indicator=False` because there are no NaN and indicators would create empty features. `keep_empty_features=False` because a column with no observed values adds nothing.

## Checks raised

- The claim "all 30 features are log10 plus one-hot" was wrong: only the risk features are log10; the others are in metres or speed units. Corrected to 35 columns (30 numeric + 5 one-hot); developer keeps no transformations.
- Imputation does nothing on current data (0 NaN); kept as a safeguard.
- The raw std of risk columns (about 7.5-9.5) was cited as reason for StandardScaler, but after scaling all numeric columns have unit variance by construction; the equitable-penalty argument rests on that.
- Standardization does not change the shape of the risk features (a mass at -30 plus a continuous tail); linear models see it as is.
- One-hot columns stay in {0, 1} while numeric columns have unit variance, so L1 and L2 penalize them on a different scale.
- With `keep_empty_features=False`, a column with no observed values in a training fold is dropped and the column count changes across folds; not triggered with the current data.
- Robust scaling was discussed (IQR is positive in all risk columns, 6.6-21.5); developer chose StandardScaler.

## Expected behavior and validation

Imputer and scaler are fit on each training fold only (no leakage); validation events never influence them. No NaN reaches any model; numeric columns of the training fold have mean 0 and variance 1 after scaling.

## Consequences

- Unpenalized models are unaffected in predictions by scaling (affine reparametrization); penalized ones are not.
- Not doing: transformations, robust scaling, missing indicators, scaling of one-hot columns.
