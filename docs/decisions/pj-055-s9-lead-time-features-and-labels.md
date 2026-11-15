# pj-055. S9 lead-time — features and labels per cut

- **Status:** accepted
- **Date:** 2026-11-14
- **Tags:** modeling | preprocessing | data
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

For each lead-time point `t_cut` (`pj-054`), inputs must be built under a shorter usable window. S3 v1 defines `build_features` with usable CDMs `time_to_tca ≥ 2` (`pj-009`, `TTC_MIN` in code). S1 fixes labels from the last CDM and LRP from the first usable at `≥ 2` (`pj-001`, `pj-003`).

## Options considered

1. **Same v1 recipe; replace usable threshold with `t_cut`** — quantile snapshots and aggregates on CDMs with `time_to_tca ≥ t_cut`; same `FEATURE_COLUMNS`.
2. **Reduced feature set at early cuts** — fewer snapshots when `n_usable` is small; different columns per `t_cut`.
3. **Relabel or redefine `risk_final` per cut** — e.g. risk at last CDM still in window vs TCA.

## Decision

Chose **option 1**:

- Build **the same v1 feature vector** (`pj-009`, `FEATURE_COLUMNS`) using only CDMs with `time_to_tca ≥ t_cut`.
- Keep **labels unchanged**: `risk_final`, `y_hr`, and S1 metadata columns for events in the cohort at that `t_cut` (`pj-054` exclusion rule).
- Do **not** change the `pj-003` event filter for `t_cut = 2`; for `t_cut ∈ {3, 4}` the cohort is the subset with at least one CDM in that window.

## Rationale (developer's own words)

Keep everything the same except the existence filter at each cut; there is no reason to do it another way.

## Checks raised

- Events with a single usable CDM at a given `t_cut` degenerate snapshots as in `pj-009` → counts rise at higher `t_cut` in EDA (e.g. 541 single-CDM events at `t_cut = 4`).
- `first_ttc` / `last_ttc` still describe the full CDM series, not restricted to the window → same leakage note as `pj-009`.
- `mission_id` remains excluded from `X` (`pj-011`).

## Expected behavior and validation

- `build_features` (or S9 wrapper) accepts `ttc_min=t_cut`; column contract tests still pass at `t_cut = 2`.
- Per-cut cohort sizes match EDA sanity checks for {2, 3, 4}.

## Consequences

- S9 implementation reuses S5 pipelines with per-cut feature matrices and cohort masks.
- No new feature columns for S9 lead-time.