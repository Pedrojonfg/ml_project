# mf-049. Computation of the median squared distance m in S10

- **Status:** accepted
- **Date:** 2026-11-15
- **Tags:** modeling
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

`gamma = c / m` (mf-047), `c = 10` (mf-048). `m` is a scale of the squared distances of the preprocessed training part (mf-044). The matrix of squared distances is needed anyway to build K.

## Mathematical framing

`m` is the median of the squared Euclidean distances over the pairs of events of the training part. Exact computation uses all distinct pairs; a subsample estimates it.

## Options considered

1. **All distinct pairs of the training part (about 16 million for 5700 events)** — exact, deterministic, no seed; the 5700x5700 matrix takes 260 MB.
2. **Random subsample of events of a size fixed by the developer, with a seed** — approximate; adds randomness and a seed.

## Decision

Chose **option 1**: `m` is the median of the squared Euclidean distances between all distinct pairs of events of the training part of each fit (outer fold and each inner fold), computed on the rows preprocessed as in mf-044, without subsample or seed.

## Rationale (developer's own words)

A; if it does not take more time, it is exact.

## Checks raised

- Measured with 5700 events: the distance matrix takes 0.8 s and the median over its upper triangle 0.7 s more, negligible against one diagonalization of about 55 s.
- `m` uses only the training part of each fit (leakage hazard).

## Expected behavior and validation

Test: `m` equals the median of the upper triangle of the squared distance matrix of the training rows and does not change when validation rows are changed.

## Consequences

- Not doing: subsample of events for `m`.
