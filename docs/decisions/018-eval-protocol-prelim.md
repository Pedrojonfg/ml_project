# 018. Evaluation protocol for proposal prelim (CRP/LRP)

- **Status:** accepted
- **Date:** 2026-10-11
- **Tags:** tech | research
- **Decided by:** human

## Context

Prelim bar is EDA + CRP + LRP (017). Need a split that is scientifically honest and, preferably, comparable to Uriot et al. User clarified A ≠ “train without holdout”.

## Options considered

1. **A** — Official Zenodo/competition **test** events; features only with `time_to_tca ≥ 2`; target = final CDM risk; report \(F_2\), \(\mathrm{MSE}_{HR}\), \(L\) (contrast paper \(L_{\mathrm{LRP}}\approx 0.694\)).
2. **B** — Random event holdout inside **train** only.
3. **C** — A + B.
4. **D** — Score on the whole dataset with no proper split.

## Decision

Chose **A**.

## Why

User selected A after correcting the misconception that A was train-without-holdout. Baselines do not fit parameters, so using the official test is appropriate and paper-comparable.

## Consequences

- Implementation must identify test `event_id`s, drop CDMs with `time_to_tca < 2` from inputs, define LRP/CRP per challenge/paper, compute metrics on test.
- Do not present train-only scores as the headline prelim result.
- Train remains for EDA counts and later model fitting (post-proposal).
