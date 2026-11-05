# mf-026. Grids of the logistic regularization strength in S6

- **Status:** accepted
- **Date:** 2026-11-04
- **Tags:** modeling
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

mf-025 selects the strength of the L2 and L1 logistic models by inner CV with the AUC criterion. In scikit-learn the strength is C = 1/lambda; the minimized objective is 0.5*||w||^2 + C*sum(loss) for L2 and ||w||_1 + C*sum(loss) for L1. About 8900 events (the `balanced` weights sum to n).

## Mathematical framing

The grid is the finite set of C values the inner CV can choose from. Spacing in log C gives equal resolution per factor of 10. L2 never sets coefficients to zero. L1 has a threshold C_min below which all coefficients are zero.

## Options considered

1. **A. One log-spaced grid common to L2 and L1** — same range for both penalties.
2. **B. Different log-spaced grids for L2 and L1** — a range per penalty.
3. **C. Linear grid** — concentrates the points on large C.

## Decision

Chose **B**.

- L2: `np.logspace(-4, 4, 25)` (C from 1e-4 to 1e4, 25 values, 3 per decade).
- L1: `np.logspace(-2, 4, 25)` (C from 1e-2 to 1e4, 25 values, 4 per decade).

## Rationale (developer's own words)

L2 (ridge) shrinks but never zeroes coefficients, so the optimum may fall in any regularization regime; a symmetric range of 8 decades around C = 1 covers from dominant penalty (1/(C*n) about 1) to negligible penalty, with about 3 points per decade. L1 (lasso) has a threshold C_min below which all coefficients are zero and the model is trivial; with n about 8900 that threshold should fall about one order of magnitude low, so starting at 1e-2 avoids spending too much budget on empty models and concentrates the 25 points in 6 decades where L1 moves between sparsity and the full model (about 4 points per decade, more resolution than L2 where it matters). To be checked at implementation with `l1_min_c`. Both grids contain C = 1 in their interior, so if it turns out best the validation will find it without fixing it a priori.

## Checks raised

- The claim that C_min of L1 falls below 1e-2 is a hypothesis, to be checked with `l1_min_c` at implementation; if C_min is above 1e-2, the points between 1e-2 and C_min are empty models → developer keeps the grid and will check.
- L1 needs a solver that supports it → left to the solver decision.

## Expected behavior and validation

Each outer training fold and repetition selects one C per penalty from its grid; the selected C and its position on the grid are stored.

## Consequences

- Still to decide: tie rule, treatment of an optimum at a grid edge (mf-013 treated it as information, no automatic extension), inner split and seed, solver and library parameters.
