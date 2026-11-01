# pj-032. S7 atlas — optional O2–O4 deferred (Mario S2 / S6)

- **Status:** accepted
- **Date:** 2026-10-28
- **Tags:** modeling | evaluation | interpretation
- **Decided by:** Pedro
- **AI involvement:** none

## Context

Optional slots **O2**, **O3**, and **O4** (pj-027) depend on deliverables Pedro does not own:

- **O2–O3:** calibrated two-stage predictions and reliability analysis (**S6**, Mario).
- **O4:** fourth jump case (**S2** taxonomy / jump definition, Mario).

O1 rules are fixed in pj-031. Core jump slots C3–C5 remain deferred in pj-030 until S2.

## Decision

**Do not write selection rules** for O2, O3, or O4 until:

1. **S2:** jump labels or operational jump rule is recorded in an ADR (team contract).
2. **S6:** `preds/` (or agreed artifact) for two-stage models exists with schema compatible with R1 contracts.

When unblocked, new ADRs must apply the same **OOF-only** (pj-028), **≥3/5 repetition stability** (pj-029), **event_id exclusion list**, and **caption** conventions unless explicitly superseded.

**Cut order** unchanged (pj-027): O3 → O1 → O4 → O2.

## Rationale (developer)

Define optional rules that do not depend on Mario’s work first (O1); wait for S2/S6 before O2–O4.

## Consequences

- S7 “decisions complete” for Pedro-owned optional content means **O1 only**; O2–O4 remain `deferred-fog` in the Parameter registry until follow-on ADRs.
- Implementation may ship core + O1 without O2–O4 panels.
