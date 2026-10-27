# pj-012. Explicit first–last delta columns

- **Status:** accepted
- **Date:** 2026-10-27
- **Tags:** modeling | preprocessing
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

pj-009 includes first- and last-usable snapshots (and quantiles) per variable. Optional v1 columns such as `x_last − x_first` would summarize total change over the usable window.

## Options considered

1. **No explicit delta columns** — rely on snapshots and aggregates.
2. **Delta on `risk` only** (first to last usable).
3. **Deltas on all four snapshot variables**.
4. **Deltas on geometry only, not `risk`**.

## Decision

Chose **option 1**: **no** explicit first–last delta columns in v1.

## Rationale (developer's own words)

Redundant given first and last usable snapshots already in the feature set.

## Checks raised

- Models can learn differences from separate first/last columns (especially trees); linear models may need explicit interaction — developer accepted redundancy tradeoff.

## Consequences

- `build_features` must not add `*_delta_*` columns unless a future ADR supersedes this.
