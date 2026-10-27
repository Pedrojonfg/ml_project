# Decision ledger

## Destination

Decisiones para **redactar/entregar** el Project Proposal: **cerradas** (016–024 + diseño 007–015). Siguiente = ejecución (Zenodo + figs CRP/LRP + LaTeX PDF).

## Notes

- Curso: Machine Learning (BAM, IE University), Prof. Nacho Molina — AY 26-27.
- Equipo: Pedro + Mario.
- **Temario a fecha proposal:** solo hasta PCA; el resto se abordará avanzando con el curso + estudio dirigido (ver 011).
- Primary: ESA Collision Avoidance (Kelvins). PHBench = reserva interna (salvo decisión en contra).
- Stack previsto: Python, scikit-learn, PyTorch · ~6 semanas · informe tipo paper + oral.
- Briefs: `research/briefs/research-brief-esa-collision-avoidance-deep.md`, `research-brief-esa-vs-phbench.md`.
- Paper local: `research/papers/uriot-etal-2020-esa-collision-avoidance.pdf`.
- Destino anterior (form de prioridades): cerrado; ADRs 001–006 conservan ese historial.

## Already decided (cited)

- Proyecto primary = ESA Collision Avoidance — source: user input 2026-10-11.
- No fusionar ESA + PHBench en un solo proyecto / dos RQs — source: `research-brief-esa-vs-phbench.md`.
- Stack / entregables del curso — source: syllabus + briefs.
- Problema base: CDMs con `time_to_tca ≥ 2` → `risk` final; HR \(= 10^{-6}\) — source: brief ESA + Kelvins.
- LRP es baseline fuerte; no liderar con accuracy; claim ≠ ganar Kelvins — source: brief ESA §1/§8.
- Instrumento de preferencias (form) — source: ADRs 001–006 / `docs/partner-priority-form-spec.md`.
- Enunciado proposal: 2 pág. texto; figuras excluidas; RQ/motivation + dataset + EDA/prelim + método/next steps; deadline 11 Oct 2026 — source: user paste / curso (ADR 012).

## Decisions

