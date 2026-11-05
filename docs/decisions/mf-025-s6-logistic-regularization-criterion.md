# mf-025. Selection criterion for the logistic regularization strength in S6

- **Status:** accepted
- **Date:** 2026-11-04
- **Tags:** modeling
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

mf-021 chose three logistic classifiers for stage 1 (unpenalized, L2, L1). The unpenalized one has no regularization strength. For the S4 regressors alpha was selected by inner 5-fold CV with the AP criterion (mf-013, mf-015); nothing is decided yet for the logistic models. About 74 HR per training fold (mf-012), so about 15 HR per inner fold.

## Mathematical framing

For L2 and L1 the strength (C = 1/lambda in scikit-learn) is chosen inside each outer training fold by inner cross-validation. AUC is the probability that a random HR event gets a higher score than a random non-HR event; it measures ordering only, is invariant to any increasing transform of the score, and weights all pairs equally.

## Options considered

1. **A. Fixed value, no selection** — no inner validation; the value has no data behind it.
2. **B. Inner CV, AP criterion** (as mf-013) — ordering with emphasis on the top of the list.
3. **C. Inner CV, AUC criterion** — ordering over all pairs.
4. **D. Inner CV, log-loss criterion** — probability quality; depends on the shift from `class_weight='balanced'`.
5. **E. Inner CV, F2 criterion** — final metric; depends on the alarm line and is a step function.

## Decision

Chose **C**: for the L2 and L1 logistic models, the regularization strength is selected by inner cross-validation inside each outer training fold, with the AUC of the stage-1 score against `y_hr` as criterion.

## Rationale (developer's own words)

It measures the ordering, and weighting the whole list equally is the best decision.

## Checks raised

- About 15 HR per inner fold make any criterion noisy → none, developer keeps C.
- AUC ignores the value of the scores, so the selection does not account for the shift from `class_weight='balanced'`; correcting it is left to calibration.

## Expected behavior and validation

One selected strength per outer training fold, repetition and penalty (L2, L1).

## Consequences

- Still to decide: grid of values, tie rule, inner split and its seed (whether mf-015 applies), solver and library parameters.
