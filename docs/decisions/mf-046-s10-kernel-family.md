# mf-046. Kernel family of kernel ridge in S10

- **Status:** accepted
- **Date:** 2026-11-15
- **Tags:** modeling
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

S10 adds kernel ridge to the S4 table. Target fixed by mf-044, preprocessing by mf-045. The kernel fixes the class of functions the model can learn. All options below are available in scikit-learn's `KernelRidge`.

## Mathematical framing

Kernel ridge fits `f(x) = sum_i alpha_i k(x_i, x)` with `alpha = (K + lambda I)^-1 y`, where `K_ij = k(x_i, x_j)`. The kernel is the similarity between two events.

## Options considered

1. **Linear**, `k(a,b) = a.b` — relation with `y` is linear in the 35 columns; same function as the S4 ridge (adds no new function class).
2. **Polynomial**, `k(a,b) = (gamma a.b + c0)^d` — interactions up to degree d matter; ridge on all monomials up to degree d (about 630 implicit variables for d = 2 on 35 columns); 3 parameters.
3. **RBF (Gaussian)**, `k(a,b) = exp(-gamma ||a-b||_2^2)` — similarity decays smoothly with Euclidean distance; one parameter; local (far from the data, `f` returns to the intercept).
4. **Laplacian**, `k(a,b) = exp(-gamma ||a-b||_1)` — similarity decays with L1 distance; one parameter; less smooth, heavier tails than RBF.

## Decision

Chose **option 3**: RBF kernel `k(a,b) = exp(-gamma ||a-b||^2)`, Euclidean distance on the 35 columns preprocessed as in mf-045. The parametrization of gamma, its grid and the other kernel parameters are left to the next decisions.

## Rationale (developer's own words)

It is the kernel we have worked with, and, unlike the linear kernel, it adds new information.

## Checks raised

- The RBF is local: far from the training events `f` approaches the intercept, so `r_hat` may stay far from -6 (see mf-044).
- Every extra kernel parameter multiplies the search grid; RBF has one (gamma) besides lambda.
- The examples used in the understanding session were RBF; this is not a reason for or against the choice.

## Expected behavior and validation

One more row in the S4 table with the same event bootstrap and paired differences vs LRP (pj-006, mf-016..mf-020).

## Consequences

- Not doing: linear, polynomial and Laplacian kernels, kernel mixtures.
- Open: gamma parametrization and grid, intercept, selection of lambda and gamma, alarm line, compute budget.
