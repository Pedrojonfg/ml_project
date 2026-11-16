# pj-071. Iteration 2 — scope and fixed elements (S8 + S5 retrain)

- **Status:** accepted
- **Date:** 2026-11-16
- **Tags:** modeling | framing | evaluation
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

S8 iteration 1 (`pj-061`..`pj-070`) ran on 2026-11-15 (5 repetitions x 5 folds, S1 protocol). Results against LRP (F₂ 0.492, L clipped 0.548):

| Model | F₂ | L clipped | `pj-026` criteria that fired |
|-------|----|-----------|------------------------------|
| mlp | 0.217 | 5.30 | R1 |
| gru | 0.036 | 49.3 | R1, R2, R3 |
| rf (S5) | 0.433 | 1.87 | R4 (`pj-043`) |
| gbdt (S5) | 0.417 | 1.87 | none |

In the GRU the best epoch fell between 47 and 50 in all 25 outer fits (cap 50, `pj-066`). `pj-044` already scheduled the S5 reopen for C2. `pj-026` says that if any criterion fires, `c` should become a nested-CV hyperparameter (option 3).

## Mathematical framing

Unchanged from earlier ADRs: target \(y = \texttt{risk\_final}\) (`pj-001`), alarm \(\hat p_{HR} = \mathbf 1\{\hat r \ge -6\}\) (`pj-062`), training target \(y_{fit} = \max(y, c)\) (`pj-026`), evaluation on unclipped `risk_final` (`pj-007`). Only the sample weights and the selection of hyperparameters change (`pj-072`, `pj-073`).

## Options considered

1. **Retrain only S8 (mlp, gru)** — assumes S5 results stay as in `pj-025`; S7/S9 unchanged.
2. **Retrain all four (rf, gbdt, mlp, gru)** — assumes both families should get the same improvement lever; S7/S9 must be regenerated.
3. **Other / none**

Elements considered for change and kept: learned alarm line `t` (`mf-012`-style) instead of −6; target as residual `risk_final − LRP`; floor `c` replaced by nested-CV `c` (`pj-026` option 3).

## Decision

Chose **option 2**. All four models are retrained under the S1 protocol. The alarm stays at −6 (no learned `t`), the target stays `risk_final`, and the floor `c` is kept for all four. The S7 atlas and the S9 outputs are regenerated from the new predictions.

## Rationale (developer's own words)

Everything is retrained. I understand the idea is that we have to improve this somehow, so I would also retrain RF and GBDT, to see if we can improve them too. I would not add an alarm line to any model; the target stays `risk_final`. We keep the floor because it can be said without any problem that all experiments have shown it is necessary, given the shape of the distribution: we tried to be honest and not use it, but the model learns better with the floor, and we computed its theoretical value. So all models keep the floor. For S7 and S9, regenerate.

## Checks raised

- `pj-026` prescribes nested-CV `c` when a criterion fires; R4 fired for RF and R1–R3 fired in S8 → the developer keeps the theoretical `c` (rationale above). The R0–R4 diagnostics are still computed and recorded.
- In the GRU, an alarm line at `t = −6.04` would have raised F₂ by +0.151 (R2); it is not used because −6 is kept for comparability (`pj-062`) → developer accepted.

## Expected behavior and validation

- Four result files (`rf`, `gbdt`, `mlp`, `gru`) produced under the same protocol, slugs and artifact layout as `pj-070` / `pj-020`.
- S7 and S9 outputs rebuilt from the new predictions; S6 is unaffected (it uses S4 predictions).

## Consequences

- Iteration-1 outputs of the four models are kept (engineering note in `LEDGER.md`) so that `pj-075` can quote a few figures.
- `pj-072`..`pj-076` define what changes inside the retrain.
