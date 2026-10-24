# pj-002. Events without any CDM at least 2 days before TCA

- **Status:** accepted
- **Date:** 2026-10-24
- **Tags:** modeling | data
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

Inputs are CDMs with `time_to_tca >= 2` (ADR 018, pj-001). In `train_data.csv`, 1212 of 13154 events (9.2 %) have no such CDM; they contain 42 of 365 HR events (11.5 %). The official test has 0 such events. LRP is undefined for them.

## Mathematical framing

Training and validation sets are restricted to events with at least one CDM with `time_to_tca >= 2`. After filtering: 11942 train events, 323 HR (2.70 %).

## Options considered

1. **Remove from train and validation** — no input exists; matches the test distribution.
2. **Keep in train with imputed/empty features** — requires an imputation choice; never seen at test time.
3. **Use their `time_to_tca < 2` CDMs as input** — breaks the truncation (target leakage).
4. **Remove from modeling, keep in EDA counts** — no effect on any model number.

## Decision

Chose **option 1** for the S1 protocol: these events are excluded from train, validation and `event_table`. Whether S2 (EDA) includes them in descriptive statistics is S2's owner's decision and is out of scope here.

## Rationale (developer's own words)

The goal is to predict with more than two days of lead time; these events have no valid input, so there is no point in keeping them in the dataset.

## Checks raised

- 42 HR events (11.5 % of HR) are lost → developer acknowledged the proportion is not negligible and kept the decision.
- Scope limitation: events first observed late (no CDM >= 2 d) are outside the model's scope → to be stated as a limitation in the report.
- LRP is undefined for these events, so validation would exclude them in any option.

## Expected behavior and validation

After filtering, train has 11942 events and 323 HR; every remaining event has at least one CDM with `time_to_tca >= 2`.

## Consequences

- `event_table` is built only from events passing the filter.
- Not doing: imputing features for these events; using CDMs with `time_to_tca < 2` as input.
