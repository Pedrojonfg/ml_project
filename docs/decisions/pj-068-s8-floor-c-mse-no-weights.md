# pj-068. S8 imbalance — floor c + MSE; no sample weights

- **Status:** accepted
- **Date:** 2026-11-15
- **Tags:** modeling | loss
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

S8 regresses `risk_final` (`pj-062`) like S5. S5 uses training-target floor `c` (`pj-026`) and does **not** use sample weights on HR (weights remain an open S5 iteration-2 fog item). S4 magnitude regressors use neither floor nor weights (`mf-008`, `mf-011`). S4/S6 logistic uses `class_weight='balanced'` (`mf-011`) — classification only.

## Mathematical framing

Training loss: mean squared error between \(\hat{r}\) and \(y_{\mathrm{fit}} = \max(\texttt{risk\_final}, c_{\mathrm{fold}})\), with \(c_{\mathrm{fold}}\) computed exactly as in `pj-026` on the fold training events used for fitting (never official CV val). Evaluation metrics still use unclipped `risk_final` (`pj-001`, `pj-007`). No per-sample weights in the MSE.

## Options considered

1. Floor `c` only (S5-consistent for regressors).
2. Sample weights only.
3. Both floor `c` and weights.
4. Neither.
5. Other / none.

## Decision

Chose **option 1**: apply **`pj-026` floor `c`** on both S8 arms; **no** train sample weights; training objective **MSE** on `y_fit`.

## Rationale (developer's own words)

Go with floor only, no weights in train, consistent with S5 — the most direct comparison — and ship that.

## Checks raised

- Combining weights + floor would be new for project regressors — rejected in favour of S5 consistency.
- `pj-026` revocation criteria R0–R4 are defined for trees; for S8, record the same diagnostics when practical; reopening `c` via nested CV still requires an ADR if R-style failure is observed.
- Inner-val early stopping (`pj-066`) monitors MSE on the same `y_fit` scale used in training.

## Expected behavior and validation

- Both MLP and GRU fit on floored targets; OOF `r_hat` scored against true `risk_final`.
- No `sample_weight` / class-balanced reweighting in the S8 loss.

## Consequences

- Parameter registry: S8 loss = MSE; S8 floor c = pj-026 recipe; S8 sample weights = none.
