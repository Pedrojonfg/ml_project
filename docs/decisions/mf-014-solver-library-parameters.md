# mf-014. Solver and library parameters for the S4 regressors

- **Status:** accepted
- **Date:** 2026-11-01
- **Tags:** modeling | reproducibility
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

mf-009 sets three regressors (unpenalized, L2, L1); mf-013 sets the alpha grids and selection. Check on one training fold (repetition 0, fold 0, scikit-learn 1.9.1): the standardized design has rank 33 of 35 (condition number 2.3e16), with two exact linear dependencies (probably `risk_agg_range = risk_agg_max - risk_agg_min`, and the five one-hot columns summing to 1 with the intercept). Lasso converged at all 25 grid points with `max_iter = 10000`, `tol = 1e-4`; iteration counts: descending alpha with warm start up to 240 (2123 in total), ascending up to 6304, cold start 16327 in total. Coefficients differed by up to 1.95 between warm start and cold start (collinearity); predictions were not compared. `Ridge(solver='cholesky')` does not use `tol`.

## Mathematical framing

Unpenalized least squares has no unique solution when the design is rank-deficient; `LinearRegression` returns the minimum-norm one. Ridge has a unique solution for alpha > 0. Lasso minimises (1/2n)||y - Xw||^2 + alpha||w||_1 by coordinate descent; with collinear columns the minimiser is not unique and the iterate depends on the starting point.

## Options considered

1. Library defaults left implicit.
2. Explicit parameters per model (chosen).
3. Warm start along the alpha grid in ascending or descending order, or cold start.

## Decision

Chose **option 2**:

- Unpenalized: `LinearRegression(fit_intercept=True, positive=False, copy_X=True)`.
- Ridge: `Ridge(fit_intercept=True, solver='cholesky', positive=False, copy_X=True)`. `tol` is not set because it is unused with cholesky.
- Lasso: `Lasso(fit_intercept=True, max_iter=10000, tol=1e-4, selection='cyclic', warm_start=True, precompute=False, positive=False, copy_X=True)`.
- Grid sweep (mf-013): alpha from the largest to the smallest value, reusing one `Lasso` object along the grid within each inner fold (warm start). A new `Lasso` object for every inner fold; nothing is carried across folds.
- Final fit of an outer training fold after alpha selection: a new `Lasso` object fit directly at the selected alpha (cold start).
- Non-convergence of lasso: the alpha is recorded as not converged, the partial solution is used, and it is flagged in the results; the point is not dropped.
- `selection='cyclic'` is deterministic, so lasso needs no seed.

## Rationale (developer's own words)

Unpenalized: `fit_intercept=True` because the features are centred by StandardScaler but the target is not, so the intercept absorbs the mean of `risk_final`. With correlated features least squares is unstable, but that is deliberate: it is the unregularised baseline. Ridge: cholesky is the direct, exact and fast solution for 35 columns and needs no `max_iter` or convergence. Lasso: 10000 iterations cover the 3593 the check needed with margin; cyclic is deterministic so it needs no seed; warm start speeds up the grid sweep. Non-converged points are not discarded: non-convergence is information about that level of regularisation. Descending alpha: 240 maximum iterations against 6304 ascending, 25x faster, and starting from the most regularised model is the most stable starting point. A new object per inner fold: each fold has different data, and carrying coefficients from another fold is an arbitrary starting point that changes the solution with collinear columns. `tol` in ridge removed: it is inert with cholesky and keeping it documents a parameter that does nothing.

## Checks raised

- The design has rank 33 of 35, so the unpenalized coefficients are the minimum-norm solution among infinitely many; it is the predictions that matter and out-of-sample ones may be unstable.
- Lasso coefficients depend on the starting point and sweep order under collinearity (up to 1.95 in one coefficient between warm and cold start); the effect on `r_hat` was not measured.
- The final cold-start fit and the warm-started grid fits can give different coefficients at the same alpha.
- Iteration counts come from one fold; other folds or repetitions may need more.

## Expected behavior and validation

No ConvergenceWarning expected on the grid; any non-converged alpha appears in the results. Re-running with the same seeds gives identical coefficients (no randomness in the solvers).

## Consequences

- The sweep order is part of the specification; changing it changes results.
- Seed decision remains only for the inner split of mf-013.
- Not doing: random coordinate selection, ascending sweep, tol on ridge, carrying objects across folds.
