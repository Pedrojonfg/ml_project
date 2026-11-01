# mf-013. Regularization strength selection for ridge and lasso (S4)

- **Status:** accepted
- **Date:** 2026-11-01
- **Tags:** modeling | evaluation
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

mf-009 sets L2 and L1 variants of the regressor (the unpenalized one needs no strength). mf-012 chooses the alarm line t per training fold. A check on one ridge (repetition 0) showed that MSE_HR unclipped is minimized at the smallest alpha while AP and F2 peak around alpha = 1e4; MSE_HR clipped is constant (1.16) for all alpha because no HR prediction reaches -6.001.

## Mathematical framing

Within each outer training fold, nested CV: stratified inner 5-fold on `y_hr`. For every candidate alpha, fit on the inner training part (imputer and scaler of mf-010 refit on that inner training part) and compute the average precision (AP) of r_hat versus `y_hr` on the inner validation part; the criterion is the mean of the 5 inner AP values. AP depends only on the ranking of r_hat, so it does not need t. Scikit-learn parametrisations differ: `Ridge` minimises ||y - Xw||^2 + alpha ||w||^2, `Lasso` minimises (1/2n) ||y - Xw||^2 + alpha ||w||_1; for lasso, alpha_max (all coefficients zero) was about 3.8 on a training fold.

## Options considered

1. **MSE_HR unclipped on inner validation.** Check: minimal at the smallest alpha.
2. **MSE_HR clipped on inner validation.** Check: constant, ties on the whole grid.
3. **F2 on inner validation, with t from the inner training part.**
4. **AP of r_hat vs `y_hr` on inner validation** (no t needed).
5. **MSE on all events.**

## Decision

Chose **option 4**.

- Criterion: mean over the 5 inner folds of the AP of r_hat vs `y_hr`; the highest alpha among ties.
- Ridge grid: 25 log-spaced alpha values from 1e0 to 1e6.
- Lasso grid: 25 log-spaced alpha values from 1e-4 to 1e2 (lower range because of the scikit-learn parametrisation).
- The grids are fixed; no extension. An optimum at the edge of a grid is information, not something to resolve automatically.
- After selection, the model is refit with the selected alpha on the whole outer training fold (the preprocessing refit on it); that model gives the validation predictions and the alarm line of mf-012.
- The seed and shuffle of the inner split are left to the seeds decision.

## Rationale (developer's own words)

AP measures the separation without depending on t, is always finite, and in the check it peaks where F2 peaks. The inner AP values are averaged rather than pooled, because pooling out-of-fold predictions with about 15 HR per fold mixes the score distributions of different models; the mean is more interpretable and treats each fold equally. Ties go to the highest alpha: with lasso they occur when the model is already constant, and the more regularised choice favours parsimony without losing performance. Fixed grids with no extension: if the optimum falls on an edge it is information.

## Checks raised

- The inner folds have about 59 training HR and about 15 validation HR; the AP of one fold is noisy.
- With lasso, 6 of the 25 grid points lie above alpha_max (constant model, AP equal to the base rate) and add nothing; kept as the developer decided.
- AP is a new metric for model selection, not one of the reported metrics (pj-007); F2, MSE_HR and L remain the reported ones.
- MSE_HR unclipped favours less regularisation and does not look at false alarms (check on ridge, repetition 0).
- The lasso solver may need many iterations at small alpha (up to 3593 at alpha = 1e-3); solver settings are decided separately.
- Selection of alpha and of t (mf-012) are chained: alpha is chosen without t.

## Expected behavior and validation

The selected alpha is stored per outer fold, repetition and penalty, so its variability can be inspected. Edge selections are reported, not corrected.

## Consequences

- Cost per model and repetition: 25 alpha x 5 inner folds x 5 outer folds, plus 5 refits.
- Not doing: criterion on F2 or MSE_HR, pooled inner predictions, grid extension.
