# Early Collision Risk Forecasting from ESA Conjunction Data Messages

Machine Learning & Communication Skills project — BAM, IE University (2026–2027).

## Data

ESA Collision Avoidance Challenge dataset, Zenodo DOI [10.5281/zenodo.4463683](https://doi.org/10.5281/zenodo.4463683) (CC BY 4.0).
Not committed. Extract it so that this path exists:

```
data/esa/Collision Avoidance Challenge - Dataset/kelvins_competition_data/{train_data,test_data,test_data_private}.csv
```

## Reproduce preliminary results

```
python scripts/run_esa_prelim.py        # CRP/LRP metrics + proposal figures
python -m pytest scripts                # metric tests
```

## Layout

- `scripts/` — metrics, baselines, figure generation
- `.agents/skills/` — project Agent Skills (override global skills with the same name in Cursor)
- `overleaf-esa-proposal/`, `presentations/` — LaTeX deliverables
- `docs/decisions/` — decision records (ADRs); `docs/plan-reparto.md` — work plan
- `research/briefs/` — background research notes
