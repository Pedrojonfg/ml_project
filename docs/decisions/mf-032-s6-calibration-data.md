# mf-032. Data used to fit the Platt calibration in S6

- **Status:** accepted
- **Date:** 2026-11-04
- **Tags:** modeling
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

mf-031 chose Platt scaling per stage-1 classifier. The outer training fold has about 7100 events and 74 HR; the validation fold is only used to evaluate. The inner split is `StratifiedKFold(5, shuffle=True, random_state=0)` (mf-028); C is selected as in mf-025..mf-027.

## Mathematical framing

Platt's (a, b) are fitted on pairs (s_i, y_hr_i). Scores of events the classifier was trained on tend to be more confident than scores of new events, so a calibration fitted on them inherits the bias. Out-of-fold scores come from models that did not see the event.

## Options considered

1. **A. Scores of the training fold itself** — no extra fits; inherits the confidence of the training scores.
2. **B. Out-of-fold scores of the inner validation** — each training event is scored by a model trained on the other four inner folds; 5 extra fits per classifier, fold and repetition; the 80% model is not exactly the final model.
3. **C. A part of the training fold reserved to calibrate** — about 15 HR for (a, b), noisy; the classifier loses data.

## Decision

Chose **B**.

- For each outer training fold, repetition and classifier, the 5 inner folds of mf-028 give an out-of-fold score s for every training event.
- The models behind those scores use the C selected for that outer fold (mf-027); the unpenalized model has no C. The imputer and the scaler are refit on the inner training part of each inner fold (mf-010).
- Platt's (a, b) are fitted on the out-of-fold scores and the labels `y_hr` of all training events of the fold.
- The final classifier is the one refit on the whole outer training fold; its scores on the validation fold are mapped with (a, b).

## Rationale (developer's own words)

Even if the 80% model is not exactly the 100% one, I prefer it to A or C. In A the problem of concept 7 occurs (the training scores are very confident, but when it really counts it fails more), and in C there is too much noise.

## Checks raised

- C is selected looking at the same inner folds that give the out-of-fold scores → a small optimism in the calibration data; developer keeps B.
- The 80% model differs from the final one in scale → developer accepts it.

## Expected behavior and validation

Out-of-fold scores computed once per outer fold, repetition and classifier; no validation-fold event enters the fit of the classifier, of C or of (a, b).

## Consequences

- Still to decide: the fitting parameters of the Platt logistic (regularization, solver, weights, target form).
