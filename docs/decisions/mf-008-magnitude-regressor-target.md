# mf-008. Magnitude regressor task and target (S4)

- **Status:** accepted
- **Date:** 2026-11-01
- **Tags:** modeling | evaluation
- **Decided by:** Mario
- **AI involvement:** opinion requested

## Context

mf-007 gives only a probability per event; MSE_HR and L (pj-007) need a continuous `r_hat` evaluated on HR events. S5 trees regress `risk_final` (pj-014) and, in a later iteration, fit on `max(risk_final, c)` (pj-026).

## Mathematical framing

Penalized linear regression (ridge / lasso) of `risk_final` (log10, unclipped) on the v1 features, trained on all 8892 events. Least squares assumes additive noise with constant variance on the whole scale; the loss is dominated by the mass of low-risk events (only 93 events have `risk_final >= -6`).

## Options considered

1. **All events, target `risk_final` untransformed.**
2. **All events, transformed target** (for example a lower floor).
3. **Only HR (or high-risk) events**, which needs a separate gate to give `r_hat` to every event.
4. **Residual over LRP** (`risk_final` - last `risk`).

## Decision

Chose **option 1**: ridge / lasso trained on all 8892 events with target `risk_final` untransformed, producing `r_hat`, the continuous log10 risk prediction per event.

## Rationale (developer's own words)

MSE_HR and L need a continuous `r_hat` evaluated on the HR events. Training only on the 93 HR would leave too little data for 30 features even with regularization, and training on all events replicates the S5 tree formulation and keeps comparability.

## Checks raised

- The target is not Gaussian with constant variance; the loss is dominated by low-risk events, so `r_hat` may be biased in the HR zone. Developer recognises this risk and keeps option 1.
- S5 trees were refitted on `max(risk_final, c)` (pj-026), so the linear model and the trees do not share the same training target; comparison remains valid on F2, MSE_HR and L.
- Interacts with the alarm / `r_hat` decision (decision 6).

## Expected behavior and validation

If `r_hat` shows systematic bias in the HR zone, the shape of the target will be reviewed (supersede or confirm this ADR). The review criterion is qualitative for now; the developer will make it concrete once the alarm / `r_hat` decision is closed and first results exist.

## Consequences

- Not doing: HR-only training, floor on the target, residual over LRP (in this ADR).
- Decision of the alarm rule and the penalty type remain open.

## Reopened and confirmed — 2026-11-01

The qualitative review trigger was met before implementation. Check run during the S4 ledger session (ridge, alpha = 1.0, repetition 0, mf-008 and mf-010 settings, one run, not tuned):

- Without a floor, the regressor never reaches r_hat >= -6 (0 of 8892; r_hat range -34.6 to -11.3), so F2 at the -6 alarm line is 0 and L is infinite. AUC of r_hat for y_hr is 0.92.
- With a floor c in {-25 ... -7} F2 is also 0; with c = -6.09 (S5 rule, pj-026) r_hat is compressed to a range of 0.1 and only 2 events alarm. Sweeping the alarm line gives best F2 = 0.31 with the floor and 0.42 without it (thresholds swept on the same out-of-fold predictions, an optimistic bound).

Developer's decision: keep option 1 (no floor, target `risk_final` untransformed); the floor does not solve the problem for a linear model. The lever that produces F2 is the alarm line, decided in a separate ADR (mf-012). Status stays accepted; not superseded.
