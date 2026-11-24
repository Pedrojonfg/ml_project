# Early Collision Risk Forecasting from ESA Conjunction Data Messages

Machine Learning & Communication Skills project — BAM, IE University (2026–2027).

## Data

ESA Collision Avoidance Challenge dataset, Zenodo DOI [10.5281/zenodo.4463683](https://doi.org/10.5281/zenodo.4463683) (CC BY 4.0).
Not committed. Extract it so that this path exists:

```
data/esa/Collision Avoidance Challenge - Dataset/kelvins_competition_data/{train_data,test_data,test_data_private}.csv
```

## Setup

```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# CPU torch wheel if needed:
# pip install torch==2.15.0 --index-url https://download.pytorch.org/whl/cpu
```

## Reproduce

```
python -m pytest tests                  # unit tests
python scripts/regen_tables.py          # rebuild markdown tables from results/ (no retrain)
```

Bake-off OOF (long; writes `results/*.json` and `preds/*.parquet`):

```
python scripts/run_s1_protocol.py
python scripts/run_s2_eda.py
python scripts/run_s4_linear.py
python scripts/run_s5_trees.py
python scripts/run_s6_two_stage.py
python scripts/run_s7_atlas.py
python scripts/run_s8.py
python scripts/run_s9.py
```

Official test **once**, models frozen (pj-081..pj-084); caches under `results/official/`:

```
PYTHONPATH=. python scripts/run_official_test.py          # all slugs
PYTHONPATH=. python scripts/run_official_test.py CRP LRP  # baselines only
```

Proposal prelim CRP/LRP figures:

```
python scripts/run_esa_prelim.py
```

## Reporting splits (pj-085)

- **Internal OOF** — event-level CV on the `pj-003` train cohort (`results/*.json`, e.g. `results/s4_table.md`).
- **Official test** — one-shot hold-out (`results/official/`, `results/official_table.md` after regen). Do not merge the two tables without labeling the split.

## Layout

- `src/` — protocol, features, models, official-test helpers
- `scripts/` — bake-off runners, `regen_tables.py`, `run_official_test.py`
- `results/`, `preds/` — metrics and OOF predictions
- `docs/decisions/` — ADRs; `docs/plan-reparto.md` — work plan
- `docs/ai-declaration.md` — contributions and AI use (S11)
- `report/references.bib` — MLA/BibTeX bibliography for the Final Report
- `presentations/` — LaTeX deliverables (proposal, progress report)

## AI declaration

See [`docs/ai-declaration.md`](docs/ai-declaration.md).
