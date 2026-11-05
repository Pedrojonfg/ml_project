# mf-022. Training events of the S6 stage-2 regressor

- **Status:** accepted
- **Date:** 2026-11-04
- **Tags:** modeling
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

Stage 2 of S6 estimates the risk (log10 Pc). The S4 regressors are trained on all events with target `risk_final` unclipped (mf-008). About 74 HR events per training fold (mf-012).

## Mathematical framing

The choice fixes which conditional expectation the regressor estimates: E[risk | features] over all events, E[risk | features, HR] over HR events only, or both HR and non-HR separately.

## Options considered

1. **A. All events** — assumes one relation between features and risk holds for HR and non-HR; estimates E[risk | features] over about 8892 events.
2. **B. HR events only** — assumes the relation is stable within HR; all seen risks are >= -6; about 74 training rows per fold.
3. **C. Two regressors, one on HR and one on non-HR** — assumes the relations differ; estimates m_HR and m_low separately.

## Decision

Chose **A**: the stage-2 regressor is trained on all events.

## Rationale (developer's own words)

Training only on HR events can make the model predict above the true value, as seen in concept 8 of the understanding. Example: if the model has only seen high-risk events (-3 or -6), for an event with risk -9 it will predict above.

## Checks raised

- Developer first chose B, then changed to A after seeing the options.
- With A the stage-2 output is one prediction E[risk | features], not separate m_HR and m_low → how the stages are combined is left to the combination decision (queue item 6).

## Expected behavior and validation

One stage-2 prediction per event, trained on the whole training fold.

## Consequences

- The stage-2 model family and its parameters are still to decide (next decision).
