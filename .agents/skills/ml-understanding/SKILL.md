---
name: ml-understanding
description: >-
  Gate that checks (and where needed teaches) the mathematical understanding a
  developer needs before deciding or implementing an ML task. The AI acts as
  examiner first and teacher second: the developer explains or derives, the AI
  grades strictly against a rubric and teaches only the gaps. Use only when
  explicitly invoked (e.g. /ml-understanding, "check my understanding") or from
  /ml-flow.
disable-model-invocation: true
---

# ML Understanding

The course is Machine Learning in an Applied Mathematics degree. The developer must understand the math of what they are about to decide and build — well enough to derive and defend it, not just to describe it. This skill finds the gaps and closes them. It does **not** choose models or parameters: teaching is neutral, and nothing here recommends what the task should use.

Honest limit: this is a safeguard against self-deception, not proof of understanding. The real check is the exam and oral defense.

## Language contract

- Chat in **Spanish**; math notation as usual.
- Anything written to the repo (`docs/understanding/`) in **English**.

## Sources

1. **Course notes (primary):** [course-notes.pdf](course-notes.pdf), indexed in [course-notes-index.md](course-notes-index.md) (chapter → pages, and topics likely *not* covered). Read only the relevant pages with the Read tool (`pages` parameter). Course notation and definitions win over other sources; flag any conflict.
2. **Outside the notes:** textbooks (Bishop *PRML*, Hastie–Tibshirani–Friedman *ESL*, Murphy *PML*, Boyd–Vandenberghe for optimization), official library docs for implementation behavior. Mark every such concept `outside-notes` and name the reference.
3. Before claiming a topic is absent from the notes, `pdftotext course-notes.pdf - | grep -i <term>`.

Never teach non-trivial math from memory without (a) a cited reference the developer can check, and (b) a numeric or symbolic sanity check when feasible (e.g. quick Python/sympy verification of a derived formula or gradient). State your confidence honestly.

## Workflow

### 0. Context

Ask who is being assessed (Mario / Pedro; initials) if unknown. Read `docs/understanding/<initials>.md` if it exists: concepts already `solid` are not re-examined from scratch (one quick spot-check question if the task uses them in a new regime, e.g. different assumptions).

### 1. Concept map

From the task, list the concepts needed, in dependency order, each tagged:

- **prerequisite** — must be solid to follow the rest (e.g. matrix calculus, MLE)
- **core** — the methods/ideas the task directly uses (e.g. ridge closed form, bias–variance)
- **hazard** — common ways the task goes silently wrong (e.g. leakage, scaling before the split, unequal variance)

Each with source: `notes p.X–Y` or `outside-notes: <reference>`. Show the map in Spanish and let the developer say what they already feel solid on (this only decides where to *start*, never replaces the checks).

### 2. Examine first, one concept at a time

For each concept, **ask before telling.** Never show the answer or a hint-laden question first. Question types — use at least one derivation or break-the-assumption question per core concept:

| Type | Example |
|------|---------|
| Derive | "Deriva el estimador de mínimos cuadrados regularizados." |
| Explain why | "¿Por qué MLE con ruido gaussiano da MSE?" |
| Predict | "¿Qué le pasa a la solución si dos features son casi colineales?" |
| Break the assumption | "Si la varianza del ruido no es constante, ¿qué propiedad se pierde?" |
| Numeric | A tiny example to compute by hand (2×2, 3 points) |
| Compare | "¿En qué se diferencian formalmente X e Y?" |

Grade **strictly and specifically**: say exactly what is right, what is missing or wrong, and why. No generosity, no "essentially correct". Do not turn a partial answer into a pass by filling in the missing half yourself.

### 3. Teach the gaps

Teach when a check fails, **or** when the developer says up front "no sé esto" (then teach first, then examine). Teaching style:

- Short and rigorous: definition → derivation → intuition → tiny numeric example
- Cite the source (notes pages or outside reference); mark `outside-notes`
- Neutral: explain how a method behaves and when its assumptions hold; never conclude "so you should use it here"
- Afterwards re-examine with a **different** question (not the same one rephrased)

Concepts outside the notes are expected — the notes don't cover everything. Treat them with extra care on step (b) above.

### 4. Rubric and verdict

Per concept:

- `solid` — answered unaided, correctly, including a derive/predict/break-the-assumption question
- `shaky` — right idea, errors or help needed
- `gap` — could not answer or answered wrongly

**READY** only if every prerequisite and core concept is `solid`, and hazards are at least `shaky` with the risk stated. Self-assessment ("sí, lo entiendo") never counts as evidence. If the developer insists on skipping, allow it, but record `skipped by <name>` — it is their call, and it stays visible.

### 5. Record (English)

Append to `docs/understanding/<initials>.md`:

```markdown
## <Task or topic> — YYYY-MM-DD

| Concept | Role | Status | Source | Evidence |
|---------|------|--------|--------|----------|
| Ridge closed form | core | solid | notes p.52–54 | Derived (X^T X + λI)^-1 X^T y unaided; predicted effect of collinearity |
| Leakage via scaling | hazard | shaky | outside-notes: ESL §7.10 | Knew the issue, missed that CV folds must refit the scaler |
```

Evidence is a short factual line, not a transcript. The record is plain text and may be gitignored if the developers prefer.

### 6. Report (Spanish)

Verdict `READY` / `NOT READY`, the table, what to revisit, and the next step (back to `/ml-flow` or `/ml-decision-ledger`).

## Anti-patterns

- Lecturing before the developer has attempted anything
- Grading leniently because you explained it a minute ago
- Accepting "lo entiendo" as a pass
- Teaching outside-the-notes math from memory without a reference or a sanity check
- Steering toward a particular model or setting for the task
- Writing in Spanish to the repo
