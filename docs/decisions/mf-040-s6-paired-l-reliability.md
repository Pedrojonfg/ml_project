# mf-040. Reliability of paired L differences between two rows in S6

- **Status:** accepted
- **Date:** 2026-11-04
- **Tags:** evaluation
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

In S4 the L interval of a model is flagged not reliable when more than 2.5% of the resamples have F2 = 0 in at least one repetition (mf-017); paired differences against LRP and CRP inherit the model's flag. In S6 there are differences between two rows that both have their own F2 (S6 row against its S4 regressor, and the 18 pairs of mf-037). Found at implementation (Stage 3).

## Mathematical framing

In a resample where F2 = 0 in a row, L is infinite and replaced by a cap (mf-017). A difference of L between rows A and B uses at least one cap in every resample where A or B has F2 = 0 in some repetition.

## Options considered

1. **Not reliable if the share of resamples where at least one of the two rows has F2 = 0 exceeds 2.5%.**
2. **Not reliable if either row exceeds 2.5% on its own.**
3. **Inherit only the flag of one row.**

## Decision

Chose option 1: the paired L difference between rows A and B is not reliable when, in more than 2.5% of the resamples, A or B has F2 = 0 in at least one repetition. For differences against LRP and CRP, the rule of S4 stays.

## Rationale (developer's own words)

Not reliable if in more than 2.5% of the resamples at least one of the two has F2 = 0. In those resamples the L difference uses at least one cap (an invented value), so if it happens too often, the difference cannot be trusted.

## Checks raised

None raised.

## Expected behavior and validation

Each paired comparison stores the share of resamples with at least one F2 = 0 and the reliability flag; a test with known shares.

## Consequences

- The reliability of each row's own L interval stays as in S4 (mf-017).
