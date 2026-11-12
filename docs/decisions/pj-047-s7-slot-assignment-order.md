# pj-047. S7 atlas — slot assignment order (exclusion list)

- **Status:** accepted (order superseded by **pj-051** for eight-core map)
- **Date:** 2026-11-12
- **Tags:** modeling | evaluation | interpretation
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

Several slots can qualify the same `event_id`. pj-031 requires that an event appear in at most one atlas panel. Assignment order determines who claims a contested event. Core jump rules (pj-045) and C1/C2/C6/O1 rules are already fixed.

**pj-051** replaces the order below with C1→…→C8→O1→O2→O3.

## Options considered

1. **C1→C2→C6 then jumps then optionals** — older note in pj-031 (O1 after C1/C2/C6 only).
2. **C1→…→C6 numeric, then O1→…→O4 numeric** (chosen).
3. **Core as in (2), optionals in reverse cut order** (O2→O4→O1→O3 per pj-027 cut list).

## Decision

Assign `event_id`s **sequentially**, updating the exclusion list after each pick:

**C1 → C2 → C3 → C4 → C5 → C6 → O1 → O2 → O3 → O4.**

Slots that are cut for schedule reasons are simply skipped; the relative order of those that remain is unchanged. Selection keys inside each slot stay as in pj-028/045/046/030/031 and follow-on O2–O4 ADRs.

## Rationale (developer's own words)

Same reasoning as before: the examples are supposedly already ordered by their insightfulness.

## Consequences

- Implementation must pick in this order (or an equivalent locked schedule) so results are reproducible.
- A jump that also qualifies C1/C2 will go to C1/C2 if reached first; C3–C5 see a reduced pool.
- C6 runs after C3–C5, so multi-fail jumps may be taken by jump slots first.

## Checks raised

- pj-027’s **cut** order (O3→O1→O4→O2) is about dropping panels under time pressure, not about exclusion priority; this ADR sets exclusion priority separately (numeric O).
