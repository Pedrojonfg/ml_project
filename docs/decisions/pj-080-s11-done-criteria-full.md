# pj-080. S11 done-criteria — full plan scope

- **Status:** accepted
- **Date:** 2026-11-24
- **Tags:** product | planning
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

`docs/plan-reparto.md` §5 defines S11 (Must) as: README, a script that regenerates tables and figures, MLA bibliography, and an AI declaration. Ownership moved to Pedro (`pj-079`). The Final Report is due 2026-11-25; cutting S11 is a live option under deadline pressure.

## Options considered

1. **Full plan S11** — README + regenerate script + MLA bib + AI declaration; no cut.
2. **Minimal delivery** — bib + AI declaration (+ short README); regen only documented, no single entrypoint.
3. **README + Declaración + bib; regen = list of scripts** — same information, no wrapper script.
4. **Other / none**

## Decision

Chose **option 1**. S11 is done only when all four plan deliverables are present:

1. README usable for reproduction.
2. Script (or equivalent entrypoint) that regenerates tables and figures.
3. MLA bibliography for the Final Report.
4. AI / contributions declaration as required by the assignment.

## Rationale (developer's own words)

Everything that was defined, without cutting anything, because there is no reason to do so.

## Checks raised

- “Script that regenerates” does not yet fix full retrain vs regenerate from existing `results/`/`preds/` by calling existing scripts → left to engineering unless a later ADR freezes it → recorded.
- Full scope is the widest option under a next-day deadline → developer confirmed no cut.

## Expected behavior and validation

- A reviewer can find README instructions, an entrypoint that regenerates tables/figs, an MLA `.bib` (or equivalent) for the Final Report, and the AI declaration text required by the course.
- Absence of any of the four items means S11 is not done under this ADR.

## Consequences

- Implementation targets the full set (`pj-079` owner).
- Regen script internals (retrain vs replay artifacts) remain engineering unless frozen later.
- Not doing: a reduced S11 for the deadline.
