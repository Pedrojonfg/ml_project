# 017. Preliminary-results bar for tonight’s proposal

- **Status:** accepted
- **Date:** 2026-10-11
- **Tags:** product | research
- **Decided by:** human

## Context

Course brief requires EDA + preliminary results. Team has only covered material through PCA; deadline is the same day. A simple learned model can help but is optional.

## Options considered

1. **A** — EDA only (sizes, imbalance, plots); no scores.
2. **B** — EDA + reproduce CRP + LRP on a clean event-level split + one results table.
3. **C** — B + a simple in-syllabus/near-syllabus model (e.g. logistic / linear).
4. **D** — B + trees/NN attempt.

## Decision

Chose **B** as the closed bar for the proposal PDF.

## Why

User: “cerramos B.” Credible “preliminary results” without overclaiming post-PCA methods. A simple model remains a nice-to-have only if B is already solid — not part of the committed bar.

## Consequences

- Must download Zenodo data and report CRP + LRP under the agreed eval protocol (next decision).
- Proposal does **not** promise a trained classifier/regressor in the prelim section.
- If extra time appears after B, a simple model may be added without changing this ADR’s minimum.
