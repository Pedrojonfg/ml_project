# pj-014. S5 tree models — regression target and prediction interface

- **Status:** accepted
- **Date:** 2026-10-27
- **Tags:** modeling | evaluation
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

Scope S5 compares Random Forest and gradient boosting to the LRP baseline under the S1 protocol (pj-004–pj-007). Scope S6 (two-stage calibrated P(HR) + magnitude) is a separate design (ADR 008); it must not be conflated with S5. Kelvins metrics consume continuous risk predictions; F₂ applies the HR threshold to predicted and true risk values.

## Options considered

1. **Direct regression of `risk_final`** — single continuous log₁₀ prediction per event; F₂, MSE_HR, and L computed as for LRP via `src/metrics.py`.
2. **HR classifier + magnitude regressor in S5** — two-stage-style pipeline within S5; requires a defined rule to assemble a scalar risk for Kelvins metrics.
3. **HR classification only in S5** — no native continuous output for MSE_HR / L without an extra mapping.

## Decision

Chose **option 1**.

## Rationale (developer's own words)

S5 should train the continuous decimal log risk and evaluate it the same way as LRP; F₂ can be obtained by thresholding that continuous prediction. The calibrated two-stage approach belongs elsewhere (S6), not in this scope.

## Mathematical framing

Training minimizes a regression loss on target \(y = \texttt{risk\_final}\) (unclipped log₁₀ operational risk, pj-001). Inference outputs \(\hat{y}\) per event. Evaluation: \(\mathrm{F}_2\) compares \(\hat{y} \ge -6\) vs \(y \ge -6\); \(\mathrm{MSE}_{HR}\) on events with \(y \ge -6\); \(L = \mathrm{MSE}_{HR} / \mathrm{F}_2\) per pj-007.

## Checks raised

- Class imbalance (~1% HR) may bias plain regression toward conservative risks; F₂ still depends on the −6 threshold (understanding record S5, hazard noted).
- Two-stage S6 remains the place for explicit P(HR) calibration and reliability analysis.

## Consequences

- `src/models/trees.py` (or equivalent) fits regressors on `risk_final`; `predict` returns continuous log₁₀ risk per event.
- No separate HR classifier in S5 for the main comparison table vs LRP.
- Prediction artifacts must expose continuous `r_hat` (and derived `p_hr` if stored, from threshold rule) consistent with the project pred contract.
