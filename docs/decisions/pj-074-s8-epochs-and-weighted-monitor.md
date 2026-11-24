# pj-074. S8 training — 100 epochs, weighted early-stopping monitor

- **Status:** accepted
- **Date:** 2026-11-16
- **Tags:** modeling | hyperparameters | optimization
- **Decided by:** Pedro
- **AI involvement:** opinion requested (whether the MLP should share the epoch cap; considerations given, no pick)

## Context

In iteration 1 (cap 50 epochs, patience 10, `pj-066`) the GRU best epoch was between 47 and 50 in all 25 outer fits, so the cap was binding. The MLP had median best epoch 34, with 2 of 25 at 47 or more. Early stopping monitored the unweighted MSE on the inner validation split (about 1400 events, about 15 HR). `pj-066` asked for the same recipe in both arms unless there is a strong reason.

## Mathematical framing

Adam updates on mini-batches; after each epoch the monitor is evaluated on the inner validation split and the best weights are restored. With HR weights (`pj-072`) the monitor is the weighted mean squared error \(\sum_i w_i \ell_i / \sum_i w_i\) on \(y_{fit}\), with the same \(w\) as in training (`pj-076`). Training is identical up to epoch 50 for equal seeds, so a larger cap changes only fits that would otherwise still be improving.

## Options considered

1. **Cap 100 for both arms**
2. **Cap 100 for the GRU only** — the MLP keeps 50; the "same recipe" clause of `pj-066` would be broken.
3. **Cap 200** — up to about 18 h of GRU time with the nested CV of `pj-073`.
4. **Other / none**

Monitor: unweighted MSE (as `pj-066`) or weighted MSE with the training \(w\).

## Decision

- **Max epochs 100** for both MLP and GRU; patience 10 unchanged; all other `pj-066` values unchanged.
- **Early-stopping monitor: weighted MSE** with the same \(w\) as training.
- **Trigger to 200 epochs (GRU):** if the median `best_epoch` over the 25 outer refits exceeds 90, the GRU cap is raised to 200 and the GRU is rerun.

Supersedes `pj-066` on max epochs and on the monitor.

## Rationale (developer's own words)

GRU 100 epochs (if still too few, we will change it to 200 later). Yes, the MLP shares it, for consistency, and because in the worst case, thanks to the patience, we stay as we were before. Weighted, so that it matches what it trains. The criterion for going to 200 could be related to the median number of epochs, maybe if it is above 90, but this is more intuition than anything else.

## Checks raised

- Patience plus restoring the best weights limits overfitting to the training set; the inner validation split has about 15 HR, so the chosen epoch is noisy, and a longer cap gives more chances for a lucky minimum → accepted.
- The monitor is a weighted MSE while L is the reported metric → accepted.
- The 90-epoch threshold is an intuition, not calibrated → recorded as such.
- Going to 200 is an extra full GRU run.

## Expected behavior and validation

- The 25 `best_epoch` values of the final run are stored; the trigger is evaluated on them.
- Fits that stopped before epoch 50 in iteration 1 reproduce the same stop with \(w = 1\) (same seeds).

## Consequences

- Parameter registry: S8 max epochs 100; monitor weighted; trigger recorded.
- Not doing: weight decay, dropout, size changes (`pj-073`: no other hyperparameter changes).
