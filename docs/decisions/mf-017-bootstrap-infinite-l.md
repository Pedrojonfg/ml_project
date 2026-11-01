# mf-017. L when F2 = 0 in a bootstrap resample (S4)

- **Status:** accepted
- **Date:** 2026-11-01
- **Tags:** modeling | evaluation
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

pj-006 computes F2 and L in every repetition of each resample and averages the 5 repetitions. L = MSE_HR / F2 is infinite when F2 = 0 (`kelvins_l`). Check on the S1 baselines: 0 of 2000 resamples with F2 = 0 for LRP (minimum F2 0.366) and CRP (minimum 0.035); not measured for the S4 regressors (F2 about 0.26 in a ridge check).

## Mathematical framing

BCa uses the order of the bootstrap values (percentiles, bias correction), so infinite values sit in the upper tail, but the mean over the 5 repetitions of a resample is infinite as soon as one repetition has F2 = 0. Discarding those resamples keeps only good cases and biases the interval downwards.

## Options considered

1. **Discard resamples with F2 = 0.**
2. **Replace L = infinity by a finite cap** (chosen).
3. **Keep infinity** (the upper end becomes unbounded if the percentile falls in the infinite mass).
4. **Mark the L interval undefined if any resample has F2 = 0.**

## Decision

Chose **option 2**:

- Cap: when a repetition of a resample has F2 = 0, its L is replaced by 10 x the largest finite per-repetition L of the same model over all resamples and repetitions (separately for L clipped and L unclipped), before averaging the 5 repetitions.
- The number of resamples with F2 = 0 in at least one repetition is counted and reported next to each L interval and each paired L difference.
- If more than 2.5 % of the resamples have F2 = 0, the L interval of that model and its paired differences are marked not reliable.

## Rationale (developer's own words)

Factor 10: one order of magnitude above the worst real case, enough to stay in the tail without distorting the body of the distribution, and not so extreme that it breaks the mean of the 5 repetitions. Applied per repetition, before averaging: capping after would let the infinity contaminate the mean. The largest finite L comes from the 10000 resamples of the same model, only those with F2 > 0; models are not mixed because each has its own scale of L. Discarding infinite resamples biases the interval downwards; a finite cap keeps the order and lets BCa compute. The threshold is 2.5 % (lowered from 5 %): above it the upper end of the BCa interval already falls in capped values.

## Checks raised

- The cap makes the upper end of an L interval, and of a paired L difference, depend on the factor 10 whenever capped values reach the percentile.
- Cases left to the drafting and confirmed by the developer: the set for the largest finite L (per repetition, per model, clipped and unclipped separately), what counts toward the 2.5 % (at least one repetition with F2 = 0), and where the flag applies (the model's L interval and its paired L differences vs LRP and CRP).
- For LRP and CRP no resample had F2 = 0 in a 2000-resample check; the rule matters for the regressors.

## Expected behavior and validation

The results report, per model, the number of resamples with F2 = 0 and the reliability flag; no infinite value enters a mean or an interval.

## Consequences

- Not doing: discarding resamples, keeping infinity, undefined interval.
