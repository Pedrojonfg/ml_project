# mf-042. Grid-edge result of the logistic strength in S6 (applies mf-029)
- **Status:** accepted
- **Date:** 2026-11-05
- **Tags:** modeling
- **Decided by:** Mario
- **AI involvement:** options + measurement (read-only)

## Context
mf-029 fixed the grids and left to the developer the decision on a selected C at an edge. After the full run: L1 selected C = 0.01 (lower edge) in 25/25 folds, with the best mean AUC also at 0.01 in 24/25. L2 selected C = 1e-4 (lower edge) in 19/25 folds, with C* in the interior (mostly 0.01-0.05) and tie sets of 5-25 values (median 13).

## Options considered
1. Leave the grids as they are and report the edge selections as a limitation.
2. Extend the L1 grid downward and rerun L1 (about 11 h).
3. Change the L2 tie rule and rerun L2.
4. A combination of 2 and 3.

## Decision
Chose **1**. Grids, rule and results stay as they are. No extension, no rerun. The edge selections are reported as a limitation.

## Rationale (developer's own words)
The AUC is almost flat across the grid, so extending it would not improve the model; it would only move the edge somewhere else without resolving it.

## Checks raised
- For L2 the flatness is supported by the tie-set sizes (median 13 of 25 values within one SE).
- For L1 the per-C curves were not stored, so a read-only measurement was made on one outer fold (rep 0, fold 0; inner 5-fold, same split as mf-028): mean AUC 0.500 at C = 1e-4 and 3e-4 (all coefficients zero, constant score), 0.947 at 1e-3, 0.949 at 3e-3, 0.944 at 1e-2, 0.937 at 3e-2, 0.930 at 1e-1; SE about 0.01. Between 1e-3 and 1e-2 the differences (about 0.005) are half an SE; below about 1e-3 the model collapses.
- This is one fold of 25: an indication, not a confirmation for all folds.

## Expected behavior and validation
No change in results. The edge flags stay in `results/s6_stage1_*.json`.

## Consequences
- S6 results stand as computed. The limitation goes into the report.
- mf-029 is closed for this run.
