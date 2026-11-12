# pj-052. S7 atlas — empty pool policy (record; remediate later by ADR)

- **Status:** accepted
- **Date:** 2026-11-12
- **Tags:** modeling | evaluation | interpretation | product
- **Decided by:** Pedro
- **AI involvement:** none

## Context

Several slot ADRs (pj-030, pj-045, pj-048, pj-049, pj-051) forbid silently relaxing qualification rules when no `event_id` qualifies. A single cross-slot policy was still open in the S7 ledger queue.

## Options considered

1. **Omit panel only** — no further process.
2. **Block S7 done** until rules are relaxed by a new ADR.
3. **Record the empty pool for every core and optional slot; decide the exact remediation in a follow-on ADR if/when it happens** (chosen).
4. **Placeholder figure** without a written record elsewhere.

## Decision

For **every** atlas slot (core C1–C8 and optionals O1–O3):

- If the qualified pool is empty, **do not** silently change thresholds, majority counts, ≥3/5, model sets, or alarm lines.
- **Leave a durable record** that the slot had zero qualifiers (implementation detail of the record — log line, `results/atlas_empty.json`, caption stub, etc. — is engineering; may be fixed when coding).
- **How to remediate** (relax a rule, drop the slot from “done”, substitute a weaker pattern, etc.) is **not** chosen now: write a **new ADR when the empty pool is observed**.

Applies equally to core and optional slots; optionals may still be omitted from the delivered figure set, but the empty outcome must still be recorded.

## Rationale (developer's own words)

For every core/optional, leave a record (we will see exactly how with an ADR when the case arises).

## Consequences

- Aligns and generalizes the “don’t relax silently” notes in prior slot ADRs.
- Implementation must emit an empty-pool artifact or equivalent before claiming the run finished.
- S7 “done” with a recorded empty core slot is a product judgment for the later ADR, not pre-settled here.

## Checks raised

- Recording alone does not fix a missing core narrative; the follow-on ADR must be written if a core panel is required for the report.
