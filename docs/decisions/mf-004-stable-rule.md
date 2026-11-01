# mf-004. stable-low / stable-high rule

- **Status:** accepted
- **Date:** 2026-11-01
- **Tags:** modeling | evaluation
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

Events with |Δ| < 1 (mf-003) are labeled stable-low or stable-high. Each event
has two values to compare with the HR threshold −6 (ADR 018): latest_risk and
y_final. For events that sit on opposite sides of −6 with a small Δ (e.g.
−6.1 → −5.9) the choice of value changes the label. The label is
analysis-only (mf-001).

## Mathematical framing

Rule A: stable-high iff y_final ≥ −6, otherwise stable-low. Rule B uses
latest_risk instead. Both are indicator functions of one coordinate of the
event; they differ exactly on stable events that cross −6.

## Options considered

1. **y_final** decides the box.
2. **latest_risk** decides the box.
3. **Both** must be on the same side; mixed events get their own class.
4. **Three boxes** (adds a stable-cross class).

## Decision

Chose **option 1**: among non-jump events, stable-high iff y_final ≥ −6;
stable-low iff y_final < −6. The boundary y_final = −6 counts as stable-high.

## Rationale (developer's own words)

A small change that ends up in the dangerous zone is enough to place the event
as stable-high.

## Checks raised

- Developer first chose option 2 citing leakage. The label is analysis-only
  (mf-001) and already depends on y_final through Δ, so the leakage argument
  does not separate options 1 and 2 → developer changed to option 1.
- Under option 1 an event such as −5.9 → −6.5 (Δ = −0.6) is stable-low even
  though it started in the dangerous zone → accepted; the crossing column
  (mf-002) records it.

## Expected behavior and validation

In EDA, check the counts of stable-low and stable-high and how many stable
events cross −6 (these are exactly the ones the rule decides).

## Consequences

- The four classes cover every event exactly once: jump-up, jump-down (by Δ),
  and stable-high / stable-low (by y_final) for the rest.
- The boundary y_final = −6 falls in stable-high (consistent with y_hr in the
  plan); confirmed by Mario.
