# pj-008. Single feature set (no stub phase)

- **Status:** accepted
- **Date:** 2026-10-27
- **Tags:** engineering | data | modeling
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

`plan-reparto.md` describes a stub feature set (`lrp` plus a few columns) so S4/S6 can start before S3 v1. Mario had not started downstream scopes; Pedro owns S3 and S5 and will deliver features before parallel model work.

## Options considered

1. **Stub then v1** — minimal column list first, full engineering later.
2. **v1 only from the first `build_features` commit** — one column contract; no separate stub.
3. **Stub as a prefix of v1 column names** — same contract, subset of columns populated early.

## Decision

Chose option 2: **v1 only**. No stub phase or stub column list for S4/S6.

## Rationale (developer's own words)

Mario has not started yet; Pedro will deliver S3 and S5 soon. A dedicated stub would duplicate work without unblocking a partner.

## Checks raised

- When Mario starts S4/S6, he must read v1 column names from `src/features.py` (and any contract doc); no interim stub document.
- `plan-reparto.md` stub wording is superseded for this execution cycle; S1 protocol unchanged.

## Consequences

- The first merged `build_features` defines the official `X` schema for all models.
- Feature-scope ADRs (pj-009+) must be complete before implementation per `/ml-flow`.
