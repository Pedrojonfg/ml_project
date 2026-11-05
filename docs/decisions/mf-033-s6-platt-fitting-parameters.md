# mf-033. Fitting parameters of the Platt calibration in S6

- **Status:** accepted
- **Date:** 2026-11-04
- **Tags:** modeling
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

mf-031 chose Platt scaling (a, b) fitted by logistic regression of `y_hr` on the stage-1 score; mf-032 fixes the data (out-of-fold scores of the training fold, about 7100 events and 74 HR). The stage-1 classifiers use `class_weight='balanced'` (mf-011), which shifts their raw output. Installed scikit-learn is 1.9.1 (exact way to write no penalty to check in the documentation at implementation).

## Mathematical framing

Platt fits p = sigma(a*s + b) on pairs (s_i, y_i). Without sample weights it estimates the true frequency of HR given s, and b absorbs the constant shift of `balanced`; with `balanced` it would calibrate to a world with 50% HR. Smoothed targets (Platt 1999, recalled, unverified) replace 0/1 with values strictly inside (0, 1).

## Options considered

1. Penalty: none, or L2 with a fixed C.
2. Class weights: none, or `balanced`.
3. Target: 0/1, or Platt's smoothed targets.
4. Solver, `max_iter`, `tol`, intercept.
5. Non-convergence handling.

## Decision

- No penalty.
- No class weights (`class_weight=None`).
- 0/1 targets.
- `solver='lbfgs'`, `max_iter=10000`, `tol=1e-4`, `fit_intercept=True`.
- If a fit does not converge: recorded, the partial solution is used and flagged in the results (as mf-014).
- Library defaults left as they are, with no effect with lbfgs: `random_state=None`, `warm_start=False`, `n_jobs=None`, `verbose=0`, `dual=False`, `intercept_scaling=1`.

## Rationale (developer's own words)

1. No penalty: Platt only fits 2 parameters; with so many events there is no overfitting risk that justifies regularizing.
2. No weights: putting `balanced` again would correct twice, since the model was already trained with `balanced`.
3. 0/1 labels: the difference with Platt 1999 is negligible.
4. lbfgs, max_iter = 10000, tol = 1e-4, fit_intercept = True: consistent with the rest of the project.
5. Same as mf-014.

## Checks raised

- Weights: the precise reason is that `balanced` would calibrate to a 50% HR world, while no weights calibrates to the real frequency, and b absorbs the shift → developer keeps no weights.
- "Negligible difference" of the smoothed targets is not measured; with about 74 HR it could matter at the extremes → developer keeps 0/1.

## Expected behavior and validation

One fit of (a, b) per outer fold, repetition and classifier, with a convergence flag.

## Consequences

- Calibration of S6 fully specified; combination and evaluation still to decide.
