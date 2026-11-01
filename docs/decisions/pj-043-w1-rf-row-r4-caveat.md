# pj-043. W1 — keep RF in Table 2 with R4 revocation note

- **Status:** accepted
- **Date:** 2026-11-01
- **Tags:** evaluation | reporting
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

pj-026 revocation criterion R4 fires for RF in `results/floor_c_diagnostics.json` (|mean `risk_final` of detected HR − missed HR| = 0.63 > threshold 0.54); GBDT passes R0–R4. pj-026 says any firing criterion reopens the ADR (switch to c as a nested-CV hyperparameter).

## Options considered

1. Keep RF in Table 2 with a note that a pre-registered revocation criterion fired and the floor-c ADR is reopened next cycle.
2. Drop RF from Table 2; GBDT as the only tree.
3. Keep RF without a note.

## Decision

Chose **option 1**. The RF row stays with a footnote; reopening pj-026 for RF is scheduled for the next cycle (C2), not done before W1.

## Rationale (developer's own words)

Keep RF with a note: revocation criterion triggered, the ADR is reopened in the next cycle.

## Consequences

- W1 Table 2 footnote on the RF row.
- C2 backlog: reopen pj-026 (option 3, nested-CV c) at least for RF.