| ID | Title | Status | Gist | Link |
|----|-------|--------|------|------|
| 001 | Canal del instrumento | accepted | Form web; markdown lo convierte el usuario a posteriori | [001-canal-instrumento.md](./001-canal-instrumento.md) |
| 002 | Captura tema/dominio | accepted | Texto libre primero; luego escalas 0–10 por dominio (páginas separadas) | [002-captura-tema-dominio.md](./002-captura-tema-dominio.md) |
| 003 | Dimensiones de prioridad | accepted | 5 escalas + definición “éxito”; temáticas antes, éxito después | [003-dimensiones-prioridad.md](./003-dimensiones-prioridad.md) |
| 004 | Fuera de temario / métodos | accepted | Escala + checklist ternario + techo de compromiso; solo a priori | [004-fuera-temario-metodos.md](./004-fuera-temario-metodos.md) |
| 005 | Scope form vs cruce | accepted | Form = datos estructurados; cruce/research/decisión fuera | [005-scope-form-vs-cruce.md](./005-scope-form-vs-cruce.md) |
| 006 | Vetos y colaboración | accepted | Vetos + estilo de trabajo; sin constraints técnicos/tiempo | [006-vetos-y-colaboracion.md](./006-vetos-y-colaboracion.md) |
| 007 | RQ primaria ESA | accepted | A+B: bake-off vs LRP + uncertainty/calibración secundaria | [007-rq-primaria-esa.md](./007-rq-primaria-esa.md) |
| 008 | Diferenciador ESA | accepted | Two-stage (P(HR) cal + magnitud) + atlas de fallos en oral | [008-diferenciador-esa.md](./008-diferenciador-esa.md) |
| 009 | Criterio de éxito ESA | accepted | Éxito = protocolo + calibración + atlas; beat LRP = bonus | [009-criterio-exito-esa.md](./009-criterio-exito-esa.md) |
| 010 | Rol PyTorch ESA | accepted | Stretch/ablación justa; no claim principal asegurado | [010-rol-pytorch-esa.md](./010-rol-pytorch-esa.md) |
| 011 | Tono temario en proposal | accepted | Plan/ladder; dispuestos a avanzar; sin fingir dominio post-PCA | [011-tono-temario-proposal.md](./011-tono-temario-proposal.md) |
| 012 | Brief oficial proposal | accepted | 2 pág. texto; figuras free; RQ+data+EDA/prelim+método/next; due 11 Oct | [012-brief-proposal-curso.md](./012-brief-proposal-curso.md) |
| 013 | Idioma del proposal | accepted | Todo el Project Proposal en English (carrera en EN) | [013-idioma-proposal.md](./013-idioma-proposal.md) |
| 014 | Título + pitch | accepted | Early Collision Risk Forecasting from ESA CDMs + pitch vs LRP | [014-titulo-pitch-proposal.md](./014-titulo-pitch-proposal.md) |
| 015 | PHBench en el PDF | accepted | No mencionar backup; proposal = solo ESA | [015-phbench-fuera-del-pdf.md](./015-phbench-fuera-del-pdf.md) |
| 016 | RQ wording (PDF) | accepted | Primary vs LRP + secondary calibrated two-stage / jumps | [016-rq-wording-proposal.md](./016-rq-wording-proposal.md) |
| 017 | Preliminary results bar | accepted | EDA + CRP + LRP (+ table); simple model optional only after B | [017-preliminary-results-bar.md](./017-preliminary-results-bar.md) |
| 018 | Eval protocol prelim | accepted | CRP/LRP on official Zenodo test; truncate ≥2d; metrics F₂/MSE_HR/L | [018-eval-protocol-prelim.md](./018-eval-protocol-prelim.md) |
| 019 | Figuras del proposal | accepted | 3: risk dist. + CDM timeline + CRP/LRP metrics | [019-figuras-proposal.md](./019-figuras-proposal.md) |
| 020 | Outline 2 páginas | accepted | P1 RQ/data/EDA start; P2 EDA/prelim + method + next | [020-outline-paginas-proposal.md](./020-outline-paginas-proposal.md) |
| 021 | Methodology framing | accepted | Already/upcoming/out-of-syllabus + paper contrast → our two-stage aims | [021-methodology-framing-proposal.md](./021-methodology-framing-proposal.md) |
| 022 | Next steps granularity | accepted | 4–5 phase bullets (not full W1–W6 table) | [022-next-steps-proposal.md](./022-next-steps-proposal.md) |
| 023 | Formato de entrega | accepted | LaTeX in-repo under `presentations/proposal/` | [023-formato-entrega-proposal.md](./023-formato-entrega-proposal.md) |
| 024 | Limitations / ethics | accepted | Subsección propia corta (risk labels, no deploy, manoeuvre bias, CC BY) | [024-limitations-ethics-proposal.md](./024-limitations-ethics-proposal.md) |
| pj-001 | Event label (S1) | accepted | Both targets from last CDM: `risk_final` (log10, stored unclipped) + `y_hr = risk_final >= -6.0` | [pj-001-event-label.md](./pj-001-event-label.md) |
| pj-002 | Events without CDM >= 2 d (S1) | accepted | Excluded from train, validation and `event_table` (1212 events, 42 HR); S2 decides its own EDA use | [pj-002-events-without-usable-cdm.md](./pj-002-events-without-usable-cdm.md) |
| pj-003 | Event filter (S1) | accepted | Keep events with >=1 CDM ttc>=2 and last CDM ttc<2 (8892 events, 93 HR); Z excluded (modeling Z = fog); Y kept in train and validation | [pj-003-event-filter.md](./pj-003-event-filter.md) |
| pj-004 | CV scheme (S1) | accepted | 5-fold, stratified on `y_hr`, shuffled, event-level | [pj-004-cv-scheme.md](./pj-004-cv-scheme.md) |
| pj-005 | Repetition and seeds (S1) | accepted | Repeated CV, R=5, seeds 42-46 | [pj-005-repetition-seeds.md](./pj-005-repetition-seeds.md) |
| pj-006 | Uncertainty reporting (S1) | accepted | Event bootstrap, B=10000, 95 % BCa, joint resampling (no bounds), per-repetition metrics averaged, paired diff vs LRP and CRP, repetition spread supplementary | [pj-006-uncertainty-reporting.md](./pj-006-uncertainty-reporting.md) |
| pj-007 | Metrics reporting (S1) | accepted | F2, MSE_HR, L; MSE_HR and L both clipped (-6.001) and unclipped | [pj-007-metrics-reporting.md](./pj-007-metrics-reporting.md) |
| pj-008 | Feature set delivery | accepted | v1 only; no separate stub phase for S4/S6 | [pj-008-feature-set-no-stub.md](./pj-008-feature-set-no-stub.md) |
| pj-009 | Event features v1 | accepted | Quantile + first/last snapshots; A1–A3 on risk; 3 geometry fields; event_table metadata | [pj-009-event-features-v1.md](./pj-009-event-features-v1.md) |
| pj-010 | Missing values (S3) | accepted | `std(risk)` = 0 if one usable CDM; else NaNs left to S4 per-fold imputation | [pj-010-missing-feature-values.md](./pj-010-missing-feature-values.md) |
| pj-011 | Categorical features v1 | accepted | No `mission_id`; one-hot `c_object_type` (5 levels) in S3, last usable CDM | [pj-011-categorical-features.md](./pj-011-categorical-features.md) |
| pj-012 | Explicit delta columns | accepted | None in v1 (first/last snapshots only) | [pj-012-explicit-deltas.md](./pj-012-explicit-deltas.md) |
| pj-013 | Feature contract doc | accepted | `FEATURE_COLUMNS` in code + `docs/contracts.md`, kept in sync; tests enforce match | [pj-013-feature-contract-doc.md](./pj-013-feature-contract-doc.md) |
| pj-014 | S5 tree regression target | accepted | Regress `risk_final`; continuous log10 `predict`; metrics as LRP | [pj-014-s5-tree-regression-target.md](./pj-014-s5-tree-regression-target.md) |
| pj-015 | S5 missing-value handling | accepted | Per-fold median `SimpleImputer`; shared pipeline for RF and GBDT | [pj-015-s5-missing-imputation.md](./pj-015-s5-missing-imputation.md) |
| pj-016 | S5 RF fixed hyperparameters | accepted | depth 4, min_samples_split 4, leaf 2, sqrt features, bootstrap, state 42+rep | [pj-016-s5-rf-hyperparameters.md](./pj-016-s5-rf-hyperparameters.md) |
| pj-017 | S5 GBDT (`GradientBoostingRegressor`) | accepted | n_estimators 200, lr 0.1, parallel constraints; no n_estimators grid at launch | [pj-017-s5-gbdt-hyperparameters.md](./pj-017-s5-gbdt-hyperparameters.md) |
| pj-018 | S5 RF `n_estimators` search | accepted | Grid {100,300,500}; pick lowest mean unclipped L over OOF CV | [pj-018-s5-rf-n-estimators-search.md](./pj-018-s5-rf-n-estimators-search.md) |
| pj-019 | S5 feature importances | accepted | Both models; impurity; mean over 25 folds; top 10 plot; mandatory B1/B3 gates | [pj-019-s5-feature-importances.md](./pj-019-s5-feature-importances.md) |
| pj-020 | S5 artifacts and `p_hr` | accepted | slugs `rf`/`gbdt`; `p_hr` = hard threshold on `r_hat`; imputer flags | [pj-020-s5-artifacts-and-p-hr.md](./pj-020-s5-artifacts-and-p-hr.md) |
| pj-021 | S5 run 0 retrospective | accepted | Fast runtime; RF F₂=0; GBDT weak vs LRP; B1 reopen; findings only | [pj-021-s5-run0-retrospective.md](./pj-021-s5-run0-retrospective.md) |
| — | No-replay Kelvins | auto-trivial | Dataset + RQ similar; claim = estudio/eval, no leaderboard 2019 | — |
| — | HR threshold in prose | auto-trivial | State \(10^{-6}\) once as competition/notification-style high-risk cut | — |
| — | Authors line | auto-trivial | Pedro + Mario (expand full names at write time if required by IE) | — |
| — | PHBench reserva | auto-trivial | Sigue en briefs/ledger interno; fuera del submission (015) | — |
| — | Figuras vs page count | auto-trivial | Figuras no cuentan; 3 plots locked in 019 (was “1–2” preview) | — |
| — | Magnitud = valor de risk | auto-trivial | No energía de impacto; es el número de riesgo operacional (Pc/risk) del CDM final | — |
| — | Citas y datos en proposal | auto-trivial | Zenodo DOI 10.5281/zenodo.4463683 + arXiv:2008.03069; CC BY 4.0 | — |
| — | Protocolo mínimo de splits | auto-trivial | Unidad = `event_id`; sin features con `time_to_tca < 2` | — |
| — | Dashboard de métricas | auto-trivial | \(F_2\), MSE_HR, \(L\); + PR-AUC / calibración; no accuracy headline | — |
| — | Ética / limitaciones base | auto-trivial | Anonimizado; no mando en vivo; sesgo por maniobras excluidas | — |
| — | Idioma del formulario (histórico) | auto-trivial | Español + términos técnicos en inglés cuando haga falta | — |

