# pj-013. Feature contract documentation (dual)

- **Status:** accepted
- **Date:** 2026-10-27
- **Tags:** engineering | data
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

R1 in `plan-reparto.md` anticipated `docs/contracts.md` for parallel work. pj-009 requires stable column names for S4/S6. Implementation will expose columns in code (`src/features.py`).

## Options considered

1. **Code only** (`FEATURE_COLUMNS` + docstring).
2. **Markdown only** (`docs/contracts.md`).
3. **Both** code and markdown, kept in sync when the schema changes.
4. **Markdown as sole source** read by code.

## Decision

Chose **option 3**: maintain **both**:

- `src/features.py`: authoritative list (e.g. `FEATURE_COLUMNS`) and `build_features` output matching it.
- `docs/contracts.md`: human-readable schema (column names, brief semantics, dtypes) for partners and the report.

Updates to v1 features must change **both** in the same change set; tests should assert `build_features` columns match `FEATURE_COLUMNS` (and optionally that `contracts.md` lists the same set).

## Rationale (developer's own words)

Use both because keeping them aligned should not be a problem with agent-assisted development.

## Checks raised

- Dual sources can drift without tests → mitigated by column-equality tests in `tests/test_features.py`.
- `contracts.md` did not exist yet → created when S3 is implemented.

## Consequences

- First S3 implementation adds/updates `docs/contracts.md`.
- Future schema changes require ledger ADR if modeling-related, plus sync of code and contract doc.
