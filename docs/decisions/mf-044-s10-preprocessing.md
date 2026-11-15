# mf-044. Preprocessing of kernel ridge in S10

- **Status:** accepted
- **Date:** 2026-11-15
- **Tags:** modeling | data
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

Kernel ridge with an RBF-type kernel compares events through distances, so the scale of each column matters (same hazard as KNN, mf-021). S4 preprocessing is fixed by mf-010. Target fixed by mf-043.

## Mathematical framing

The kernel depends on the Euclidean distance between preprocessed rows. Columns on large scales dominate the distance; standardizing puts the numeric columns on a common scale. One-hot columns take values 0/1.

## Options considered

1. **As S4 (mf-010)** — median imputer, `StandardScaler` on the 30 numeric columns, 5 one-hot columns unscaled; a category change adds 1 to the squared distance (2 if two columns change), the same as a one-standard-deviation difference in a numeric column.
2. **Scale all 35 columns** — one-hot columns get unit variance; rare categories weigh more than in option 1.
3. **No scaling** — distances in original units; large-valued columns dominate and gamma has no common meaning across columns.
4. **Numeric columns only** — categories do not enter the similarity.

## Decision

Chose **option 1**: mf-010 unchanged. Median `SimpleImputer` fit on the training fold (all 35 columns, `add_indicator=False`, `keep_empty_features=False`); `StandardScaler(with_mean=True, with_std=True)` fit on the training fold, applied to the 30 numeric columns only; the 5 one-hot columns left unscaled; no transformations. Refit on each training part (outer fold and each inner fold).

## Rationale (developer's own words)

Same as before; it is coherent with what was decided previously.

## Checks raised

- With 35 columns and about 7100 training events, distances may concentrate (flagged for KNN, mf-021); if all distances are similar, all kernel values are similar and K is almost flat. Relevant when choosing the gamma grid.
- The scaler is fit on training data only, inside every inner and outer split (leakage hazard).

## Expected behavior and validation

Same preprocessing code path as ridge, lasso and KNN (`make_preprocessor` in `src/models/linear.py`).

## Consequences

- Not doing: scaling the one-hot columns, dropping categories, other transformations.
