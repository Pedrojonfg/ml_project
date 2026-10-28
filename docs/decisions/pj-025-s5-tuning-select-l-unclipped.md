# pj-025. S5 hyperparameter selection — use unclipped L (supersedes pj-022)

- **Status:** accepted
- **Date:** 2026-10-28
- **Tags:** modeling | evaluation
- **Decided by:** Pedro
- **AI involvement:** options + critique
- **Supersedes:** pj-022 (selection metric only)

## Context

pj-022 switched S5 grid selection to clipped L. Run analysis (2026-10-28) showed the trees' failure comes from the training target (the −30 floor dominating leaf means), not from the selection metric. A training-target floor c is being introduced (pj-026). Clipped MSE_HR treats a prediction of −18 on a true HR event as if it were −6.001, i.e. it forgives the magnitude of missed HR events.

## Options considered

1. Keep clipped L for selection (pj-022).
2. Unclipped L for selection.
3. F₂ or a composite rule.

## Decision

Chose **option 2**: S5 hyperparameter grids select the candidate with the **lowest unclipped L** on pooled OOF predictions (all folds and repetitions). Tie → smaller value of the tuned parameter.

Reporting is unchanged: pj-007 (both clipped and unclipped), aggregated per pj-006.

## Rationale (developer's own words)

Select hyperparameters by unclipped L: errors on missed HR events should weigh heavily, and once the training target has a floor c there is no reason to clip them. Reporting keeps both versions (pj-007); the priority now is the unclipped model.

## Checks raised

- If c is close to −6, predictions never fall far below −6, so clipped and unclipped MSE_HR nearly coincide; the choice matters mostly when c is far from −6.
- F₂ = 0 still gives L = ∞ for every candidate; covered by revocation criterion R0 in pj-026.

## Consequences

- `_select_n_estimators` uses pooled `L_unclipped`.
