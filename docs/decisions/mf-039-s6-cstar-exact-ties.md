# mf-039. C* when several C tie exactly at the maximum mean AUC (S6)

- **Status:** accepted
- **Date:** 2026-11-04
- **Tags:** modeling
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

mf-027 defines SE for C*, "the grid value with the highest mean AUC", but not which C* when several C tie exactly at the maximum mean. Each C has its own SE (the standard deviation of its 5 inner-fold AUCs). Found at implementation (Stage 3). Complements mf-027 without changing it.

## Mathematical framing

The tie set is {C : mean(C) >= mean(C*) - SE(C*)}; with several candidates for C*, the choice changes SE and so the set and the selected C.

## Options considered

1. **The smallest C among the tied maxima** (the strongest penalty).
2. **The largest C among the tied maxima.**
3. **Another rule.**

## Decision

Chose **the smallest C among the tied maxima**: SE is computed for the smallest C whose mean AUC equals the maximum.

## Rationale (developer's own words)

It is coherent with the tie rule: I already prefer the most penalized model, so if there is a tie at the maximum, I use the SE of the most penalized one, which gives a wider tie set and pushes even more toward simplicity.

## Checks raised

- The SE of the smallest C does not always give a wider tie set; it can be smaller than the SE of another tied C → developer keeps the rule.

## Expected behavior and validation

Stored C* and SE per fold, repetition and penalty (mf-027); a test with two exactly tied C.

## Consequences

- None beyond mf-027.
