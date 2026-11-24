# pj-078. S9 lead-time at t_cut = 2 — reuse bake-off GBDT

- **Status:** accepted
- **Date:** 2026-11-21
- **Tags:** evaluation | modeling
- **Decided by:** Pedro
- **AI involvement:** options + critique; opinion requested (for/against arguments)

## Context

`pj-077` aligns S9 GBDT training with the iteration-2 protocol (`pj-072`/`pj-073`). At `t_cut = 2` the lead-time cohort matches the main S1 bake-off (8892 events). Iteration-2 GBDT metrics and OOF predictions already exist in `results/gbdt.json` and `preds/gbdt.parquet`. Cuts `t_cut ∈ {3, 4}` and leave-mission-out use different cohorts or splits and are not covered by that artifact.

## Mathematical framing

The lead-time point at `t_cut = 2` for the GBDT series is defined to be the same estimator and the same out-of-fold predictions as the main bake-off GBDT row, not an independent nested-CV retrain inside the S9 script.

## Options considered

1. **Reuse bake-off GBDT at t_cut = 2** — assumes that point is the same experiment as the main table; no GBDT retrain there; cuts 3–4 and LMO still regenerate under `pj-077`.
2. **Retrain t_cut = 2 in S9 and require numerical match** — same mathematics, two runs; equality is a test.
3. **Retrain t_cut = 2 without requiring match** — same recipe, independent run; small differences possible.
4. **Other / none**

## Decision

At `t_cut = 2` on the lead-time curve, reuse the bake-off GBDT from `results/gbdt.json` (and matching preds); do not retrain that point. Cuts 3 and 4 and LMO still regenerate under `pj-077`.

## Rationale (developer's own words)

Simple, it makes sense, it saves compute.

## Checks raised

- The curve at two days is no longer an independent check of the bake-off → accepted (reuse is intentional).
- LMO and `t_cut ∈ {3, 4}` are not saved by this choice → recorded.

## Expected behavior and validation

- `results/s9_leadtime.json` at `t_cut = 2` reports GBDT metrics taken from `results/gbdt.json` (same L unclipped / dashboard fields as stored there).
- Artifacts for `t_cut ∈ {3, 4}` and LMO are produced by a fresh run under `pj-077`.
- Linear rows remain selected per `pj-056` (still computed in S9).

## Consequences

- Parameter registry: S9 lead-time GBDT at `t_cut = 2` = bake-off reuse.
- Overwriting previous S9 JSON/PNG is an engineering detail at implementation.
- Not doing: skipping regen of cuts 3–4 or LMO.
