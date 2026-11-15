# mf-050. Alarm line of kernel ridge in S10

- **Status:** accepted
- **Date:** 2026-11-15
- **Tags:** modeling | evaluation
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

mf-012 fixes the alarm line criterion for the S4 regressors: t maximizes F2 on training-fold predictions, candidates = r_hat of the training HR events, ties to the median. Kernel ridge can nearly memorize the training events (small lambda against the eigenvalues of K), so in-sample r_hat may be close to `risk_final` while predictions for new events are shrunk (understanding record S10, questions 8, 8b, 13). The selection of lambda (mf-048) already produces held-out predictions in the 5 inner folds.

## Mathematical framing

The line t is a threshold on r_hat. It is calibrated for the distribution of r_hat it will meet: predictions of events the model has not been fit on.

## Options considered

1. **In-sample predictions of the final model on its training events (mf-012 unchanged)** — each event weighs on its own prediction; no extra cost.
2. **Leave-one-out predictions** — each event predicted by a model fit without it; closed form `(y_i - f(x_i)) / (1 - H_ii)` with `H = K (K + lambda I)^-1` from the diagonalization of the final fit; with the centering of mf-046 the formula is approximate (the mean includes the left-out event; error of order 1/n).
3. **Held-out predictions of the 5 inner folds with the selected lambda** — each event predicted by a model fit on the other 4 inner folds (80% of the outer training fold), with its own m and mean (mf-049, mf-046); `c = 10`; exact; reuses the selection computations.

## Decision

Chose **option 3**. In each outer fold, the training r_hat used for the alarm line are the held-out predictions of the 5 inner folds (`StratifiedKFold(5, shuffle=True, random_state=0)`, mf-015), each fit with the selected lambda (mf-048), its own m (mf-049) and its own training mean of y (mf-046). With them, t follows mf-012: maximizes F2, candidates = held-out r_hat of the HR events of the outer training fold, ties to the median. Validation predictions come from the model refit on the whole outer training fold (mf-048); alarm if r_hat >= t.

## Rationale (developer's own words)

C, because it is more exact than B.

## Checks raised

- The same held-out predictions select lambda and calibrate t.
- Inner models are trained on 80% of the outer training fold and the final model on 100%, so the distribution of r_hat may differ somewhat between them.
- t depends on the seed of the inner split.
- All predictions used for t come from the outer training fold only (no leakage from validation).
- Avoids the risk of option 1 (t calibrated on memorized r_hat).

## Expected behavior and validation

Stored per fold and repetition: selected lambda, t, and the number of held-out predictions used. Test: no outer validation event enters the computation of t; held-out predictions of the inner folds equal the predictions of a fit that excluded that inner fold.

## Consequences

- Not doing: in-sample alarm line, leave-one-out closed form.
- Open: library parameters and numerical details, compute budget.
