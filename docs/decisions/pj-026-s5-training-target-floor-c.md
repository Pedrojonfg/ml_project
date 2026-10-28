# pj-026. S5 training-target floor c derived from F₂ theory

- **Status:** accepted
- **Date:** 2026-10-28
- **Tags:** modeling | preprocessing | evaluation
- **Decided by:** Pedro
- **AI involvement:** options + critique; opinion requested (tolerances of R2–R4)

## Context

Runs 0 and 1 (pj-016/pj-024 settings) gave RF OOF F₂ = 0 and GBDT F₂ ≈ 0.07, far below LRP (≈ 0.49). Diagnosis: with squared error each leaf predicts the mean of `risk_final`; about 80 % of events sit at the −30 floor, so even among events with LRP in (−6, −5] the mean is ≈ −19.8 and never reaches −6. More capacity cannot fix this.

With a floor c on the training target, a leaf with HR fraction p predicts approximately p·μ_HR + (1 − p)·m(c), where m(c) is the mean of `max(y, c)` over non-HR events. The leaf raises an alarm (≥ −6) iff

p ≥ p*(c) = (−6 − m(c)) / (μ_HR − m(c)).

So choosing c is equivalent to choosing the HR fraction a leaf needs before it alarms. Without a floor (c = −30), p* ≈ 0.96, which explains F₂ = 0.

## Options considered

1. c = −6.001 (same value as the metric clip): p* ≈ 0.001, alarms almost everywhere.
2. Derive c from the F_β-optimal threshold for calibrated probabilities, p* = F*/(1 + β²) (Lipton, Elkan & Naryanaswamy, 2014; outside course notes; checked by simulation, 2026-10-28).
3. Treat c as a hyperparameter selected by CV (nested CV to avoid optimistic selection).

## Decision

Chose **option 2**.

Within each training fold (never using validation events):

1. μ_HR = mean of `risk_final` over HR events (`risk_final >= -6.0`).
2. F* = F₂ of LRP (`lrp` vs `risk_final`) on the training-fold events.
3. p* = F*/5 (β = 2).
4. Solve p*(c) = p* for c with Brent's method on the bracket [−29.99, −6.0005].
5. Fit the model on y_fit = max(`risk_final`, c).

Evaluation targets are unchanged: metrics use the original unclipped `risk_final` (pj-001, pj-007), aggregated per pj-006; grid selection per pj-025.

Reference values (full train, F* = 0.4923): c ≈ −6.092, p* ≈ 0.098; per-fold range −6.100 to −6.084. Sensitivity: F* ∈ [0.3, 0.6] gives c ∈ [−6.115, −6.054].

## Revocation criteria (mandatory, automatic)

Computed from OOF predictions after each run and written to `results/floor_c_diagnostics.json`. Pooled predictions follow the same pooling as pj-025; minimum counts refer to distinct HR events. If **any** criterion fires → reopen this ADR and switch to option 3 (c as a hyperparameter chosen by nested CV, grid centred on the theoretical c).

| ID | Assumption checked | Fires if |
|----|--------------------|----------|
| R0 | The model reaches F > 0 | OOF F₂ = 0 |
| R1 | Realised F₂ is close to the assumed F* | mean OOF F₂ (pj-006) < F*/2 or > 2·F* (F* = mean over folds of LRP F₂ used) |
| R2 | −6 is the F₂-optimal alarm line | max over t ∈ [−7, −5] (step 0.01) of F₂ with alarm `r_hat >= t`, minus F₂ at t = −6, exceeds **0.05** |
| R3 | Leaf HR fractions are calibrated | in the alarm zone (`r_hat >= -6`), observed HR rate / mean p̂ outside [0.5, 2], where p̂ = clip((`r_hat` − c)/(μ_HR − c), 0, 1) with that fold's c and μ_HR; not evaluable if fewer than 10 HR events in the zone |
| R4 | A single μ_HR fits all HR events | mean `risk_final` of detected HR minus mean of missed HR, in absolute value, exceeds 0.8 × SD of `risk_final` among HR training events (Cohen's d = 0.8, "large"; ≈ 0.54 on full train); not evaluable if fewer than 10 HR in either group |

Tolerance provenance: R2 sits above the repetition-to-repetition spread of GBDT F₂ observed in run 1 (0.051–0.089); R1 and R3 factor-2 bands are pragmatic, not standard; R4 uses Cohen's (1988) convention. Proposed by the AI at the developer's request, accepted by the developer.

Not a revocation criterion: trees losing to LRP on L. If R0–R4 pass and results remain poor, the cause lies elsewhere (features, loss, model), not in c.

## Rationale (developer's own words)

Derive c from F₂ theory so as not to waste unnecessary compute. Use the LRP F₂ as F*; compute c in each fold. Accept the proposed tolerances.

- F* = LRP F₂: there is no leakage, and it is better to take this number than an arbitrary one. There is not enough compute for a fixed-point iteration (F* from the model's own F₂): we are still polishing the model and will do several more runs, so it would multiply the time of every run. Once everything is done and tuned, a fixed point may be considered.
- Per fold: consistent with pj-015 (data-derived quantities fitted on the training fold only).

## Checks raised

- F* is an assumption (the model performs at roughly the LRP level), not information leakage, because LRP needs no training and its F₂ is computed on the training fold only. R1 checks it.
- Near −6, c is very sensitive: −6.09 behaves very differently from −6.001 (p* ≈ 0.10 vs 0.001).
- The derivation optimises F₂ only; L also contains MSE_HR.
- Leaves with few HR events give noisy fractions; R3 checks this.

## Consequences

- `src/models/trees.py`: per-fold c computation; fit on floored target; diagnostics R0–R4.
- Supersedes nothing; adds a training-target transform to pj-014 (target remains `risk_final` for evaluation).
