# pj-064. S8 architecture — tabular MLP + masked GRU

- **Status:** accepted
- **Date:** 2026-11-15
- **Tags:** modeling
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

S8 has two arms (`pj-061`): tabular input is `pj-009` `FEATURE_COLUMNS`; sequence input is per-usable-CDM channels with a mask (`pj-063`). Both arms regress `risk_final` with alarm at −6 (`pj-062`). S5 already consumes the same tabular `X` with tree models.

## Mathematical framing

**Tabular arm:** a feedforward MLP maps \(x \mapsto \hat{r}\) via stacked affine layers and pointwise nonlinearities (e.g. ReLU). Same event vector as S5; different estimator family.

**Sequence arm:** a GRU reads the masked CDM sequence step by step, maintaining a hidden state; a head maps the event representation to \(\hat{r}\). Masked (padding) steps do not update the representation as valid observations (`pj-063`).

## Options considered

1. **MLP on pj-009 + masked GRU** — feedforward tabular ablation + step-by-step sequence encoder.
2. **MLP + LSTM** — same sequence idea, heavier gating.
3. **MLP + small attention / transformer** — all-to-all step weighting.
4. **MLP only (drop sequence)** — conflicts with `pj-061`.
5. **Other / none**

## Decision

Chose **option 1**: tabular arm = **MLP**; sequence arm = **GRU** with the agreed mask.

## Rationale (developer's own words)

Confirmed: MLP on the usual tabular `X` like S5; for the sequence, GRU — relatively simple, understandable, and it works with the mask scheme we defined.

## Checks raised

- MLP depth/width, GRU hidden size / number of layers, and how the GRU sequence is pooled into one event vector (last valid state vs masked mean, etc.) are not fixed here — later ADRs / parameter registry.
- Max sequence length `T` remains deferred-fog (`pj-063`).

## Expected behavior and validation

- Tabular path: `FEATURE_COLUMNS` → MLP → scalar `r_hat` (then `p_hr` at −6 per `pj-062`).
- Sequence path: `(T, C)` + mask → GRU → scalar `r_hat` with the same alarm rule.
- Both arms evaluated under S1 folds/metrics (`pj-004`–`pj-007`).

## Consequences

- Hyperparameter and training ADRs must list every MLP/GRU knob the code will use (no silent library defaults).
- Implementation may use PyTorch `nn.GRU` with `pack_padded` / mask-aware pooling consistent with `pj-063`.
