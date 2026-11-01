# pj-035. Progress Report — two evaluation tables (W1)

- **Status:** accepted
- **Date:** 2026-11-01
- **Tags:** product | evaluation | reporting
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

The Project Proposal (ADR 018) reported CRP and LRP on the **official Zenodo test** split. Learned models (S4 syllabus regressors, S5 trees) are evaluated under the **S1 protocol** on the train/validation `event_table` with pooled **out-of-fold (OOF)** predictions (pj-004–006, pj-028). Mixing those scores in one table without labels misleads readers. pj-034 places preliminary bake-off under Impact; this ADR fixes how splits appear in W1.

## Mathematical framing

Metrics are computed on different event sets and protocols. A single table implies comparability of rows that is not guaranteed (official test n=2167 vs internal n=8892; baselines vs OOF learned models).

## Options considered

1. **A** — Main table = internal OOF only; official test limited to one LRP/CRP anchor row or footnote.
2. **B** — **Two tables**: (1) official test — CRP/LRP (proposal continuity); (2) internal OOF bake-off — LRP plus learned models on the same S1 protocol.
3. **C** — All models on official test.
4. **D** — Internal OOF only; do not mention official test.

## Decision

Chose **B — two tables**, each with an explicit title naming the split and protocol.

**Table 1 (official test):** CRP and LRP only, as in the proposal (ADR 018); metrics F₂, MSE_HR, L per pj-007; state that this split is for baseline reproduction, not model selection.

**Table 2 (internal bake-off):** Rows = LRP (same protocol as models) + syllabus models (S4: ols/ridge/lasso per mf-009) + S5 rf/gbdt when results exist; evaluation = pooled OOF on `event_table`; same metric dashboard (pj-007). Footnotes as needed: S4 regressor F₂ uses mf-012 alarm line t (not fixed −6); LRP and S5 use −6 (pj-001, pj-020); bootstrap / L reliability per pj-006 and mf-017 for S4 rows when reported.

## Rationale (developer's own words)

Chose option B: two separate tables so official-test baselines are not confused with internal cross-validated model scores.

## Checks raised

- Two tables use more space in a 2-page report → keep Table 1 compact (two rows); Table 2 may aggregate variants (e.g. best ridge/lasso) if space requires — follow-on ADR on row policy (pj-036).
- Official test must not be used to pick atlas cases (pj-028); Table 1 is reporting only.

## Expected behavior and validation

Every numeric row in the PDF is traceable to a named split. Check: no caption says “test” without specifying official vs internal OOF.

## Consequences

- W1 LaTeX: `\ref` two tables with distinct labels (e.g. `tab:official-baselines`, `tab:internal-bakeoff`).
- Next ADR: which rows/columns in Table 2 (logistic variants, bootstrap columns, clipped vs unclipped).
