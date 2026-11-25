# pj-082. Official test — single fit on full filtered train

- **Status:** accepted
- **Date:** 2026-11-24
- **Tags:** evaluation | modeling
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

`pj-081` includes learned models on the one-shot official test (R5: frozen models, once). The internal bake-off stores out-of-fold predictions per fold/repetition (`preds/*.parquet`), not a single fitted checkpoint per slug. A rule is required to produce test predictions without using the test for selection.

## Mathematical framing

Each official-test row is the prediction of one estimator \(\hat{f}\) fit on the full filtered training set and applied to test events. It is not an aggregate of the 25 outer-fold estimators from S1 CV.

## Options considered

1. **One fit on all filtered train** — hyperparameters frozen a priori; one `r_hat` / `p_hr` per test event.
2. **25 fold/rep fits, aggregate predictions on test** — CV defines an ensemble.
3. **One fit per repetition (5 seeds), aggregate** — coarser ensemble.
4. **Baselines only on test** — conflicts with `pj-081`.
5. **Other / none**

## Decision

Chose **option 1**. For each model in `pj-081` except CRP/LRP baselines: fit once on the full filtered training set (`pj-003`), then predict the official test. Do not ensemble outer-fold models. Hyperparameter, alarm, and preprocessing values for that fit are frozen before seeing the test; the concrete freezing rule is a separate decision.

## Rationale (developer's own words)

Option A, because it is the most coherent with prior decisions and what makes most sense. It is literally testing the built models.

## Checks raised

- Internal artifacts are OOF per fold, not one checkpoint → A defines the final estimator; hyperparameter freezing still required → deferred to the next decision.
- Alarm `t`, imputer, scaler, floor `c(w)` estimated on that same full-train fit (no test) — expected companion; confirm in the freezing ADR → recorded.
- Does not use the test for selection (R5) → recorded.

## Expected behavior and validation

- Official-test script produces one prediction vector per `pj-081` learned slug from a single full-train fit.
- No test event enters fitting, imputation statistics, scaling, alarm selection, or hyperparameter choice.

## Consequences

- Next decision: how each hyperparameter (and alarm `t`, imputer, scaler, `c(w)`) is fixed for that single fit.
- Event filter on test and reporting vs OOF remain later on the agenda.
- Not doing: fold-ensemble predictions on the official test.
