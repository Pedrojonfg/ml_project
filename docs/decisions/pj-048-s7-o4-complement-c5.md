# pj-048. S7 atlas — O4 fourth jump complementary to C5

- **Status:** accepted (**renamed O3**, complement to **C7**, by pj-051)
- **Date:** 2026-11-12
- **Tags:** modeling | evaluation | interpretation
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

pj-027 lists optional **O4** as a fourth temporal jump. pj-032 deferred O2–O4 rules until S2/S6 existed. pj-045 defines core **C5** as a jump (either class) where ≥2 of {LRP, rf, gbdt} are correct on the final label in ≥3/5 OOF reps, selected by argmax \(|\Delta|\). Putting **both** a successful jump-up and a successful jump-down in the **core** was judged too heavy; one success stays core (C5), the other class can appear as optional O4.

**pj-051 (2026-11-12):** this panel is **O3**; the catch jump core slot is **C7** (ex-C5). Rules below are unchanged except for those IDs.

## Mathematical framing

Let \(J_{\mathrm{C5}}\) be the `jump_class` of the event assigned to C5. O4 uses the same correctness rule as C5 (pj-045) on the complementary class
\[
J_{\mathrm{O4}} =
\begin{cases}
\texttt{jump-down} & \text{if }J_{\mathrm{C5}}=\texttt{jump-up},\\
\texttt{jump-up} & \text{if }J_{\mathrm{C5}}=\texttt{jump-down}.
\end{cases}
\]
Selection among O4 qualifiers: argmax \(|\Delta|\); tie → smallest `event_id`. Exclusion list per pj-047 (O4 after O1–O3 in the optional block, after all core slots).

## Options considered

1. **Fixed O4 = jump-down catch** — independent of C5.
2. **Complement of C5’s class** (chosen) — show both directions when insightful, without two core success panels.
3. **Leave O4 undefined / always cut**.

## Decision

- **Qualification:** same as C5 (pj-045) but restricted to `jump_class = J_O4` (opposite of the selected C5 event).
- **Selection:** argmax \(|\Delta|\); tie → smallest `event_id`.
- **If C5 has no assigned event** (empty C5 pool): **do not emit O4** (no opposite class to complement).
- **If O4 pool empty:** do not relax rules; omit the panel (optional).
- **Schedule:** O4 remains optional; may be cut under pj-027’s cut order if the realized panel is not insightful after seeing results — cutting does not rewrite this selection rule.

Caption: same style as C5 (k/5, per-model correctness counts, mean preds on k reps, \(\Delta\), \(|\Delta|\), `jump_class`).

Partial progress on pj-032 (O4 only); O2/O3 still open.

## Rationale (developer's own words)

It is interesting to see (assuming it happens) that there are cases where the models adapt well on both jump-up and jump-down, but putting both in the core seems too much. Select by argmax of jump magnitude.

## Consequences

- Implementation needs C5’s chosen `event_id` / `jump_class` before selecting O4.
- Core stays at one “majority catch” jump (C5); the other direction is optional.

## Checks raised

- If C5 is jump-up, O4 cannot duplicate that class; the interesting “both directions work” story needs both panels present.
- Empty O4 is allowed; it is not a failed core.
