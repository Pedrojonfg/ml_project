# mf-047. Intercept handling of kernel ridge in S10

- **Status:** accepted
- **Date:** 2026-11-15
- **Tags:** modeling
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

scikit-learn's `KernelRidge` has no intercept (parameters checked in sklearn 1.9.1: alpha, kernel, gamma, degree, coef0, kernel_params). Without one, far from the training events `f(x) = sum_i alpha_i k(x_i, x)` tends to 0. In the 8892 events `risk_final` has mean -26.6, median -30 (the minimum value), maximum -2.7, and 93 events with `risk_final >= -6`. Target mf-044, preprocessing mf-045, kernel mf-046.

## Mathematical framing

The RBF is local: for an event far from all training events every `k` is close to 0, so the prediction is the baseline level of the model. Without intercept the baseline is 0, above every observed `risk_final`; with the training mean as baseline it is about -26.6.

## Options considered

1. **No intercept, no centering** — baseline 0; far events are predicted above the maximum observed risk, hence above any alarm line near -6.
2. **Subtract the training mean of `y`, add it back to the predictions** — baseline = training mean; the penalty acts on deviations from it. Not equal to a jointly estimated unpenalized intercept, because the `x` are not centered.
3. **Jointly estimated unpenalized intercept** — `b` fit together with `alpha` (closest to `fit_intercept=True` in the S4 ridge); needs a bordered linear system solved by hand.
4. **Subtract another constant fixed by the developer** (for example the training median, currently -30) — same mechanism as option 2 with a different constant.

## Decision

Chose **option 2**. In every fit, `y` is centered with the mean of the `y` of the training part used for that fit; `KernelRidge` is fit on `y - mean`; the mean is added back to the predictions. This is applied inside each inner fold of the hyperparameter selection and in the final fit on the outer training fold, each with the mean of its own training part. The `x` are not centered beyond mf-045.

## Rationale (developer's own words)

Chosen mostly by elimination. I discarded option 1 because tending to 0 would probably cause false alarms (not sure); I think options 3 and 4 are too complex.

## Checks raised

- Option 1 and false alarms: mathematically true in the limit of events far from the training events; how many validation events are in that regime depends on gamma and on the alarm line t (mf-012), not measured. A small diagnostic on training-only data was offered and not run.
- Option 4 uses the same mechanism as option 2 (subtract a constant, add it back), only with a different constant; option 3 is the more complex one.
- The centering constant is computed on training data only (leakage hazard).
- With the mean as baseline, events far from the data get `r_hat` near -26.6, so they cannot raise an alarm; missed HR events in sparse regions are the consequence to look at.

## Expected behavior and validation

Test: with a very large lambda the prediction equals the training mean for every event; predictions for an event far from all training events approach the mean. Both follow from the framing above.

## Consequences

- Not doing: jointly estimated intercept, other constants, centering of the `x` beyond mf-045.
- Open: gamma parametrization and grid, selection of lambda and gamma, alarm line, compute budget.
