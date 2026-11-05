# mf-038. Score used by the Platt calibration in S6

- **Status:** accepted
- **Date:** 2026-11-04
- **Tags:** modeling
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

mf-031 chose Platt scaling on "the score s" of each stage-1 logistic model but did not define which number s is. A logistic model gives z (log-odds, `decision_function`) and q = sigma(z) (`predict_proba`). With `class_weight='balanced'`, q is shifted upward (mf-011). Found at implementation (Stage 3).

## Mathematical framing

Platt computes p = sigma(a*s + b). With s = z this is a linear recalibration in log-odds: b absorbs a constant shift and a rescales. With s = q a sigmoid is nested inside another sigmoid. Both keep the order of the events for a > 0.

## Options considered

1. **s = z** (log-odds, `decision_function`).
2. **s = q** (probability, `predict_proba`).
3. **Another transformation of z or q.**

## Decision

Chose **s = z**: Platt is fitted on the log-odds (`decision_function`) of the stage-1 classifier, both for the out-of-fold scores of the training fold (mf-032) and for the validation-fold scores.

## Rationale (developer's own words)

Calibrate on z (log-odds, decision_function). Platt computes p = sigma(a*s + b); if s = z, that is a linear transformation in log-odds, which is the natural way to recalibrate (adjusting scale and shift). Using q = sigma(z) would put one sigmoid inside another, a more complicated transformation for no reason.

## Checks raised

None raised.

## Expected behavior and validation

For every classifier, fold and repetition, (a, b) is fitted on the out-of-fold z of the training events.

## Consequences

- The AUC criterion of mf-025 gives the same value on z or q (monotone), so it needs no change.
