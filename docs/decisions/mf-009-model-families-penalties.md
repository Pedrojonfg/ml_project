# mf-009. Model families and penalties (S4)

- **Status:** accepted
- **Date:** 2026-11-01
- **Tags:** modeling
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

mf-007 fixes the logistic task and mf-008 the magnitude regressor task; neither fixes the penalty. `docs/plan-reparto.md` names ridge/lasso only for the magnitude regressor ("logística (HR) + ridge/lasso (magnitud)").

## Mathematical framing

For each task (logistic classification, linear regression) three penalty regimes: none (maximum likelihood / least squares), L2 (ridge: loss + lambda ||w||_2^2, shrinks, no sparsity), L1 (lasso: loss + lambda ||w||_1, sparsity, no closed form). Six models in total.

## Options considered

1. **Unpenalized only.**
2. **Unpenalized + L2.**
3. **Unpenalized + L2 + L1.**
4. **L2 + L1 without the unpenalized version.**
5. **Option 3 plus elastic net.**

## Decision

Chose **option 3**: for each task (logistic and regressor), three variants: unpenalized, L2 (ridge) and L1 (lasso). Six models in the S4 table.

## Rationale (developer's own words)

Each variant answers a different question (does regularizing help, does sparsity help); they are cheap to fit. The plan names ridge and lasso only for the magnitude regressor; L2 and L1 for classification are my decision, not the plan's. Elastic net stays in fog.

## Checks raised

- Unpenalized fits may be unstable: v1 features are strongly correlated (`risk_snap_*`, `risk_agg_*`) and there are 93 positives; interacts with scaling (preprocessing) and solver / iteration decisions.
- How the six models combine into F2, MSE_HR and L (each evaluated alone, or logistic paired with regressor) is open; closed by the alarm / `r_hat` decision.
- Elastic net is not decided; recorded as fog.

## Expected behavior and validation

Six models produce predictions for every event under the S1 protocol (pj-004, pj-005); metrics as in pj-007.

## Consequences

- Penalty strength (lambda / C) and solver settings remain to be decided (decisions 7 and 8).
- Not doing: elastic net, KNN (deferred by the developer).

## Scope note — 2026-11-01

After the alarm-rule decision (mf-012), the developer decided that the three logistic models are kept for S6 and do not enter the S4 table. The S4 table has three rows, one per regressor (unpenalized, ridge, lasso). This decision stays accepted but is not implemented in S4; solver and selection decisions of S4 (mf-013, mf-014, mf-015) cover the regressors only.

## Scope note — 2026-11-12

KNN is no longer deferred: mf-043 adds it to the S4 table as a magnitude regressor. The rest of this decision is unchanged.
