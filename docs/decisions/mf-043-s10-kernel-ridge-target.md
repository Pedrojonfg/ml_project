# mf-043. Target of kernel ridge in S10

- **Status:** accepted
- **Date:** 2026-11-15
- **Tags:** modeling
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

S10 adds kernel ridge as one more row of the S4 table (docs/plan-reparto.md). Understanding for kernel ridge done on 2026-11-15 (docs/understanding/mf.md, "S10: kernel ridge (RBF)"). The target of the S4 regressors is fixed by mf-008; S5 trees use a training-target floor c (pj-026). IDs mf-021..mf-042 are taken (KNN on scope/s4-knn; S6 on scope/s6-*), so S10 starts at mf-043.

## Mathematical framing

Kernel ridge minimizes the squared error on `risk_final` plus lambda times the squared norm of the function in the kernel's space. The loss is the same squared error as OLS, ridge and lasso, so the S4 rows share the objective and differ only in the function class and the penalty.

## Options considered

1. **`risk_final` untransformed, all events (mf-008)** — assumes squared error on the log10 risk scale is the quantity to minimize; the S10 row is comparable with OLS, ridge, lasso and KNN.
2. **`risk_final` with a floor c on the training target (as S5, pj-026)** — assumes very low risks add little and dominate the fit; trains on a clipped version of `y`, so it differs from the S4 rows in its target.
3. **HR classifier** — assumes only high risk or not matters; gives no `r_hat`, so MSE_HR and L = MSE_HR/F2 cannot be computed.

## Decision

Chose **option 1**. Kernel ridge predicts `risk_final` untransformed, on all 8892 events (mf-008); continuous `r_hat`, giving F2, MSE_HR and L like the other S4 rows.

## Rationale (developer's own words)

It predicts the same target as ridge and lasso; it is the most coherent with the decisions taken before.

## Checks raised

- In S4, a floor on the target gave F2 = 0 (c in [-25, -7]) or compressed `r_hat` (c = -6.09) for the linear models (mf-008 reopened and confirmed); that evidence is not about kernel ridge.
- With a local kernel such as RBF, predictions for events far from the training events approach the intercept, so `r_hat` may stay far from -6 at least as much as in the linear models (information, not a veto).
- Choosing between options 1 and 2 by looking at validation numbers would tune the target on the evaluation folds; any such comparison would have to be fixed before seeing results.

## Expected behavior and validation

One more row in the S4 table with the same event bootstrap and paired differences against LRP (pj-006, mf-016..mf-020).

## Consequences

- Not doing: floor on the target, HR classifier (kernel logistic), HR-only training.
- Remaining S10 decisions: preprocessing, kernel family, kernel parameters, intercept, selection of lambda and gamma, alarm line, compute budget.
