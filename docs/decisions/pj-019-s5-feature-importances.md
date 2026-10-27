# pj-019. S5 feature importances — figures and aggregation

- **Status:** accepted
- **Date:** 2026-10-27
- **Tags:** modeling | interpretation
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

Scope S5 delivers importance plots for the report (RQ: which physical / CDM-derived signals matter vs LRP). Kelvins metrics still come from repeated CV (pj-004–006); importances are **interpretation only**, not the primary evaluation path.

v1 `X` has 35 columns with correlated snapshots (e.g. multiple `risk_snap_*` on the same usable window).

## Options considered

1. **Models:** RF only, GBDT only, or both.
2. **Method:** impurity-based `feature_importances_` vs permutation importance on a scoring metric.
3. **Training scope for importance:** single fit on full filtered train vs average over CV folds.
4. **Display:** top-k bars; optional extension when ranks are nearly tied.

## Decision

1. **Both** Random Forest (pj-016, `n_estimators` from pj-018) and `GradientBoostingRegressor` (pj-017).
2. **Impurity-based** `feature_importances_` (normalized per fitted model), **not** permutation importance at launch.
3. **Aggregate over all 25 fits** (K=5 folds × R=5 repetitions): for each fit, train imputer + model on the fold train set only; read `feature_importances_`; **average** the vectors across the 25 fits; rank features by this mean.
4. **Plot:** horizontal bar chart (or equivalent) per model. Show **top 10** by mean importance. **Extend to up to 15** features if ranks 11–15 have mean importance **≥ 95%** of the 10th-ranked feature’s mean importance (include contiguous ranks from 11 upward while the rule holds and count ≤ 15).

Export a CSV/JSON table of mean importances (all 35 features) for reproducibility; the figure uses the 10–15 rule above.

## Rationale (developer's own words)

Plot both models since we train both anyway. Use impurity importances for now (permutation left aside unless correlation between snapshots makes attribution unclear). Averaging over 25 folds is methodologically cleaner than one full-train fit. Show top 10 bars; widen to top 15 when the next features look almost as important as the 10th.

## Mathematical framing

Impurity importance sums weighted impurity decreases at splits using each feature, normalized to sum to 1 per fitted model. Averaging across 25 fold-specific models yields a stable ranking for correlated tabular features; it does not identify causal effects of individual CDM variables.

## Checks raised

- Correlated `risk_snap_*` columns can split importance mass across snapshots (see teaching note in project chat); permutation importance would stress-test predictions but costs more compute.
- Importance models use the same hyperparameters as evaluation but are **not** the same OOF prediction pipeline; prose must label plots as interpretability on fold training sets.
- RF uses the pj-018-selected `n_estimators` in each of the 25 importance fits.

## Dimensionality reduction

**No PCA or other unsupervised reduction** on S5 inputs for importance or prediction. Named v1 features (pj-009) stay interpretable for the report. Correlation among snapshots is handled in prose and via the revisit rules below, not by replacing `X` with components.

## Revisit triggers — impurity vs permutation (or method change)

Impurity importances can **split credit** across correlated columns without hurting CV metrics. That is often **expected**, not a bug. Use the rules below to separate “write a limitation paragraph” from “reopen pj-019”.

### A. Sufficient with impurity only (do **not** reopen)

All of the following:

1. **CV metrics** (L, F₂ vs LRP) are already reported under pj-004–007; importance is supplementary.
2. Among the **top 10** by mean impurity, several `risk_snap_*` / `risk_agg_*` columns appear together, and pairwise Pearson **|r| ≥ 0.85** on the filtered train `X` (computed once on full train for diagnostics only).
3. **Non-risk** columns (e.g. `miss_distance_*`, `relative_speed_*`, `obj_*`) still appear somewhere in the **top 15**, or the report text states that trees lean on risk summaries vs LRP-like behaviour.
4. RF and GBDT importance rankings are **qualitatively similar** (same broad families in top 5, e.g. risk snapshots vs geometry).

**Action:** one short **Limitations** sentence: correlated snapshots; impurity is not causal; no method change.

### B. Mandatory automatic checks (always run)

After mean impurity importances are computed, the S5 pipeline **must** run **B1** and **B3** below and write results to `results/importance_diagnostics.json` (or equivalent). These are algorithmic gates: they decide whether pj-019’s impurity method stays acceptable or must be reopened.

**Feature families** (for B3): **risk** = name starts with `risk_`; **geometry** = `miss_distance_`, `relative_speed_`, or `t_weighted_rms_`; **metadata** = `n_cdm`, `first_ttc`, `last_ttc`, `n_usable_cdms`, `ttc_span_usable`; **object** = `obj_`.

| ID | Check | Procedure | **Reopen pj-019 if** |
|----|-------|-----------|------------------------|
| **B1** | Impurity vs permutation (both models) | Repetition index **0** (seed 42), **fold index 0**: on train, fit imputer + model with pj-016/pj-017/pj-018 settings; on val, `sklearn.inspection.permutation_importance` with `scoring="neg_mean_squared_error"`, `n_repeats=5`, `random_state=42`. Top 5 features by **global** mean impurity (pj-019) vs top 5 by permutation on that val fold. Run separately for **RF** and **GBDT**. | **Either** model: overlap of top-5 name sets **< 3** **or** rank-1 name differs between impurity and permutation. |
| **B3** | RF vs GBDT rank-1 family | Using **mean impurity** rankings (25-fold average). | Rank-1 feature differs between RF and GBDT **and** the two rank-1 features map to **different** families from the list above (e.g. risk vs geometry). |

If **B1** or **B3** fires → **reopen pj-019** (supersede or amend: add permutation-based figures and/or revised narrative rules). Do not publish impurity-only claims in the report until resolved or explicitly overridden in a new ADR with developer sign-off.

If **neither** fires → impurity plots stand; section A may still apply for correlated-snapshot limitation text.

### C. Manual / contextual triggers (not auto-run)

| ID | Trigger | Action |
|----|---------|--------|
| B2 | Domain expectation that geometry matters, but no geometry in top 15 and geometry sum **< 5%** impurity for both models | Developer decides whether to reopen; document in report. |
| B4 | Report/oral requires remove-feature or causal claims | Reopen for permutation or ablation ADR. |

### D. Not a revisit trigger

- High correlation alone (section A.2).
- LRP beating trees on L (model comparison outcome, not importance method).
- Choosing PCA (out of scope for S5 unless a separate feature ADR is opened).

## Consequences

- `src/models/trees.py` or analysis script: after CV metric run (or integrated), 25× importance vectors → mean → ranked export + two figures (`rf`, `gbdt`).
- **Always** run mandatory checks **B1** and **B3**; save `results/importance_diagnostics.json` with: top-15 impurity lists per model, B1 top-5 overlap and rank-1 match per model, B3 rank-1 families and `reopen_required` boolean, max pairwise |r| among top-10 (diagnostic for section A).
- Reopen impurity method when B1 or B3 fires; optional revisit for B2/B4 via new ADR.