## Parameter registry

Every modeling parameter the implementation needs. Library defaults must be listed explicitly; an unlisted default is an undecided parameter.

| Parameter | Value | ADR |
|-----------|-------|-----|
| HR threshold (log10 risk) | -6.0 | pj-001 |
| Event label | `risk_final` = `risk` of CDM with min `time_to_tca` | pj-001 |
| Stored continuous target | unclipped | pj-001 |
| Metric reporting | F2, MSE_HR, L; MSE_HR and L clipped (-6.001) and unclipped | pj-007 |
| Number of folds K | 5, stratified on `y_hr`, shuffled | pj-004 |
| Random seeds (fold assignment) | 42, 43, 44, 45, 46 (R = 5 repetitions) | pj-005 |
| Train/validation event filter | >=1 CDM ttc>=2 and last CDM ttc<2 (Y included) | pj-003 |
| Events with no CDM >= 2 d | excluded from train/val/`event_table` | pj-002 |
| Bootstrap resamples B | 10000 | pj-006 |
| Interval level / method | 95 %, BCa | pj-006 |
| Bootstrap resampling | events jointly, with replacement, no bounds on HR count | pj-006 |
| Aggregation over repetitions | average per-repetition metrics | pj-006 |
| Paired baselines | LRP and CRP | pj-006 |
| Usable CDM cutoff (features) | `time_to_tca >= 2` | pj-002, pj-003 |
| Snapshot quantiles (`time_to_tca` within usable) | 25, 50, 75 | pj-009 |
| Snapshot + aggregate variables | `risk`, `miss_distance`, `relative_speed`, `t_weighted_rms`; A1–A3 on `risk`; `n_cdm`, `first_ttc`, `last_ttc` | pj-009 |
| Single usable CDM (snapshots) | repeat same row value per variable | pj-009 |
| Explicit `lrp` feature column | omitted (last usable `risk` snapshot only) | pj-009 |
| `std(risk)` when `n_usable_cdms == 1` | 0 | pj-010 |
| Other feature NaNs in S3 | pass through; imputation in S4+ per fold | pj-010 |
| `mission_id` in v1 `X` | excluded | pj-011 |
| `c_object_type` encoding | one-hot in S3: DEBRIS, UNKNOWN, PAYLOAD, ROCKET BODY, TBA | pj-011 |
| `c_object_type` source row | last usable CDM per event | pj-011 |
| Unseen `c_object_type` at inference | all type dummies 0 | pj-011 |
| S5 training target | `risk_final` (unclipped log10) | pj-014 |
| S5 model output (`predict`) | continuous log10 risk per event | pj-014 |
| S5 Kelvins metrics | F2, MSE_HR, L from continuous predictions via `metrics.py` (same as LRP) | pj-014, pj-007 |
| S5 imputation | `SimpleImputer`, strategy `median`, fit on train fold only | pj-015 |
| S5 imputation scope | applied to all `FEATURE_COLUMNS` before both tree models | pj-015 |
| S5 imputation / booster revisit | material NaNs or GBR too slow → reopen pj-015 **with** pj-017 (HGBT + optional split pipeline) | pj-015 |
| S5 RF `max_depth` | 4 | pj-016 |
| S5 RF `min_samples_split` | 4 | pj-016 |
| S5 RF `min_samples_leaf` | 2 | pj-016 |
| S5 RF `max_features` | sqrt | pj-016 |
| S5 RF `bootstrap` | True | pj-016 |
| S5 RF `max_samples` | None | pj-016 |
| S5 RF `criterion` | squared_error | pj-016 |
| S5 RF `random_state` | 42 + repetition_index (0…4) | pj-016 |
| S5 RF `n_jobs` | -1 | pj-016 |
| S5 RF `n_estimators` | search {100, 300, 500}; select min mean unclipped L (OOF); tie → smaller | pj-018 |
| S5 GBDT estimator | GradientBoostingRegressor | pj-017 |
| S5 GBDT `n_estimators` | 200 (fixed at launch) | pj-017 |
| S5 GBDT `learning_rate` | 0.1 | pj-017 |
| S5 GBDT `max_depth` | 4 | pj-017 |
| S5 GBDT `min_samples_split` | 4 | pj-017 |
| S5 GBDT `min_samples_leaf` | 2 | pj-017 |
| S5 GBDT `subsample` | 1.0 | pj-017 |
| S5 GBDT `max_features` | sqrt | pj-017 |
| S5 GBDT `loss` | squared_error | pj-017 |
| S5 GBDT `random_state` | 42 + repetition_index (0…4) | pj-017 |
| S5 importance method | impurity `feature_importances_` (not permutation at launch) | pj-019 |
| S5 importance aggregation | mean over 25 CV train fits (5 folds × 5 reps) | pj-019 |
| S5 importance models | RF (pj-018 `n_estimators`) + GBDT | pj-019 |
| S5 importance plot default | top 10; ranks 11–15 if mean importance ≥ 0.95 × rank-10 | pj-019 |
| S5 dimensionality reduction | none (no PCA on v1 `X` for trees) | pj-019 |
| S5 importance mandatory checks | B1 permutation vs impurity top-5 (fold 0, rep 0); B3 RF vs GBDT rank-1 family; auto `reopen_required` | pj-019 |
| S5 importance manual revisit | B2 geometry invisible; B4 remove-feature / causal claims | pj-019 |
| S5 results paths | `results/rf.json`, `results/gbdt.json` | pj-020 |
| S5 preds paths | `preds/rf.parquet`, `preds/gbdt.parquet` | pj-020 |
| S5 `r_hat` | continuous log10 `predict` | pj-020, pj-014 |
| S5 `p_hr` | 1.0 if `r_hat >= -6.0` else 0.0 (not calibrated) | pj-020, pj-001 |
| S5 `SimpleImputer` `add_indicator` | False | pj-020 |
| S5 `SimpleImputer` `keep_empty_features` | False | pj-020 |

