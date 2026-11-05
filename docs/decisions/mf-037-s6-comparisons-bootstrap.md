# mf-037. Uncertainty and comparisons of the S6 rows

- **Status:** accepted
- **Date:** 2026-11-04
- **Tags:** evaluation
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

S6 has 9 rows, one per (stage-1 classifier, stage-2 regressor) pair (mf-024). In S4 the uncertainty comes from an event-level bootstrap with a fixed index matrix (seed 2026), BCa intervals, an L cap when F2 = 0 and a reliability flag above 2.5% of resamples with F2 = 0, with paired differences against LRP and CRP (mf-016..mf-020).

## Mathematical framing

A paired comparison needs the difference of the metrics in each resample and the interval of that difference; overlapping individual intervals do not test it. The F2 of two rows with the same classifier is identical (same p and same t), and the MSE_HR of two rows with the same regressor is identical (same r_hat).

## Options considered

1. **All 36 pairs among the 9 rows.**
2. **Only the 18 pairs that change one stage** (9 with the same regressor and different classifier, 9 with the same classifier and different regressor).
3. **No comparison among the S6 rows.**

## Decision

- The same bootstrap procedure as S4 (mf-016..mf-020) for the 9 rows, with nothing changed.
- Paired differences of every S6 row against LRP, CRP and its equivalent S4 row (the regressor of the pair).
- Option 2: the 18 pairs among S6 rows that change only the classifier or only the regressor.

## Rationale (developer's own words)

1. The same procedure as S4: there is no reason to change it, so the intervals are directly comparable.
2. The pairs where only one stage changes answer clear questions: does it matter which classifier I use with this regressor? does it matter which regressor I use with this classifier? The other 18 pairs change both at once.
3. Nothing changes with respect to S4.

## Checks raised

- A comparison with the same classifier has an F2 difference of exactly 0, and one with the same regressor has an MSE_HR difference of exactly 0; the S6 row against its S4 regressor has an MSE_HR difference of exactly 0 → developer keeps the design.
- The paired intervals are computed per resample, not from the individual intervals (the developer's first idea that these comparisons come for free from the individual intervals was corrected).
- 9 x 3 + 18 = 45 paired intervals without correction for multiple comparisons.

## Expected behavior and validation

For every comparison: point estimate of the difference, BCa interval and the L reliability flag, as in S4.

## Consequences

- All modeling decisions of S6 are taken; the parameter registry must be complete before implementation.
