# Flow: S2 — Deep EDA + jump taxonomy
- Owner: Mario
- Source: docs/plan-reparto.md (S2, Phase 0); jump definition is a contract at R1 (docs/dependencias-y-reuniones.md)
- Split: EDA figures (missions, imbalance) = plumbing -> /implementa, no gates. Jump definition (threshold in log10, window, stable-low/high rule) = modeling -> full flow.
- Understanding: READY (2026-10-31) — docs/understanding/mf.md
- Decisions: complete (2026-11-01) — mf-001..mf-006 accepted; deferred-fog (non-blocking): lead-time and latest_risk bin edges. Ledger: docs/decisions/LEDGER.md
- Implementation: done (2026-11-01) — src/taxonomy.py, src/eda/figures.py, scripts/run_s2_eda.py, tests/test_taxonomy.py, tests/test_eda_figures.py; outputs in results/eda/
- Audit: clean except one open item (2026-11-01) — every modeling construct traces to mf-001..mf-006 / pj-001..003; resolved: (1) CUTS (0.5, 1.0, 2.0) in scripts/run_s2_eda.py registered as EDA-only sensitivity values (Mario, 2026-11-01); open: (2) test split not labeled yet (mf-001: inspected only at R5)
- Detours:
