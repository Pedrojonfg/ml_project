# pj-062. S8 task — regress `risk_final`; alarm at −6

- **Status:** accepted
- **Date:** 2026-11-15
- **Tags:** modeling | evaluation
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

S8 has two arms (tabular MLP and sequence; `pj-061`). S5 regresses `risk_final` and derives `p_hr` by thresholding continuous predictions at −6 (`pj-014`, `pj-020`). S4 magnitude regressors use a learned alarm threshold `t` on `r_hat` (`mf-012`). Kelvins metrics need a continuous `r_hat` for MSE_HR and L (`pj-007`); F₂ needs an alarm rule.

## Mathematical framing

Training minimizes a regression loss on \(y = \texttt{risk\_final}\) (unclipped log₁₀ operational risk, `pj-001`). Inference outputs \(\hat{r}\) per event. Alarm: \(\hat{p}_{\mathrm{HR}} = \mathbf{1}\{\hat{r} \ge -6\}\). Evaluation uses F₂, MSE_HR, and L as for LRP / S5 (`pj-007`).

## Options considered

1. **Regress `risk_final` + alarm at −6 (both arms)** — same interface as S5/LRP.
2. **Regress `risk_final` + learned `t` (mf-012-style)** — can correct scale bias for F₂; alarm ≠ HR definition cut.
3. **Classify `y_hr` only** — needs a separate map to `r_hat` for MSE_HR / L.
4. **Different task/alarm per arm** — arms less comparable to each other.
5. **Other / none**

## Decision

Chose **option 1**: both S8 arms train **regression of `risk_final`** and use **alarm at −6** on `r_hat` for F₂.

## Rationale (developer's own words)

For now −6, because it is the most comparable.

## Checks raised

- A model biased toward low risks can have poor F₂ under a hard −6 cut even if ranking is decent — same trade-off accepted for S5; developer accepted for S8.
- Concrete regression loss (MSE, Huber, …) and whether `pj-026` training-target floor `c` applies to S8 remain open.

## Expected behavior and validation

- Each S8 arm exposes continuous `r_hat` and `p_hr = 1{r_hat >= -6}` per event under the S1 fold protocol.
- Metrics match `pj-007` using that `r_hat` / alarm pair (no learned alarm `t` in S8 for now).

## Consequences

- Sequence and tabular arms share this task/alarm contract (`pj-061`).
- Later ADRs fix loss form, optional floor `c`, architectures, and training details.
