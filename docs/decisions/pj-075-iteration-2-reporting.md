# pj-075. Reporting of iteration 2

- **Status:** accepted
- **Date:** 2026-11-16
- **Tags:** evaluation | writing
- **Decided by:** Pedro
- **AI involvement:** opinion requested (considerations on what each option shows; no pick)

## Context

Iteration 2 (`pj-071`..`pj-076`) retrains rf, gbdt, mlp and gru. `pj-070` leaves main table versus appendix to the writing. `pj-033` frames the report as protocol rigor plus models in progress, not as a bake-off win; `pj-061` says neither S8 arm is the main claim; `pj-043` is the precedent of keeping a row with a footnote.

## Options considered

1. **Show both iterations** for the four models, labeled.
2. **Show only the final iteration** and say in the text that it is the second one, with a few supporting figures.
3. **Show only the final iteration** with no mention of the first.
4. **Other / none**

## Decision

Chose **option 2**: the final iteration is reported, the text states that it is the second one and in which respects it improved. Which first-iteration figures appear is left open (fog).

## Rationale (developer's own words, paraphrased at the developer's request)

The first iteration is not reported in full, because the modeling approach was not changed in response to the final results. It was changed because we found, by other means, that some initial parameters were not the best: for example, the best number of epochs always concentrated between 47 and 50, which showed that the epoch cap was too low. We therefore consider it honest to state in the text that the reported results come from a second iteration, in which some parameters were changed to try to improve them, and to give the reasons. The initial setup was deficient; the models themselves were not at fault. We will report the final iteration, say that it is the second, and state briefly in which respects it improved. Showing the whole first iteration is not necessary.

## Checks raised

- The argument "the initial parameters were not the best" covers the epoch cap, which was seen in the inner early stopping. It does not cover the HR weights or the retraining of RF and GBDT, which respond to weak out-of-fold results → the text should say so. No further response recorded.
- All tuning is done on the same folds, so the final numbers are somewhat optimistic; nested selection (`pj-073`) limits this for \(w\) and `n_estimators` only.

## Expected behavior and validation

- The text names the iteration and the reasons for the change.
- Whatever first-iteration figures are quoted can be traced to the preserved iteration-1 outputs.

## Consequences

- Iteration-1 outputs are preserved before the rerun overwrites the slugs (`LEDGER.md`, engineering row).
- Fog: which first-iteration figures appear in the text.
