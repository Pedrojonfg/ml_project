# pj-006. Uncertainty reporting

- **Status:** accepted
- **Date:** 2026-10-24
- **Tags:** modeling | evaluation
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

93 HR events (pj-003) make every metric noisy. Predictions come from repeated 5-fold CV (pj-004, pj-005), so each event has 5 out-of-fold predictions per model.

## Mathematical framing

Event-level bootstrap. In each resample, events are drawn with replacement from all events jointly (the number of HR varies, about 93 ± 10; no bounds on it), using the same resampled events for every repetition and, in paired comparisons, for every model. The metric is computed in each repetition and averaged over the 5 repetitions. B = 10000 resamples; 95 % BCa interval. Paired comparison: bootstrap interval of metric(model) - metric(baseline) on the same resamples, for baseline = LRP and baseline = CRP. The spread of the metric across the 5 repetitions is reported as supplementary information, not as a confidence interval.

## Options considered

1. **Spread across folds** — simple; folds share training data, so it underestimates noise.
2. **Event-level bootstrap** — also gives paired differences.
3. **Both.**

Resampling: all events jointly, or positives and negatives separately. Interval: percentile or BCa. Aggregation over repetitions: average predictions first, or average metrics.

## Decision

Event-level bootstrap as above; per-repetition metrics averaged; across-repetition spread reported as supplementary information.

## Rationale (developer's own words)

10000 resamples because it is cheap. 95 % by convention. Joint resampling (with no bounds when in doubt). BCa, the corrected interval (flagged for personal review: not fully understood yet). Averaging metrics rather than predictions because it is more professional and closer to what will be used. The across-repetition spread is reported.

## Checks raised

- Resamples with a very low or high number of HR are kept; about 1-4 % of resamples fall outside 70-115 HR → developer kept no bounds.
- Averaging predictions would act as a 5-model ensemble and flatter the metric → developer chose averaging metrics.
- Intervals will be wide with 93 HR.
- The across-repetition spread has 5 values on the same 93 HR and underestimates total uncertainty → reported only as supplementary.

## Expected behavior and validation

For LRP and CRP (no training) all repetitions coincide, so the repetition average equals a single evaluation and the spread is zero. The bootstrap interval of LRP's L on the filtered set should be of the order of the earlier estimate (SE ~0.1-0.2).

## Consequences

- The implementation lives in `src/evaluation.py` (S4 owner); this ADR is its specification.
- Not doing: bounds on resample HR counts; stratified resampling.
