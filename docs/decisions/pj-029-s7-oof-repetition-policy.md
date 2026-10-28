# pj-029. S7 atlas — OOF repetition policy (≥3/5) and caption statistics

- **Status:** accepted
- **Date:** 2026-10-28
- **Tags:** modeling | evaluation | interpretation
- **Decided by:** Pedro
- **AI involvement:** options + critique on multiplicity

## Context

Each event has five OOF predictions per model (pj-005: seeds 42–46). Atlas slots C1–C2 need a rule for when a contrast “counts” (pj-028). Pedro rejected qualifying on a single repetition or on “any one of five” without stability, to avoid repetition-level multiplicity that looks like cherry-picking.

## Options considered

1. **Single repetition** (e.g. seed 42 only) for all slots.
2. **Any of 5** repetitions qualifies the event (union).
3. **≥ k of 5** repetitions must satisfy the slot rule; then pick among qualifiers by pj-028.
4. **All 5** must satisfy (very strict).

Chose **3** with **k = 3**.

## Decision

### Per-repetition evaluation

For each seed in {42, 43, 44, 45, 46}, evaluate the slot rule (C1 or C2) using **that repetition’s OOF row only** (LRP deterministic; `r_hat`/`p_hr` from the matching row in `preds/*.parquet` for rf/gbdt). F₂ classification uses threshold −6 inclusive on `r_hat` vs true `y_hr` (pj-001, pj-020).

### Qualification (C1 and C2)

An event **qualifies** for the slot if the contrast holds in **at least 3 of 5** repetitions:

| Slot | Per-repetition condition (must hold in ≥3 reps) |
|------|--------------------------------------------------|
| **C1** | True HR; LRP FN; at least one of {rf, gbdt} TP |
| **C2** | True HR; LRP TP; at least one of {rf, gbdt} FN (both FN if both are shown as failing) |

If both rf and gbdt can satisfy C1 in different reps, the figure still uses the tree named in pj-028 (tree that realizes TP in the majority of qualifying reps; tie → larger mean absolute residual on FN side — if still tied, smallest `event_id`).

### Selection among qualifiers

Among qualifying events, choose **argmax `risk_final`** (pj-028).

### Caption / figure note (mandatory)

For each core contrast panel (C1, C2), report:

1. **Stability:** `k/5` repetitions where the slot condition holds (e.g. `4/5`).
2. **Means over qualifying repetitions only:** for LRP and for the tree(s) shown, **mean `r_hat`** across the OOF rows of those `k` repetitions (true `risk_final` is single-valued; show it once).

Optional one-line: spread (min–max) of `r_hat` across the five reps for transparency.

Same **≥3/5** policy applies to **C3–C6 and optional slots** when their rules are defined in follow-on ADRs, unless superseded.

## Rationale (developer's own words)

Requiring the pattern in at least 3/5 repetitions is necessary to avoid “cheating” via repetition cherry-pick. Among events that pass, taking the largest `risk_final` is fine; add a note with the mean and the percentage of seeds where it happens.

## Consequences

- Atlas code counts, per event, how many reps satisfy each slot before ranking by `risk_final`.
- Empty pool if no event meets ≥3/5 → report in implementation and revisit rule via new ADR (do not relax silently).
- C3–C6 selection ADRs must reference this repetition policy.

## Checks

- **LRP** often identical across reps → C1/C2 variability is mostly fold assignment + tree fits.
- **≥3/5** is a project choice, not a universal standard; document `k/5` in the figure so reviewers see stability.
- Mean `r_hat` over qualifying reps is descriptive, not a registered metric for the bake-off table.
