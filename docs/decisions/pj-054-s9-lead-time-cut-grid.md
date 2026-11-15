# pj-054. S9 lead-time axis — cut grid and cohort per point

- **Status:** accepted
- **Date:** 2026-11-14
- **Tags:** evaluation | data | preprocessing
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

S9 lead-time analysis measures how predictive skill changes when inputs may use only CDMs with `time_to_tca` at least `t_cut` days before TCA. The main internal cohort has 8 892 events and 93 HR after `pj-003`. On Kelvins train (same filter), coarser cuts shrink the cohort and HR counts (EDA 2026-11-13): at `t_cut ≥ 3`, 639 events drop (19 HR); at `t_cut ≥ 4`, 1 272 events drop (25 HR); at `t_cut ≥ 5`, 40 additional HR are lost vs `t_cut = 4` with median usable CDMs ≈ 6.

Baseline production protocol uses `t_cut = 2` (`TTC_MIN` in `src/protocol.py`). S2 records lead time of the last usable CDM at `t ≥ 2` for analysis only (`mf-005`); S9 changes the **input window**, not the jump cut.

## Mathematical framing

For each `t_cut`, define usable CDMs as rows with `time_to_tca ≥ t_cut`. Features and LRP at that point use only that sub-series. Labels remain `risk_final` and `y_hr` from S1 for events that **remain in the cohort** at that `t_cut`. Metrics are computed on the cohort for that point (population differs across `t_cut` unless noted in reports).

## Options considered

1. **Grid {2, 3, 4}** — three operating points; aligns with brief-style −4/−3/−2 d framing; 68 HR at `t_cut = 4`.
2. **Grid {2, 4}** — two endpoints only.
3. **Integer grid 2…6** — finer axis; fewer HR and fewer usable CDMs at high cuts.
4. **Grid {2, 3, 4, 5}** — adds a fourth point where HR count falls faster (53 HR at ≥5 in EDA).

**Cohort rule (paired with any grid):**

- **A.** At each `t_cut`, include only events with ≥1 CDM at `time_to_tca ≥ t_cut`; exclude others for that point’s metrics.
- **B.** Fixed event set 8 892 at every `t_cut` with missing inputs imputed or stubbed (not used in v1 feature contract today).

## Decision

- **Grid:** `t_cut ∈ {2, 3, 4}` (days).
- **Cohort:** **A** — drop events with no CDM at or above each `t_cut` for that point’s train/eval and feature build.

## Rationale (developer's own words)

Grid {2, 3, 4} is enough operationally interesting detail; beyond that there are too few HR events to be worth the extra training cost.

## Checks raised

- Different `n` and HR count per point → report `n_events` and `n_hr` per `t_cut` on the curve or in a table caption.
- Loss of 19 HR when moving from 2→3 and 6 more when 3→4 is expected under rule A; curve mixes “earlier view” and “smaller cohort” → developer accepted; document in W2.
- Official test evaluation for lead-time points is **not** decided here (internal OOF first, consistent with W1 `pj-035`).

## Expected behavior and validation

- Three metric points per model row; monotonicity of skill vs `t_cut` is **not** assumed — only reported.
- LRP at `t_cut` is risk at the smallest `time_to_tca` among CDMs with `time_to_tca ≥ t_cut` (same definition as baseline LRP when `t_cut = 2` and `pj-003` holds).

## Consequences

- Implement a `t_cut` parameter in the S9 feature/CDM filter (default 2 elsewhere unchanged).
- Does not reopen `mf-003` jump cut or `pj-003` event filter for `t_cut = 2`.