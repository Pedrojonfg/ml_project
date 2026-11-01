# pj-036. Progress Report — table rows, columns, and EDA weight (W1)

- **Status:** accepted
- **Date:** 2026-11-01
- **Tags:** product | evaluation | reporting
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

pj-035 fixes two tables (official test vs internal OOF). S4 code now ships `results/{ols,ridge,lasso}.json` with pooled OOF metrics and BCa bootstrap (mf-016–020). Pedro chose minimal weight for early EDA that does not connect to later protocol/model work.

## Mathematical framing

Table rows must match implemented artifacts. F₂ for S4 regressors uses mf-012 alarm line t; F₂ for LRP and S5 trees uses fixed −6 (pj-001, pj-020). L uses the F₂ paired with each row’s alarm rule (mf-012 for regressors).

## Options considered

1. **Sparse Table 2** — LRP + best linear only + best tree.
2. **Full bake-off rows** — LRP + ols + ridge + lasso + rf + gbdt on internal OOF.
3. **Include logistic rows** — six penalty variants plus regressors.
4. **EDA-heavy Problem section** — repeat proposal EDA figures and narrative.

## Decision

**Narrative (Problem):** Do not lean on the initial EDA exploration unless a figure or fact is **directly illustrative** of the protocol or failure modes story; default is to pass over most EDA detail.

**Table 1 (official test):** Unchanged from pj-035 — CRP and LRP; columns F₂, MSE_HR, L (proposal continuity).

**Table 2 (internal OOF bake-off):**
- **Rows:** LRP (same protocol as learned models), **ols**, **ridge**, **lasso**, **rf**, **gbdt**. No logistic variants in W1 (ledger fog: logistics reserved for S6).
- **Columns:** **F₂** and **L (clipped)** as the main reported pair per pj-007.
- **Linear rows only:** report **95 % BCa bootstrap intervals** for F₂ and for L (clipped) from `results/<slug>.json` (point ± interval or separate interval columns — integrator chooses layout; intervals required for the three linear models).
- **Tree and LRP rows:** point estimates only in W1 (bootstrap for S4 linears is the priority given space and S4 ownership).
- **Mandatory table footnote:** S4 regressors choose an alarm threshold t per fold to maximize F₂ on training-fold predictions (mf-012); LRP and S5 models use the protocol HR line at −6. F₂ values are therefore not directly comparable without that note.

## Rationale (developer's own words)

Would skip most of the initial EDA in the report because it does not relate much to what we did afterward, unless something is very illustrative. Would use three linear rows, F₂ and L, bootstrap intervals on the linears, and a footnote that we are not using the same alarm method for every model.

## Checks raised

- Lasso can match LRP on pooled F₂ but not on L — footnote and both columns reduce misread.
- Bootstrap intervals only on three rows keeps the table readable in two pages.

## Expected behavior and validation

Table 2 has six model rows; linear cells show intervals where `bootstrap` exists in JSON; footnote cites mf-012 vs pj-001/pj-020.

## Consequences

- Mario regenerates or copies numbers from committed JSON when writing W1.
- MSE_HR and unclipped L remain in repo, not required in W1 table.
