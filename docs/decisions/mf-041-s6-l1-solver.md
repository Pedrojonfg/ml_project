# mf-041. Solver of the L1 logistic model in S6 (supersedes the L1 part of mf-030)

- **Status:** accepted
- **Date:** 2026-11-04
- **Tags:** modeling
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

mf-030 chose `saga` (max_iter=10000, tol=1e-4, random_state=0) for the L1 logistic model so that L1 and L2 treat the intercept the same, and noted the cost risk. Measured at implementation on one outer training fold (7113 events, 74 HR): `saga` reached max_iter=10000 at every C tried (1e-2 to 1e4), also with tol=1e-3 and 1e-2, at 28 to 43 s per fit; at C=0.1 its solution had sum|w| 94 and intercept -22.5, against 14 and -3.7 for `liblinear`, and a lower validation AUC (0.931 against 0.944). The cost with mf-030 was about 35 hours of sequential computation. `liblinear` converged in 34 to 133 iterations, 0.5 to 2.7 s per fit.

## Mathematical framing

`liblinear` supports L1 but penalizes the intercept: it adds a constant feature of value `intercept_scaling`, and the penalty acts on its weight, so a larger `intercept_scaling` makes the intercept's penalty smaller. Measured at C=0.1: intercept -3.68 (scaling 1), -4.14 (10), -4.161 (100), -4.163 (1000); unpenalized L2 reference -4.21.

## Options considered

1. **A. Keep mf-030** (`saga`) — all L1 fits not converged; about 35 h.
2. **B. `liblinear` for L1** — converges in seconds; penalizes the intercept slightly, reducible with `intercept_scaling`.
3. **C. `saga` with other parameters** — convergence not shown; looser tolerance did not help.
4. **D. Remove L1** (change mf-021) — 6 rows instead of 9.

## Decision

Chose **B**. For the L1 logistic model: `solver='liblinear'`, `l1_ratio=1.0`, `intercept_scaling=100`, `max_iter=10000`, `tol=1e-4`, `random_state=0`, `dual=False`, `fit_intercept=True`, `class_weight='balanced'`, `warm_start=False`. If a fit does not converge: recorded, the partial solution is used and flagged (as mf-014 and mf-030). The unpenalized and L2 models stay as in mf-030. mf-030 is superseded only for the L1 solver and its inert defaults.

## Rationale (developer's own words)

liblinear for L1: saga does not converge even with a looser tolerance, so the L1 results would be partial solutions that are not a true lasso. liblinear converges in seconds and gives a similar AUC. It does penalize the intercept, but a model that converges with a minor defect is better than one that does not converge at all; the effect on the intercept can be reduced with intercept_scaling. intercept_scaling = 100: from there the intercept stabilizes, and going higher does not improve anything but increases the iterations.

## Checks raised

- The intercept of L1 is still very slightly penalized (about 0.05 from the unpenalized L2 reference at C=0.1; the two are not strictly comparable because the penalties differ) → developer accepts it.
- The reason for `saga` in mf-030 (same intercept treatment in L1 and L2) is only approximately kept.

## Expected behavior and validation

L1 fits converge in tens to hundreds of iterations; convergence flags stored per fit as before.

## Consequences

- mf-030 stays valid for the unpenalized and L2 models.
- The Parameter registry row for the L1 solver changes.
