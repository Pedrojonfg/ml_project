# mf-043. KNN magnitude regressor in S4

- **Status:** accepted
- **Date:** 2026-11-12
- **Tags:** modeling | evaluation
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

mf-009 left KNN out of S4 (deferred by the developer). On 2026-11-12 the developer reopened it: KNN enters the S4 table as a fourth row beside OLS, ridge and lasso. Understanding for KNN done the same day (docs/understanding/mf.md, "S4 addendum: KNN"). Reuses mf-008 (target), mf-010 (preprocessing), mf-012 (alarm line), mf-013 (selection by inner AP).

## Mathematical framing

KNN regression: `r_hat(x)` is the mean `risk_final` of the K training events nearest to x under the Euclidean distance on the preprocessed columns. Distance depends on the scale of each column, so the mf-010 preprocessing is kept. The output is continuous, so mf-012 applies unchanged. A training event is its own nearest neighbour (distance 0): predictions on the training fold must exclude the event itself, or `r_hat` carries its own `risk_final` (with K = 1 it is exact and in-sample F2 = 1).

## Options considered

1. **Task:** (A) magnitude regressor, (B) HR classifier (fraction of HR neighbours).
2. **K:** (A) fixed grid chosen by inner CV with inner AP as in mf-013, (B) one fixed K.
3. **Preprocessing and distance:** (A) mf-010 as is + Euclidean on 35 columns, (B) Euclidean on the 30 numeric columns only, (C) Manhattan.
4. **Alarm line:** (A) mf-012 criterion with the event excluded from its own neighbours, (B) inner out-of-fold predictions, (C) event kept as its own neighbour.

## Decision

- **Task:** magnitude regressor. Target `risk_final` untransformed, all 8892 events (mf-008); output continuous `r_hat`. Gives F2, MSE_HR and L like the other S4 rows.
- **K selection:** stratified inner 5-fold on `y_hr` within each outer training fold; criterion = mean over inner folds of AP of `r_hat` vs `y_hr` (mf-013); ties to the largest K. Fixed grid K in {5, 10, 20, 50, 100, 200, 400}, not extended (an optimum on an edge is information). Refit with the selected K on the whole outer training fold.
- **Preprocessing and distance:** mf-010 unchanged (median imputer; `StandardScaler` on the 30 numeric columns; the 5 one-hot columns unscaled, fit on the training fold). Euclidean distance on the 35 columns; neighbours with equal weights.
- **Alarm line:** mf-012 option 1 unchanged (maximize F2 on training-fold predictions, candidates = `r_hat` of the training HR events, ties by median), with each training event excluded from its own neighbours.

## Rationale (developer's own words)

Task: chose option A. K: "A es lo mejor, ya que mantiene el mismo procedimiento de los otros modelos de S4". Preprocessing/distance and alarm line: chose option A; no further rationale given beyond the options as presented (same preprocessing as mf-010, same alarm criterion as mf-012 with only the self-neighbour corrected).

## Checks raised

- Self-neighbour bias applies to the training-fold predictions for `t`; the inner validation predictions in K selection are not affected (validation events are not in the inner training part).
- 35 dimensions with about 7100 training events: distances may concentrate (curse of dimensionality). Not acted on; record in results if KNN underperforms.
- With about 74 HR events in a training fold, large K averages mostly non-HR neighbours; AP should show it.
- Exact library parameters (`KNeighborsRegressor` algorithm, `weights`, `p`, `n_jobs`) to be written explicitly in the code and added to the ledger, as in mf-014 and mf-020.

## Expected behavior and validation

Fourth row of the S4 table with the same event bootstrap and paired differences vs LRP (pj-006, mf-016..mf-020). Stored per fold and repetition: selected K and `t`. Test: a training event is never its own neighbour; with K = 1 on the training fold the prediction does not equal its own `risk_final`.

## Consequences

- mf-009 stays accepted; its "Not doing: KNN" is superseded by this ADR.
- Code: `src/models/linear.py` (or a new `knn.py`), `scripts/run_s4_linear.py`, tests; outputs `results/knn.json`, `preds/knn.parquet`; the S4 table script gets one more row.
- Not doing: HR classifier KNN (fraction of neighbours), distance weights, other metrics, elastic net.

## Result note — 2026-11-12

First run (`results/knn.json`): the selected K was 400, the upper edge of the grid, in 23 of 25 folds (K = 20 in one, K = 5 in one). Per mf-043 the edge is information and the grid is not extended; the developer confirmed keeping the grid as is. KNN is reported as it is: F2 = 0.270, L clipped = 4.304, worse than LRP in F2 and L (paired differences with intervals excluding 0).
