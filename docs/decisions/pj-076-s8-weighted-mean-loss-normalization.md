# pj-076. S8 weighted loss — weighted-mean normalization

- **Status:** accepted
- **Date:** 2026-11-16
- **Tags:** modeling | loss
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

`pj-072` adds HR weights to the networks' MSE. A mini-batch of 64 events can be summarized in two ways; PyTorch has both conventions (`CrossEntropyLoss(weight=...)` with `reduction='mean'` divides by the sum of weights; multiplying the loss by weights and calling `.mean()` divides by the batch size). In scikit-learn the trees use the weighted mean for `sample_weight`.

## Mathematical framing

With squared errors \(\ell_i\) and weights \(w_i\) (\(w\) for HR, 1 otherwise):

- **A (weighted mean):** \(L = \sum_i w_i \ell_i / \sum_i w_i\).
- **B (sum over batch size):** \(L = \sum_i w_i \ell_i / B\).

Inside a batch an HR event weighs \(w\) times a non-HR event in both. B scales the batch loss (and gradient) with the number of HR in the batch (+14% for one HR, +42% for three HR with \(w = 10\); +9.5% overall at \(w = 10\), +1% at \(w = 2\)). Both have the same minimizer on the whole data; only the training dynamics differ. On a fixed validation split they differ by a constant, so early stopping picks the same epoch.

## Options considered

1. **A — weighted mean**
2. **B — sum divided by batch size**
3. **Other / none**

## Decision

Chose **option 1 (A)** for the training loss of both networks and for the early-stopping monitor.

## Rationale (developer's own words)

A, weighted mean, for consistency with the trees.

## Checks raised

None raised beyond the dynamics difference described above.

## Expected behavior and validation

- With all weights equal to 1 the loss equals the plain MSE of iteration 1.
- Unit check: weighted-mean loss on a small batch equals \(\sum w\ell / \sum w\).

## Consequences

- Registry: S8 loss normalization = weighted mean.
- Reclassified from an `auto-trivial` engineering detail to a developer decision at the developer's request.
