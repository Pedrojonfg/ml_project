# mf-020. Bootstrap implementation details and inert library defaults (S4)

- **Status:** accepted
- **Date:** 2026-11-01
- **Tags:** modeling | evaluation | reproducibility
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

The Stage 4 audit of S4 found choices in the code that no ADR registered: the interpolation method of the BCa percentiles, the application of the mf-017 cap beyond the resamples, and library defaults that are inert for the registered settings. None changes the current results.

## Mathematical framing

BCa endpoints are quantiles of the bootstrap distribution; `np.quantile` interpolates linearly between order statistics by default. The mf-017 cap is a finite replacement of an infinite per-repetition L; the original-sample estimate and the leave-one-event-out jackknife values are statistics of the same family, so the same cap keeps them finite.

## Options considered

1. **Register the implementation as it is.**
2. **Choose another quantile interpolation method or restrict the cap to the resamples.**

## Decision

Chose **option 1**:

- BCa endpoints: `np.quantile(boot, p, method="linear")`.
- The mf-017 cap (per model, per repetition, before averaging) is also applied to the original-sample estimate and to the jackknife values, with the same per-model cap. With the current data it has no effect (F2 > 0 in every repetition of the original sample).
- Library defaults left unchanged and recorded as inert for the registered settings: `LinearRegression(n_jobs=None, tol=1e-06)`; `Ridge(max_iter=None, random_state=None, tol=1e-04)` (unused by the `cholesky` solver); `SimpleImputer(missing_values=nan, fill_value=None, copy=True)`; `StandardScaler(copy=True)`.

## Rationale (developer's own words)

"Sí, registrar": the implemented details are registered as they are.

## Checks raised

- The interpolation method changes the interval endpoints only slightly with B = 10000; its effect was not measured.
- The imputer of S4 comes from the S5 helper `make_imputer` (`src/models/trees.py`); its values equal mf-010 today, but a change of pj-015 would change S4.
- The scaler selects columns by position 0..29; if `keep_empty_features=False` dropped an empty column the positions would shift (not triggered: 0 NaN in the training data).
- If no finite L exists, the L point estimate stays infinite in the JSON (mf-019); not triggered.

## Expected behavior and validation

Results are unchanged by this ADR; the tests of `src/evaluation.py` and `src/models/linear.py` keep passing.

## Consequences

- Not doing: another interpolation method, restricting the cap to the resamples.
