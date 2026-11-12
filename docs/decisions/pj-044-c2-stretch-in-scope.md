# pj-044. C2 — S8/S9/S10 enter scope; ownership through Sentence Outline

- **Status:** accepted
- **Date:** 2026-11-12
- **Tags:** product | planning
- **Decided by:** Pedro + Mario (team)
- **AI involvement:** none

## Context

`docs/plan-reparto.md` §11 listed S8 (PyTorch), S9 (lead-time / leave-mission-out) and S10 (kernel ridge) as cuttable stretch (`~`). ADR 010 still frames PyTorch as a non-primary ablation. W2 Sentence Outline is due **Sunday 15 November 2026**; after that delivery the team freezes new experimental scope for the outline. Must-have S7 (atlas) implementation is still pending; S5 has open C2 reopens (`pj-019` B1, `pj-026` R4 for RF; see `pj-042`, `pj-043`).

## Options considered

1. Keep the cut list: drop S8/S9/S10 if time runs out.
2. Bring **all three** into C2 scope and finish them before the Sunday freeze, with an explicit ownership split.
3. Bring only a subset (e.g. S9+S10, defer S8).

## Decision

Chose **option 2**. For C2 through the Sentence Outline freeze:

| Scope | Owner | Role |
|-------|--------|------|
| **S7** Failure atlas (implementation) | **Pedro** | Must; first |
| **S5** open reopens (`pj-019`, `pj-026` / RF floor-c) | **Pedro** | Before freezing bake-off numbers |
| **S8** PyTorch ablation | **Pedro** | In scope (still an ablation vs LRP under the same protocol; ADR 010 claim rank unchanged) |
| **S9** Lead-time / leave-mission-out | **Pedro** | In scope |
| **S10** Kernel ridge | **Mario** | In scope |
| **S11** Repo / bib / AI declaration | **Mario** | Due with W2 on Sunday |
| **W2** Sentence Outline | **Pedro** integrates | Sunday 15 Nov 2026; no new experiments after this freeze for the outline |

Supersedes the operational cut of S8/S9/S10 in `docs/plan-reparto.md` §11 for this cycle (KNN already reopened via mf-043). Does **not** make PyTorch the primary claim (ADR 010 stands).

## Rationale (developers' own words)

The team decided S8, S9 and S10 will be part of the project and will not be cut. Pedro owns S7, S8, S9 and the remaining S5 work; Mario owns S10. Sunday is the delivery of S11 and the Sentence Outline; after the outline, nothing new is included.

## Consequences

- Pedro execution order for the Thu 12 → Sun 15 window: **S7 → S5 reopens → S9 → S8**, then W2 freeze (parallel: Mario on S10 + S11).
- S5 reopens precede S8/S9 so bake-off / importance numbers in the outline are not rewritten after stretch rows land.
- Stretch rows use the same event folds and comparison protocol as S4–S6 where applicable.
- Update Destination in `LEDGER.md`; annotate plan cut list as revoked for C2 by this ADR.
