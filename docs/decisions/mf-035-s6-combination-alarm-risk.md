# mf-035. Combination of the two stages in S6: alarm rule and predicted risk

- **Status:** accepted
- **Date:** 2026-11-04
- **Tags:** modeling | evaluation
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

Per event, stage 1 gives a calibrated probability p (Platt, mf-031..033) and stage 2 gives r_hat = E[risk | features] over all events (mf-022, mf-023, mf-034), so m_HR and m_low are not separately available. Metrics: F2, MSE_HR and L, clipped and unclipped (pj-007). In S4 the alarm was r_hat >= t, with t maximizing F2 on the training-fold predictions (mf-012). Out-of-fold scores of the training fold exist from mf-032.

## Mathematical framing

The alarm needs a binary decision per event; MSE_HR needs a predicted risk per event. Platt with a > 0 is increasing, so the alarm set at an optimal t on p equals the one on the raw score s: calibration does not change F2. MSE_HR with r_hat equals the stage-2 regressor's MSE_HR.

## Options considered

- Alarm: p >= t with t maximizing F2; r_hat >= t (as S4); a rule combining p and r_hat.
- Predicted risk: r_hat as it is; a function of p and r_hat.
- Predictions on which t is chosen: in-sample p of the training fold (as mf-012), or out-of-fold p.

## Decision

- **Alarm (F2):** alarm if p >= t. In each outer training fold, repetition and model, t maximizes F2 (beta = 2) on the out-of-fold calibrated p of the training events (the out-of-fold scores of mf-032 mapped with Platt's (a, b)). Candidates for t: the p values of the HR events of the training fold. Ties: the median of the tied candidates (for an even number, the mean of the two central ones), as mf-012. t and its variability across folds are stored.
- **Predicted risk (MSE_HR):** r_hat of stage 2 as it is.
- **Evaluation:** the validation fold is scored with the final classifier and Platt's (a, b) for the alarm, and with the stored S4 r_hat for the risk.

## Rationale (developer's own words)

Alarm: use p >= t, with t chosen to maximize F2 in training (as mf-012). The calibrated p is designed to distinguish HR from non-HR, which is what the alarm needs. Predicted risk: use r_hat directly. MSE_HR measures the error in the risk prediction, and r_hat is the risk estimate; p is a class probability, not a risk number. Each stage contributes what it knows: stage 1 decides whether it is HR, stage 2 how much risk there is. For t: the out-of-fold p is already computed, and using it avoids the bias of choosing t on the same events the classifier was trained on.

## Checks raised

- Calibration does not change F2 (monotone transform of s with a > 0) → developer keeps p >= t.
- MSE_HR of every two-stage model equals the S4 regressor's, so only F2 (and L) varies among the 9 combinations → developer keeps r_hat directly.
- If Platt's a <= 0 in a fold, the alarm set changes (reversed order) → flagged as in mf-031.

## Expected behavior and validation

Out-of-fold F2 above 0 for the two-stage models; stored t per fold.

## Consequences

- Still to decide: the evaluation (calibration metric, bins of the reliability diagram, comparisons with the bootstrap).
