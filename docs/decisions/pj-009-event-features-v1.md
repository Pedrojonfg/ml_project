# pj-009. Event-level features v1 (tabular)

- **Status:** accepted
- **Date:** 2026-10-27
- **Tags:** modeling | data | preprocessing
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

S3 builds `X` for event-level models (S4/S5/S6) from CDMs with `time_to_tca >= 2` (pj-002, pj-003). pj-008 drops a separate stub phase; this ADR defines the first and only feature contract (v1). Targets remain `risk_final` and `y_hr` from S1; they must not appear in `X`. Sequence models are out of scope here (optional S8).

## Mathematical framing

Each event is one row. Inputs use only CDMs in the usable window (`time_to_tca >= 2`). Multi-snapshot values interpolate each scalar along the usable sub-series ordered by `time_to_tca` (farther from TCA to closer). For `risk`, the last usable value equals LRP; v1 does not add a separate `lrp` column (developer choice to avoid duplicate naming).

## Options considered

1. **Last usable only + minimal aggregates** — smallest `X`; weak trajectory signal.
2. **Fixed CDM index snapshots** — simple; poor alignment across heterogeneous series lengths.
3. **Quantiles of `time_to_tca` within usable CDMs, plus first/last usable anchors** — comparable across event lengths; degenerates cleanly when only one usable CDM exists.
4. **Full sequence / padding** — deferred to S8.

For aggregates: A1 (count/span), A2 (extrema), A3 (center), A4 (slope), A5 (discrete jumps), gap features — developer selected A1–A3 on `risk` only; excluded A4, A5, and gap features.

## Decision

**Multi-snapshot (per variable below):** first usable CDM, last usable CDM, and values at **25th, 50th, and 75th percentiles** of `time_to_tca` among usable CDMs (same value taken from the event’s usable rows; tie-breaking: use linear interpolation along `time_to_tca` when needed).

**Variables under this snapshot scheme:**

- `risk`
- `miss_distance`
- `relative_speed`
- `t_weighted_rms`

**Aggregates on `risk` over usable CDMs only:**

- **A1:** `n_usable_cdms`, `ttc_span_usable` (= max `time_to_tca` − min `time_to_tca` among usable rows)
- **A2:** `min`, `max`, `max − min`
- **A3:** `mean`, `std`

**From `event_table` (S1 metadata, not targets):** include `n_cdm`, `first_ttc`, `last_ttc` in `X`.

**Excluded from v1:** explicit `lrp` column (last usable `risk` snapshot carries the same information); A4 temporal slope; A5 discrete jump counts/thresholds; gap features; geometry beyond the three fields above.

**Single usable CDM:** all snapshot values for a given variable equal that single row’s value (no NaN solely due to length).

## Rationale (developer's own words)

Use quantile snapshots (25, 50, 75) plus first and last usable so events of different lengths stay comparable; include A1 and A2 because extrema do not fully replace count/span; include A3 (mean and std) for stability/volatility of reported risk. Skip slope and discrete jumps because they are ill-defined or low value for many events. Add three interpretable geometry/uncertainty fields with the same snapshot rule. Do not add a separate `lrp` column because last usable `risk` is the same; include `n_cdm`, `first_ttc`, and `last_ttc` from the event table as campaign context.

## Checks raised

- Last usable `risk` duplicates LRP baseline input → accepted; evaluation still compares model predictions to LRP vector, not to presence of `lrp` in `X`.
- `first_ttc` / `last_ttc` describe the full CDM series (including post-cutoff CDMs) → not leakage; document in reports that they are not restricted to the usable window.
- `n_cdm` counts all CDMs; `n_usable_cdms` counts usable only → both kept; partial redundancy accepted.
- High column count from 4 variables × 5 snapshots + aggregates → accepted for tree models; linear models may need regularization in S4.
- Geometry field choice is not expert-validated → three standard Kelvins fields; broader covariance blocks left for future work.

## Expected behavior and validation

- `build_features(event_table, cdm)` returns one row per `event_id` in `event_table`, numeric columns only for features (plus `event_id` key), deterministic given CDM data.
- Events with one usable CDM: snapshot columns constant per variable; aggregates with defined formulas (`std` may be 0 with single point).
- Tests: no `risk_final` / `y_hr` in feature columns; last usable `risk` matches `event_table.lrp`; usable-only rule respected.

## Consequences

- Column naming convention must be documented in `src/features.py` (implementation).
- Mario consumes this schema for S4/S6 when started.
- S8 sequence features, if any, are a separate ADR.
