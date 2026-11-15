# pj-061. S8 scope — tabular MLP and sequence model

- **Status:** accepted
- **Date:** 2026-11-15
- **Tags:** modeling | framing
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

S8 is the PyTorch ablation under the shared S1 protocol (`010`, `pj-044`). `pj-009` deferred full sequence/padding to S8 while defining tabular event features for S3–S6. Plan text describes S8 as MLP/sequence ablation on the same table and folds.

## Mathematical framing

Two distinct input maps into neural predictors, both evaluated with the same event-level folds and Kelvins metrics (F₂, MSE_HR, L; `pj-004`–`pj-007`). Tabular arm: fixed event vector from pj-009. Sequence arm: ordered usable CDMs into a sequence encoder. Neither arm is the primary project claim (`010`).

## Options considered

1. **Tabular MLP only** — assumes pj-009 summaries suffice; no padding/mask contract.
2. **Sequence model only** — assumes value is in CDM order; tabular NN redundant.
3. **Both** — assumes two comparable ablations justify two input contracts and two table rows.
4. **Other / none**

## Decision

Chose **option 3**: S8 includes **both** a tabular MLP and a sequence CDM model.

## Rationale (developer's own words)

Both; both provide interesting insights, so we will try to do both.

## Checks raised

- Two implementation fronts on W2 Sentence Outline freeze day → developer accepted.
- Sequence signal may overlap with pj-009 trajectory summaries → accepted; still treated as a distinct ablation row.

## Expected behavior and validation

- Bake-off / results table includes at least one tabular-MLP row and one sequence-model row under the S1 protocol (same event cohort and fold definition as other model rows).

## Consequences

- Further S8 ADRs fix task/loss, sequence representation, architectures, preprocessing, training, and table row identity for each arm.
- Parameter registry lists both arms; architecture and training values remain open until those ADRs.
