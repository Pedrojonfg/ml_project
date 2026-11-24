# pj-077. S9 GBDT — iteration-2 training protocol

- **Status:** accepted
- **Date:** 2026-11-21
- **Tags:** modeling | hyperparameters | evaluation
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

`pj-071` requires regenerating S9 after the S5/S8 iteration-2 retrain. S9 does not consume `preds/*.parquet`; it retrains GBDT (and S4 linears) at each lead-time cut and each leave-mission-out fold (`pj-056`, `pj-059`). The current S9 code path still uses iteration-1 selection: `n_estimators` only via `pj-024`/`pj-025`, floor `c` at `w = 1` (`pj-026`), no HR sample weights. Iteration 2 defines HR weights, `c(w)`, and nested selection of `w` (and, for trees, `n_estimators`) in `pj-072`/`pj-073`.

## Mathematical framing

Unchanged task: regress `risk_final`, alarm at −6, evaluate with the S1 dashboard (`pj-007`). What changes for the S9 GBDT row is the training objective weighting and the hyperparameter selection unit: same as the main bake-off GBDT under iteration 2.

## Options considered

1. **Iteration-2 protocol in S9** — assumes S9 GBDT should learn with the same criterion as `results/gbdt.json`; consequence: at each `t_cut` / LMO fold, select `(w, n_estimators)` by nested CV (`pj-073`), fit with HR weights and floor `c(w)` (`pj-072`).
2. **Keep iteration-1 protocol in S9** (`pj-056`/`pj-025`) — assumes the curve/LMO measure the older tree; consequence: S9 and the main bake-off are different estimators.
3. **Other / none**

## Decision

Chose **option 1**. Both the lead-time curve and LMO use the iteration-2 GBDT protocol. Linear rows stay as in `pj-056`/`pj-059` (S4 unchanged by iteration 2). Supersedes the GBDT hyperparameter clause of `pj-056`/`pj-059` that pointed only at `pj-024`/`pj-025`.

## Rationale (developer's own words)

With all the new pieces, because those models are better prepared.

## Checks raised

- `pj-056`/`pj-059` cite S5 selection via `pj-024`/`pj-025` → superseded for S9 GBDT only; LRP and linear rows unchanged → developer confirmed option 1.
- At `t_cut ∈ {3, 4}` fewer HR events make nested selection of `w` noisier → recorded; developer confirmed.
- Runtime rises because each point/fold runs the joint `(w, n)` search → recorded; developer confirmed.

## Expected behavior and validation

- Lead-time and LMO artifacts store chosen `w` and `n_estimators` (and floor `c`) per cut/fold for GBDT.
- S4 α selection and linear pick rules remain `mf-013` / `pj-056`.

## Consequences

- Parameter registry: S9 GBDT hyperparameters follow `pj-072`/`pj-073`.
- `t_cut = 2` GBDT reuse vs retrain: resolved in `pj-078` (reuse bake-off).
- Not doing: changing linear protocol; adding RF/MLP/GRU rows to S9.
