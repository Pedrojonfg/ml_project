# pj-007. Metrics reporting

- **Status:** accepted
- **Date:** 2026-10-24
- **Tags:** modeling | evaluation
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

Challenge metrics: F2, MSE_HR and L = MSE_HR / F2 (ADR 018). Uriot et al. clip predicted risk at -6.001 inside MSE_HR (Sec. 4.3); this is optimal under that loss and can only lower MSE_HR.

## Mathematical framing

F2 depends only on the -6.0 threshold and is unaffected by clipping. MSE_HR and L are reported in two versions: clipped at -6.001 and unclipped.

## Options considered

1. Clipped only (comparable to the paper).
2. Unclipped only (measures real distance).
3. Both.

## Decision

Chose **both**: F2, MSE_HR and L, with MSE_HR and L in clipped and unclipped versions.

## Rationale (developer's own words)

Clipped, to compare with the original paper; unclipped, because it is the most honest and we want to characterize the magnitude of the risk.

## Checks raised

- The clipped version rewards a metric trick, not better risk estimates → reported next to the unclipped one so the gap is visible.

## Expected behavior and validation

Clipped MSE_HR <= unclipped MSE_HR for any predictions.

## Consequences

- Stored targets stay unclipped (pj-001).
- Not adding PR-AUC or calibration here (S6).
