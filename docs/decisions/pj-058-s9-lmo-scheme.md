# pj-058. S9 leave-mission-out — evaluation scheme

- **Status:** accepted
- **Date:** 2026-11-14
- **Tags:** evaluation | data
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

S9 includes leave-mission-out (LMO) alongside the lead-time curve (`pj-053`). `mission_id` is constant per event, excluded from `X` (`pj-011`), but train and test mission mixes differ in Kelvins (brief). The internal cohort has 8 892 events, 93 HR, **19 missions** with events (EDA 2026-11-14): median ≈208 events/mission, minimum 4 events on one mission, **13 missions** with ≥1 HR, **6 missions** with no HR in this cohort. Event CV remains the primary protocol (`pj-004`); LMO is a stretch stress test.

## Mathematical framing

For each mission `m`, form train = events with `mission_id ≠ m`, test = events with `mission_id = m`. Fit models on train only; compute dashboard metrics (`pj-007`) on test. Repeat for all missions present in the cohort. This is **not** the repeated 5×5 stratified event CV; no mixing with `make_folds()` unless a later ADR says so.

**Mission label per event:** `mission_id` from the training CSV (constant per event); implementation joins from raw CDM, same rule as S2 EDA (`mission_id.first()` per `event_id`).

## Options considered

1. **Leave-one-mission-out (19 folds)** — one held-out mission per iteration; standard LMO.
2. **LMO restricted to missions above size / HR thresholds** — fewer folds.
3. **Single held-out mission (or test-like missions only)** — targeted shift, not full LMO.
4. **LMO plus rank comparison vs event CV** — extra reporting column.

## Decision

Chose **option 1**: **19-fold leave-one-mission-out**, one fold per mission in the internal cohort.

Lead-time `t_cut`, model rows, primary reported metric for the LMO table, and handling of held-out missions with zero HR events are **not** fixed in this ADR (see consequences).

## Rationale (developer's own words)

It is the standard definition of LMO.

## Checks raised

- Six missions have **no HR** in the internal cohort → F₂ and L on a pure-negative held-out set are ill-defined or zero; needs an explicit rule in a follow-up ADR.
- Two missions have **≤5 events** → high variance per fold.
- Cost: 19× full training if every model and selection is repeated; may match the lean S9 model set decided for the lead-time curve (`pj-056`) in a later ADR.
- Official test remains out of scope for case selection (`pj-028` spirit); LMO here uses the same internal cohort as the bake-off.

## Expected behavior and validation

- Output: table or JSON with one metric row per held-out `mission_id`, plus `n_test` and `n_hr_test`.
- Optional summary: mean/median across missions with documented exclusions.

## Consequences

- Engineering: attach `mission_id` to events for S9 (not a feature column).
- Next ADRs: LMO model rows, `t_cut` (default 2 expected), zero-HR fold policy, primary metric for W2 table, comparison vs event-CV ranking (optional per brief).