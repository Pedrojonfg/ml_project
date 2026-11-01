# Flow: S4 — Syllabus models vs LRP
- Owner: Mario
- Source: docs/plan-reparto.md (S4): logistic (HR) + ridge/lasso (magnitude) [+ KNN] on event folds; table vs LRP; bootstrap in src/evaluation.py. Depends on S1 (protocol), S3 (features).
- Split: all modeling (model choice, regularization, thresholds, bootstrap) -> full flow. Table/plot formatting = plumbing.
- Understanding: skipped by Mario (2026-11-01) — docs/understanding/mf.md; only gaussian-MLE and Bernoulli likelihood partially checked (both shaky); KNN deferred
- Decisions: complete (2026-11-01) — mf-007..mf-017 accepted (mf-008 reopened and confirmed); logistic models kept for S6; no blocking deferred-fog. Ledger: docs/decisions/LEDGER.md
- Implementation: pending
- Audit: pending
- Detours: 2026-11-01 — decision 6 evidence (r_hat never reaches -6 without a floor; floor c in [-25,-7] gives F2 = 0 and c = -6.09 compresses r_hat to 0.1) reopened mf-008; confirmed without floor. Alarm line moved to its own ADR (mf-012).
