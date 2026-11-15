# pj-067. S8 network sizes, GRU pooling, and max length T

- **Status:** accepted
- **Date:** 2026-11-15
- **Tags:** modeling | hyperparameters
- **Decided by:** Pedro
- **AI involvement:** opinion requested (criteria and concrete sizes); developer ratified

## Context

`pj-064` chose a tabular MLP and a masked GRU without fixing widths, depth, pooling, or sequence cap `T` (`pj-063` left `T` deferred-fog). Empirical usable-CDM lengths on Kelvins train CDMs with `time_to_tca >= 2` have max 17 (p99 ≈ 16).

## Mathematical framing

MLP: \(x \mapsto \hat{r}\) via two hidden ReLU layers then a linear scalar head. GRU: masked sequence \(\mapsto\) hidden states; event vector = hidden state at the **last valid** (unmasked) step; linear head \(\mapsto \hat{r}\). Sequences longer than `T` keep the `T` steps **closest to TCA** (smallest `time_to_tca` among usable CDMs); shorter sequences are padded and masked.

## Options considered

1. **Criteria package (ratified):** MLP `d → 128 → 64 → 1` (ReLU), dropout 0; GRU `hidden_size=64`, 1 layer, dropout 0, last-valid pooling; `T=20`.
2. Smaller MLP `64 → 32 → 1` / other hidden sizes in 32–128.
3. Other / none.

## Decision

Chose **option 1**.

| Knob | Value |
|------|-------|
| MLP hidden layers | 128, then 64; ReLU; output dim 1 |
| MLP dropout | 0 |
| GRU `hidden_size` | 64 |
| GRU `num_layers` | 1 |
| GRU dropout | 0 |
| GRU pooling | last valid (masked) state |
| Max length `T` | 20 |
| Truncation rule | keep usable CDMs closest to TCA |

## Rationale (developer's own words)

Use what is in the stated criteria; no problem recording that the AI suggested numbers and I ratified them — it fits my current knowledge. I may want to test more combinations later; for now this is good enough.

## Checks raised

- `T=20` covers all observed usable lengths (max 17) on train CDMs profiled 2026-11-15; if a longer series appears, truncation applies.
- Channel list `C` for the GRU input still follows `pj-063` (implementation enumerates columns explicitly).
- How event-level `c_object_type` attaches to the sequence arm remains a minor open detail (repeat last-usable one-hot or omit) — if omitted, document in code; prefer last-usable one-hot broadcast or concat at the head without a new ADR if engineering-only.

## Expected behavior and validation

- MLP parameter shapes match `d → 128 → 64 → 1`.
- GRU batch tensors `(B, T=20, C)` with mask `(B, 20)`; padded steps do not define the “last valid” index.
- Future width/depth sweeps require a superseding ADR.

## Consequences

- Supersedes deferred-fog for `S8 sequence max length T` from `pj-063` in the parameter registry.
- Implementation must not silently change these sizes.
