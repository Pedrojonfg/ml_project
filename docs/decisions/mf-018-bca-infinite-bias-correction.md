# mf-018. BCa interval when the bias correction is infinite (S4)

- **Status:** accepted
- **Date:** 2026-11-01
- **Tags:** modeling | evaluation
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

pj-006 uses 95 % BCa intervals; mf-016 and mf-017 fix the seed and the L cap. BCa bias correction z0 = Phi^-1(share of bootstrap values strictly below the estimate) is infinite when that share is 0 or 1. The first implementation clipped the share to [1/(2B), 1 - 1/(2B)] on its own. Check on the current OLS, ridge and lasso runs: 0 of 15 BCa calls per model had a share of 0 or 1, and no resample had F2 = 0.

## Mathematical framing

If the estimate lies at an extreme of its own bootstrap distribution, the bias correction is not defined. The share counts values strictly below the estimate, so with step-wise metrics such as F2, many resamples can equal the estimate and the share can be 0 or 1 even if the estimate is central.

## Options considered

1. **Clip the share to [1/(2B), 1 - 1/(2B)].**
2. **Mark BCa as not computable and report no interval** (chosen).
3. **Fall back to the percentile interval.**

## Decision

Chose **option 2**. If z0 is infinite for a metric and model, the BCa interval is marked not computable: the point estimate is reported without interval and a note says BCa was not computable. No fallback method. The same rule applies to the paired differences against LRP and CRP. If every bootstrap value equals the estimate exactly, the interval is [v, v] (zero uncertainty is a valid result, not a failure).

## Rationale (developer's own words)

If the estimator is at 0 % or 100 % of its bootstrap distribution, the interval has no statistical sense, and publishing a corrected one would be misleading. Zero uncertainty is a valid result, not a failure.

## Checks raised

- The first implementation clipped the share; it is replaced by this rule.
- The share counts strictly-below values, so ties at the estimate can trigger the rule for a central estimate.

## Expected behavior and validation

The results store a null interval and a flag for the metric and model (and paired difference) where BCa was not computable.

## Consequences

- Not doing: clipped share, percentile fallback.
