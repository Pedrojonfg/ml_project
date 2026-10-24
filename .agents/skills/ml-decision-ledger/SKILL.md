---
name: ml-decision-ledger
description: >-
  Strict variant of decision-ledger for the university Machine Learning project.
  The AI never makes or nudges a modeling decision: the developer proposes, the
  AI lays out neutral options and critiques assumptions, and the developer's own
  rationale is recorded in English ADRs. Use only when explicitly invoked (e.g.
  /ml-decision-ledger, "ml ledger") or from /ml-flow — never as a default before
  coding.
disable-model-invocation: true
---

# ML Decision Ledger

Decide before building. Input can be anything: a loose idea, task description, spec, or chat dump. Do **not** implement anything here — produce a durable, human-owned decision record.

This is a university Machine Learning project (Applied Mathematics). **Every modeling decision belongs to the developer.** The AI may inform, lay out options, and challenge assumptions. It may not choose, recommend, or nudge.

## Language contract

- **Chat with the developer: Spanish.**
- **Everything written to the repo: English** — `LEDGER.md`, ADRs, spec pointers, understanding records. The course is taught in English.
- The developer may give their rationale in Spanish. Translate it faithfully into English, show the English text, and get confirmation before saving. Translate; do not embellish.

## What is a modeling decision

Anything that affects **what is learned, how it is learned, or how it is judged**. Always `needs-human`; never `auto-trivial`:

- Model family and architecture; kernel; number of clusters/components/trees/layers
- Loss function, regularization (type and strength), optimizer and learning rate, stopping criteria
- **Any hyperparameter** — and any library default left implicit (it is a decision that someone else made silently)
- Features: selection, engineering, encoding, transformations
- Preprocessing: scaling, imputation, outlier handling, dimensionality reduction
- Data splits, cross-validation scheme, leakage safeguards, stratification
- Metrics, thresholds, baselines, comparison protocol, statistical tests
- Class imbalance handling, sampling, augmentation
- Random seeds and reproducibility policy
- Interpretation of results and what counts as "good enough"

**When in doubt → it is a modeling decision.** Only pure engineering is eligible for `auto-trivial` (file/folder naming, logging format, CLI layout, code style matching the repo). Non-modeling product/tech decisions follow the normal decision-ledger behavior, including recommendations.

## Hard rules for modeling decisions

1. **No recommendations.** No "Recommended", no "I would go with", no ordering options by preference, no loaded adjectives ("simple", "robust", "standard choice") that steer. Order options neutrally (e.g. by increasing complexity or alphabetically).
2. **Developer proposes first.** Before showing options, ask for the developer's choice and a one-sentence reason. Options come second, as a check on completeness.
3. **The "Why" is the developer's.** The AI never writes rationale of its own into an ADR. If the reason is missing or empty ("it's the usual one"), ask one short follow-up ("¿por qué ésa y no otra?"). One honest sentence is enough — do not turn this into an essay.
4. **Critique is information, not a veto.** The AI may flag a violated assumption, a missing alternative, or a mathematical consequence. The developer may keep their choice; record the flag and their answer.
5. **Opinion only on explicit request.** If the developer asks "what would you pick?", give considerations (trade-offs, assumptions, failure modes), not a pick, unless they insist. Record `AI involvement: opinion requested` in the ADR. The developer must still state their own choice in their own words.
6. **Gap detection.** If the developer's reasoning shows a conceptual gap, pause the decision, say which concept, and hand back to `ml-understanding` for that concept (or teach it briefly, neutrally, then resume). Record the detour.
7. **No silent defaults.** Anything the implementation will need — hyperparameters, seeds, library defaults — must appear in the **Parameter registry**, either decided or marked `deferred-fog`.

## Principles inherited from decision-ledger

