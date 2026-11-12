# pj-051. S7 atlas — S4 contrast slots C3/C4, eight-core renumber, O4→O3

- **Status:** accepted
- **Date:** 2026-11-12
- **Tags:** modeling | evaluation | interpretation
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

The atlas used six core slots (pj-027) with learned models = {rf, gbdt} plus LRP. S4 regressors (ols, ridge, lasso, knn) use a fold-wise alarm line `t` (mf-012) because `r_hat` often never reaches −6. The developer wants two **additional core** panels parallel to C1/C2 but with S4, **without** putting S4 into jump majorities. Optional ex-O4 (complement to the “majority catch” jump) is renamed **O3** because the former calibration O3 is skipped (pj-050).

## Slot map (authoritative)

| ID | Role | Source rule |
|----|------|-------------|
| **C1** | LRP FN, tree TP | pj-028, pj-029, pj-046 |
| **C2** | tree FN, LRP TP | pj-028, pj-029, pj-046 |
| **C3** | LRP FN, S4 majority TP | this ADR |
| **C4** | S4 majority FN, LRP TP | this ADR |
| **C5** | jump-up, majority FN | ex-C3, pj-045 |
| **C6** | jump-down, majority FP | ex-C4, pj-045 |
| **C7** | jump, majority correct | ex-C5, pj-045 |
| **C8** | multi-fail {LRP,rf,gbdt} | ex-C6, pj-030 |
| **O1** | difficult triple TP | pj-031 |
| **O2** | S6 calibration flip | pj-049 |
| **O3** | jump catch, opposite class to C7 | ex-O4, pj-048 |
| — | former calibration O3 | still skipped (pj-050) |

**S4 models in C3/C4:** {ols, ridge, lasso, knn}. **Not** used in C5–C8 jump/multi-fail majorities (still {LRP, rf, gbdt} only).

## Decision — C3 / C4

Shared: OOF only; ≥3/5 reps (pj-029); true HR; LRP vs −6; each S4 model uses its **mf-012** fold/`rep` alarm (`r_hat >= t` or stored `p_hr`); among qualifiers **argmax `risk_final`**, tie → apply pj-046 with wrong=LRP and right=mean `r_hat` over S4 models that realize the majority side on the k reps (if undefined, smallest `event_id`); exclusion order below.

### C3 (S4 analog of C1)

Per rep: LRP FN; **≥ 3 of 4** S4 models TP. Event qualifies if that holds in ≥3/5 reps.

### C4 (S4 analog of C2)

Per rep: LRP TP; **≥ 3 of 4** S4 models FN. Event qualifies if that holds in ≥3/5 reps.

Caption: k/5; mean LRP; per S4 slug, count of reps TP/FN (0–5); mean `r_hat` on k reps; note that S4 alarms use `t` not −6.

## Decision — renumber jumps / multi-fail / O3

- pj-045 slots rename **C3→C5, C4→C6, C5→C7** (rules unchanged; majority set unchanged).
- pj-030 C6 rename **→ C8**.
- pj-048 O4 rename **→ O3**; complement is opposite `jump_class` to **C7** (not C5).
- pj-047 assignment order becomes:

**C1→C2→C3→C4→C5→C6→C7→C8→O1→O2→O3.**

## Rationale (developer's own words)

Use `t` because that is how S4 alarms work. For C3/C4 require a majority (3 or 4) of the S4 models. Add C3 and C4 so there are eight core panels; do not put S4 models into the jump slots. Rename so O4 becomes O3.

## Consequences

- pj-027’s “six core” count is superseded for C2: **eight** core panels.
- Implementation and captions must use the new IDs.
- Empty C3/C4 pool → omit/reopen; do not silently switch to −6 for S4.

## Checks raised

- KNN may rarely TP under its own `t`; majority 3/4 still allows C3 if three linears succeed.
- pj-046 applied to four S4 heads uses mean `r_hat` on the majority side as the “right” (C3) or “wrong” (C4) prediction for the squared-error tie-break.
