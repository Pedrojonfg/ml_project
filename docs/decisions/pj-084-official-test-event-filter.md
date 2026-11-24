# pj-084. Official test — event filter (≥1 usable CDM)

- **Status:** accepted
- **Date:** 2026-11-24
- **Tags:** data | evaluation
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

`pj-081`–`pj-083` define the one-shot official-test evaluation. Train/validation use `pj-003` (at least one CDM with `time_to_tca ≥ 2` and last CDM with `time_to_tca < 2`). On the Kelvins official test, every event’s last public CDM has `time_to_tca ≥ 2` (no post-2d label CDM in the public files; labels come from `test_data_private`). Applying `pj-003` literally yields zero test events.

## Mathematical framing

Operational early-warning evaluation requires that each scored event have at least one usable early CDM (`time_to_tca ≥ 2`) as model input. The competition test does not expose a near-TCA public CDM; the target is the private `true_risk`. The inclusion rule on test is therefore the usable-input half of the train filter, not the full `pj-003` pair.

## Options considered

1. **`pj-003` literal on test** — also requires last CDM `ttc < 2` → empty set on this dataset.
2. **All official-test events (ADR 018 wording)** — same cohort here if every event has a usable CDM.
3. **At least one CDM with `ttc ≥ 2`** — operational usable-input criterion; on this test equals all 2167 events / 150 HR.
4. **Other / none**

## Decision

Chose **option 3**. Official-test evaluation keeps events with **at least one CDM with `time_to_tca ≥ 2`**. Model inputs use only those CDMs. Labels are private `true_risk` (ADR `018`). This is **not** full `pj-003` (no requirement that the last public CDM have `ttc < 2`).

## Rationale (developer's own words)

Option C: that it has some CDM with two days or more of lead time, operational criterion.

## Checks raised

- Full `pj-003` on this test → 0 events → developer switched off literal `pj-003` → recorded.
- On the current Kelvins test, option 3 and “all events” coincide (n=2167, 150 HR) → recorded.
- If a future test had events with no usable early CDM, those would be excluded under this ADR → recorded.

## Expected behavior and validation

- Official-test metrics are computed on the kept event set (2167 / 150 HR on the current files).
- No public CDM with `time_to_tca < 2` is used as a model input.

## Consequences

- Parameter registry: official-test event filter = ≥1 CDM with `ttc ≥ 2`.
- Reporting vs OOF remains on the agenda (OOF uses `pj-003` train cohort; test uses this filter — different populations; must not be conflated in one table without a note).
- Not doing: requiring last public CDM `ttc < 2` on the official test.
