# mf-036. Calibration measure and reliability diagram of S6

- **Status:** accepted
- **Date:** 2026-11-04
- **Tags:** evaluation
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

Calibrated p comes from Platt per stage-1 classifier (mf-031..033), so calibration is a property of the 3 classifiers, not of the 9 pairs (mf-024). About 93 HR among 8892 events (about 1%, mf-012); each event has one out-of-fold p per repetition, 5 repetitions (pj-005).

## Mathematical framing

Brier = mean of (p - y)^2 over events, y = 1 if HR; a proper scoring rule that mixes calibration and discrimination and uses no bins. A reliability diagram groups events by p and compares the mean p of each group with its observed HR fraction.

## Options considered

- Number: Brier; ECE; log-loss; several; none.
- Bins: equal width with k bins; equal count (quantiles) with k bins.
- Diagram aggregation: one repetition; the 5 repetitions pooled; one diagram per repetition averaged bin by bin.

## Decision

- **Number:** Brier, computed per repetition on all 8892 out-of-fold p and averaged over the 5 repetitions (as pj-006).
- **Diagram bins:** equal count, k = 10: in each repetition the events are sorted by p and split into 10 groups of nearly equal size (`np.array_split`).
- **Diagram aggregation:** one diagram per repetition (mean p and observed HR fraction per bin), then the two values of each bin are averaged over the 5 repetitions, bin by bin.
- One Brier value and one diagram per stage-1 classifier (3 each).

## Rationale (developer's own words)

1. Brier: with only 93 HR, a binned metric will be noisy; Brier does not use bins and is more stable with few events.
2. Equal count, k = 10: equal width does not work because with 1% HR everything falls in the first bin; quantiles spread the events evenly.

## Checks raised

- Brier mixes calibration and discrimination; the diagram is needed to see the calibration itself → developer keeps A.
- With k = 10 there are about 9 HR per bin and the points of the diagram are noisy → developer keeps k = 10.
- Bins change between repetitions because quantiles depend on the data; averaging bin by bin is an approximation.
- The splitting into groups by `np.array_split` is a detail chosen by the AI and confirmed by the developer.

## Expected behavior and validation

3 Brier values and 3 diagrams (10 points each); Brier of a constant p equal to the HR rate as a reference.

## Consequences

- Still to decide: the comparisons and the bootstrap of the S6 rows against LRP, CRP and S4/S5.
