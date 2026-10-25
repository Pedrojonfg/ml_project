# Flow: S1 event protocol
- Owner: Pedro
- Understanding: READY (2026-10-24)
- Decisions: complete (2026-10-24) — ledger: docs/decisions/LEDGER.md (pj-001..007)
- Implementation: done (2026-10-24) — src/protocol.py, tests/test_protocol.py, scripts/run_s1_protocol.py, results/s1_baselines.json; 37 tests pass
- Audit: findings (2026-10-24) — constructs matching the ledger: seeds, n_splits, shuffle, stratification, HR threshold, clip values, event filter. Unregistered inherited values: F2 beta = 2, CRP constant = -5.0 (both from Uriot et al., fixed in src/metrics.py), tie rule for equal minimum time_to_tca (no ties in the data). Pending developer decision.
- Detours: none
