# mf-016. Seed of the bootstrap generator (S4)

- **Status:** accepted
- **Date:** 2026-11-01
- **Tags:** modeling | reproducibility | evaluation
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

pj-006 fixes the event-level bootstrap (B = 10000, 95 % BCa, joint resampling, paired differences vs LRP and CRP) but not the seed of the random generator. pj-005 fixes only the fold seeds (42..46).

## Mathematical framing

One index matrix of B = 10000 resamples of the 8892 events is drawn once from a seeded generator and reused for every model, every repetition and the paired comparisons, so paired differences are computed event by event on identical resamples.

## Options considered

1. **One fixed seed for all models.**
2. **One seed per model.**
3. **No seed.**

## Decision

Chose **option 1**: seed 2026, fixed, the same for all models; the index matrix is drawn once with `numpy.random.default_rng(2026)` and reused.

## Rationale (developer's own words)

With the same seed the 10000 resamples are identical across models and the paired differences (pj-006) are computed event by event on the same samples. Reproducible across runs.

## Checks raised

- The equality of resamples holds only if the indices are generated once and reused for all models and repetitions.
- The generator type (`numpy.random.default_rng`) is a library detail added when drafting; the developer confirms it.
- A fixed seed gives one realisation of the bootstrap; its variability across seeds was not measured.

## Expected behavior and validation

Re-running gives identical intervals; two models share the same resample indices.

## Consequences

- Not doing: per-model seeds, unseeded bootstrap.
