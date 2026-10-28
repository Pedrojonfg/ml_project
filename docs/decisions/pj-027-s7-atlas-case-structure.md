# pj-027. S7 failure atlas — core vs optional case categories (option C)

- **Status:** accepted
- **Date:** 2026-10-28
- **Tags:** modeling | evaluation | interpretation
- **Decided by:** Pedro
- **AI involvement:** options + critique; structure aligned with academic case-study practice

## Context

Scope S7 delivers a qualitative failure atlas (ADR 008–009): CDM timelines plus which models fail or succeed, under the S1 protocol. Quantitative tables remain primary; the atlas explains patterns without cherry-picking only favorable examples. Pedro chose **option C**: a fixed **core** set for the main report/oral plus **optional** cases cut first if time runs out.

## Options considered

1. **Fixed 5–10 undifferentiated cases** — single pool, no core/optional split.
2. **Balanced 5 FN + 5 jumps** — meeting default from `dependencias-y-reuniones.md`.
3. **Core + optional (option C)** — mandatory narrative slots + supplementary cases.
4. **Rule-only selection with cap K** — no predefined categories.

Chose **3**.

## Decision

### Core (mandatory for S7 “done”; target **6** figure panels)

| Slot | Category | Intent |
|------|----------|--------|
| C1 | **LRP false negative, learned model true positive** | Show where a tree model (S5) catches an HR event LRP misses under F₂ threshold −6. |
| C2 | **Learned model false negative, LRP true positive** | Reverse contrast: baseline still strong when the learned model misses. |
| C3–C5 | **Temporal jump — three distinct outcomes** | Three jump-like events (S2 taxonomy when available; provisional jump rule until then) chosen so **outcomes differ** (e.g. LRP succeeds vs fails; learned model succeeds vs fails). One representative trajectory per slot; prose explains why outcomes diverge. |
| C6 | **Hard event — multiple models fail** | At least **two** of {LRP, rf, gbdt} fail F₂ on the same true HR event (extend to S4/S6 preds when available). |

**Learned model** in C1–C2: use **rf** or **gbdt** (whichever is true positive or false negative as required); both may appear in the same figure if helpful. S4/S6 are not required for C1–C2 at launch.

**Jump count:** three jump slots are **core**; a fourth jump case is **optional** (O4 below), not required for S7 done.

### Optional (first cut if schedule tight; up to **4** slots)

| Slot | Category | Intent |
|------|----------|--------|
| O1 | **Difficult true positive** | HR event where a model succeeds despite an unfavorable CDM series (positive counterweight to failure focus). |
| O2 | **Calibration / two-stage (S6)** | Case illustrating calibrated `P(HR)` and/or magnitude head vs single-stage `r_hat` (requires Mario S6 preds; defer implementation until preds exist). |
| O3 | **Second calibration angle** | Optional companion to O2 (e.g. reliability mismatch on the same or another event) — include only if O2 is included and time allows. |
| O4 | **Fourth temporal jump** | Extra jump outcome not covered by C3–C5. |

Cut order if reducing scope: **O3 → O1 → O4 → O2** (calibration last among optionals because it depends on S6).

### Principles (developer)

- Avoid selecting cases only where Pedro’s models win; include LRP success stories (C2, jump slots where LRP TP).
- Primary operational worry for the competition-style metric is **missing true HR (false negatives)**, not maximizing precision alone; core slots emphasize FN contrasts but are not the only failure mode in the dataset.
- Tree **explanation** in prose may use CDM `risk` timelines, `r_hat`/`p_hr` per model, and S5 **feature importances** (pj-019); full local interpretability (e.g. SHAP) is out of scope unless added later via new ADR.

## Rationale (developer's own words, translated)

Pedro wants an open atlas, not only bad news. The two most important contrasts are (1) LRP FN with the tree/GBDT TP and (2) the reverse. Then several temporal jumps (three or four) with **different outcomes**, to explain why similar-looking jumps behave differently — accepting that tree explanations will require learning. A “everyone fails” hard case is valuable. Difficult successes and calibration/two-stage examples are worth including but should be **cut first** if there is no time; two-stage is not fully clear yet but optional calibration cases can wait for S6.

## Consequences

- Next ADRs must define **objective selection rules** within each slot (OOF prediction source, ordering, tie-breaks) and provisional **jump** labeling until S2 ships.
- Implementation lives under `src/atlas/`; figures referenced from Results/Oral.
- Core = 6 panels minimum; optional pool does not block S7 completion.

## Checks on this choice

- **Jump definition** may change when Mario’s S2 taxonomy lands → may require re-picking C3–C5/O4 or updating captions, not necessarily changing slot counts.
- **Multi-model fail (C6)** needs a precise rule for “fail” (F₂ only vs also magnitude error) — not fixed in this ADR.
- **−6.001 / floor c** (pj-026) affects tree **training**, not LRP; it must not be confused with LRP’s dominant failure mode in atlas prose.
