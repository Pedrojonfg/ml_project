---
legacy: [docs/decisions]
default-branch: main
---
# Project

Course ML project (BAM, IE University): early collision-risk forecasting from ESA Conjunction Data Messages. Team Pedro + Mario; deliverables are paper-style reports + oral. Stack: Python, scikit-learn, PyTorch. Official test stays unused for model selection. Deadline pressure: W2 Sentence Outline freeze 2026-11-15; Final Report 2026-11-25; oral late November.

## Language

- Chat: each person's profile
- Repo (records, code comments, docs): English

## Ownership

| Domain | Mode | Notes |
|--------|------|-------|
| framing | own | objective, targets, unit of analysis, success bar |
| data & splits | own | inclusion, folds, CV, leakage |
| preprocessing & features | own | scaling, imputation, encoding, feature contracts |
| model & loss | own | family, architecture, loss; includes PyTorch ablation design |
| hyperparameters & optimization | own | grids, defaults that affect fit |
| evaluation | own | metrics, thresholds, baselines, bootstrap protocol |
| reproducibility | own | seeds, determinism |
| interpretation | own | claims allowed in reports |
| architecture | advise | module boundaries, I/O layout |
| testing | advise | what to test, fixtures |
| dependencies | advise | adding libraries (e.g. torch) |
| engineering hygiene | auto | naming, CLI, plot style matching repo |
| research question & claims | own | RQ wording, what is claimed vs not |
| method (writing) | own | how methods are described |
| structure (writing) | advise | outline, section budget |
| format (writing) | auto | LaTeX/template mechanics |

When unsure, prefer own over advise, and advise over auto. `people/<h>.md` may tighten a mode for one person.
Everyone defends every own decision: yes

## Sources

- `docs/plan-reparto.md` — scope IDs S1–S11, ownership, phases
- `docs/decisions/` — legacy ADRs + LEDGER (read-only; stop appending)
- `docs/dependencias-y-reuniones.md` — meeting decisions / go-no-go history
- ESA Kelvins / Zenodo dataset path in README — data location and license
- ADR `010` — PyTorch is fair ablation, not primary claim
- `pj-044` — S8/S9/S10 in C2 scope; Pedro owns S8/S9; Mario S10+S11

## Milestones

- 2026-11-15 — W2 Sentence Outline freeze (no new experimental scope after)
- 2026-11-25 — W3 Final Report
- 2026-11-28 — Oral (approx.; slides 26–28 Nov)
