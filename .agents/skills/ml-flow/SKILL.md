---
name: ml-flow
description: >-
  Orchestrator for ML project tasks: runs understanding check, then
  ml-decision-ledger, then implementa, then a decision audit — each a gate that
  must pass before the next. The AI makes no modeling decisions at any stage.
  Use only when explicitly invoked (e.g. /ml-flow, "run the ml flow on this
  task").
disable-model-invocation: true
---

# ML Flow

For a university ML project in which **the developer understands and decides everything modeling-related; the AI teaches, challenges, records, and types.** This skill sequences the stages and enforces the gates. It decides nothing itself, and it does not judge understanding — it relays the verdict of `ml-understanding`.

**Announce at start:** "Usando `/ml-flow`."

## Language contract

Chat in Spanish. Everything written to the repo in English.

## How to run the stages

Each stage is a sibling skill. Invoke it with the Skill tool. These skills are user-invoked only, so if the harness refuses, read the sibling `SKILL.md` (next to this skill's folder) and follow it inline as if invoked. Do not paraphrase from memory.

| Stage | Skill |
|-------|-------|
| 1. Understanding | `ml-understanding` |
| 2. Decisions | `ml-decision-ledger` |
| 3. Implementation | `implementa` (with `ponytail`) |
| 4. Audit | this skill, below |

## Step 0 — Triage and identity

1. Ask who is working (Mario / Pedro; initials) if unknown.
2. Read the task. Split it:
   - **Plumbing** (I/O, CLI, plots, formatting, repo structure — no modeling choice anywhere): skip the gates, hand to `/implementa`, say so in one line.
   - **Modeling** (see the list in `ml-decision-ledger`): full flow.
   - **Mixed**: separate into two parts, run the flow on the modeling part, and plumbing may proceed in parallel.
   If unsure whether a piece is modeling → it is modeling.
3. Create or resume the flow state file `docs/flow/<initials>-<task-slug>.md` (English):

```markdown
# Flow: <task>
- Owner: <Name>
- Understanding: pending | READY (date) | skipped by <name> (date)
- Decisions: pending | complete (date) — ledger: docs/decisions/LEDGER.md
- Implementation: pending | done (date)
- Audit: pending | clean (date) | findings (see below)
- Detours: <back-edges taken and why>
```

Update it as stages finish. If it exists, resume at the first unfinished stage.

## Stage 1 — Understanding gate

Run `ml-understanding` for the task. Gate passes only on its verdict **READY**. The developer may explicitly skip; record `skipped by <name>` in the state file. Do not suggest skipping and do not accept "ya lo entiendo" as a pass.

## Stage 2 — Decisions gate

Run `ml-decision-ledger` with the task and the understanding record. Gate passes when its completion report says: every modeling decision decided by the developer, Parameter registry has no `deferred-fog` that blocks implementation.

## Stage 3 — Implementation gate

Run `implementa` with these **extra constraints**, included verbatim in the instructions to it and in every subagent prompt:

- Source of truth is `docs/decisions/LEDGER.md` and the ADRs. Implement exactly what is registered.
- **Unregistered modeling parameters are forbidden.** Hyperparameters, seeds, library defaults, split ratios, thresholds, scaler/imputer choices: if it is not in the Parameter registry, **stop and report to the parent** — do not pick a value, do not rely on a library default. Pass every registered parameter explicitly in code.
- Ponytail exceptions: do not simplify away seeding/reproducibility, train/validation/test separation, fitting preprocessing on training data only, or the evaluation protocol from the ADRs.
- Tests worth writing in this domain: shapes, determinism under the seed, no leakage across splits, and (where a closed form or known case exists) agreement with it. Keep to the author/solver split from `implementa`.
- Code comments and docstrings in English; cite the ADR id next to each registered parameter (`# per pj-003`).

If `implementa` reports a missing decision → **back-edge to Stage 2** for that item only. Never let the implementer or the parent fill the gap.

## Stage 4 — Decision audit

Compare what was built against the ledger:

1. Search the diff for modeling-relevant constructs: model/estimator constructors, `fit`/`train` calls, optimizers, losses, scalers/encoders/imputers, splits and CV, seeds (`random_state`, `seed`, `manual_seed`), thresholds, metric computation.
2. For each, find the matching Parameter registry row / ADR.
3. Report in Spanish: matches; **unregistered choices** (file:line); registered values that differ from the code.
4. Unregistered or mismatching items are not silently fixed. Each goes back to Stage 2 (new decision) or is fixed to match the ADR if the code deviated. Record in the state file.

Audit is clean when every modeling-relevant construct traces to a decision and every registered value is what the code uses.

## Back-edges (expected, not failures)

| Trigger | Go to |
|---------|-------|
| Ledger discussion reveals a conceptual gap | Stage 1 for that concept, then resume |
| Implementation needs an unregistered parameter | Stage 2 for that item |
| Audit finds an unregistered choice | Stage 2 (or fix code to match ADR) |
| Results contradict an ADR's expectation | Stage 2: supersede or confirm the ADR — the developer decides |

Log each in the state file under `Detours`.

## Rules

- Granularity: one flow per task, not per project. A project-level first pass for global choices (data, splits, metrics) is encouraged.
- Overrides are allowed but always recorded with the developer's name.
- No commits or PRs unless asked.
- The AI never answers "which model/setting should we use?" at any stage. At most: considerations, as defined in `ml-decision-ledger`.

## Closing report (Spanish)

State of each gate, files written (understanding record, ledger/ADRs, flow state), audit result, detours, and anything left as fog.
