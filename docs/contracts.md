# Feature contract (S3 v1)

Source of truth in code: `FEATURE_COLUMNS` in `src/features.py`. This file must list the same columns.

Built by `build_features(event_table, cdm)` — one row per `event_id` in `event_table`. Usable CDMs: `time_to_tca >= 2` (pj-002, pj-003). Targets `risk_final` / `y_hr` are not features.

## Snapshot variables (first / last usable + p25, p50, p75 on `time_to_tca`)

For each of `risk`, `miss_distance`, `relative_speed`, `t_weighted_rms`:

| Column | Meaning |
|--------|---------|
| `{var}_snap_first` | Value at farthest usable TCA (max `time_to_tca`) |
| `{var}_snap_last` | Value at closest usable TCA (min `time_to_tca`); for `risk`, equals LRP |
| `{var}_snap_p25` | Linear interpolation at 25th percentile of usable `time_to_tca` |
| `{var}_snap_p50` | 50th percentile |
| `{var}_snap_p75` | 75th percentile |

Single usable CDM: all five equal that row’s value (pj-009).

## Risk aggregates (usable window only)

| Column | Type | Notes |
|--------|------|-------|
| `n_usable_cdms` | float | Count of CDMs with `time_to_tca >= 2` |
| `ttc_span_usable` | float | max − min `time_to_tca` among usable |
| `risk_agg_min` | float | |
| `risk_agg_max` | float | |
| `risk_agg_range` | float | max − min |
| `risk_agg_mean` | float | |
| `risk_agg_std` | float | 0 if `n_usable_cdms == 1` (pj-010) |

## Event metadata (from `event_table`)

| Column | Type |
|--------|------|
| `n_cdm` | float |
| `first_ttc` | float |
| `last_ttc` | float |

## Object type (one-hot, last usable CDM, pj-011)

| Column | Level |
|--------|-------|
| `obj_DEBRIS` | DEBRIS |
| `obj_UNKNOWN` | UNKNOWN |
| `obj_PAYLOAD` | PAYLOAD |
| `obj_ROCKET_BODY` | ROCKET BODY |
| `obj_TBA` | TBA |

Unseen `c_object_type` at inference: all five 0.

## Full column list (order in `FEATURE_COLUMNS`)

`risk_snap_first`, `risk_snap_last`, `risk_snap_p25`, `risk_snap_p50`, `risk_snap_p75`,
`miss_distance_snap_first`, `miss_distance_snap_last`, `miss_distance_snap_p25`, `miss_distance_snap_p50`, `miss_distance_snap_p75`,
`relative_speed_snap_first`, `relative_speed_snap_last`, `relative_speed_snap_p25`, `relative_speed_snap_p50`, `relative_speed_snap_p75`,
`t_weighted_rms_snap_first`, `t_weighted_rms_snap_last`, `t_weighted_rms_snap_p25`, `t_weighted_rms_snap_p50`, `t_weighted_rms_snap_p75`,
`n_usable_cdms`, `ttc_span_usable`, `risk_agg_min`, `risk_agg_max`, `risk_agg_range`, `risk_agg_mean`, `risk_agg_std`,
`n_cdm`, `first_ttc`, `last_ttc`,
`obj_DEBRIS`, `obj_UNKNOWN`, `obj_PAYLOAD`, `obj_ROCKET_BODY`, `obj_TBA`.
