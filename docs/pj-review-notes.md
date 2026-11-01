# Pedro — things to review myself

Personal notes; not part of the decision record. Kept untracked on purpose.

## BCa bootstrap interval (chosen in pj-006)

- Status: **I do not fully understand it yet.** I chose it over plain percentile intervals.
- What to check before the oral: what the bias correction and the acceleration constant each do; why the percentiles used are not 2.5 / 97.5; how the acceleration is computed (jackknife over events); whether it behaves sensibly for F2 and for paired differences with only 93 HR.
- Be ready to explain it in one minute, or fall back to percentile intervals and say so.

## Averaging metrics across repetitions (chosen in pj-006)

- Status: **to review later.** I chose to compute the metric in each of the 5 CV repetitions and average the 5 numbers, instead of averaging the predictions per event first.
- What to check: why this is closer to what will be used (one model trained once, not a 5-model ensemble); how the bootstrap must reuse the same resampled events across the 5 repetitions; that the average of F2 is not the F2 of the averaged predictions; what changes for S7 (failure atlas) and S6 (calibration), which need one prediction per event.
