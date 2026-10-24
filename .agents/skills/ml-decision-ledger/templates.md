# ML decision ledger templates

All repo artifacts are written in **English**.

## LEDGER.md

```markdown
# Decision ledger

## Destination

<what "done deciding" looks like for this effort>

## Notes

- Course / task constraints (assignment text, deadlines, allowed tools)
- Standing preferences for this effort

## Already decided (cited)

- <gist> — source: <path or "assignment text">

## Decisions

| ID | Title | Status | Decided by | Gist | Link |
|----|-------|--------|------------|------|------|
| pj-001 | Loss function | accepted | Pedro | Cross-entropy; labels are Bernoulli | [pj-001-loss.md](./pj-001-loss.md) |
| — | Log file format | auto-trivial | AI (engineering) | Plain text. Reason: matches existing logging in `src/...` | — |

Status values: `accepted` | `auto-trivial` | `superseded` | `deferred-fog`

## Parameter registry

Every modeling parameter the implementation needs. Library defaults must be listed explicitly — an unlisted default is an undecided parameter.

| Parameter | Value | ADR |
|-----------|-------|-----|
| random seed | 42 | [mj-002-seeds.md](./mj-002-seeds.md) |
| L2 strength (lambda) | deferred-fog (chosen by CV, scheme in pj-004) | pj-004 |

## Fog (not yet sharp)

- <suspected decision area — revisit when unblocked>

## Out of scope

- <ruled out of this destination + why>
```

## ADR (`<initials>-NNN-slug.md`)

Keep it short. The **Rationale** is the developer's own words (translated to English if needed, nothing added).

```markdown
# <initials>-NNN. <Title>

- **Status:** accepted | superseded by <id> | deferred
- **Date:** YYYY-MM-DD
- **Tags:** modeling | data | evaluation | engineering | <area>
- **Decided by:** <Name>
- **AI involvement:** none | options + critique | opinion requested

## Context

What forces the decision. Cite task text, earlier ADRs, data facts.

## Mathematical framing

What is being optimized or assumed (objective, distributional or structural assumptions, what the choice changes).

## Options considered

1. **<Name>** — assumes …; consequence …
2. **<Name>** — …
3. **<Name>** — …

## Decision

Chose **<Name>**.

## Rationale (developer's own words)

<One or a few sentences from the developer.>

## Checks raised

- <assumption flag or missing alternative the AI raised> → <developer's response>
  (or "None raised")

## Expected behavior and validation

Falsifiable expectation ("we expect X to improve Y because …") and how it will be checked.

## Consequences

- Follow-ups / constraints this creates
- What we are explicitly *not* doing
```

## Auto-trivial ledger line (engineering only)

```markdown
| — | <Title> | auto-trivial | AI (engineering) | <choice>. Reason: <one line> | — |
```

## Spec pointer (optional)

```markdown
## Decisions

- YYYY-MM-DD: <gist> — see [pj-001-slug.md](../decisions/pj-001-slug.md)
```
