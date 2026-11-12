# pj-045. S7 atlas — C3–C5 jump selection rules (unblocks pj-030)

- **Status:** accepted (**IDs C5–C7** after pj-051 renumber; rules unchanged)
- **Date:** 2026-11-12
- **Tags:** modeling | evaluation | interpretation
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

pj-027 requires three core jump panels (originally C3–C5; **C5–C7** as of pj-051) with distinct outcomes. pj-030 deferred their selection rules until S2 taxonomy existed. Mario’s S2 labels are in `src/taxonomy.py` (mf-002..mf-004): `jump_class` from \(\Delta = \texttt{risk\_final} - \texttt{lrp}\) with cut \(c=1\). Atlas scoring remains OOF-only (pj-028) with ≥3/5 repetition stability (pj-029) and F₂ threshold −6 inclusive on LRP / `r_hat` (pj-001, pj-020).

## Mathematical framing

Each event has a final label \(y_{\mathrm{hr}} = \mathbf{1}\{\texttt{risk\_final} \ge -6\}\) and, per repetition, three binary alarms for \(\{\mathrm{LRP}, \mathrm{rf}, \mathrm{gbdt}\}\). “Majority” means at least two of those three. Jump magnitude is \(|\Delta|\). There is no separate pre/post-jump model prediction: the narrative “missed the jump” is operationalized as majority wrong on the **final** label for that jump class.

## Options considered

1. **Label-only** — pick by `jump-up` / `jump-down` without model-outcome patterns.
2. **Outcome-only** — TP/FN patterns without requiring a jump label.
3. **Cross label × outcome (chosen)** — one jump-up miss, one jump-down miss, one jump (either class) where the majority catch the final label.
4. **Pool + diversity** — single ranked pool with distinct outcome vectors, no pre-assigned slot meanings.

## Decision

### Shared

- Predictions: OOF train/val only (pj-028).
- Models in the majority count: **{LRP, rf, gbdt}** (same set as C6 at launch).
- Stability: slot condition in **≥ 3 of 5** repetitions (pj-029).
- Among qualifiers: **argmax \(|\Delta|\)** (largest jump magnitude). Tie → **smallest `event_id`**.
- `event_id` exclusion across atlas panels (pj-031): a case used in C1–C6 or optionals must not be reused.

### C3 — jump-up, majority miss the rise to HR

- `jump_class = jump-up` and true HR (`y_hr = 1`).
- Per qualifying repetition: **≥ 2 of 3** models are **FN** (prediction / LRP \(< -6\)).
- Event qualifies if that holds in ≥3/5 reps; then argmax \(|\Delta|\).

### C4 — jump-down, majority miss the drop to non-HR

- `jump_class = jump-down` and true **non**-HR (`y_hr = 0`).
- Per qualifying repetition: **≥ 2 of 3** models are **FP** (prediction / LRP \(\ge -6\)).
- Event qualifies if that holds in ≥3/5 reps; then argmax \(|\Delta|\).

### C5 — jump (either class), majority catch the change

- `jump_class \in \{\texttt{jump-up}, \texttt{jump-down}\}`.
- Per qualifying repetition: **≥ 2 of 3** models are **correct** on the final label (TP if HR, TN if non-HR).
- Event qualifies if that holds in ≥3/5 reps; exclude `event_id`s already taken by C1–C4/C6 (and earlier optionals if already assigned); then argmax \(|\Delta|\).

### Caption (mandatory, each of C3–C5)

- `jump_class`, \(\Delta\), \(|\Delta|\`, true `risk_final` / `y_hr`.
- **k/5** repetitions satisfying the slot rule.
- Per model in {LRP, rf, gbdt}: count of reps (0–5) that are wrong (C3/C4) or right (C5) on this event.
- Mean prediction (LRP value / `r_hat`) over the **k** qualifying repetitions.

### Supersession

Supersedes **Decision 1** of pj-030 (deferral of C3–C5 selection rules). C6 in pj-030 is unchanged. O4 remains for a follow-on ADR (pj-032 still covers O2–O4 until written).

## Rationale (developer's own words)

Precisely what is dangerous about jumps is failing to catch them, so seeing one example of each miss and one where the change is caught seems the most illustrative.

## Consequences

- Atlas implementation can select C3–C5 from `jump_class` + OOF preds of LRP/rf/gbdt.
- Empty pool for a slot → do not silently relax majority or ≥3/5; report and reopen via new ADR (same spirit as C6 in pj-030).
- Figure prose may still describe the CDM timeline; scoring stays on the final label.

## Checks raised

- C4 requires final non-HR; jump-down events that remain HR do not qualify for C4.
- C5 may narratively resemble a “success” jump; exclusion list prevents duplicating C1/C2 `event_id`s.
- Extending the majority set to S4/S6 models needs a separate ADR (alarm lines may differ from −6).
