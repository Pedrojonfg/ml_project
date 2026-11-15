# mf-048. Hyperparameters of kernel ridge in S10

- **Status:** accepted
- **Date:** 2026-11-15
- **Tags:** modeling | evaluation
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

RBF kernel with `gamma = c / m` (mf-045, mf-047), target mf-043, preprocessing mf-044, centering mf-046. Selection protocol of the other S4 rows: mf-013 (criterion), mf-015 (inner split), mf-021 (grid edge as information). Measured on a sample of 2000 events: median squared distance m about 56, nearest-neighbour squared distance about 3.9 (median). For `c = 10`, the kernel value is about 4.5e-5 for a typical pair and about 0.5 for the nearest neighbour. Eigenvalues of K (sample of 2000, c = 10): maximum 42, median 0.64, 10th percentile 0.13; they scale about with n. One diagonalization of a 3000x3000 matrix takes 8 s on 16 cores (about 55 s extrapolated to 5700); all lambda values of one `c` come from the same one.

## Mathematical framing

For fixed c, lambda trades the fit to the training events against the smoothness of `f`: eigen-directions of K with eigenvalue much smaller than lambda are shrunk away, those much larger are kept. `c` fixes the locality of the kernel.

## Options considered

1. **c:** (A) 0.1, (B) 1, (C) 10, (D) 30 (kernel values for a typical pair and for the nearest neighbour in the table of mf-047 context); or tuned over a grid of 3 to 7 values at 5.7 to 13 hours.
2. **lambda grid:** (A) 1e-2 to 1e2 (4 decades), (B) 1e-3 to 1e3 (6 decades), (C) 1e-4 to 1e4 (8 decades); 25 log-spaced values.
3. **Criterion:** (A) mean inner AP as mf-013, (B) squared error on all events, (C) inner L or F2 (needs an alarm line inside each inner fold). **Grid edge:** (A) fixed grid, edge is information, (B) automatic extension, (C) one-standard-error rule.

## Decision

- `c = 10`, fixed, not tuned (`gamma = 10 / m`, m per mf-049).
- lambda grid: `np.logspace(-3, 3, 25)`.
- Selection: inner `StratifiedKFold(n_splits=5, shuffle=True, random_state=0)` on `y_hr` within each outer training fold (mf-015); criterion = mean over the 5 inner folds of the AP of `r_hat` vs `y_hr` (mf-013); exact ties go to the highest lambda.
- Grid fixed, never extended; an optimum on the edge is information, not something to resolve automatically (mf-013, mf-021).
- After selection, refit with the selected lambda on the whole outer training fold, preprocessing and centering refit on it (mf-044, mf-046); that model gives the validation predictions and feeds the alarm line.

## Rationale (developer's own words)

For `c`: I think it is the most balanced; the kernel value of the nearest neighbour is 0.5. For the lambda grid: the most balanced, for the same reason as before. For criterion and edge: it is the most coherent with what we have been doing throughout the project.

## Checks raised

- `c` is fixed without validation; its effect on the results is not measured.
- The 0.5 for the nearest neighbour comes from a sample of 2000 events; with about 5700 training events the nearest neighbour is closer and the value somewhat higher.
- The inner AP criterion and the alarm line of mf-012 measure different things, as in the other S4 rows.
- An optimum on the edge of the lambda grid is reported, not corrected.

## Expected behavior and validation

Stored per fold and repetition: the selected lambda, the mean inner AP per lambda, `m`, gamma and the alarm line. Test: with a very large lambda the prediction equals the training mean; the selected lambda is deterministic under the seed.

## Consequences

- Not doing: tuning `c`, other lambda ranges, other criteria, automatic grid extension, one-standard-error rule.
- Cost: one diagonalization per inner fold (5 per outer fold), 25 outer folds.
- Open: alarm line, library parameters and numerical details, compute budget.

## Result note — 2026-11-15

First full run (`results/kernel_ridge.json`, 2 repetitions, 10 outer folds, 3654 s): the selected lambda was in the interior of the grid in all 10 folds (from 0.056 to 3.2; grid 1e-3 to 1e3), so no edge flag. gamma about 0.179 (m about 56). The alarm line t (mf-050) fell between -12.9 and -21.5, far below -6. Kernel ridge is reported as it is: F2 = 0.199 [0.158, 0.247], MSE_HR clipped = 1.148, L clipped = 5.77 [4.05, 8.74]; worse than LRP in F2 and L (paired differences with intervals excluding 0) and worse than the other S4 rows in F2 and L clipped. `c = 10` was fixed without validation (mf-048), so the effect of c is not measured. Reasons for the gap are not investigated.
- Not saved: `preds/kernel_ridge.parquet` (the run ended with an ImportError for pyarrow after writing the json; pyarrow is not installed here nor in requirements.txt).
