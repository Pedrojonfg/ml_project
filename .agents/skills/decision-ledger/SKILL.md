---
name: decision-ledger
description: >-
  Surfaces all non-trivial product and code decisions for a proposal (idea, PRD,
  or spec), explains alternatives and trade-offs at a non-expert level with a
  clear recommendation, auto-resolves trivial choices into the log, and writes a
  traceable decision ledger plus lightweight ADRs. Use only when explicitly
  invoked (e.g. /decision-ledger, "decision ledger", "map decisions", "clarify
  decisions", "tradeoff board") — never as a default before coding.
disable-model-invocation: true
---

# Decision Ledger

Decide before building. Input can be anything: a loose idea, PRD, spec, or chat dump. Do **not** implement the feature in this skill — produce shared understanding and a durable decision record.

## Principles

1. **Plan, don't do** — resolve decisions; hand off when the way is clear.
2. **Don't re-ask** — anything already explicit in the input, prior ADRs, ledger, or settled repo precedent is `already-decided`. Cite the source; move on.
3. **Repo is precedent** — prefer consistency with existing stack patterns, naming, and prior decisions over "ideal greenfield."
4. **Educate on trade-offs** — especially for code/stack choices: plain language, alternatives, costs, then a marked recommendation.
5. **Trivial ≠ silent** — auto-resolve low-risk choices, but log them as `auto-trivial` with a one-line why.
6. **One place of truth** — detail lives in the ADR (or auto entry); the ledger only indexes with a gist + link.

## Workflow

### 1. Gather context

- Treat `$ARGUMENTS` / the user message as the proposal (any format).
- Search the repo for prior decisions and constraints:
  - `docs/decisions/**`, `**/adr/**`, `**/ADR*`, `DECISIONS.md`, `CONTEXT.md`
  - Specs / PRDs / constitution / AGENTS.md / README stack notes
  - Dominant patterns in code (auth, data access, API style, folder layout)
- If no repo (or empty): proceed from the proposal + stated stack only; note that precedent was unavailable.

### 2. Coverage scan (internal)

Classify candidates across **product** and **tech**. For each item mark one of:

| Status | Meaning |
|--------|---------|
| `already-decided` | Explicit in input or prior docs/code precedent |
| `auto-trivial` | Low risk; agent will choose and log |
| `needs-human` | Non-trivial; must ask |
| `fog` | In scope but not sharp enough to decide yet |
| `out-of-scope` | Ruled outside this destination |

**Product taxonomy (adapt as needed):** goals & success; scope/out-of-scope; roles; data/entities; journeys & edge cases; non-functionals (perf, security, privacy); integrations; terminology.

**Tech taxonomy (adapt as needed):** architecture boundaries; data store & schema; API/contracts; authN/Z; state & sync; error/observability; testing strategy; deployment/ops; library/pattern choices that diverge from precedent.

Skip pure execution details (task breakdown, commit order) unless they block correctness.

### 3. Announce the agenda (before asking)

Publish a short agenda **once**:

- **Destination** — one or two lines (what “done deciding” looks like)
- **Blocks** — prefer one pass; if explanations will be long, split (e.g. Product → Tech) and say so up front with approximate counts
- **Reuse** — what is `already-decided` (bullets with sources)
- **Auto** — what you will resolve as `auto-trivial` (preview; write after confirmation of the agenda or as you go)
- **Human queue** — titles of `needs-human` items, ordered by dependency (frontier first)
- **Fog / out of scope** — brief

Wait for a quick OK / adjustments if the agenda is wrong, then proceed.

### 4. Resolve in frontier rounds

Build a **design tree**: a question blocked on an unsettled answer belongs in a later round.

**Per human decision (exactly one at a time):**

```markdown
**Decision:** <clear question ending in ?>

**Why it matters:** <one plain sentence — shipping / rework stake>

**Recommended:** Option <X> — <1–3 sentences why, tied to this project>

| Option | What it means | Trade-offs |
|--------|---------------|------------|
| A | … | … |
| B | … | … |
| C | … | … |

Reply with a letter, "yes"/"recommended", or a short alternative.
```

Rules for the table and prose:

- 2–5 mutually exclusive options when discrete choices exist; otherwise suggest a short answer + rationale.
- For **code/stack** options: explain jargon in-line so a non-expert of that stack can choose.
- Depth matches stakes — short for small forks; longer when the choice is hard to reverse.
- Look up facts yourself (docs, repo); never ask the user for what tools can answer.
- After each accepted answer: write artifacts immediately (step 5), then advance the frontier.

**Auto-trivial:** resolve without asking when impact is low and one option clearly matches precedent or convention. Still write the ledger entry.

Stop when: frontier empty, user says done/stop, or only fog remains (record fog; don't invent fake precision).

### 5. Write artifacts

Default location: `docs/decisions/` (create if missing). If the repo already uses another ADR path, follow that and keep `LEDGER.md` beside those files (or at `docs/decisions/LEDGER.md` linking out).

Templates: [templates.md](templates.md)

On each resolution:

1. Update `LEDGER.md` (index line + gist).
2. For `needs-human` and significant tech/product forks: add `NNN-slug.md` (next free number).
3. For `auto-trivial`: ledger entry only (`status: auto-trivial`) — no separate ADR unless the user asks.
4. If a living spec/PRD exists and the decision changes it: add a pointer under a `## Decisions` / clarifications section (link to ADR/ledger), don't duplicate the full rationale.

### 6. Completion report

- Counts: human answered / auto-trivial / already-decided cited / fog left / out of scope
- Paths to `LEDGER.md` and new ADRs
- Blockers remaining (fog) and whether it's safe to plan/build
- Suggested next step (plan, implement, or another ledger pass on a focus area)

## Done when

- [ ] Agenda announced and human queue worked (or user stopped)
- [ ] Every resolved item is in the ledger (including auto-trivial)
- [ ] Non-trivial decisions have ADRs with options + why
- [ ] No silent assumptions that should have been decisions
- [ ] Completion report delivered
