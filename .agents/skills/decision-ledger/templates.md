# Decision ledger templates

## LEDGER.md

```markdown
# Decision ledger

## Destination

<what “done deciding” looks like for this effort>

## Notes

- Domain / stack constraints
- Skills or docs every session should respect
- Standing preferences for this effort

## Already decided (cited)

- <gist> — source: <path or “user input”>

## Decisions

| ID | Title | Status | Gist | Link |
|----|-------|--------|------|------|
| 001 | Auth model | accepted | Session JWT in httpOnly cookie | [001-auth-model.md](./001-auth-model.md) |
| — | Component file naming | auto-trivial | Match existing `PascalCase.tsx` | — |

Status values: `accepted` | `auto-trivial` | `superseded` | `deferred-fog`

## Fog (not yet sharp)

- <suspected decision area — revisit when unblocked>

## Out of scope

- <ruled out of this destination + why>
```

## ADR (`NNN-slug.md`)

Lightweight MADR-style. Keep short; link out rather than pasting specs.

```markdown
# NNN. <Title>

- **Status:** accepted | superseded by NNN | deferred
- **Date:** YYYY-MM-DD
- **Tags:** product | tech | <area>
- **Decided by:** human | auto-trivial

## Context

What forces the decision. Cite proposal section, issue, or repo precedent.

## Options considered

1. **<Name>** — <one-line>. Pros: … Cons: …
2. **<Name>** — …
3. **<Name>** — …

## Decision

Chose **<Name>**.

## Why

Rationale in plain language (include recommendation reasoning the user accepted).

## Consequences

- Follow-ups / constraints this creates
- What we are explicitly *not* doing
```

## Auto-trivial ledger line

Use when no ADR file is warranted:

```markdown
| — | <Title> | auto-trivial | <choice>. Reason: <one line, e.g. matches precedent in `src/...`> | — |
```

## Spec pointer (optional)

When updating an existing spec after a decision:

```markdown
## Decisions

- YYYY-MM-DD: <gist> — see [NNN-slug.md](../decisions/NNN-slug.md)
```
