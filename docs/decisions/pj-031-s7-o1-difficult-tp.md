# pj-031. S7 atlas — O1 difficult true positive (high range_risk, stable TP)

- **Status:** accepted
- **Date:** 2026-10-28
- **Tags:** modeling | evaluation | interpretation
- **Decided by:** Pedro
- **AI involvement:** options + critique; overlap with jump cases discussed

## Context

Optional slot **O1** (pj-027) balances the failure-focused core with a **difficult success**: models succeed despite a demanding CDM `risk` trajectory. Pedro rejected **severity-only** selection (argmax `risk_final` among TPs): the most extreme HR cases should show stable success (e.g. 5/5), not a 3/5 TP in an “easy win” slot. He chose **high intra-event volatility** among stable triple true positives.

Jump core slots **C3–C5** will use S2 taxonomy when available. O1 may still be jump-like in time series; overlap is avoided by **event_id**, not by excluding all jump labels.

## Decision

### Measure

On usable CDMs only (`time_to_tca >= 2`), per event:

**`range_risk` = max(risk) − min(risk)** over those rows (same `risk` column as protocol).

### Per repetition (seeds 42–46)

True HR (`y_hr = 1`); **LRP TP**, **rf TP**, **gbdt TP** (F₂ threshold −6 inclusive on predictions / LRP value).

### Event qualifies for O1

- **≥ 3 of 5** repetitions satisfy the triple-TP rule (pj-029 stability).
- **`event_id` not already used** in any other atlas panel (C1, C2, C6, C3–C5, O4 when assigned, O2–O3 when assigned). Same physical case must not appear twice in the atlas; a jump may qualify for O1 if it is **not** selected for C3–C5/O4.

### Select one event

Among qualifiers, **argmax `range_risk`**. Tie → smallest `event_id`.

### Caption (mandatory)

Same style as pj-029 / pj-030:

- **k/5** repetitions with triple TP.
- **Mean** LRP, rf, and gbdt predictions over those **k** repetitions.
- Report **`range_risk`** once (fixed per event).
- Optional: note if S2 jump label applies (informational only; not an exclusion rule).

### Academic note (recorded)

Re-using the **same `event_id`** in two atlas sections is poor practice (redundant, looks like padding). Re-using the **same pattern** (jump + success vs jump + failure) on **different** events is fine. Exclusion by assigned `event_id` list implements this.

## Rationale (developer's own words)

3/5 repetitions with all three models TP is enough. Do not exclude all jumps from O1—only exclude events already shown in earlier atlas slots. Among qualifying events, take the largest `range_risk` (most impactful volatile series) with frequency and mean in the note, like C1/C2.

## Consequences

- O1 selection runs **after** core C1, C2, C6 event_ids are fixed; re-run or swap O1 if a later pick collides (collision should be prevented by exclusion list).
- When C3–C5 are chosen, their ids are added to the exclusion list before finalizing O1 if O1 was picked earlier → implementation should **resolve order** or re-select O1 once jump ids exist.

## Checks

- High `range_risk` correlates with jump labels; narrative differs (unanimous TP vs outcome contrast in C3–C5).
- If no event meets ≥3/5 triple TP after exclusions, report empty O1 and skip panel (optional slot).
