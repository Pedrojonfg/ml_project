# pj-033. Progress Report thesis (W1)

- **Status:** accepted
- **Date:** 2026-11-01
- **Tags:** product | reporting
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

W1 Progress Report is ≤2 pages of text (figures free). The proposal already stated RQs and CRP/LRP on the official test. Trees (S5) do not yet beat LRP on F₂/L under the S1 protocol. Project success criterion remains ADR 009 (protocol + calibration + atlas; beat LRP = bonus). This ADR fixes the *claim of this deliverable*, not the project-wide success bar.

## Mathematical framing

No new estimator. The choice controls which quantities are foregrounded in prose: protocol rules (event unit, ttc≥2 filter, repeated stratified CV, rare-event metrics) versus bake-off scores versus EDA/jump shares.

## Options considered

1. **A — Protocol-first** — assumes W1 value is how the problem is constructed; bake-off is secondary evidence.
2. **B — Bake-off-first** — assumes W1 value is numbers vs LRP; protocol in a few sentences.
3. **C — Rigor + models-in-progress** — assumes progress = data decisions for usable decision-support evidence plus early models still in progress due to rigor and understanding before implementation.
4. **D — Jump/EDA-first** — assumes progress = taxonomy and imbalance; models only mentioned.

## Decision

Chose **C and A**: rigor + models-in-progress, with protocol/data decisions as the primary narrative spine; bake-off supports that story and is marked preliminary.

## Rationale (developer's own words)

We have taken a large set of decisions on how to manage the data so it serves our purpose (obtain information that can be used with real-world impact), and we have started building and comparing several models; this is still in progress because we are ensuring methodological rigor and understanding each model before implementing it (e.g. RF or gradient boosting, not yet covered in class).

## Checks raised

- “Real-world impact” vs ADR 009 / proposal (no deployment, no commanding) → keep prose as decision-support insight / when not to trust; do not claim operational impact.
- S4 just landing + trees behind LRP → say preliminary / in progress; do not freeze rankings as final.
- RF/GBDT ahead of syllabus → consistent with ADR 011.

## Expected behavior and validation

Readers should finish the PDF understanding (i) the event-level early-CDM protocol and (ii) that a first model comparison exists and is still being hardened—not that LRP has been beaten. Check: no sentence claims a competition win or deployment readiness.

## Consequences

- Page weight: protocol + methodological stance first; results table second; jumps/EDA as support; S6/S7 as next steps only.
- Follow-on W1 ADRs: outline/space, which split to report, tables, figures.
- Explicitly not doing: Progress Report as a leaderboard claim or as a finished bake-off.
