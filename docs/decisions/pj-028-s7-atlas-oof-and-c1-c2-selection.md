# pj-028. S7 atlas — data source (OOF only) and C1/C2 selection rules

- **Status:** accepted
- **Date:** 2026-10-28
- **Tags:** modeling | evaluation | interpretation | data
- **Decided by:** Pedro
- **AI involvement:** critique on test-set use; selection rule recorded from developer

## Context

The failure atlas (pj-027) needs concrete `event_id`s per slot. Predictions must come from an honest evaluation protocol (S1, pj-004–006). Pedro asked why the atlas uses OOF rather than the official competition test split.

## Decision 1 — Atlas data source

**Use out-of-fold (OOF) predictions on the S1 train/validation `event_table` only.** Do **not** select atlas cases or narrative quotes from the **official Kelvins test** split used for the one-shot final evaluation.

### Why (for the record)

| Using official test for atlas | Using OOF on train/val |
|------------------------------|-------------------------|
| Test is touched many times indirectly while browsing “interesting” events → **narrative overfitting** / data snooping. | OOF mimics unseen events **within** the protocol you already report in tables. |
| Course/Kelvins rule: test reserved for **final** metrics, not exploratory case picking. | Same data the models were compared on in CV; stories align with reported folds. |
| Very small HR count on test (~150 HR events) → easy to cherry-pick memorable outliers. | Larger pool; selection rules (below) still required to stay objective. |

LRP on each event is computed from usable CDMs (protocol); tree `r_hat`/`p_hr` come from `preds/rf.parquet` and `preds/gbdt.parquet` **OOF rows** (see pj-020). Optional S4/S6 preds follow the same rule when added.

**Official test** may appear only in **aggregate** final numbers (R6 freeze), not as atlas panel sources unless a future ADR explicitly overrides this (not proposed).

## Decision 2 — C1 and C2 event pick

Among events that **qualify** for the slot under OOF F₂ rules (threshold −6 inclusive on `r_hat` vs true `y_hr` from `risk_final`):

| Slot | Qualification (OOF, per pj-027) | Select |
|------|----------------------------------|--------|
| **C1** | True HR; **LRP** FN; **rf or gbdt** TP (at least one tree TP on same event) | Event with **largest `risk_final`** (most severe HR on log₁₀ scale among qualifiers) |
| **C2** | True HR; **rf or gbdt** FN (if both trees, both FN); **LRP** TP | Same: **largest `risk_final`** among qualifiers |

**“Worst” / “peor” `risk_final`:** numerically **maximum** `risk_final` (e.g. −4.5 is more severe than −6.0).

**Model for C1/C2 in the figure:** prefer the tree that realizes the contrast (gbdt TP in C1; the FN tree in C2). If both trees satisfy the slot, pick the tree with **more extreme error** on `r_hat` vs `risk_final` (larger signed residual on the FN model); tie → `deferred-fog` until pj-029.

## Rationale (developer)

For C1 and C2, among false-negative cases choose the event with the worst (most severe) `risk_final`.

## Consequences

- Atlas scripts read `event_table`, LRP, and OOF parquets only (no test CSV for case mining).
- pj-029 (or follow-on) must fix: **which OOF row** when an event has multiple repetitions; jump slots C3–C6 rules; tie-break on equal `risk_final`.

## Checks

- Qualification must use **one consistent OOF policy** across slots (not yet fixed).
- C2 with both rf and gbdt FN is stricter than “either FN”; if pool is empty, reopen slot rule via new ADR.
