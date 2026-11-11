# pj-034. Progress Report outline — problem / solution / impact (W1)

- **Status:** accepted
- **Date:** 2026-11-01
- **Tags:** product | reporting
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

W1 is ≤2 pages of text (figures excluded). pj-033 fixes the thesis (protocol spine + models in progress). This ADR fixes section order and narrative arc, not figure/table content (separate ADRs).

## Mathematical framing

No estimator change. Controls reader path: which claims appear before scores, and how much space Problem vs Solution vs Impact receive.

## Options considered

1. **Proposal mirror** — RQ → data/EDA → prelim → next (similar to ADR 020).
2. **Problem → solution → impact** — goal and dataset context → decisions and why → effects on evidence and next steps, including delta vs proposal.
3. **Results-centered** — bake-off table first.
4. **Chronological scopes** — S1, S2, S3, … in order.

## Decision

Chose **2 (problem → solution → impact)** with this map:

1. **Problem** — what we aim to do (RQs / decision-support framing); what EDA raised; how the dataset works; prior evaluation criteria (Kelvins \(L\), CRP/LRP, early CDMs with ttc≥2). Compressed reminder, not a full proposal rewrite.
2. **Solution** — decisions taken and why (protocol, features, jump taxonomy as analysis-only, models under rigorous / understanding-first build, including syllabus and tree work).
3. **Impact** — what each decision changes for usable evidence (leakage control, rare-event metrics, fair comparison to LRP); preliminary bake-off as empirical impact; next steps; explicit **delta vs the proposal**.
4. **Closing** — contributions and AI declaration (outside the PSI arc).

Preliminary model scores sit under **Impact**, not as a standalone “Results” chapter.

**Amendment (2026-11-01, Pedro):** the problem → solution → impact arc is the **implicit** order of ideas, not the section titles. Explicit headings are conventional academic ones: Introduction; Data and Evaluation Protocol; Methods; Preliminary Results; Discussion and Next Steps; Declaration of Contributions and AI Use.

## Rationale (developer's own words)

Follow a problem–solution–impact structure: what we want to do, what the EDA raised, how the dataset worked, what criteria were used in the past — what decisions we have taken and why — what impact each decision has and how this affects next steps, plus what has changed since the proposal.

## Checks raised

- “Impact” in prose = effect on evidence and evaluation, not operational deployment (pj-033).
- Problem block must stay short so Solution/Impact keep page weight.
- Bake-off under Impact aligns with pj-033 (not a win claim).

## Expected behavior and validation

A reader can summarize protocol decisions before reading any model row. Check: no section titled like a final-paper Results chapter dominating page 1.

## Consequences

- Pending ADRs: which split to report, table rows/columns, figure set.
- Writing: Mario integrates W1; Pedro supplies S1/S3/S5 prose; Mario S2/S4 per plan-reparto.
