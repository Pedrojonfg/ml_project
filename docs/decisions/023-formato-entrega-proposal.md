# 023. Delivery format for the Project Proposal

- **Status:** accepted
- **Date:** 2026-10-11
- **Tags:** tech | process
- **Decided by:** human

## Context

Need a PDF today (≤2 pages text). Repo already uses LaTeX for presentations (`presentations/**`).

## Options considered

1. **A** — Google Docs / Word → PDF.
2. **B** — LaTeX article in the repo.
3. **C** — Markdown → Pandoc PDF.
4. **D** — Overleaf cloud LaTeX.

## Decision

Chose **B**: LaTeX in-repo.

**Path convention:** `presentations/proposal/` (main `.tex` + figures + built PDF), consistent with existing `presentations/` layout.

## Why

User selected B. Matches repo tooling and gives tight control over page budget and figures.

## Consequences

- Create `presentations/proposal/` when writing starts (execution, not this ADR).
- Prefer `article`/`extarticle` 10–11pt, two pages of body text; figures can float or sit after/near mentions without counting toward the text limit as per course brief.
- Export/submit the compiled PDF; keep sources versioned.
