# mf-051. Numerical computation of kernel ridge in S10

- **Status:** accepted
- **Date:** 2026-11-15
- **Tags:** modeling | engineering
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

For every lambda of the grid (mf-048) the fit needs `alpha = (K + lambda I)^-1 (y - mean)` (mf-046). Measured with n = 5700: Cholesky solve for one lambda 9.7 s, one `eigh` 77 s (gives all lambda). Estimated totals: about 8.5 h with one `KernelRidge` fit per lambda, about 2.9 h with one decomposition per fit (5 inner folds x 25 outer folds, plus the final fit of each outer fold). Eigenvalues of K for c = 10 reach down to about 1e-7 (sample of 2000).

## Mathematical framing

With `K = U diag(w) U^T`, `alpha = U diag(1/(w + lambda)) U^T (y - mean)` for every lambda from one decomposition. Same solution as the Cholesky solve of `(K + lambda I) alpha = y - mean`, up to rounding.

## Options considered

1. **`KernelRidge(alpha=lambda, kernel="rbf", gamma=gamma)` per lambda, float64** — library default solver (Cholesky); about 8.5 h in total.
2. **Own decomposition with `numpy.linalg.eigh`, float64, one per fit** — all lambda from it; about 2.9 h.
3. **float32** — less memory and time; eigenvalues near 1e-7 are at the precision limit of float32.
4. **Eigenvalues:** (1) used as computed, stop with an error if any `w + lambda <= 0`; (2) negative ones clipped to 0.

## Decision

Chose **option 2** with eigenvalue treatment **(1)**. In every fit (each inner fold and the final fit of the outer fold): `K = exp(-gamma * d2)` with `d2` the squared Euclidean distances in float64 (gamma from mf-047, mf-048, mf-049); `eigh` of K in float64; for each lambda, `alpha = U diag(1/(w + lambda)) U^T (y - mean)`; prediction for a new event `K(x, train) alpha + mean` (mf-046). Eigenvalues used as computed; the run stops with an error if any `w + lambda <= 0`. The final fit of the outer fold uses the selected lambda only.

## Rationale (developer's own words)

B, I need to optimize time. For the eigenvalues: option 1.

## Checks raised

- The solution is the same as `KernelRidge`'s; a test checks agreement on a small sample.
- BLAS threads are left at the default, so the last digits may vary between runs; there is no randomness in the fit (the only seed is the inner split, mf-015).
- With lambda at least 1e-3 and rounding errors of order 1e-13, the stop condition should not trigger.

## Expected behavior and validation

Tests: agreement with `sklearn.kernel_ridge.KernelRidge(kernel="rbf")` on a small sample for several lambda; a very large lambda gives the training mean; inner held-out predictions equal a fit that excluded that fold (mf-050).

## Consequences

- Not doing: one `KernelRidge` fit per lambda, float32, clipping of eigenvalues.
- Open: reuse of the S4 folds, metrics and bootstrap.
