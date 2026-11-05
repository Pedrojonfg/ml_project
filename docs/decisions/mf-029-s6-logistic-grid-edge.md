# mf-029. Grid-edge treatment of the logistic strength in S6

- **Status:** accepted
- **Date:** 2026-11-04
- **Tags:** modeling
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

mf-026 fixes the C grids; mf-027 selects C with the one standard error rule, choosing the smallest C of the tie set. For the S4 regressors the grids are fixed without extension and an optimum at the edge is information, not something to resolve automatically (mf-013).

## Mathematical framing

An optimum at a grid edge may mean the best value lies outside the grid. With mf-027 there are two values: C* (highest mean AUC) and the selected C (smallest C of the tie set); the edge is checked on the selected C.

## Options considered

1. **Same as S4** — fixed grids, no automatic extension; an edge optimum is reported and the developer decides what to do.
2. **Automatic extension of the grid** — the code widens the grid until the optimum is interior; the final grid depends on the data.

## Decision

Chose **same as S4**: the grids are fixed. For every outer training fold, repetition and penalty, the code flags a selected C located at an edge of its grid, stores the flag and does not extend the grid.

## Rationale (developer's own words)

If the optimum falls on the edge, I decide manually what to do instead of the code extending the grid on its own.

## Checks raised

- C* at an edge with an interior selected C is not flagged under this definition, so that edge information is lost unless C* is also stored (mf-027 already stores C*).
- With mf-027 choosing the smallest C of the tie set, the lower edge may be hit more often than with a plain argmax.

## Expected behavior and validation

Results store, per fold, repetition and penalty: selected C, its grid position and the edge flag.

## Consequences

- Still to decide: solver and library parameters of the logistic models.
