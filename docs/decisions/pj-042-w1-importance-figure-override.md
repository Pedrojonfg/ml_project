# pj-042. W1 — publish RF impurity importances despite B1 gate (amends pj-019 for W1 only)

- **Status:** accepted
- **Date:** 2026-11-01
- **Tags:** interpretation | reporting
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

pj-019 makes gate B1 mandatory and forbids publishing impurity-only claims while it fires unless a new ADR with developer sign-off overrides it. `results/importance_diagnostics.json`: B1 fires for both models (RF: top-5 overlap 3, rank-1 differs; GBDT: overlap 2, rank-1 differs); B3 passes; max pairwise |r| among RF top-10 = 0.91. pj-037 lists the RF importance plot as a W1 figure.

## Options considered

1. Text only: state the claim robust to both methods (risk summaries dominate), no figure or ranking.
2. Publish the impurity figure with an explicit caveat that permutation importance disagrees on ordering.
3. Drop importances from W1.

## Decision

Chose **option 2**, for the W1 Progress Report only. The caption must state: impurity-based, averaged over 25 fold fits; not causal; permutation importance on one validation fold agrees that risk summaries dominate but ranks them differently; the individual ranking is not claimed. pj-019 remains open for the Final Report (permutation-based figure or revised narrative).

## Rationale (developer's own words)

Keep the figure in the Progress Report with an explicit warning that permutation importance disagrees on the order.

## Consequences

- W1 prose claims only that trees rely mainly on risk summaries; no "most important feature" claim.
- Reopening pj-019 stays on the C2 backlog.
