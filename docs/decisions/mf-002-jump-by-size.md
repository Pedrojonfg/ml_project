# mf-002. What defines a jump: size of change only

- **Status:** accepted
- **Date:** 2026-10-31
- **Tags:** modeling | evaluation
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

mf-001 fixes the taxonomy as an analysis/reporting tool. The label is built
from Δ = y_final − latest_risk (log10 units). The plan default calls an event a
jump by size of Δ only. A separate notion is whether the event crosses the HR
threshold (−6, ADR 018). The two disagree on some events (e.g. −6.1 → −5.9 has
Δ = 0.2 and crosses; −5.5 → −4.4 has Δ = 1.1 and does not).

## Mathematical framing

Size-only: jump-up iff Δ ≥ c, a function of Δ alone. Threshold-crossing is a
step function of (latest_risk, y_final), discontinuous at −6: arbitrarily small
changes near −6 flip it. Size-only has no such discontinuity in Δ, but the
cut c is still a hard threshold (set in mf-003).

## Options considered

1. **Size only** — jump iff |Δ| ≥ c.
2. **Crossing only** — jump-up iff latest_risk < −6 ≤ y_final (and the reverse).
3. **Size and crossing** — both conditions at once.
4. **Size or crossing** — either condition.
5. **Two separate axes** — size class and crossing flag stored without fusing.

## Decision

Chose **option 1** (size only). Crossing of −6 is recorded as a **separate
analysis-only column** (up / down / none), not part of the jump label.

## Rationale (developer's own words)

Option 1 is the plan default, and it would help reduce noise. Crossing of −6 is
still worth looking at, but as an analysis column.

## Checks raised

- Crossing alone flips on tiny changes near −6 (e.g. −6.01 → −5.99, Δ = 0.02),
  possibly noise → developer chose size-only, citing noise reduction.
- Size-only does not remove regression-to-the-mean effects at extreme
  latest_risk → deferred to mf-006.
- Under size-only an event that newly becomes high-risk with small Δ (e.g. −6.1
  → −5.9) is labeled stable-high → developer accepts this and keeps the
  crossing column for analysis.
- Developer's earlier stated interest in the not-dangerous → dangerous
  transition is served by the crossing column, not by the label.

## Expected behavior and validation

In EDA, count events that cross −6 with |Δ| < c, to see how many "newly
dangerous" events the jump label does not separate. The crossing column must
not enter X (mf-001).

## Consequences

- The cut c, symmetry and operator are decided in mf-003.
- stable-low / stable-high follow from HR membership of y_final (mf-004).
- The crossing column is an extra output of S2; engineering name chosen at
  implementation.
