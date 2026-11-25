# pj-085. Final Report — two tables (OOF vs official test)

- **Status:** accepted
- **Date:** 2026-11-24
- **Tags:** evaluation | writing
- **Decided by:** Pedro
- **AI involvement:** options + critique; opinion requested (what each split shows / common practice)

## Context

Internal bake-off metrics use event-level CV on the `pj-003` train cohort. Official-test metrics use the one-shot protocol `pj-081`–`pj-084` (different population and base rate). W1 (`pj-035`) already used two tables for the Progress Report (official test CRP/LRP only; OOF for learned models). The Final Report needs how both appear now that learned models also run on the official test.

## Mathematical framing

Scores on different event sets and protocols are not row-comparable in one table without an explicit split label. Separating tables keeps the claim of each number tied to its sampling distribution.

## Options considered

1. **Two separate tables** — OOF bake-off vs official test; clear claims; no mixing.
2. **OOF as main table; official test as paragraph / appendix** — internal protocol leads.
3. **Official test as main table; OOF as support** — challenge emphasis.
4. **Other / none**

## Decision

Chose **option 1**. The Final Report uses **two separate tables**:

1. **Internal OOF bake-off** — event-level CV on the `pj-003` cohort; model comparison and uncertainty under the training protocol.
2. **Official test (one-shot)** — models and baselines per `pj-081`–`pj-084`; reported once after freeze; not used for selection.

Do not merge rows from the two splits into one unlabeled table. Prose states what each table is for.

## Rationale (developer's own words)

Two tables apart, clear claim. Do not mix things; be clear what each one is for. Option A.

## Checks raised

- Populations differ (HR rate, mission mix, `pj-003` vs usable-CDM test filter) → separate tables address that → accepted.
- Extends W1 two-table idea with learned models now on the official-test table (`pj-081`) → recorded.
- Space cost in a page-limited report → accepted for claim clarity.

## Expected behavior and validation

- A reader can tell which numbers are OOF and which are official test without reading a footnote first.
- No single table presents OOF and official-test rows as directly comparable without a split marker (and this ADR forbids that unmarked merge).

## Consequences

- Writing/layout follows two-table structure; which metrics/columns inside each table can follow `pj-007` / existing result JSON fields unless a later writing ADR narrows them.
- Merge-to-`main` timing remains the last item on this agenda if still `needs-human`.
- Not doing: one mixed bake-off+test table as the default presentation.
