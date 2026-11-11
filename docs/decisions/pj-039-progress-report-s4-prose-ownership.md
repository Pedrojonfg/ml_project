# pj-039. Progress Report — S4 prose ownership and depth (W1)

- **Status:** accepted
- **Date:** 2026-11-01
- **Tags:** product | reporting | process
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

S4 modeling decisions are Mario’s scope (mf-007..mf-020; implementation in `src/models/linear.py`, `src/evaluation.py`). Pedro integrates S1/S3/S5 content for W1 but is not the owner of S4 technical choices.

## Decision

**W1 prose for S4:** Mario drafts **two to four sentences** in the Solution/Impact block (or Pedro inserts a short placeholder until Mario edits). Content level:

- Name the deliverable: **OLS, ridge, and lasso** regressors on event features under the same OOF protocol as trees.
- Point to **nested regularization selection** (mf-013) and **event bootstrap with BCa** (pj-006 spirit, mf-016–020) without reproducing grids or solver lists.
- State that **alarm rule mf-012** applies to regressors (cross-ref Table 2 footnote).

Pedro does **not** need to enumerate all S4 ADRs in the oral or W1; he needs enough to place Table 2 rows honestly. Full decision list stays in `docs/decisions/mf-007`–`mf-020` and the ledger Parameter registry.

**Count for orientation:** **14 accepted modeling ADRs** mf-007..mf-020 (plus three auto-trivial engineering lines for paths/slugs); **implementation complete** per `docs/flow/mf-s4-syllabus-models.md`.

## Rationale (developer's own words)

Pedro does not know S4 in depth because it is not his part of the work; W1 should not force him to explain Mario’s modeling stack beyond a short summary and the table footnote.

## Consequences

- Mario owns accuracy of S4 sentences and bootstrap interval copy in Table 2.
- Pedro owns LRP/trees/protocol cross-references and overall PSI narrative (pj-033, pj-034).
