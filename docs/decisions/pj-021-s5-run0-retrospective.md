# pj-021. S5 first training run — findings (run 0)

- **Status:** accepted (findings only; follow-up decisions not yet taken)
- **Date:** 2026-10-27
- **Tags:** evaluation | modeling
- **Decided by:** Pedro
- **AI involvement:** analysis from `results/` and `preds/` after `scripts/run_s5_trees.py`

## Context

First end-to-end S5 run on Kelvins train (8892 events, 93 HR). Hyperparameters per pj-016..018. Wall time ~3.5 minutes for RF grid {100,300,500} + final RF + GBDT + importances + diagnostics on WSL (single machine, `n_jobs=-1` for RF).

## Compute envelope (positive)

Full pipeline is **fast enough** that later trade-offs should **favor quality** (larger grids, permutation importances, bootstrap via pj-006, repeated diagnostics) over saving runtime, unless profiling shows otherwise.

## OOF prediction behaviour (44460 rows = 8892 × 5 reps)

| Model | `r_hat` median | % preds ≥ −6 (HR) | OOF F₂ | L clipped (vs LRP ~0.55) |
|-------|----------------|-------------------|--------|---------------------------|
| LRP (S1 baseline) | — | — | ~0.49 | ~0.55 |
| RF (`n_estimators`=100) | ~−28.9 | **0%** | **0.0** | ∞ |
| GBDT | ~−29.3 | ~0.33% | ~0.11 | ~13.3 |

RF never exceeds the HR threshold on OOF predictions → recall 0 → F₂=0. GBDT fires HR on a small fraction of rows (still far below true HR prevalence ~1.05%).

## RF `n_estimators` search (pj-018)

Grid completed; selected **100** by lowest mean unclipped L. When F₂=0 for candidates, selection is driven almost entirely by MSE_HR on true HR events and may not rank models by discrimination.

## Importance diagnostics (pj-019)

`reopen_required: true` because **B1 RF** failed (rank-1 impurity `risk_agg_min` vs permutation `risk_agg_range`; overlap 4/5). B3 did not fire (both rank-1 in risk family). Top-10 RF features highly correlated (max pairwise |r| ≈ 0.94 among risk summaries).

## Implications (not decisions)

- Heavy regularization (depth 4, `min_samples_split` 4) plus ~80% labels at −30 and squared-error regression may push models toward **safe low predictions**, hurting F₂ more than LRP.
- pj-018 criterion may need pairing with F₂ or a composite when comparing tree counts.
- pj-019 revisit path is active for RF importances; report should not over-claim physical attribution until resolved or limited to GBDT-consistent story.

## Consequences

- Ledger fog items updated for S5 iteration 2.
- No change to pj-014..020 until new ADRs supersede.
