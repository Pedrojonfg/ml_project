# mf-005. Lead time of the last valid CDM

- **Status:** accepted
- **Date:** 2026-11-01
- **Tags:** modeling | evaluation
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

latest_risk comes from the last CDM with time_to_tca ≥ 2 d, which can be
anywhere from 2 d upward. The same Δ is a larger surprise when less time
remains for the risk to change. mf-003 uses one cut c = 1 for every event.

## Mathematical framing

The label (mf-002..004) is a function of Δ and y_final only. Lead time t is the
time_to_tca of the last valid CDM and is known at t0. Options either leave the
label unchanged and record t, or make the cut depend on t (piecewise, a
function c(t), or a normalized Δ/σ(t)).

## Options considered

1. **Single cut** — mf-003 unchanged, lead time ignored.
2. **Analysis column** — single cut; t stored separately for grouping tables.
3. **Piecewise cuts** by lead-time bins.
4. **Cut as a function c(t).**
5. **Normalized Δ**, |Δ|/σ(t) ≥ k, with σ(t) estimated from train.
6. **Decide after EDA** (deferred).

## Decision

Chose **option 2**: keep the single cut of mf-003 and record the lead time of
the last valid CDM as a separate analysis-only column, used to group tables.

## Rationale (developer's own words)

It is consistent with what we did in mf-002, it would be very useful for
grouping tables, and the cut would not need to change.

## Checks raised

- A cut that depends on lead time would partly supersede mf-003 → not
  needed, mf-003 stays as is.
- Splitting into lead-time bins reduces events per group (about 150 HR events
  in the test per the plan) → bins left to EDA.
- The same Δ is not equally surprising at different lead times; the label does
  not capture this → accepted; handled by grouping tables by lead time.
- Distribution of lead time is unknown (no data in the repo) → checked in EDA.

## Expected behavior and validation

In EDA, report the distribution of lead time and the jump-class shares per
lead-time group. If lead time is concentrated in a narrow range, the grouping
adds little.

## Consequences

- One extra output column in S2: lead time = time_to_tca of the last valid CDM.
- The bin edges used to group tables are deferred-fog until the EDA shows the
  distribution (developer agreed).
- mf-003 is unchanged.