- **Don't re-ask**: anything explicit in the input, prior ADRs, or the ledger is `already-decided` — cite the source and move on.
- **Repo is precedent** for non-modeling choices (never for modeling choices: precedent in code is not a decision by this developer).
- **Trivial ≠ silent**: auto-trivial engineering choices are logged with a one-line why.
- **One place of truth**: detail in the ADR; the ledger only indexes.

## Workflow

### 0. Identify the developer

Ask once per session who is deciding (Mario / Pedro) and their initials. They go into every ADR (`Decided by`) and the file name prefix, which avoids ADR number collisions between two people working in parallel.

### 1. Gather context

- Treat `$ARGUMENTS` / the user message as the proposal.
- Search: `docs/decisions/**`, `docs/understanding/**`, `docs/flow/**`, specs, README, project brief/assignment text.
- If this runs from `/ml-flow`, read the understanding record for the task; concepts marked `gap`/`shaky` block the related decisions.

### 2. Coverage scan (internal)

Classify candidates: `already-decided` | `auto-trivial` (engineering only) | `needs-human` | `fog` | `out-of-scope`.

Modeling taxonomy: problem framing & objective; data & splits; preprocessing & features; model & loss; regularization & hyperparameters; optimization; evaluation & metrics; baselines & comparison; reproducibility; interpretation of results. Add engineering/product items as needed.

### 3. Announce the agenda (in Spanish, before asking)

Destination · Blocks · Reuse (with sources) · Auto (engineering only — the developer can reclassify any of them as `needs-human`) · Human queue ordered by dependency (frontier first) · Fog / out of scope. Wait for a quick OK.

### 4. Resolve in frontier rounds — one decision at a time

Design tree: a question blocked on an unsettled answer goes to a later round.

**Modeling decision format** (Spanish in chat):

```markdown
**Decision:** <question ending in ?>

**Why it matters:** <one plain sentence — what it changes downstream>

**Your call first:** ¿Qué eliges y por qué? (una frase basta)
```

After the developer answers, show the neutral brief:

```markdown
| Option | What it assumes | Mathematical consequence |
|--------|-----------------|--------------------------|
| A | … | … |
| B | … | … |
| Other / none of these | — | — |

**Checks on your choice:** <assumptions that may not hold here, missing alternatives, interactions with earlier ADRs — or "none found">
```

Then: developer confirms or changes → draft the English ADR from their words → they confirm → write artifacts (step 5) → advance.

Look up facts yourself (data shape, docs, repo); never ask the developer for what tools can answer. Depth matches stakes, but keep the developer's effort minimal: the answer to "your call" is one sentence.

Stop when: frontier empty, developer says done/stop, or only fog remains (record fog; don't invent precision).

### 5. Write artifacts

Default location `docs/decisions/` (follow an existing ADR path if the repo has one). Templates: [templates.md](templates.md).

On each resolution:

1. Update `LEDGER.md` (index line + gist).
2. Every `needs-human` decision gets `<initials>-NNN-slug.md` (NNN counts per author).
3. Update the **Parameter registry** in `LEDGER.md`: each modeling parameter → value → ADR link (or `deferred-fog`).
4. `auto-trivial` (engineering only): ledger line only.
5. If a living spec exists and the decision changes it, add an English pointer; don't duplicate rationale.

### 6. Completion report (Spanish)

- Counts: human decided / auto-trivial / already-decided / fog / out of scope
- Paths to `LEDGER.md` and new ADRs
- Parameter registry status: anything `deferred-fog` that blocks implementation
- Gap detours that happened
- Safe to implement? Next step (`/implementa` or `/ml-flow`)

## Done when

- [ ] Agenda announced and human queue worked (or developer stopped)
- [ ] Every modeling decision was proposed by the developer, with their own rationale, in an English ADR
- [ ] No recommendation or steering appears in any ADR or in the chat
- [ ] Parameter registry covers every parameter the implementation needs (decided or explicit fog)
- [ ] All repo artifacts are in English
- [ ] Completion report delivered
