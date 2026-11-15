# pj-053. S9 scope — lead-time curve and leave-mission-out

- **Status:** accepted
- **Date:** 2026-11-14
- **Tags:** evaluation | planning
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

`pj-044` brought S9 (lead-time / leave-mission-out) into C2 scope with Pedro as owner, before the W2 Sentence Outline freeze (Sunday 15 November 2026). S9 depends on S1 (protocol, folds) and S5 (tree bake-off). The stretch is not the primary RQ (`007`, `008`) but supports ops-facing narrative in W2.

## Options considered

1. **Lead-time skill curve only** — assumes one stretch artefact; no mission-shift table.
2. **Leave-mission-out only** — assumes mission-OOD stress test; no early-warning timeline.
3. **Both** — assumes time to implement two linked analyses under the same protocol.

## Decision

Chose **option 3**: S9 delivers **both** (a) a lead-time skill curve and (b) a leave-mission-out evaluation for W2.

## Rationale (developer's own words)

There is enough time to do both properly rather than shipping only one stretch artefact.

## Checks raised

- `plan-reparto` budgets ~4 h for S9; two deliverables increase implementation and writing load vs a single artefact → developer accepted.
- Leave-mission-out needs `mission_id` per event (not in S1 `event_table` today) → engineering add-on, not a change to v1 `X` (`pj-011`).

## Expected behavior and validation

- W2 includes at least one lead-time figure/table and one mission-shift table or equivalent comparison, both tied to the same metric dashboard as S1 (`pj-007`).

## Consequences

- Further S9 ADRs fix lead-time grid, cohort rules, models, LMO scheme, and outputs.
- S6 rows on the lead-time curve remain optional (fog until decided); default S9 bake-off rows follow a later ADR.