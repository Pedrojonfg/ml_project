# pj-072. HR sample weights with recomputed floor `c`

- **Status:** accepted
- **Date:** 2026-11-16
- **Tags:** modeling | loss | preprocessing
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

Iteration 1 left predictions compressed around the floor (MLP `r_hat` between −6.23 and −5.84 at percentiles 1–99.9; GRU between −6.14 and −5.75), so the −6 alarm line sits about 0.09 above the floor `c ≈ −6.09`. `pj-068` fixed "no sample weights"; the ledger lists loss and HR weights as S5 iteration-2 levers. Precedent: `mf-011` uses `class_weight='balanced'` in the logistic models only. The original competition paper could not be checked (PDF missing from the repo).

## Mathematical framing

Training weights: \(w_i = w\) if `risk_final` \(\ge -6\), else 1. With a weighted-mean predictor, a region with HR fraction \(p\) predicts \(m(c) + p_w(\mu_{HR} - m(c))\), where \(p_w = \dfrac{w p}{w p + 1 - p}\) and \(m(c)\) is the mean of \(\max(y, c)\) over non-HR training events.

`pj-026` chooses `c` so that the alarm \(\hat r \ge -6\) fires exactly when \(p \ge p^* = F^*/5\) (F\* = F₂ of LRP on the training part). With weights the same requirement becomes:

\[
q(c) = \frac{-6 - m(c)}{\mu_{HR} - m(c)} = p^*_w,\qquad p^*_w = \frac{w\,p^*}{w\,p^* + 1 - p^*},
\]

solved with Brent on the `pj-026` bracket \([-29.99, -6.0005]\), per training part, never using validation events. For \(w = 1\) it reduces to `pj-026`.

Reference values on the full train (93 HR of 8892, \(p^* = 0.0985\)):

| w | 1 | 2 | 5 | 10 | 20 | 50 | ≈94 |
|---|---|---|---|---|---|---|-----|
| c | −6.092 | −6.184 | −6.461 | −6.927 | −7.872 | −10.80 | −15.30 |

Metrics keep using unclipped `risk_final` (`pj-001`, `pj-007`).

## Options considered

1. **Change the loss (Huber / quantile)** — assumes a robust or high-quantile fit is enough; unavailable for RF in scikit-learn without a new dependency; the theoretical `c` would not carry over directly.
2. **HR weights, `c` unchanged** — with \(w > 1\) the −6 line would no longer be F₂-optimal: the alarm would fire from \(p \approx 0.052\) (w = 2) or \(p \approx 0.011\) (w = 10) instead of 0.098.
3. **HR weights + recomputed `c`** — keeps the −6 alarm line F₂-optimal under the weighted-mean model; works for all four models.
4. **Both a new loss and weights**
5. **Other / none**

## Decision

Chose **option 3**: weights \(w\) on HR events in all four models, with `c` recomputed from the equation above. The weighted R3 diagnostic converts the weighted probability back with \(p = p_w / (w - (w-1)\,p_w)\). Supersedes the "no sample weights" clause of `pj-068` and extends the derivation of `pj-026`.

## Rationale (developer's own words)

Intuitively, HR weights plus recalculating `c` seems the most logical to me. It works for all models, it is easily understandable and explainable, and it fits the work done previously.

## Checks raised

- A large \(w\) lowers `c` and weakens the floor (86% of non-HR at the floor with w ≈ 94, SD of \(y_{fit}\) among non-HR ≈ 1.96) → the grid is capped at 10 (`pj-073`).
- `R3` of `pj-026` assumes unweighted predictions; unconverted it would fire by construction → converted as above.
- `min_samples_leaf` in the trees counts samples, not weights → noted, no change made.

## Expected behavior and validation

- Unit check: \(c(w=1)\) equals the `pj-026` value (−6.092 on the full train).
- \(c(w)\) decreases monotonically in \(w\) on the same training part.
- Both families receive the same weights; `R0`–`R4` recomputed with the converted `R3`.

## Consequences

- `floor_c` and `floor_c_diagnostics` take `w`; RF/GBDT pass `sample_weight`; the networks use the weighted mean (`pj-076`).
- Not doing: Huber/quantile loss, alarm line other than −6, residual-on-LRP target.
