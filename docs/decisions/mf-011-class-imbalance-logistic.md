# mf-011. Class imbalance handling in the logistic model (S4)

- **Status:** accepted
- **Date:** 2026-11-01
- **Tags:** modeling
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

93 HR among 8892 events (1.05 %, pj-003). mf-007 defines the logistic output as `predict_proba`, the estimated HR probability per event.

## Mathematical framing

Weighted cross-entropy: sum_i w_{y_i} [ -y_i log p_i - (1 - y_i) log(1 - p_i) ] (+ penalty, mf-009), with weights w_k = n / (2 n_k) computed on the training fold (about 74 HR of 7100 events, weight ratio about 94 : 1). For a well-specified model the fitted odds are multiplied by about that ratio (logit shift about 4.5), so the output is no longer P(HR | x).

## Options considered

1. **Unweighted.**
2. **`class_weight='balanced'`.**
3. **Manual weights.**
4. **Resampling in the training fold.**

## Decision

Chose **option 2**: `class_weight='balanced'` in the logistic models only, weights computed on the training fold. The regressor (mf-008) is not weighted.

## Rationale (developer's own words)

With 1.05 % positives, the unweighted cross-entropy barely sees the 93 HR: the gradient is dominated by the ~8800 negatives. Reweighting forces the model to take the rare class seriously during training. The alarm threshold (decision on the alarm rule) is adjusted afterwards on the resulting probabilities.

## Checks raised

- Exception to mf-007: with `class_weight='balanced'`, `predict_proba` is an inflated score, not P(HR | x). It still ranks events but is not calibrated. Developer accepts it and records the exception here.
- The unweighted maximum-likelihood probabilities are low but correct under a well-specified model; the practical problem of an unweighted model is a fixed 0.5 threshold, which the alarm-rule decision handles.
- The weighted loss has a different scale than the unweighted one, so the range of regularization strength (C) to explore depends on this choice.
- Weights are computed per training fold (about 74 HR of 7100 events), not from the total 93.

## Expected behavior and validation

Predicted scores are higher on average than the HR base rate (1.05 %) for the penalized and unpenalized logistic fits; the HR events receive higher scores than the non-HR events on average.

## Consequences

- The logistic scores cannot be read as probabilities; calibration is S6's objective.
- The alarm rule (decision 6) works on scores, not on calibrated probabilities.
- Not doing: unweighted fit, manual weights, resampling.

## Scope note — 2026-11-01

After the alarm-rule decision (mf-012), the developer decided that the three logistic models are kept for S6 and do not enter the S4 table. The S4 table has three rows, one per regressor (unpenalized, ridge, lasso). This decision stays accepted but is not implemented in S4; solver and selection decisions of S4 (mf-013, mf-014, mf-015) cover the regressors only.
