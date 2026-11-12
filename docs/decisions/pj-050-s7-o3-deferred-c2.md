# pj-050. S7 atlas — O3 not defined for C2 (sufficient without it)

- **Status:** accepted
- **Date:** 2026-11-12
- **Tags:** modeling | evaluation | interpretation | product
- **Decided by:** Pedro
- **AI involvement:** none

## Context

pj-027 lists optional **O3** as a second calibration / two-stage angle, included only if O2 is included and time allows; it is first in the optional cut order (O3→O1→O4→O2). O2 selection is now fixed (pj-049). The developer judged the atlas decision set sufficient for C2 without an O3 picking rule.

## Options considered

1. **Define O3 now** — e.g. reverse flip (calibrated fails, raw succeeds) or a second ≥5/9 event.
2. **Leave O3 undefined for C2** (chosen) — omit the panel; may add a follow-on ADR later.
3. **Hard-delete O3 from pj-027 layout** — would reopen the slot catalogue.

## Decision

**Do not write an O3 selection rule in C2.** Implementation **skips** the O3 panel. pj-047’s assignment order simply omits O3 (C1…C6→O1→O2→O4). A future ADR may define O3 without reopening O2/O4.

Closes the remaining open item of pj-032 for this cycle.

## Rationale (developer's own words)

For now I would leave it; with this, it is enough.

## Consequences

- S7 optional calibration story is **O2 only** (plus O4 jump complement unrelated to S6).
- Cut-list references to O3 remain historical; skipping O3 matches “cut first if needed.”

## Checks raised

- Oral/report must not promise a second calibration panel unless O3 is revived.
