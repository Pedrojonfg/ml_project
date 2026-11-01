# mf-015. Seed of the inner split for alpha selection (S4)

- **Status:** accepted
- **Date:** 2026-11-01
- **Tags:** modeling | reproducibility
- **Decided by:** Mario
- **AI involvement:** options + critique

## Context

mf-013 selects alpha by a stratified inner 5-fold CV inside each outer training fold; mf-014 shows the solvers are deterministic, so the inner split is the only random element left in S4. pj-005 fixes the outer seeds (42..46).

## Mathematical framing

The inner partition decides which events (about 59 training and 15 validation HR per inner fold) are used for the AP criterion, so it can change the selected alpha. A fixed seed makes the choice reproducible but the result is one realisation of the partition.

## Options considered

1. **Fixed seed, same for all outer folds and repetitions.**
2. **Seed varying with outer fold and repetition** (for example derived from the outer seed).
3. **No shuffle** (partition by event order).

## Decision

Chose **option 1**: `StratifiedKFold(n_splits=5, shuffle=True, random_state=0)` for the inner split of every outer training fold, in every repetition.

## Rationale (developer's own words)

Fixed seed 0 with shuffle, different from the outer seeds (42-46) to avoid coincidences between partitions. The same for all because the variability already comes from the outer fold; changing the inner seed would add a source of noise that cannot be isolated from the selection of alpha.

## Checks raised

- Each outer training fold has different events, so the 25 inner partitions differ even with the same seed. The seed is not shared data between partitions.
- A fixed seed hides the variability of alpha selection across inner partitions; it does not remove it. The effect was not measured.
- The outer and the inner splits act on datasets of different size, so equal seeds would not have produced equal partitions in any case.

## Expected behavior and validation

Re-running with the same outer seeds gives identical selected alphas.

## Consequences

- No other source of randomness in S4 (OLS, Ridge cholesky and Lasso cyclic are deterministic).
- Not doing: varying inner seeds, repeated inner CV.
