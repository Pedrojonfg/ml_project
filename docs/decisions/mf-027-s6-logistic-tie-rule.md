# mf-027. Tie rule for the logistic regularization strength in S6

- **Status:** accepted
- **Date:** 2026-11-04
- **Tags:** modeling
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

mf-025 selects C by inner 5-fold CV with the AUC criterion; mf-026 fixes the grids (C = 1/lambda: a larger C is a weaker penalty). For the S4 regressors the tie rule was the highest alpha, the strongest penalty (mf-013). About 15 HR per inner fold.

## Mathematical framing

Let AUC_k(C) be the AUC on inner fold k = 1..5, mean(C) their mean, C* the grid value with the highest mean, s the sample standard deviation (divisor 4) of AUC_k(C*), and SE = s / sqrt(5). The tie set is {C : mean(C) >= mean(C*) - SE}.

## Options considered

1. **A. Exact equality of the mean AUC** — rarely acts.
2. **B. Fixed tolerance on |AUC - max AUC|** — acts more often; the tolerance is a new parameter.
3. **C. Within one standard error of the maximum** — the tolerance comes from the data; large when the inner folds hold few HR.

And the choice among the tied values: the smallest C (the strongest penalty), chosen earlier in this session.

## Decision

Chose **C** with the smallest C of the tie set.

- SE: sample standard deviation (divisor 4) of the 5 inner-fold AUCs of the candidate with the highest mean AUC, divided by sqrt(5).
- Selected C: the smallest C in {C : mean(C) >= mean(C*) - SE}.

## Rationale (developer's own words)

I prefer the most penalized one because it produces smaller coefficients, which gives a simpler and more stable model. That the rule acts more when there are few events per fold is coherent with preferring simpler models when the data cannot distinguish between candidates.

## Checks raised

- Option C changes which model is selected, not only the tie-breaking → developer keeps C.
- If the SE is large, the tie set can extend to very strong penalties; with L1, an empty model (AUC 0.5) enters the tie set only if 0.5 >= max mean - SE.

## Expected behavior and validation

For every outer training fold, repetition and penalty: store C*, SE, the size of the tie set and the selected C.

## Consequences

- Still to decide: treatment of an optimum at a grid edge, inner split and seed (whether mf-015 applies), solver and library parameters.
