# Flow: S10 — Kernel ridge (syllabus sessions 19-21)
- Owner: Mario
- Source: docs/plan-reparto.md (S10, optional `~`): kernel ridge as one extra row in the S4 table; depends on S3 (features). Reuses S4 protocol (event folds, bootstrap in src/evaluation.py).
- Split: all modeling (kernel, kernel parameters, regularization, selection, preprocessing, alarm line) -> full flow. Table row = plumbing.
- ID note: mf-021..mf-043 are taken (S6 and KNN); S10 decisions were renumbered from mf-043..mf-052 to mf-044..mf-053 on merge into main.
- Understanding: READY (2026-11-15) — docs/understanding/mf.md, section "S10: kernel ridge (RBF)"; all concepts solid (memorizing model vs alarm line raised from shaky to solid, 2026-11-15, after questions 12-13); open questions carried to the ADR (kernel family, gamma parametrization, no intercept in KernelRidge, diagonal self-weight for the alarm line)
- Decisions: complete (2026-11-15) — mf-044..mf-053 accepted; no blocking deferred-fog. Ledger: docs/decisions/LEDGER.md
- Implementation: code done (2026-11-15) — src/models/kernel_ridge.py (agents: tests by sonnet, module by fable), dispatch + reps subset + extra fold_records in src/models/linear.py, scripts/run_s4_linear.py, scripts/make_s4_table.py, tests/test_kernel_ridge.py (22 tests, 75 passing with linear/knn/evaluation); full run done 2026-11-15 (results/kernel_ridge.json, results/s4_table.md); preds/kernel_ridge.parquet NOT saved (pyarrow missing)
- Audit: clean on code (2026-11-15) — every modeling construct traces to mf-044..mf-053; only unregistered item `eigh UPLO="L"` (numpy default) added to the registry
- Detours: none in the flow. Run note: the first full run ended without preds/kernel_ridge.parquet because pyarrow is not installed in this environment nor listed in requirements.txt.
