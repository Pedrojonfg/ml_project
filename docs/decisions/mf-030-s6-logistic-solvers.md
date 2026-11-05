# mf-030. Solvers and library parameters of the logistic models in S6

- **Status:** accepted (the L1 solver part is superseded by mf-041)
- **Date:** 2026-11-04
- **Tags:** modeling
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

mf-021 chose three logistic models (unpenalized, L2, L1) with `class_weight='balanced'` (mf-011). Installed scikit-learn is 1.9.1, where `penalty` is deprecated and the penalty is set through C and l1_ratio (exact form to check in the documentation at implementation). For the S4 lasso: `max_iter=10000`, `tol=1e-4`; if it does not converge the alpha is recorded, the partial solution used and flagged (mf-014).

## Mathematical framing

The solver is the algorithm that searches the coefficients. `lbfgs` is deterministic and supports L2 and no penalty; `saga` supports L1 without penalizing the intercept and is stochastic. Without penalty and under perfect separation the maximum does not exist and no solver converges.

## Options considered

1. **A. lbfgs for unpenalized and L2, liblinear for L1** — liblinear also penalizes the intercept.
2. **B. lbfgs for unpenalized and L2, saga for L1** — saga is stochastic.
3. **C. saga for the three** — all stochastic and slower.

## Decision

Chose **B**.

- Unpenalized and L2: `solver='lbfgs'`. L1: `solver='saga'`.
- `max_iter=10000`, `tol=1e-4` for both solvers (as the S4 lasso, mf-014).
- `random_state=0` (used by saga; lbfgs does not use it).
- `warm_start=False`.
- `fit_intercept=True`.
- If a fit does not converge: the C is recorded as not converged, the partial solution is used and flagged in the results; the point is not dropped (as mf-014).
- Library defaults left as they are, with no effect with these solvers: `intercept_scaling=1`, `dual=False`, `n_jobs=None`, `verbose=0`.

## Rationale (developer's own words)

lbfgs is deterministic and works well for L2. For L1 I use saga because I want L1 and L2 to treat the intercept the same. max_iter and tol as in S4. random_state = 0, consistent with the rest of the project. warm_start=False, simpler. Non-convergence as in mf-014. fit_intercept = True, because a logistic regression needs an intercept.

## Checks raised

- Unpenalized fits may not converge under separation → non-convergence policy as mf-014.
- saga with `tol=1e-4` and `max_iter=10000` can be slow: 25 values x 5 inner folds x 5 outer folds x 5 repetitions = 3125 fits for L1 → developer keeps the values and will see the cost at implementation.
- The exact way to write each penalty in 1.9.1 is to be checked against the documentation at implementation.

## Expected behavior and validation

Non-convergence flags stored per fit; lbfgs results identical across runs; saga results identical across runs with `random_state=0`.

## Consequences

- Stage-1 classifier fully specified once the calibration decisions are taken.
