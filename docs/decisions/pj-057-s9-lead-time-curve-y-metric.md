# pj-057. S9 lead-time curve — primary y-axis metric

- **Status:** accepted
- **Date:** 2026-11-14
- **Tags:** evaluation
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

S9 lead-time curve plots skill at `t_cut ∈ {2, 3, 4}` for LRP, GBDT, and the best among `{ols, ridge, lasso}` per cut (`pj-056`). The project dashboard reports F₂, MSE_HR, and L in clipped and unclipped forms (`pj-007`). S5 GBDT/RF hyperparameter selection uses lowest pooled OOF **L unclipped** (`pj-025`). S4 α selection uses inner-fold AP (`mf-013`); row comparison uses the same metric bundle as the bake-off.

## Options considered

1. **F₂** — emphasize HR detection as lead time increases.
2. **L unclipped** — emphasize the competition composite with honest magnitude on HR events.
3. **L clipped** — align MSE_HR with Uriot clipping in the figure.
4. **F₂ on the figure; L (and optionally MSE_HR) in a companion table** — split readability vs completeness.
5. **MSE_HR unclipped only** — magnitude without the F₂ denominator.

## Decision

Chose **L unclipped** as the **primary y-axis** of the lead-time skill curve.

Secondary metrics (F₂, MSE_HR clipped/unclipped) remain available in results JSON and may appear in a table or caption; no requirement to remove them from stored outputs (`pj-007`).

**Revision trigger (explicit):** if the figure is too hard to explain in W2, or instructor feedback finds the choice inconsistent with how models are trained/evaluated, the team may switch the primary y-axis to **F₂** via a new ADR before the final report freeze.

## Rationale (developer's own words)

L unclipped is the most coherent choice for now; if later it proves too messy, or the professor says it is a bit inconsistent with how we train the forests, we change it to F2.

## Checks raised

- GBDT hyperparameter pick at each `t_cut` already minimizes **L unclipped** (`pj-056`); the y-axis matches GBDT selection. Linear candidates are picked among `{ols, ridge, lasso}` by **L unclipped** at that cut (`pj-056`); α within each linear still comes from AP (`mf-013`) — partial asymmetry, not changed by this ADR.
- When F₂ is near zero, L unclipped diverges; points at high `t_cut` with few HR need `n_hr` in the caption (`pj-054`).
- User mentioned forest training: S5 selection is **L unclipped** (`pj-025`); if feedback instead targets S4 α vs L on the axis, address in prose or a follow-up ADR.

## Expected behavior and validation

- Curve JSON/plot stores `L_unclipped` per model, `t_cut`, and repetition aggregate per `pj-006` policy where wired.
- Clipped L and F₂ remain in sidecar fields for revision or tables.

## Consequences

- W2 lead-time figure defaults to ylab = `L` (unclipped, as in `pj-007` labeling).
- Parameter registry updated; optional table still reports F₂.