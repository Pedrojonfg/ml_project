# pj-005. Repetition and seeds

- **Status:** accepted
- **Date:** 2026-10-24
- **Tags:** modeling | evaluation | reproducibility
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

With 93 HR, a single 5-fold partition makes results depend on one random split (pj-004).

## Mathematical framing

Repeated stratified 5-fold, R = 5 repetitions, each with its own seed; every event is validated once per repetition. Repetitions give a more stable estimate on the same 93 HR; they do not add positives.

## Options considered

1. **Single seed, single partition.**
2. **Repeated CV with several seeds** (R = 3, 5 or 10).

Seed values: consecutive from 0, a base seed, or a free list.

## Decision

Chose repeated CV with R = 5 and seeds **42, 43, 44, 45, 46** (base 42, increments of 1).

## Rationale (developer's own words)

Several seeds and averaging make sense because there are few HR. The seed values do not matter.

## Checks raised

- The seeds were fixed without looking at results.
- Per-event predictions are averaged across repetitions, and uncertainty resamples events, never event-repetition pairs → to be fixed in the uncertainty ADR.
- Model-internal randomness (trees, networks) is not covered here → decided in S3–S6.

## Expected behavior and validation

Re-running with the same seeds reproduces identical fold assignments.

## Consequences

- 25 fits per model per evaluation.
- Not doing: tuning the seed.
