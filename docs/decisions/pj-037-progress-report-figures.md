# pj-037. Progress Report — figure set (W1)

- **Status:** accepted
- **Date:** 2026-11-01
- **Tags:** product | reporting
- **Decided by:** Pedro
- **AI involvement:** opinion requested (integrator discretion within bounds)

## Context

Figures do not count toward the two-page text limit (course brief; ADR 019 precedent). pj-036 minimizes EDA narrative; figures should support protocol decisions, model comparison, and jump/importance story—not repeat proposal EDA for its own sake.

## Options considered

1. **Proposal trio** — risk distribution, CDM timeline, baseline metrics bar.
2. **EDA-heavy** — missions, imbalance, jump share sensitivity plots.
3. **Results-oriented** — importances + jump taxonomy + at most one protocol schematic.
4. **Text-only W1** — no figures.

## Decision

Chose **3 with integrator discretion** (Mario as W1 integrator may pick exact cropping and order within these bounds):

**De-emphasize:** standalone EDA figures (missions, imbalance density) unless one panel is needed to justify rare-event evaluation in a single sentence.

**Include (priority order):**
1. **Random Forest feature importances** — `results/importance_rf.png` (or equivalent top-features plot from pj-019); supports “what models use” under Impact.
2. **Jump taxonomy** — one figure grounded in S2 (e.g. jump-class shares at c = 1 or a simple schematic of stable vs jump-up/down tied to mf-003/mf-004); links secondary RQ narrative without long EDA prose.
3. **Optional third:** CDM **timeline schematic** (reuse proposal asset) **only if** it clarifies ttc ≥ 2 protocol in Problem; **or** GBDT importances if RF alone is insufficient for one sentence in text.

**Exclude from default set:** official-test baseline bar chart if Table 1 already lists CRP/LRP (avoid duplicate).

Target **2–3 figures** total for W1.

**As built (2026-11-01):** (1) CDM timeline schematic reused from the proposal; (2) `results/eda/imbalance.png` reused as the jump figure (HR rarity + jump classes at c = 1, same event set, no reason to regenerate); (3) RF impurity importances reused with the caveat required by pj-042. All three on one figures page after the references.

## Rationale (developer's own words)

Little from the exploration phase unless very illustrative; prefer Random Forest importances, jump-related material, etc. Integrator has some freedom because Pedro has not written this document type before.

## Checks raised

- Jump panels depend on S2 labels (mf-001..006); captions must say analysis-only, not modeling input.
- Importance plots are impurity-based (pj-019); one clause in caption is enough.

## Expected behavior and validation

PDF has ≤3 main figures aligned with Table 2 story; no gallery of EDA for its own sake.

## Consequences

- Figure paths and captions live in W1 LaTeX under Mario’s integration.
- Final Report may restore fuller EDA if needed later.
