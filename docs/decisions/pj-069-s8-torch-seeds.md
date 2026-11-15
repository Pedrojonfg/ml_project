# pj-069. S8 PyTorch seeding — one seed per CV repetition

- **Status:** accepted
- **Date:** 2026-11-15
- **Tags:** modeling | reproducibility
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

S1 uses R=5 repetitions with seeds 42–46 (`pj-005`). S8 training adds PyTorch weight init, dropout (if any), DataLoader shuffle, and the inner 80/20 split (`pj-066`).

## Mathematical framing

For repetition index `r` with protocol seed `s_r ∈ {42,43,44,45,46}`, all S8 RNGs for that repetition (Python `random`, NumPy, `torch`, CUDA if used, and the inner split) are seeded from `s_r` (and fold index may further offset the inner split as in `pj-066`). Bit-exact GPU determinism is not required.

## Options considered

1. One seed per CV repetition (pj-005 values); seeded but not strict CUDA determinism.
2. Single global seed for all reps.
3. Strict `cudnn.deterministic` / deterministic algorithms everywhere.
4. Other / none.

## Decision

Chose **option 1**.

## Rationale (developer's own words)

One seed per repetition, and no need to chase stricter determinism as long as it is seeded.

## Checks raised

- Non-deterministic GPU kernels may still cause tiny run-to-run diffs — accepted.
- Inner-split seeding must remain tied to fold/rep (`pj-066`).

## Expected behavior and validation

- Re-running the same repetition with the same code/data yields closely reproducible metrics; exact bitwise equality on GPU is not a gate.

## Consequences

- Registry: S8 torch seed = CV repetition seed from `pj-005`; strict determinism = no.
