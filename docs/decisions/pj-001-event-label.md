# pj-001. Event label definition

- **Status:** accepted
- **Date:** 2026-10-24
- **Tags:** modeling | data
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

Each event has several CDMs; inputs are restricted to CDMs with `time_to_tca >= 2` (ADR 018). The challenge target is the final risk of the event (Uriot et al. 2020, Eq. 1). `risk` is already on a log10 scale; HR is `risk >= -6.0`. Two-stage modeling is the secondary RQ (ADR 008).

## Mathematical framing

Per event e, let c*(e) be the CDM with the smallest `time_to_tca`. Targets:
- `risk_final(e) = risk(c*(e))`, log10 scale.
- `y_hr(e) = 1[risk_final(e) >= -6.0]`.

The clipping at -6.001 used by the challenge metric is a property of evaluation, not of the stored target.

## Options considered

1. **Continuous only** — HR derived at evaluation time; one target.
2. **Binary only** — MSE_HR and therefore L cannot be computed.
3. **Both** — continuous and binary, binary derived from continuous; supports a two-stage model.

(Stored-target variants: **raw** `risk_final`, or clipped at -6.001.)

## Decision

Chose **both** targets from the last CDM: `risk_final` (continuous, log10) and `y_hr`. The continuous target is stored **unclipped**.

## Rationale (developer's own words)

Both targets are needed for two-stage models: classify P(HR) and estimate the magnitude. The target is stored unclipped (choice a).

## Checks raised

- `y_hr` must be defined only as `risk_final >= -6.0`, so there is a single definition → recorded in the framing above.
- Clipping at -6.001 is an optimal move under the competition loss (Uriot §4.3) and shrinks MSE_HR → developer decided to keep the target unclipped and to report both clipped and unclipped metrics (separate metrics ADR).
- "Last CDM" means smallest `time_to_tca` per event, as in `scripts/esa_kelvins_metrics.py`. Events with no usable CDM are handled in a separate ADR.

## Expected behavior and validation

`y_hr.mean()` on train should be ~2.8 % (13154 events). On test, 150 of 2167 events (6.9 %). Check that `event_table` reproduces these counts.

## Consequences

- `event_table` stores `risk_final` unclipped and `y_hr`.
- Clipped metrics are computed at evaluation time only.
- Not doing: modeling the full CDM vector of the last CDM.
