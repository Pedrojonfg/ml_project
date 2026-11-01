# mf-019. L cap when a model has no finite L in any resample (S4)

- **Status:** accepted
- **Date:** 2026-11-01
- **Tags:** modeling | evaluation
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

mf-017 replaces L = infinity by 10 x the largest finite per-repetition L of the same model. If a model has F2 = 0 in every repetition of every resample, no finite L exists and the cap is undefined; the first implementation raised an error.

## Mathematical framing

With no finite L there is no scale for the cap and the distribution of L is entirely infinite.

## Options considered

1. **Raise an error.**
2. **Mark the L interval and its paired differences not computable and not reliable** (chosen).
3. **Use a fixed numeric fallback cap.**

## Decision

Chose **option 2**. If no resample has a finite L, there is no cap to apply and no interval to compute: the L interval and its paired differences are marked not computable and not reliable, as in mf-018.

## Rationale (developer's own words)

If no resample has a finite L, there is no cap to apply and no interval to compute. It is marked not computable, like with infinite z0.

## Checks raised

- Does not trigger with the current OLS, ridge and lasso runs (no resample with F2 = 0).

## Expected behavior and validation

The results report no interval and the not-reliable flag for L and its paired differences; F2 and MSE_HR are unaffected.

## Consequences

- Not doing: error, fixed fallback cap.
