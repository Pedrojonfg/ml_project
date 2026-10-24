# pj-004. Cross-validation scheme

- **Status:** accepted
- **Date:** 2026-10-24
- **Tags:** modeling | evaluation
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

After pj-003 the dataset has 8892 events and 93 HR (1.05 %). `event_table` has one row per event, so splitting rows splits by `event_id` and no CDMs of one event cross folds.

## Mathematical framing

K-fold over events: train on (K-1)/K of events, validate on 1/K. With K = 5 and 93 HR: ~74 HR in training and ~19 in each validation fold. Stratification on `y_hr` keeps the HR proportion near 1.05 % in every fold.

## Options considered

1. **K = 3** — ~31 HR per validation fold, ~62 HR to train; more pessimistic bias.
2. **K = 5** — ~19 HR per validation fold, ~74 to train.
3. **K = 10** — ~9 HR per validation fold, ~84 to train; noisier folds, more compute.

Stratified on `y_hr` or not.

## Decision

Chose **K = 5**, stratified on `y_hr`, shuffled, split at event level.

## Rationale (developer's own words)

Five folds is a good middle point. Stratify so that every fold keeps a similar share of HR, since there are only 93 HR.

## Checks raised

- Stratification is on `y_hr` only; mission mix is not balanced across folds → recorded as a limitation (the paper warns mission imbalance matters).
- Unstratified splits would leave some folds with very few HR (earlier simulation: 15 % chance of a fold with < 8 HR for 66 HR).

## Expected behavior and validation

Each validation fold has 18 or 19 HR; no `event_id` appears in two folds.

## Consequences

- Fold assignment is produced once in S1 and stored; other scopes consume it.
- Not doing: stratifying by mission.
