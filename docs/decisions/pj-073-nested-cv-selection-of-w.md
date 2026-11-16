# pj-073. Selection of w (and `n_estimators`) by nested CV

- **Status:** accepted
- **Date:** 2026-11-16
- **Tags:** modeling | hyperparameters | evaluation
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

`pj-072` introduces the weight \(w\). S4 selects its hyperparameters with an inner CV inside each outer training fold (`mf-013`, `mf-015`, AP criterion); S5 selected `n_estimators` on pooled OOF predictions of the same folds used for reporting (`pj-024`, `pj-025`, L unclipped), which leaves the reported number slightly optimistic. Each outer training fold has about 74 HR events (about 25 per inner validation fold with 3 folds). The GRU needs at least 100 epochs (`pj-074`), which bounds the affordable number of fits.

## Mathematical framing

For each model, repetition \(r\) and outer fold: split the outer training part with `StratifiedKFold(n_splits=3, shuffle=True, random_state=42+r)` stratified by `y_hr`. For each candidate, fit on the inner training part (with its own \(c(w)\), `pj-072`), predict the held-out part, pool the three held-out prediction sets, and compute L unclipped (`pj-007`) once on the pooled set. Select the candidate with the lowest pooled L; refit on the whole outer training part with that candidate (and \(c(w)\) recomputed there) and predict the official validation fold. The official validation fold never takes part in selection.

## Options considered

1. **Inner CV, 5 folds** (as S4) — about 15 HR per inner fold; 21 fits per outer fold with 4 values of w.
2. **Pooled OOF of the outer folds** (as S5) — cheap; the reported metrics are optimistic.
3. **Inner CV, reduced (3 folds)** — 13 fits per outer fold with 4 values of w; about 25 HR per inner fold, trained on 2/3 of the part.
4. **Other / none**

## Decision

Chose **option 3**:

- Inner CV with **3 folds**, stratified by HR, seed `42 + r` (as `pj-069`).
- Candidates: \(w \in \{1, 2, 5, 10\}\); for RF and GBDT jointly with `n_estimators` \(\in \{300, 500, 1000\}\) (`pj-024`).
- Criterion: **pooled L unclipped** over the three held-out parts.
- Ties (including L = ∞): the **smallest w**; if still tied, the smaller `n_estimators` (`pj-025` precedent).
- \(w\) is selected **per model and per outer fold**.
- No other hyperparameter changes in any of the four models.

## Rationale (developer's own words)

w is chosen by cross-validation, because it is the most reliable. Inner CV but only 3 folds, because the GRU must have at least 100 epochs. L unclipped, as in S5, because it includes MSE_HR. w separately for each model. Pooled, for stability and consistency. w = 1, 2, 5, 10 so as not to exceed the cost. If there is a tie, the smallest w, being the closest to not weighting, the closest to the "pure" model. `n_estimators` is chosen together with w; it is the most reliable even if it costs more time. I see no reason to change other hyperparameters. Stratified by HR, and the seed tied to the repetition, as `pj-069`.

## Checks raised

- About 25 HR per inner validation fold: the selection is noisy → accepted.
- L = ∞ ties are possible when a candidate reaches F₂ = 0 on the pooled set → tie rule above.
- Cost: 13 fits per outer fold for the networks (about 1.6 h for the MLP and up to about 9 h for the GRU at 100 epochs, estimates from iteration 1 timings); RF/GBDT cost not timed, and multiplied by 3 for the joint grid.

## Expected behavior and validation

- The chosen \(w\) (and `n_estimators`) per outer fold is stored in the result JSON.
- Same inputs and seeds give the same choices on CPU.
- Official validation folds are not read during selection.

## Consequences

- Replaces the S5 selection of `n_estimators` on pooled outer OOF (`pj-024`, `pj-025`) for this iteration.
- Not doing: 5 inner folds, selection on outer OOF, a common \(w\) for all models.
