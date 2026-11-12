# pj-046. S7 atlas — C1/C2 selection tie-break after `risk_final`

- **Status:** accepted
- **Date:** 2026-11-12
- **Tags:** modeling | evaluation | interpretation
- **Decided by:** Pedro
- **AI involvement:** options + critique; opinion requested on replacing `risk_final` as primary key

## Context

pj-028 selects C1/C2 among qualifiers by argmax `risk_final`. Equal `risk_final` was deferred-fog in the ledger. pj-029 already picks which tree appears in the panel when both rf and gbdt can realize the contrast. The developer considered using a squared-error contrast as the **primary** sort key instead of `risk_final`, then rejected that for operational priority.

## Mathematical framing

For a qualifying event and slot, let \(y = \texttt{risk\_final}\) and let \(p_{\mathrm{wrong}}\), \(p_{\mathrm{right}}\) be the means of the wrong-side and right-side predictions over the **k** qualifying OOF repetitions (pj-029). Predictions are LRP’s value or tree `r_hat`. Squared errors \(e = (p - y)^2\). Contrast score
\[
s = e_{\mathrm{wrong}} - e_{\mathrm{right}}.
\]
C1: wrong = LRP, right = panel tree (TP side). C2: wrong = panel tree (FN side), right = LRP.

## Options considered

1. **Primary `risk_final` only** — leave ties unspecified or use `event_id`.
2. **Primary contrast score \(s\)** — drop severity as the first key.
3. **Lexicographic: `risk_final` then \(s\)** (chosen) — severity first; contrast only on ties.
4. **Lexicographic: \(s\) then `risk_final`**.

## Decision

Among events that already qualify for C1 or C2 (pj-028, pj-029):

1. **Primary:** argmax `risk_final` (unchanged from pj-028).
2. **If tied on `risk_final`:** argmax \(s = e_{\mathrm{wrong}} - e_{\mathrm{right}}\) with \(p\) = mean prediction on the k qualifying reps; wrong/right roles as above; panel tree from pj-028/pj-029.
3. **If still tied:** smallest `event_id`.

Does **not** replace `risk_final` as the primary operational criterion.

## Rationale (developer's own words)

What should worry you most is not the case where one model is most spectacularly wrong, but the case where the risk is highest and you are wrong. The second criterion is fine but not as operationally important.

## Consequences

- Implements the former fog line “S7 tie-break equal `risk_final`” for C1/C2.
- C3–C5 keep argmax \(|\Delta|\) (pj-045); C6/O1 keep their own keys (pj-030, pj-031).
- Caption may optionally report \(s\) when a tie was broken; not required.

## Checks raised

- Continuous `risk_final` makes exact ties rare; the second key is still defined for reproducibility.
- Opinion was requested on using \(s\) as primary; developer kept severity first.
