# pj-066. S8 training — Adam, batch 64, early stopping

- **Status:** accepted
- **Date:** 2026-11-15
- **Tags:** modeling | hyperparameters | optimization
- **Decided by:** Pedro
- **AI involvement:** opinion requested (max epochs and patience)

## Context

Both S8 arms (MLP and masked GRU; `pj-064`) train under the S1 fold protocol after fold-fit impute+scale (`pj-065`). Optimizer, loop length, and early-stopping must be explicit so PyTorch defaults are not silent decisions.

## Mathematical framing

Parameters \(\theta\) are updated with Adam on mini-batches of the fold training set (minus an inner hold-out). Early stopping monitors regression loss / MSE on the inner validation split and restores the best \(\theta\) before emitting OOF `r_hat` on the official CV validation fold. The official CV validation fold is never used to stop or select weights within that fold.

## Options considered

1. **Package A:** Adam `lr=1e-3`, `weight_decay=0`, batch 64, max 50 epochs, patience 10, ~20% inner val, same recipe both arms.
2. **Package B:** max 100 epochs, patience 10 (same otherwise).
3. **Package C:** max 50 epochs, patience 5 (same otherwise).
4. **Other / none**

## Decision

Chose **package A**, including registered Adam `betas=(0.9, 0.999)` and `eps=1e-8`, inner validation fraction `0.20`, and a shuffled inner split with seed tied to fold/repetition (S1 seed spirit).

Same training recipe for tabular MLP and sequence GRU.

## Rationale (developer's own words)

Adam with \(10^{-3}\) (adaptive, so a small miss is OK); batch 64; early stopping yes; same recipe for both models unless there is a strong reason; no weight decay for the first Adam pass (keep it simple). Max epochs 50 and patience 10 from option A after opinion was requested.

## Checks raised

- Inner-val F₂ would be very noisy with ~1% HR — monitor is regression loss/MSE, not F₂.
- Adam hyperparameters beyond `lr` / `weight_decay` must be listed — `betas` and `eps` recorded as above.
- Network sizes (MLP width/depth, GRU hidden size, dropout) remain open.

## Expected behavior and validation

- Each fold train: split ~80/20 train/inner-val; fit imputer/scaler on the 80% only (or on full fold train before split — **must not** use official CV val; prefer fit on the early-stopping train subset only to avoid inner leakage into scaling — implementation must pick one and document; statistics must not use the official CV validation fold).
- Stop when inner-val loss does not improve for 10 epochs, or at epoch 50; restore best checkpoint.
- Identical optimizer/loop settings for both arms.

## Consequences

- Parameter registry lists the training knobs below.
- Architecture size, class imbalance / floor `c`, torch seeding, and bake-off row identity need further ADRs.
