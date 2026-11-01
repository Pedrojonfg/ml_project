# pj-030. S7 atlas — C6 multi-model failure; jump slots deferred to S2

- **Status:** accepted
- **Date:** 2026-10-28
- **Tags:** modeling | evaluation | interpretation
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

Core slot **C6** (pj-027) is a hard HR event where several models fail F₂ together. Jump slots **C3–C5** (and optional **O4**) need a jump taxonomy from Mario’s **S2**; Pedro chose to **block** those atlas selection rules until S2 decisions exist.

## Decision 1 — Defer jump atlas rules

**C3, C4, C5, and O4** case-selection ADRs are **not written** until an S2 taxonomy ADR (or team contract) defines jump labels or an agreed operational rule. Implementation of jump panels may proceed later without reopening C1/C2/C6.

## Decision 2 — C6 qualification and selection

Apply pj-028 (OOF on train/val only) and pj-029 (≥3/5 repetitions).

### Per repetition (each seed 42–46)

Event must be **true HR** (`y_hr = 1`). Count **F₂ failures** (predicted not HR: `r_hat` or LRP value **< −6.0**, threshold inclusive on ≥ −6) for:

- **LRP** (protocol prediction),
- **rf** OOF,
- **gbdt** OOF.

**Repetition satisfies C6** if **≥ 2** of these three fail on that event.

### Event qualifies

**≥ 3 of 5** repetitions satisfy the per-repetition C6 rule.

### Select one event

Among qualifiers, **argmax `risk_final`** (most severe HR). Tie → smallest `event_id`.

### Caption (mandatory)

- **k/5** repetitions where ≥2 models fail.
- For each of LRP, rf, gbdt: **count of repetitions** (0–5) where that model is FN on this event.
- **Mean `r_hat`** (LRP value treated as prediction) for each model **over the k qualifying repetitions** (same style as pj-029).

When S4/S6 preds exist, C6 **may** be extended in a new ADR to require failures among learned models there; at launch C6 uses {LRP, rf, gbdt} only.

## Rationale (developer's own words)

Block jump cases until Mario decides S2. Continue with C6 using the same anti-cherry-pick repetition rule as C1/C2; among stable multi-failure events, take the most severe `risk_final` and report seed counts and means in the note.

## Consequences

- Atlas pipeline can implement C1, C2, C6 before S2.
- Empty C6 pool → report and revisit via new ADR (do not relax ≥3/5 or ≥2 models silently).
- Jump figures remain placeholders until S2 + follow-on pj-031+ ADRs.

## Checks

- An event can qualify C6 with LRP + rf failing but gbdt TP — still valid (≥2 failures).
- Requiring ≥3/5 avoids selecting an event that is only “hard” under one shuffle.
