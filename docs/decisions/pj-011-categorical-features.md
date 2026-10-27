# pj-011. Categorical features in v1

- **Status:** accepted
- **Date:** 2026-10-27
- **Tags:** modeling | preprocessing | data
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

Kelvins CDMs include `mission_id` (19 levels, constant per event) and `c_object_type` (nominal object class, almost constant per event). pj-009 v1 is otherwise numeric snapshots and aggregates. Train/test mission mix differs (brief); object-type vocabulary is small and fixed in the released data.

## Options considered

1. **Exclude both** from `X`.
2. **Include `mission_id`** (integer or one-hot).
3. **Include `c_object_type` only** (one-hot or defer encoding to S4).
4. **Include both**.

Encoding: raw in S3 vs one-hot in S3 vs encoding in S4 only.

## Decision

- **`mission_id`:** **not** included in v1 `X`.
- **`c_object_type`:** included via **one-hot encoding in S3** with fixed levels: `DEBRIS`, `UNKNOWN`, `PAYLOAD`, `ROCKET BODY`, `TBA`.
- **Value per event:** take `c_object_type` from the **last usable CDM** (`time_to_tca >= 2`, same anchor as LRP). If multiple types appear among usable rows (rare), last usable wins.
- **Unseen category at inference:** columns all zero (document in report as limitation); no `mission_id` fallback.

## Rationale (developer's own words)

Do not use mission IDs because new missions can appear and the model would be tied to mission identities; what differs across missions is mainly data/sensor quality, not a fixed offset applied to all measurements. Use one-hot for object type because new types are not expected beyond the five in the dataset; it is acceptable if the model is only defined for those classes, but not acceptable to restrict predictions to a fixed set of mission IDs.

## Checks raised

- `mission_id` can proxy data-quality and shift; excluding it may lose train signal but targets generalization to unseen missions → developer accepted.
- Test or future rows with a new `c_object_type` string → all-zero type dummies; predictions may be unreliable for that case → report limitation.
- Two train events change type across CDMs → last-usable rule chosen; negligible count.

## Expected behavior and validation

- `build_features` adds five binary columns (naming convention in `src/features.py`).
- No `mission_id` column in feature output.
- Tests: known type maps to correct dummy; constant per event on sample.

## Consequences

- S4 does not one-hot `c_object_type` for v1 (already done in S3).
- Parameter registry lists dummy levels.
