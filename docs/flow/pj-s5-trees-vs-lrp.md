# Flow: S5 trees vs LRP
- Owner: Pedro
- Understanding: READY (2026-10-27); floor-c concepts added 2026-10-28
- Decisions: in progress (2026-10-28) — pj-014..020, pj-022, pj-024..026; ledger: docs/decisions/LEDGER.md
- Implementation: done for pj-014..020, pj-024, pj-025; pending for pj-026
- Audit: findings — OOF predictions overwritten across repetitions (metrics were last repetition only, contradicting pj-006); code fixed 2026-10-28, results need a rerun
- Detours:
  - 2026-10-27: results contradicted expectations (RF F₂ = 0) → Stage 2: pj-022 (selection metric), pj-024 (relaxed regularization)
  - 2026-10-28: run 1 still RF F₂ = 0; diagnosis = −30 floor dominates leaf means → Stage 2: pj-025 (unclipped selection), pj-026 (training-target floor c)
