# pj-063. S8 input representation — tabular X + masked CDM sequences

- **Status:** accepted
- **Date:** 2026-11-15
- **Tags:** modeling | data | preprocessing
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

S8 has two arms (`pj-061`), both regressing `risk_final` with alarm at −6 (`pj-062`). Event-level tabular features are defined in `pj-009`; that ADR deferred full sequence / padding to S8. S5 consumes the same tabular contract (`FEATURE_COLUMNS`).

## Mathematical framing

**Tabular MLP:** one row \(x \in \mathbb{R}^{d}\) per event from `pj-009`; map \(x \mapsto \hat{r}\).

**Sequence arm:** for each event, an ordered series of usable CDMs (`time_to_tca >= 2`), with per-step channels aligned to the same underlying variables used in the S5 / `pj-009` design (e.g. `risk`, `miss_distance`, `relative_speed`, `t_weighted_rms`, …) — not the quantile-aggregated tabular vector. Length varies; a binary (or boolean) **mask** marks valid steps so padded positions do not enter the loss or pooled representation.

## Options considered

1. **MLP = pj-009 `X`; sequence = same underlying CDM channels + mask** — shared substance with S5, different geometry.
2. **MLP = pj-009; sequence = subset of channels only** — thinner temporal input.
3. **Sequence = tabular `X` without raw CDM steps** — not a true sequence ablation.
4. **Fixed pad/truncate without mask** — pad values can bias the encoder.
5. **Other / none**

## Decision

Chose **option 1**:
- Tabular MLP uses `pj-009` `FEATURE_COLUMNS` as `X`.
- Sequence uses per-usable-CDM channels aligned with S5 / `pj-009` variables in the `time_to_tca >= 2` window, with **masking** for variable length.
- Maximum sequence length cap `T` is **deferred-fog** (still required for batching at implementation).

## Rationale (developer's own words)

The MLP uses the usual tabular `X` to predict `Y` as a neural net. For CDM channels, use the same substance as in S5 — trying to do the same thing another way. For sequence length, use a mask, because that is what I know and understand how it works, and I will not implement something I do not understand.

## Checks raised

- Quantile snapshots and A1–A3 aggregates remain on the tabular arm only; the sequence arm sees per-CDM values — developer accepted.
- How `c_object_type` (and other event-level categoricals) attach to the sequence arm is not fixed here — deferred to a later ADR or fog.
- Numeric max length `T` must be set before batched training — marked deferred-fog.

## Expected behavior and validation

- Tabular arm: `build_features` / `FEATURE_COLUMNS` unchanged as the MLP input.
- Sequence arm: tensor shape `(batch, T, C)` (or equivalent) plus mask of shape `(batch, T)`; masked positions do not contribute to the pooled event representation used for `r_hat`.
- Only CDMs with `time_to_tca >= 2` appear as valid sequence steps (same usable window as S1/S3).

## Consequences

- Architecture ADRs consume these two input contracts.
- Implementation must define channel list `C` explicitly (can mirror pj-009 variable set per CDM) and eventually fix `T`.
- Parameter registry: tabular input = pj-009; sequence = masked usable CDMs; `T` = deferred-fog.
