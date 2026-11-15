# mf-048. Rule for gamma of kernel ridge in S10

- **Status:** accepted
- **Date:** 2026-11-15
- **Tags:** modeling
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

RBF kernel `k(a,b) = exp(-gamma ||a-b||^2)` (mf-046) on the 35 columns preprocessed as in mf-045. Measured on a random sample of 2000 events (seed 0): the squared Euclidean distance between two events has percentiles 5/25/50/75/95 = 17/36.7/56.1/79.8/121.7; to the nearest neighbour 0.77/3.86/10.94 (5th/50th/95th percentile). Kernel value for a typical pair (squared distance 56): 0.95 for gamma 0.001, 0.57 for 0.01, 0.004 for 0.1, about 0 for 1.

## Mathematical framing

gamma sets how fast similarity decays with squared distance; its useful range depends on the scale of the squared distances, which depends on the data of each fold. A rule `gamma = c / m`, with `m` a data-based scale of the squared distances, makes `c` a pure number independent of that scale.

## Options considered

1. **Fixed grid of gamma values chosen by the developer, selected by inner validation together with lambda** — each gamma needs its own K and decomposition in every inner fold.
2. **Rule from the data: `gamma = c / m`, `m` = median squared distance of the training part, `c` fixed or in a small grid** — gamma adapts to the scale of each fold; adds a median computation to every fit.
3. **scikit-learn default `gamma = 1/n_features = 1/35`, not tuned** — one gamma for all folds; between the 0.01 and 0.1 rows of the table above.
4. **A single gamma fixed by the developer, not tuned** — same as 3 with the developer's value.

## Decision

Chose **option 2**. In every fit, `gamma = c / m`, with `m` the median of the squared Euclidean distances between events of the training part of that fit, computed on the rows preprocessed as in mf-045; `KernelRidge(kernel="rbf", gamma=gamma)`. The values of `c` and the exact computation of `m` are left to the next decision.

## Rationale (developer's own words)

I think it is the option where gamma adapts best.

## Checks raised

- The median adapts gamma to the scale of each fold, but it does not say which `c` to use; `c` remains a free parameter.
- With `c = 1`, a pair at the median squared distance has kernel value `e^-1`.
- `m` must be computed on the training part of each fit only (leakage hazard).
- Whether `m` uses all pairs or a subsample is open.

## Expected behavior and validation

Test: gamma scales inversely if the preprocessed rows are multiplied by a constant factor with `c` fixed (kernel values stay equal); `m` is computed from the training part only.

## Consequences

- Not doing: fixed absolute gamma grid, sklearn default gamma, a single fixed gamma.
- Open: alarm line, library parameters and numerical details, compute budget (`c`, `m` and the selection are in mf-049 and mf-050).
