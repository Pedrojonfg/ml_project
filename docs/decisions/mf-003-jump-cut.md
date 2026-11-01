# mf-003. Jump cut: value, symmetry, operator

- **Status:** accepted
- **Date:** 2026-10-31
- **Tags:** modeling | evaluation
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

mf-002 defines a jump by size of Δ = y_final − latest_risk (log10 units).
A cut c is needed. Δ = 1 means the risk is multiplied by 10, Δ = 0.5 by ≈3.2,
Δ = 2 by 100. No data is in the repo yet, so the distribution of Δ is unknown.

## Mathematical framing

Labels: jump-up iff Δ ≥ c; jump-down iff Δ ≤ −c; otherwise stable. The number
of events labeled as jumps is non-increasing in c. If the measurement noise in
log risk is comparable to c, many jumps may be noise.

## Options considered

1. **c = 0.5** (×≈3.2)
2. **c = 1** (×10, plan default)
3. **c = 2** (×100)
4. **Set after EDA** from the distribution of Δ (deferred)

Symmetry: same c for up and down | different values. Operator: ≥ | >.

## Decision

Chose **c = 1**, symmetric (jump-up iff Δ ≥ 1, jump-down iff Δ ≤ −1), with
the limit included (≥).

## Rationale (developer's own words)

It is neither too strict nor too permissive. It is the value we have been
working with since the beginning, and it gives me confidence.

## Checks raised

- Developer first chose 0.5 as "more strict"; a lower cut is more permissive
  (more events labeled as jumps) → changed to 1.
- Interaction with mf-002 (noise reduction): smaller c lets smaller, possibly
  noisy changes count → developer chose 1.
- A symmetric cut does not give symmetric class counts under
  regression-to-the-mean → deferred to mf-006.
- c = 1 is the plan default, not derived from data → to be checked in EDA.

## Expected behavior and validation

In EDA, report the share of events in each class at c = 0.5, 1, 2 and check
that jump-up and jump-down are not nearly empty. Revisit only via a new ADR
that supersedes this one.

## Consequences

- stable-low / stable-high follow in mf-004.
- Label code takes c = 1 explicitly, passed as a parameter (per mf-003).
