# pj-022. S5 hyperparameter selection — use L clipped (supersedes pj-018 selection rule)

- **Status:** superseded by pj-025
- **Date:** 2026-10-27
- **Tags:** modeling | evaluation
- **Decided by:** Pedro
- **AI involvement:** options + critique
- **Supersedes:** pj-018 selection rule only (grid {100, 300, 500} unchanged)

## Context

pj-007 requires **reporting** F₂, MSE_HR, and L in **both** clipped (−6.001) and unclipped forms. pj-018 selected RF `n_estimators` by **lowest mean unclipped L** on OOF predictions. After run 0 (pj-021 findings), RF candidates had F₂ = 0 and unclipped selection did not align with the clipped metric used for paper-style comparison.

## Options considered

1. Keep **unclipped L** for tuning (pj-018).
2. Use **clipped L** for tuning (MSE_HR clipped at −6.001, same F₂ as pj-007).
3. Use **F₂** or a composite rule only (deferred to a later ADR if needed).

## Decision

Chose **option 2**: for **S5 hyperparameter selection** (starting with pj-018 `n_estimators` grid and any future S5 tree grids unless superseded), select the candidate with the **lowest mean clipped L** on pooled OOF validation predictions (K × R), with F₂ computed unclipped on thresholds as in pj-007.

**Tie-break (unchanged from pj-018):** among equal clipped L, prefer the **smaller** hyperparameter value when the tuned parameter is `n_estimators`; for other grids, document tie-break in the ADR that defines the grid.

**Reporting (unchanged):** pj-007 still requires both clipped and unclipped metrics in results tables; this ADR affects **selection only**.

## Rationale (developer's own words)

We already decided in S1 to report both L versions; now is the time to change the tuning decision and use L clipped for selection, which will imply further decisions.

## Checks raised

- When F₂ = 0, clipped L is infinite for all candidates (run 0 RF grid); this rule does not distinguish them until F₂ > 0 or a separate tie-break ADR is added.
- Clipped L can favour metric behaviour aligned with the paper while unclipped tables still show honest magnitude (pj-007).
- GBDT has no `n_estimators` grid yet; when added, use the same selection metric unless a new ADR says otherwise.

## Consequences

- Supersedes the selection sentence in pj-018; implementation `select_rf_n_estimators` must use `L_clipped` (MSE_HR clip −6.001).
- Re-run RF search after other hyperparameter changes that restore F₂ > 0.
- Follow-up decisions likely: behaviour when all candidates have F₂ = 0 / L clipped = ∞; regularization or loss changes (not decided here).
