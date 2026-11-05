# mf-031. Calibration method of the stage-1 score in S6

- **Status:** accepted
- **Date:** 2026-11-04
- **Tags:** modeling
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

Stage 1 gives a score s per event from each of the three logistic models (mf-021); `class_weight='balanced'` shifts the raw output (mf-011). One calibrator per classifier, so 3 calibrations (mf-024). About 74 HR per training fold (mf-012).

## Mathematical framing

Platt scaling maps s to p = sigma(a*s + b) with two parameters (a, b) fitted by logistic regression of y_hr on s. With a > 0 it is increasing and keeps the order of the events; with a < 0 it reverses the order; with a = 0 it gives the same p to all events.

## Options considered

1. **A. Platt scaling** — assumes a sigmoid distortion; 2 parameters; order-preserving for a > 0.
2. **B. Isotonic regression** — assumes only monotonicity; step function; more data per step.
3. **C. Platt and isotonic** — 6 calibrators.
4. **D. No calibration** — the raw output is shifted by `balanced`.

## Decision

Chose **A**: Platt scaling for each of the three stage-1 classifiers. If the fitted a is not positive, the fit is used as it is and the fold is flagged in the results.

## Rationale (developer's own words)

From what was seen in the understanding, I think Platt scaling is better than isotonic. With a positive, it keeps the order of the events, while isotonic gives a step function and I see it as less precise.

## Checks raised

- With about 74 HR per fold, Platt (2 parameters) is less sensitive to noise than a step function → none, developer keeps A.
- Platt with a > 0 does not change the AUC; the calibration changes the values of p, which affect the final result only through the combination and the alarm line (not yet decided).
- A fitted a < 0 reverses the order of the events → developer chose to keep the fit and flag it, for later analysis.

## Expected behavior and validation

One (a, b) per classifier, outer training fold and repetition, stored with a flag when a <= 0.

## Consequences

- Still to decide: the data the calibrator is fitted on, and the fitting parameters of the Platt logistic (regularization, solver, weights, target form).
