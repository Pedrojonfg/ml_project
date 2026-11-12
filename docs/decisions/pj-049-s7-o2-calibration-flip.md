# pj-049. S7 atlas — O2 calibration flip (≥5 of 9 S6 combos)

- **Status:** accepted
- **Date:** 2026-11-12
- **Tags:** modeling | evaluation | interpretation
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

Optional slot **O2** (pj-027) should illustrate why the calibrated two-stage alarm helps. S6 stores nine combinations `s6_<clf>__<reg>` with columns including `z`, `p_cal`, `p_hr`, `r_hat` (mf-021..mf-035). Alarm with calibration uses fold-wise `t` on `p_cal` maximizing F₂ on training-fold calibrated scores (mf-035). Using that same `t` on raw probabilities would confound “calibration helps” with “threshold was tuned for `p_cal`”. pj-032 deferred O2 until S6 preds existed.

## Mathematical framing

For each outer fold and each of the nine S6 combos, define two alarms on an event:

- **Calibrated:** alarm iff `p_cal` ≥ `t` (existing mf-035 `t` for that fold/classifier).
- **Raw:** let \(p_{\mathrm{raw}}\) be the pre-Platt probability (logistic sigmoid of the stage-1 score `z`, or the library probability before Platt — same monotone transform of the score used to fit Platt). Choose **`t_raw`** on the **training fold only** by the same rule as mf-035: maximize F₂ (β=2) of the raw alarm vs `y_hr`, candidates = raw probabilities of training HR events, ties by median. Alarm iff \(p_{\mathrm{raw}} \ge t_{\mathrm{raw}}\).

A combo **flips fail→success** on an OOF event in a repetition if the raw alarm is wrong (FN or FP vs true `y_hr`) and the calibrated alarm is right (TP or TN).

## Options considered

1. **Same `t` on raw and `p_cal`** — simpler; unfair to raw.
2. **Separate `t_raw` (chosen)** — same selection recipe as mf-035 on raw scores in-fold.
3. **Contrast vs LRP/S4 `r_hat` ≥ −6** — different story (not calibration).

## Decision

### Per repetition (seeds 42–46), per event

Count how many of the **nine** S6 combos flip fail→success under the raw vs calibrated alarms above (using that repetition’s OOF row and that fold’s `t` / `t_raw`).

### Event qualifies for O2

- The fail→success flip count is **≥ 5** in **≥ 3 of 5** repetitions (pj-029 stability), **or** — equivalently for implementation — require the flip count ≥5 on at least 3 reps; caption reports k/5 and mean flip counts.
- Clarification locked here: qualification uses **≥5 flips in a repetition** and the event needs **≥3/5** such repetitions (same spirit as other slots).
- `event_id` not already used (pj-047 order: O2 after O1, after all core).

### Select one event

Among qualifiers, **argmax** the **mean over qualifying repetitions** of (number of flipping combos in that rep). Tie → smallest `event_id`.

### Caption (mandatory)

- k/5 reps with ≥5 flips.
- Mean number of flipping combos over those k reps.
- List which combos flip most often (optional short table).
- Note that `t` and `t_raw` are both train-fold F₂-optimal (mf-035 recipe).

### Schedule

O2 remains optional (pj-027); may be cut under the cut list after seeing results without changing this rule.

Partial progress on pj-032 (O2); O3 still open.

## Rationale (developer's own words)

Option 7: explain why the two-part model helps — fail to success on 5 or more of the 9 models; show the case where the change is largest in the sense that more vigilantes are fixed. For the raw alarm, use a separate threshold chosen like the calibrated one (option B), not the calibrated `t` reused on raw scores.

## Consequences

- Atlas code must compute `t_raw` per fold/classifier (or per combo if C differs) when building O2; may cache beside existing `t`.
- Empty O2 pool → omit panel; do not relax “≥5 of 9” or ≥3/5 silently.

## Checks raised

- Raw probability definition must match the score Platt was fit on (log-odds `z` per mf-038).
- Counting nine combos mixes classifiers and regressors; stage-2 `r_hat` does not enter the flip (alarm-only story), but combo identity still labels which head pair is shown in the caption.
