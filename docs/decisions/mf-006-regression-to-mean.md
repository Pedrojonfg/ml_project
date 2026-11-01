# mf-006. Regression to the mean at extreme latest_risk

- **Status:** accepted
- **Date:** 2026-11-01
- **Tags:** modeling | evaluation
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

If log risk behaves like a noisy measurement, events with very high latest_risk
tend to end lower and events with very low latest_risk tend to end higher, with
no real change in risk (regression to the mean). Part of jump-down at high
latest_risk and of jump-up at low latest_risk could then be expected
statistically. This is a hypothesis; no data is in the repo yet.

## Mathematical framing

Let m(l) = E[Δ | latest_risk = l]. The hypothesis is m(l) < 0 for large l and
m(l) > 0 for small l. The label (mf-002..004) is a function of Δ and y_final
and does not use m(l).

## Options considered

1. **Nothing** — interpret with care when reading results.
2. **Group by latest_risk level** — analysis-only: latest_risk in bins used to
   group tables.
3. **Expected Δ** — estimate m(l) from train and compare the actual Δ with it.
4. **Correct the label** — apply the cut to Δ − m(l).

## Decision

Chose **option 2**: no change to the label; latest_risk is binned for grouping
tables. Bin edges are deferred to EDA.

## Rationale (developer's own words)

It is the simplest option to address and classify the problem.

## Checks raised

- latest_risk already exists as a column in event_table → the "column" is its
  bins; no new value is created.
- Option 2 does not correct the effect, it makes it visible per group →
  developer confirmed: it is "note and look", not "fix".
- Option 4 would contradict mf-003 → not chosen.
- The size of the effect is unknown without data → measured in EDA.

## Expected behavior and validation

In EDA, report mean Δ and jump-class shares per latest_risk bin. If mean Δ is
clearly negative at high bins and positive at low bins, the hypothesis holds;
if flat, it does not. If it holds, revisit with a new ADR (e.g. option 3).

## Consequences

- No new output value: grouping by bins of latest_risk in reports.
- Bin edges are deferred-fog until the EDA (does not block the label).
- mf-003 is unchanged.