## Fog (not yet sharp)

- **S5 iteration 2 — objective for tuning:** optimize F₂, L clipped, or composite when F₂≈0? (run 0: pj-018 picked `n_estimators` via L unclipped while RF F₂=0 for all grid values — pj-021).
- **S5 iteration 2 — imbalance / tail:** sample weights on `y_hr`, asymmetric loss, deeper/weaker regularization, or separate HR detector + magnitude (overlap with S6).
- **S5 iteration 2 — RF hyperparameter grid expansion** now that compute ≈3.5 min/run (pj-021): depth, `min_samples_*`, larger `n_estimators` grid, optional `criterion`.
- **S5 pj-019 reopen:** permutation importances or grouped risk features after B1 RF fail (pj-021).
- **S5 pj-006 bootstrap:** wire trees into `evaluation.py` when it exists (quality-first per pj-021).
- Rúbrica interna exacta del profe para el project (syllabus describe entregables, no desglose de puntos).
- Papel empírico final de cada familia de modelos (lineal / trees / NN) — se resolverá al implementar; el proposal no lo congela (011).
- Nombres legales / affiliation exactos en el header del PDF (IE formatting).

- Modeling events whose last CDM has `time_to_tca >= 2` (type Z; label CDM is also an input) — needs a different task definition (pj-003).

## Out of scope

- Reparto de roles Pedro / Mario en el proposal (no lo pide el enunciado; confirmado usuario).
- Paper final, slides de oral, implementación completa del bake-off.
- Reabrir o rediseñar el form de prioridades (001–006).
- Co-proyecto ESA + PHBench.
- Decidir de nuevo RQ/ángulo/dataset (007–015); este pase solo submission packing (016–024).
