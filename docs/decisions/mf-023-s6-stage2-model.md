# mf-023. Stage-2 model of S6

- **Status:** accepted
- **Date:** 2026-11-04
- **Tags:** modeling
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

mf-022 trains the stage-2 regressor on all events. S4 built three regressors on all events with target `risk_final` unclipped: unpenalized, ridge, lasso (mf-008, mf-009, mf-013, mf-014); their predictions exist in `preds/{ols,ridge,lasso}.parquet`. S5 has RF and GBDT regressors (pj-014..026). mf-021 chose the three logistic variants for stage 1.

## Mathematical framing

Stage 2 estimates E[risk | features] over all events. The choice fixes the model class (linear with no penalty, L2 or L1) and the parameters to decide for each.

## Options considered

1. **A. Unpenalized (OLS)** — linear in the features; unstable coefficients under collinearity.
2. **B. Ridge** — linear plus alpha * ||w||^2; shrinks without zeroing.
3. **C. Lasso** — linear plus alpha * ||w||_1; zeroes some coefficients.
4. **D. The three S4 regressors** — three stage-2 models; combined with the three logistic variants of mf-021 this gives up to 9 two-stage models unless a later decision pairs them.
5. **E. S5 trees (RF or GBDT)** — non-linear; owned by Pedro with its own ADRs (pj-014..026); needs a decision to reuse predictions or retrain.

## Decision

Chose **D**: the three S4 regressors (unpenalized, ridge, lasso) are the stage-2 models of S6.

## Rationale (developer's own words)

I want to compare variants, and I think it is the most coherent with what I have been doing.

## Checks raised

- D with the three stage-1 variants (mf-021) gives up to 9 two-stage models → how stage 1 and stage 2 pair (all 9, or matched) is not decided; added to the queue.
- The S4 predictions exist already; whether S6 reuses them or refits is not decided.
- Developer asked whether choosing E would give priority to Pedro's work; answer given: it is a dependency choice, not a priority (AI involvement: options + critique).

## Expected behavior and validation

Three stage-2 regressors per fold and repetition, as in S4.

## Consequences

- New queue items: pairing of stage-1 and stage-2 variants; reuse vs refit of the S4 predictions.
- Alpha selection, solver and parameters of the regressors follow S4 (mf-013, mf-014) unless a later decision changes them.
