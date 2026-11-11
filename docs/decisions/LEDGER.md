# Decision ledger

## Destination

Project Proposal: **cerradas** (016–024). Ejecución S1–S5 + S4 code en `main`. **W1 Progress Report:** decisiones pj-033..pj-043 **accepted**; borrador en `presentations/progress-report/`. Pendiente C2: reabrir pj-019 (B1) y pj-026 (R4, RF).

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
| pj-018 | S5 RF `n_estimators` search | accepted | Grid {100,300,500}; selection rule → pj-022 | [pj-018-s5-rf-n-estimators-search.md](./pj-018-s5-rf-n-estimators-search.md) |
| pj-022 | S5 tuning selection metric | superseded by pj-025 | Hyperparameter pick: lowest mean **L clipped** OOF (pj-007 clip); report both L still | [pj-022-s5-tuning-select-l-clipped.md](./pj-022-s5-tuning-select-l-clipped.md) |
| pj-025 | S5 tuning selection metric (v2) | accepted | Supersedes pj-022: select by lowest pooled OOF **unclipped** L; report both (pj-007) | [pj-025-s5-tuning-select-l-unclipped.md](./pj-025-s5-tuning-select-l-unclipped.md) |
| pj-026 | S5 training-target floor c | accepted | Fit on max(risk_final, c); c per training fold from F₂-optimal threshold p* = F*/5, F* = LRP F₂; revoke via R0–R4 | [pj-026-s5-training-target-floor-c.md](./pj-026-s5-training-target-floor-c.md) |
| pj-024 | S5 relaxed trees + estimator grids | accepted | depth 8, split 2, leaf 1; n_estimators {300,500,1000} RF+GBDT; select L clipped | [pj-024-s5-relaxed-tree-hyperparameters.md](./pj-024-s5-relaxed-tree-hyperparameters.md) |
| pj-019 | S5 feature importances | accepted | Both models; impurity; mean over 25 folds; top 10 plot; mandatory B1/B3 gates | [pj-019-s5-feature-importances.md](./pj-019-s5-feature-importances.md) |
| pj-020 | S5 artifacts and `p_hr` | accepted | slugs `rf`/`gbdt`; `p_hr` = hard threshold on `r_hat`; imputer flags | [pj-020-s5-artifacts-and-p-hr.md](./pj-020-s5-artifacts-and-p-hr.md) |
| mf-001 | Purpose and scope of jump taxonomy | accepted | Analysis/reporting only (never X, target or weights); computed on train and official test; test labels only inspected, not used for modeling before R5. Decided by Mario | [mf-001-purpose-scope.md](./mf-001-purpose-scope.md) |
| mf-002 | What defines a jump | accepted | Size of Δ only; crossing of −6 kept as a separate analysis-only column (up/down/none). Decided by Mario | [mf-002-jump-by-size.md](./mf-002-jump-by-size.md) |
| mf-003 | Jump cut | accepted | c = 1, symmetric (Δ ≥ 1 up, Δ ≤ −1 down), limit included. Decided by Mario | [mf-003-jump-cut.md](./mf-003-jump-cut.md) |
| mf-004 | stable-low / stable-high rule | accepted | For non-jump events (−1 < Δ < 1): stable-high iff y_final ≥ −6, else stable-low (−6 exact is stable-high). Decided by Mario | [mf-004-stable-rule.md](./mf-004-stable-rule.md) |
| mf-005 | Lead time of the last valid CDM | accepted | Single cut kept (mf-003); lead time recorded as an analysis-only column for grouping tables; bin edges deferred to EDA. Decided by Mario | [mf-005-lead-time.md](./mf-005-lead-time.md) |
| mf-006 | Regression to the mean | accepted | Label unchanged; latest_risk binned for grouping tables (note and look, not a correction); bin edges deferred to EDA. Decided by Mario | [mf-006-regression-to-mean.md](./mf-006-regression-to-mean.md) |
| mf-007 | Logistic task and target (S4) | accepted | Logistic trained on all 8892 events, target `y_hr`, outputs `predict_proba`. Decided by Mario | [mf-007-logistic-task-target.md](./mf-007-logistic-task-target.md) |
| mf-008 | Magnitude regressor task and target (S4) | accepted | Ridge/lasso trained on all 8892 events, target `risk_final` untransformed, outputs continuous `r_hat`; reopened 2026-11-01 after HR-zone check (r_hat never reaches -6), confirmed without floor; alarm line moves to mf-012. Decided by Mario | [mf-008-magnitude-regressor-target.md](./mf-008-magnitude-regressor-target.md) |
| mf-009 | Model families and penalties (S4) | accepted | Logistic and regressor each in three variants: unpenalized, L2, L1 (six models); elastic net and KNN out. Decided by Mario | [mf-009-model-families-penalties.md](./mf-009-model-families-penalties.md) |
| mf-010 | Preprocessing for S4 linear models | accepted | Median imputer (safeguard, 0 NaN observed) on 35 cols; StandardScaler on the 30 numeric cols, one-hot unscaled; no transformations; fit on train fold. Decided by Mario | [mf-010-preprocessing-linear-models.md](./mf-010-preprocessing-linear-models.md) |
| mf-011 | Class imbalance in the logistic model (S4) | accepted | `class_weight='balanced'` on the logistic only, weights from the training fold; `predict_proba` becomes an inflated score, exception to mf-007. Decided by Mario | [mf-011-class-imbalance-logistic.md](./mf-011-class-imbalance-logistic.md) |
| mf-012 | Alarm line for the S4 regressors | accepted | Alarm if r_hat >= t; t maximizes F2 (beta 2) on the training-fold predictions, candidates = r_hat of training HR, ties by median; recomputed per model, fold and repetition; t stored as a diagnostic. Changes F2 vs the -6 protocol line. Decided by Mario | [mf-012-alarm-line-regressors.md](./mf-012-alarm-line-regressors.md) |
| mf-013 | Regularization strength selection (S4) | accepted | Nested stratified inner 5-fold; criterion = mean inner AP of r_hat vs y_hr, ties to highest alpha; ridge 25 log-points 1e0..1e6, lasso 25 log-points 1e-4..1e2; fixed grids; refit on the outer train fold. Decided by Mario | [mf-013-regularization-selection.md](./mf-013-regularization-selection.md) |
| mf-014 | Solver and library parameters, S4 regressors | accepted | Explicit sklearn parameters: OLS and Ridge(cholesky) with intercept; Lasso max_iter 10000, tol 1e-4, cyclic, warm start along descending alpha, new object per inner fold, cold final fit; non-converged alphas flagged, not dropped. Decided by Mario | [mf-014-solver-library-parameters.md](./mf-014-solver-library-parameters.md) |
| mf-015 | Seed of the inner split (S4) | accepted | `StratifiedKFold(5, shuffle=True, random_state=0)` for every inner split, all outer folds and repetitions. Decided by Mario | [mf-015-inner-split-seed.md](./mf-015-inner-split-seed.md) |
| — | S4 module location (S4) | auto-trivial | AI (engineering) | `src/models/linear.py`, bootstrap in `src/evaluation.py` per ownership map in `docs/plan-reparto.md`. Reason: repo layout only | — |
| — | S4 result slugs (S4) | auto-trivial | AI (engineering) | `ols`, `ridge`, `lasso`; `results/<slug>.json`, `preds/<slug>.parquet` as in pj-020. Reason: naming only | — |
| — | S4 `p_hr` column (S4) | auto-trivial | AI (engineering) | `p_hr` = 1.0 if `r_hat >= t` (mf-012) else 0.0, as for S5 (pj-020). Reason: column filled from a decided rule; Mario may reclassify | — |
| mf-016 | Seed of the bootstrap generator (S4) | accepted | Seed 2026, `numpy.random.default_rng(2026)`, index matrix drawn once and reused for all models and repetitions. Decided by Mario | [mf-016-bootstrap-seed.md](./mf-016-bootstrap-seed.md) |
| mf-017 | L when F2 = 0 in a bootstrap resample (S4) | accepted | Per repetition, before averaging, L = inf is replaced by 10 x the largest finite per-repetition L of the same model (clipped and unclipped apart); count of resamples with F2 = 0 reported; > 2.5 % marks the L interval and paired L differences not reliable. Decided by Mario | [mf-017-bootstrap-infinite-l.md](./mf-017-bootstrap-infinite-l.md) |
| mf-018 | BCa interval when the bias correction is infinite (S4) | accepted | z0 infinite (share 0 or 1): BCa marked not computable, point estimate without interval, no fallback; same for paired differences; all-equal bootstrap values give [v, v]. Decided by Mario | [mf-018-bca-infinite-bias-correction.md](./mf-018-bca-infinite-bias-correction.md) |
| mf-019 | L cap when no finite L exists (S4) | accepted | No finite L in any resample: no cap, L interval and paired differences marked not computable and not reliable. Decided by Mario | [mf-019-l-cap-no-finite-l.md](./mf-019-l-cap-no-finite-l.md) |
| mf-020 | Bootstrap implementation details and inert library defaults (S4) | accepted | `np.quantile(method="linear")` for BCa endpoints; mf-017 cap also applied to the original-sample estimate and the jackknife; inert library defaults of OLS, Ridge, imputer and scaler recorded. Decided by Mario | [mf-020-bootstrap-implementation-details.md](./mf-020-bootstrap-implementation-details.md) |
| mf-021 | Stage-1 classifier of S6 | accepted | The three logistic variants (unpenalized, L2, L1) are the stage-1 classifiers, to compare results. Decided by Mario | [mf-021-s6-stage1-classifier.md](./mf-021-s6-stage1-classifier.md) |
| mf-022 | Training events of the S6 stage-2 regressor | accepted | Stage-2 regressor trained on all events, not HR only, to avoid predicting above the true value on low-risk events. Decided by Mario | [mf-022-s6-stage2-training-events.md](./mf-022-s6-stage2-training-events.md) |
| mf-023 | Stage-2 model of S6 | accepted | The three S4 regressors (unpenalized, ridge, lasso) are the stage-2 models, to compare variants. Decided by Mario | [mf-023-s6-stage2-model.md](./mf-023-s6-stage2-model.md) |
| mf-024 | Pairing of stage-1 and stage-2 variants in S6 | accepted | All 9 combinations of the three classifiers with the three regressors, to see what each stage contributes. Decided by Mario | [mf-024-s6-pairing.md](./mf-024-s6-pairing.md) |
| mf-025 | Selection criterion for the logistic regularization strength in S6 | accepted | L2 and L1 strengths chosen by inner CV inside each outer training fold with the AUC of the stage-1 score as criterion. Decided by Mario | [mf-025-s6-logistic-regularization-criterion.md](./mf-025-s6-logistic-regularization-criterion.md) |
| mf-026 | Grids of the logistic regularization strength in S6 | accepted | Different log-spaced grids: L2 logspace(-4,4,25), L1 logspace(-2,4,25). Decided by Mario | [mf-026-s6-logistic-grids.md](./mf-026-s6-logistic-grids.md) |
| mf-027 | Tie rule for the logistic regularization strength in S6 | accepted | One standard error rule on the inner-fold AUC; the smallest C (strongest penalty) of the tie set. Decided by Mario | [mf-027-s6-logistic-tie-rule.md](./mf-027-s6-logistic-tie-rule.md) |
| mf-028 | Inner split and seed of the logistic models in S6 | accepted | Same inner split as S4 (mf-015), to avoid mixing two sources of variation. Decided by Mario | [mf-028-s6-logistic-inner-split.md](./mf-028-s6-logistic-inner-split.md) |
| mf-029 | Grid-edge treatment of the logistic strength in S6 | accepted | Same as S4: fixed grids, flag stored for a selected C at an edge, the developer decides manually. Decided by Mario | [mf-029-s6-logistic-grid-edge.md](./mf-029-s6-logistic-grid-edge.md) |
| mf-030 | Solvers and library parameters of the logistic models in S6 | accepted (L1 solver superseded by mf-041) | lbfgs for unpenalized and L2, saga for L1; max_iter 10000, tol 1e-4, random_state 0, warm_start False, fit_intercept True; non-convergence as mf-014. Decided by Mario | [mf-030-s6-logistic-solvers.md](./mf-030-s6-logistic-solvers.md) |
| mf-031 | Calibration method of the stage-1 score in S6 | accepted | Platt scaling for each of the three classifiers; a fit with a <= 0 is kept and flagged. Decided by Mario | [mf-031-s6-calibration-method.md](./mf-031-s6-calibration-method.md) |
| mf-032 | Data used to fit the Platt calibration in S6 | accepted | Out-of-fold scores of the inner 5-fold validation with the selected C; (a, b) fitted on all training events of the fold. Decided by Mario | [mf-032-s6-calibration-data.md](./mf-032-s6-calibration-data.md) |
| mf-033 | Fitting parameters of the Platt calibration in S6 | accepted | No penalty, no class weights, 0/1 targets, lbfgs with max_iter 10000 and tol 1e-4, intercept, non-convergence as mf-014. Decided by Mario | [mf-033-s6-platt-fitting-parameters.md](./mf-033-s6-platt-fitting-parameters.md) |
| mf-034 | Source of the stage-2 predictions in S6 | accepted | The stage-2 predictions are the stored S4 predictions of the three regressors, with no refit. Decided by Mario | [mf-034-s6-stage2-predictions-source.md](./mf-034-s6-stage2-predictions-source.md) |
| mf-035 | Combination of the two stages in S6: alarm rule and predicted risk | accepted | Alarm p >= t with t maximizing F2 on the out-of-fold calibrated p of the training fold; predicted risk is the stage-2 r_hat. Decided by Mario | [mf-035-s6-combination-alarm-risk.md](./mf-035-s6-combination-alarm-risk.md) |
| mf-036 | Calibration measure and reliability diagram of S6 | accepted | Brier per repetition averaged over 5; equal-count bins with k = 10, per repetition then averaged bin by bin; 3 values and 3 diagrams. Decided by Mario | [mf-036-s6-calibration-measure-diagram.md](./mf-036-s6-calibration-measure-diagram.md) |
| mf-037 | Uncertainty and comparisons of the S6 rows | accepted | Same bootstrap as S4; paired differences against LRP, CRP and the S4 regressor; 18 pairs among S6 rows that change one stage only. Decided by Mario | [mf-037-s6-comparisons-bootstrap.md](./mf-037-s6-comparisons-bootstrap.md) |
| mf-038 | Score used by the Platt calibration in S6 | accepted | Platt is fitted on the log-odds z (decision_function) of the stage-1 classifier, not on the probability. Found at implementation. Decided by Mario | [mf-038-s6-platt-input-score.md](./mf-038-s6-platt-input-score.md) |
| mf-039 | C* when several C tie exactly at the maximum mean AUC (S6) | accepted | SE of the one-standard-error rule is computed for the smallest C among the tied maxima. Found at implementation. Decided by Mario | [mf-039-s6-cstar-exact-ties.md](./mf-039-s6-cstar-exact-ties.md) |
| mf-040 | Reliability of paired L differences between two rows in S6 | accepted | A paired L difference is not reliable if more than 2.5% of the resamples have F2 = 0 in at least one of the two rows. Found at implementation. Decided by Mario | [mf-040-s6-paired-l-reliability.md](./mf-040-s6-paired-l-reliability.md) |
| mf-041 | Solver of the L1 logistic model in S6 | accepted | liblinear (intercept_scaling 100, max_iter 10000, tol 1e-4) replaces saga for L1, which did not converge at any C (supersedes the L1 part of mf-030). Found at implementation. Decided by Mario | [mf-041-s6-l1-solver.md](./mf-041-s6-l1-solver.md) |
| mf-042 | Grid-edge result of the logistic strength in S6 | accepted | Grids left as they are; edge selections (L1 25/25 at 0.01, L2 19/25 at 1e-4) reported as a limitation; one-fold L1 AUC curve shows a flat zone 1e-3..1e-2 and collapse below. Decided by Mario | [mf-042-s6-logistic-grid-edge-result.md](./mf-042-s6-logistic-grid-edge-result.md) |
| — | S6 stage-1 execution split over (repetition, fold) tasks in several processes | auto-trivial | Engineering only: the 25 outer folds are independent and seeded, so results are identical to the sequential run; chosen by Mario (option A) after L1 with liblinear was measured at about 25-30 h sequential. No ADR | — |
| — | S6 output names and figure layout | auto-trivial | AI (engineering) | Files `s6_<clf>__<reg>`, `s6_stage1_<clf>`, columns `z`, `p_cal`, `p_hr` (alarm flag, contract of pj-020), 3-panel reliability figure at 150 dpi, checkpoints in `data/s6_cache/`. Reason: naming and plotting only | — |
| — | S6 `random_state` of lbfgs models | auto-trivial | AI (engineering) | lr_none and lr_l2 pass `random_state=None` (mf-030 says 0, "lbfgs does not use it"); inert, no effect on results. Found at audit | — |
| pj-027 | S7 atlas case structure | accepted | Option C: 6 core slots (2 LRP/model contrasts, 3 jumps, 1 multi-fail) + 4 optional (cut order O3,O1,O4,O2) | [pj-027-s7-atlas-case-structure.md](./pj-027-s7-atlas-case-structure.md) |
| pj-028 | S7 atlas OOF source + C1/C2 pick | accepted | Cases from train/val OOF only, not official test; C1/C2 = argmax `risk_final` among qualifiers | [pj-028-s7-atlas-oof-and-c1-c2-selection.md](./pj-028-s7-atlas-oof-and-c1-c2-selection.md) |
| pj-029 | S7 OOF repetition policy | accepted | Slot qualifies if contrast in ≥3/5 reps; caption: k/5 + mean `r_hat` on qualifying reps | [pj-029-s7-oof-repetition-policy.md](./pj-029-s7-oof-repetition-policy.md) |
| pj-030 | S7 C6 + jump defer | accepted | C6: ≥2 of {LRP,rf,gbdt} FN in ≥3/5 reps; argmax `risk_final`; C3–C5/O4 blocked on S2 | [pj-030-s7-c6-and-jump-defer.md](./pj-030-s7-c6-and-jump-defer.md) |
| pj-031 | S7 O1 difficult TP | accepted | ≥3/5 triple TP; argmax `range_risk`; exclude used `event_id` only | [pj-031-s7-o1-difficult-tp.md](./pj-031-s7-o1-difficult-tp.md) |
| pj-032 | S7 O2–O4 deferred | accepted | Rules wait for S6 preds and S2 jump taxonomy | [pj-032-s7-o2-o4-deferred.md](./pj-032-s7-o2-o4-deferred.md) |
| pj-033 | Progress Report thesis (W1) | accepted | C+A: protocol/data rigor spine + models-in-progress; not bake-off-as-win | [pj-033-progress-report-thesis.md](./pj-033-progress-report-thesis.md) |
| pj-034 | Progress Report outline (W1) | accepted | Problem → solution → impact; bake-off under Impact; AI declaration at end | [pj-034-progress-report-outline.md](./pj-034-progress-report-outline.md) |
| pj-035 | Progress Report evaluation splits (W1) | accepted | Two tables: official test CRP/LRP; internal OOF bake-off for learned models | [pj-035-progress-report-two-tables.md](./pj-035-progress-report-two-tables.md) |
| pj-036 | Progress Report tables + EDA weight (W1) | accepted | Tab2: LRP+ols/ridge/lasso+rf/gbdt; F2+L; BCa on linears; mf-012 footnote; minimal EDA prose | [pj-036-progress-report-tables.md](./pj-036-progress-report-tables.md) |
| pj-037 | Progress Report figures (W1) | accepted | 2–3 figs: RF importances, jumps; minimal EDA; integrator discretion | [pj-037-progress-report-figures.md](./pj-037-progress-report-figures.md) |
| pj-038 | Progress Report protocol prose (W1) | accepted | 3–5 sentences + pointer to pj-001..007 | [pj-038-progress-report-protocol-prose.md](./pj-038-progress-report-protocol-prose.md) |
| pj-039 | Progress Report S4 prose ownership (W1) | accepted | Mario 2–4 sentences; Pedro table footnote only; mf-007..020 reference | [pj-039-progress-report-s4-prose-ownership.md](./pj-039-progress-report-s4-prose-ownership.md) |
| pj-040 | Progress Report contributions + AI (W1) | accepted | Equal plan framing; Pedro Cursor / Mario Claude; detail deferred | [pj-040-progress-report-contributions-ai.md](./pj-040-progress-report-contributions-ai.md) |
| pj-041 | Progress Report next steps (W1) | accepted | Four bullets: S6, S7, harden uncertainty, Sentence Outline | [pj-041-progress-report-next-steps.md](./pj-041-progress-report-next-steps.md) |
| pj-042 | W1 importance figure despite B1 | accepted | Amends pj-019 for W1 only: RF impurity figure with permutation-disagreement caveat; pj-019 reopened for final report | [pj-042-w1-importance-figure-override.md](./pj-042-w1-importance-figure-override.md) |
| pj-043 | W1 RF row with R4 note | accepted | RF kept in Table 2 with footnote; pj-026 R4 fired for RF, reopen in C2 | [pj-043-w1-rf-row-r4-caveat.md](./pj-043-w1-rf-row-r4-caveat.md) |
| — | Output column names (S2) | auto-trivial | AI (engineering) | `jump_class` for the label; analysis columns named at implementation. Reason: naming only, no modeling effect | — |
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
| S5 RF `max_depth` | 8 | pj-024 |
| S5 RF `min_samples_split` | 2 | pj-024 |
| S5 RF `min_samples_leaf` | 1 | pj-024 |
| S5 RF `max_features` | sqrt | pj-016 |
| S5 RF `bootstrap` | True | pj-016 |
| S5 RF `max_samples` | None | pj-016 |
| S5 RF `criterion` | squared_error | pj-016 |
| S5 RF `random_state` | 42 + repetition_index (0…4) | pj-016 |
| S5 RF `n_jobs` | -1 | pj-016 |
| S5 hyperparameter selection metric | lowest **unclipped** L on pooled OOF (all folds × reps); tie → smaller value | pj-025 (supersedes pj-022) |
| S5 training target transform | y_fit = max(`risk_final`, c_fold); evaluation uses unclipped `risk_final` | pj-026 |
| S5 floor c | per training fold: solve p*(c) = F*/5 (β = 2), Brent on [−29.99, −6.0005]; ≈ −6.09 on full train | pj-026 |
| S5 F* for c | F₂ of LRP on the training fold | pj-026 |
| S5 μ_HR for c | mean `risk_final` of HR events in the training fold | pj-026 |
| S5 floor-c revocation | R0 F₂=0; R1 F₂ outside [F*/2, 2F*]; R2 threshold-sweep gain > 0.05 (t ∈ [−7, −5], step 0.01); R3 alarm-zone HR rate / mean p̂ outside [0.5, 2] (≥10 HR); R4 \|detected − missed HR mean\| > 0.8·SD_HR (≥10 HR per group) → nested-CV c | pj-026 |
| S5 RF `n_estimators` | search {300, 500, 1000}; select per pj-025; tie → smaller n | pj-024, pj-025 |
| S5 GBDT estimator | GradientBoostingRegressor | pj-017 |
| S5 GBDT `n_estimators` | search {300, 500, 1000}; select per pj-025; tie → smaller n | pj-024, pj-025 |
| S5 GBDT `learning_rate` | 0.1 | pj-017 |
| S5 GBDT `max_depth` | 8 | pj-024 |
| S5 GBDT `min_samples_split` | 2 | pj-024 |
| S5 GBDT `min_samples_leaf` | 1 | pj-024 |
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
| Jump label usage | analysis and reporting only; never feature, target or weight | [mf-001](./mf-001-purpose-scope.md) |
| Jump label scope | train and official test (test inspected only at R5) | [mf-001](./mf-001-purpose-scope.md) |
| Jump cut c | 1 (log10 units) | [mf-003](./mf-003-jump-cut.md) |
| Jump cut sensitivity values (EDA only) | 0.5, 1.0, 2.0; comparison of class shares only, they do not change the cut c = 1 | [mf-003](./mf-003-jump-cut.md) |
| Jump cut symmetry | symmetric (up: Δ ≥ c; down: Δ ≤ −c) | [mf-003](./mf-003-jump-cut.md) |
| Jump cut operator | ≥ / ≤ (limit included) | [mf-003](./mf-003-jump-cut.md) |
| Jump label depends on HR crossing | no (size of Δ only) | [mf-002](./mf-002-jump-by-size.md) |
| HR-crossing analysis column (up/down/none) | yes, analysis-only, never in X | [mf-002](./mf-002-jump-by-size.md) |
| stable-low / stable-high rule | by y_final vs −6 (non-jump events only) | [mf-004](./mf-004-stable-rule.md) |
| Boundary y_final = −6 | stable-high | [mf-004](./mf-004-stable-rule.md) |
| Lead-time handling | single cut; lead time as analysis-only column (time_to_tca of last valid CDM) | [mf-005](./mf-005-lead-time.md) |
| Lead-time bin edges for grouping tables | deferred-fog (decide after EDA shows the distribution; does not block the label or the column) | [mf-005](./mf-005-lead-time.md) |
| Regression-to-the-mean handling | no correction; group tables by latest_risk bins | [mf-006](./mf-006-regression-to-mean.md) |
| latest_risk bin edges for grouping tables | deferred-fog (decide after EDA; does not block the label) | [mf-006](./mf-006-regression-to-mean.md) |
| S4 logistic training population | all 8892 events of `event_table` | [mf-007](./mf-007-logistic-task-target.md) |
| S4 logistic target | `y_hr` (`risk_final >= -6.0`) | [mf-007](./mf-007-logistic-task-target.md) |
| S4 logistic output | `predict_proba` per event; with mf-011 weights it is an inflated score, not P(HR \| x) (exception) | [mf-007](./mf-007-logistic-task-target.md), [mf-011](./mf-011-class-imbalance-logistic.md) |
| S4 magnitude regressor training population | all 8892 events of `event_table` | [mf-008](./mf-008-magnitude-regressor-target.md) |
| S4 magnitude regressor target | `risk_final` (log10, unclipped, no floor) | [mf-008](./mf-008-magnitude-regressor-target.md) |
| S4 magnitude regressor output | continuous `r_hat` (log10 risk) per event | [mf-008](./mf-008-magnitude-regressor-target.md) |
| S4 HR-zone bias review criterion | triggered 2026-11-01; mf-008 confirmed without floor (no target floor for linear models) | [mf-008](./mf-008-magnitude-regressor-target.md) |
| S4 logistic penalty variants | none, L2, L1 | [mf-009](./mf-009-model-families-penalties.md) |
| S4 magnitude regressor penalty variants | none (OLS), L2 (ridge), L1 (lasso) | [mf-009](./mf-009-model-families-penalties.md) |
| S4 elastic net / KNN | not included (fog / deferred) | [mf-009](./mf-009-model-families-penalties.md) |
| S4 imputation | `SimpleImputer`, strategy `median`, fit on train fold, all 35 columns | [mf-010](./mf-010-preprocessing-linear-models.md) |
| S4 `SimpleImputer` `add_indicator` | False | [mf-010](./mf-010-preprocessing-linear-models.md) |
| S4 `SimpleImputer` `keep_empty_features` | False | [mf-010](./mf-010-preprocessing-linear-models.md) |
| S4 scaling | `StandardScaler` fit on train fold, 30 numeric columns only; 5 one-hot columns unscaled | [mf-010](./mf-010-preprocessing-linear-models.md) |
| S4 `StandardScaler` `with_mean` / `with_std` | True / True | [mf-010](./mf-010-preprocessing-linear-models.md) |
| S4 feature transformations | none | [mf-010](./mf-010-preprocessing-linear-models.md) |
| S4 logistic `class_weight` | `'balanced'` (w_k = n / (2 n_k)), computed on the training fold | [mf-011](./mf-011-class-imbalance-logistic.md) |
| S4 regressor sample weights | none | [mf-011](./mf-011-class-imbalance-logistic.md) |
| S4 regressor alarm rule | alarm iff `r_hat >= t` (not -6) | [mf-012](./mf-012-alarm-line-regressors.md) |
| S4 alarm line t: criterion | maximize F2 (beta = 2) on the training-fold predictions | [mf-012](./mf-012-alarm-line-regressors.md) |
| S4 alarm line t: candidates | `r_hat` values of the HR events of the training fold | [mf-012](./mf-012-alarm-line-regressors.md) |
| S4 alarm line t: ties | median of the tied candidates (even count: mean of the two central) | [mf-012](./mf-012-alarm-line-regressors.md) |
| S4 alarm line t: granularity | recomputed per model, fold and repetition; t and its variability stored in results | [mf-012](./mf-012-alarm-line-regressors.md) |
| S4 MSE_HR / L | MSE_HR on true HR events with `r_hat` (independent of t); L = MSE_HR / F2 with the F2 of t | [mf-012](./mf-012-alarm-line-regressors.md) |
| S4 alpha selection scheme | nested: stratified (`y_hr`) inner 5-fold within each outer training fold; seed and shuffle of the inner split per mf-015 | [mf-013](./mf-013-regularization-selection.md) |
| S4 alpha selection criterion | mean over the 5 inner folds of AP of `r_hat` vs `y_hr`; ties to the highest alpha | [mf-013](./mf-013-regularization-selection.md) |
| S4 ridge alpha grid | 25 log-spaced values, 1e0 to 1e6 (`Ridge` parametrisation) | [mf-013](./mf-013-regularization-selection.md) |
| S4 lasso alpha grid | 25 log-spaced values, 1e-4 to 1e2 (`Lasso` parametrisation) | [mf-013](./mf-013-regularization-selection.md) |
| S4 alpha grid extension | none (fixed grids; an edge optimum is reported, not corrected) | [mf-013](./mf-013-regularization-selection.md) |
| S4 final fit after selection | refit with selected alpha on the whole outer training fold; preprocessing refit on it | [mf-013](./mf-013-regularization-selection.md) |
| S4 selected alpha storage | per outer fold, repetition and penalty, in results | [mf-013](./mf-013-regularization-selection.md) |
| S4 `fit_intercept` (OLS, Ridge, Lasso) | True | [mf-014](./mf-014-solver-library-parameters.md) |
| S4 `LinearRegression` `positive` / `copy_X` | False / True | [mf-014](./mf-014-solver-library-parameters.md) |
| S4 `Ridge` solver / `positive` / `copy_X` | `cholesky` / False / True (`tol` not set: unused with cholesky) | [mf-014](./mf-014-solver-library-parameters.md) |
| S4 `Lasso` `max_iter` / `tol` | 10000 / 1e-4 | [mf-014](./mf-014-solver-library-parameters.md) |
| S4 `Lasso` `selection` | `cyclic` (deterministic, no seed) | [mf-014](./mf-014-solver-library-parameters.md) |
| S4 `Lasso` `warm_start` / `precompute` / `positive` / `copy_X` | True / False / False / True | [mf-014](./mf-014-solver-library-parameters.md) |
| S4 `Lasso` alpha sweep order | descending, one object per inner fold, nothing carried across folds | [mf-014](./mf-014-solver-library-parameters.md) |
| S4 `Lasso` final fit after selection | new object, selected alpha only, cold start | [mf-014](./mf-014-solver-library-parameters.md) |
| S4 `Lasso` non-convergence | record alpha as not converged, use partial solution, flag in results; do not drop | [mf-014](./mf-014-solver-library-parameters.md) |
| S4 inner split seed / shuffle | `random_state=0`, `shuffle=True`, same for all outer folds and repetitions | [mf-015](./mf-015-inner-split-seed.md) |
| S4 inner split | `StratifiedKFold(n_splits=5)` on `y_hr` | [mf-015](./mf-015-inner-split-seed.md) |
| S4 bootstrap generator / seed | `numpy.random.default_rng(2026)`, fixed, same for all models | [mf-016](./mf-016-bootstrap-seed.md) |
| S4 bootstrap indices | drawn once (B = 10000 x 8892 events) and reused for all models, repetitions and paired comparisons | [mf-016](./mf-016-bootstrap-seed.md) |
| S4 bootstrap L when F2 = 0 (per repetition) | L replaced before averaging the 5 repetitions | [mf-017](./mf-017-bootstrap-infinite-l.md) |
| S4 bootstrap L cap | 10 x the largest finite per-repetition L of the same model over all resamples and repetitions; L clipped and unclipped apart | [mf-017](./mf-017-bootstrap-infinite-l.md) |
| S4 bootstrap F2 = 0 count | resamples with F2 = 0 in at least one repetition, reported next to each L interval and paired L difference | [mf-017](./mf-017-bootstrap-infinite-l.md) |
| S4 bootstrap L reliability threshold | > 2.5 % of resamples with F2 = 0 marks the model's L interval and its paired L differences vs LRP and CRP not reliable | [mf-017](./mf-017-bootstrap-infinite-l.md) |
| S4 BCa when z0 is infinite | not computable: null interval, point estimate kept, flag stored; no clipping, no percentile fallback; also for paired differences | [mf-018](./mf-018-bca-infinite-bias-correction.md) |
| S4 BCa when all bootstrap values equal the estimate | interval [v, v] | [mf-018](./mf-018-bca-infinite-bias-correction.md) |
| S4 L cap when no finite L exists | no cap; L interval and paired differences not computable and not reliable | [mf-019](./mf-019-l-cap-no-finite-l.md) |
| S4 BCa percentile interpolation | `np.quantile(..., method="linear")` | [mf-020](./mf-020-bootstrap-implementation-details.md) |
| S4 L cap scope | per model and repetition: resamples, original-sample estimate and jackknife values | [mf-020](./mf-020-bootstrap-implementation-details.md) |
| S4 inert library defaults | `LinearRegression(n_jobs=None, tol=1e-06)`; `Ridge(max_iter=None, random_state=None, tol=1e-04)` (unused with cholesky); `SimpleImputer(missing_values=nan, fill_value=None, copy=True)`; `StandardScaler(copy=True)` | [mf-020](./mf-020-bootstrap-implementation-details.md) |
| S6 stage-1 classifiers | three logistic variants: unpenalized, L2, L1 (`class_weight='balanced'` per mf-011); regularization and solver still to decide | [mf-021](./mf-021-s6-stage1-classifier.md) |
| S6 stage-2 training events | all events (not HR only) | [mf-022](./mf-022-s6-stage2-training-events.md) |
| S6 stage-2 models | the three S4 regressors: unpenalized, ridge, lasso; pairing with stage 1 and reuse vs refit still to decide | [mf-023](./mf-023-s6-stage2-model.md) |
| S6 pairing of stages | all 9 combinations (3 classifiers x 3 regressors); 3 calibrations, one per classifier | [mf-024](./mf-024-s6-pairing.md) |
| S6 logistic strength criterion | inner CV inside each outer training fold, AUC of the stage-1 score vs `y_hr`; L2 and L1 only | [mf-025](./mf-025-s6-logistic-regularization-criterion.md) |
| S6 logistic strength grids | L2: `np.logspace(-4, 4, 25)`; L1: `np.logspace(-2, 4, 25)` (C = 1/lambda) | [mf-026](./mf-026-s6-logistic-grids.md) |
| S6 logistic strength tie rule | one standard error rule: SE = sample std (divisor 4) of the 5 inner-fold AUCs of the best-mean candidate / sqrt(5); tie set = {C : mean AUC >= max mean - SE}; smallest C chosen | [mf-027](./mf-027-s6-logistic-tie-rule.md) |
| S6 logistic C* on exact ties of the maximum mean AUC | the smallest C among the tied maxima; its SE defines the tie set | [mf-039](./mf-039-s6-cstar-exact-ties.md) |
| S6 logistic inner split | `StratifiedKFold(n_splits=5, shuffle=True, random_state=0)`, same as S4 | [mf-028](./mf-028-s6-logistic-inner-split.md) |
| S6 logistic grid-edge treatment | grids fixed, no automatic extension; flag stored when the selected C is at an edge; the developer decides manually | [mf-029](./mf-029-s6-logistic-grid-edge.md) |
| S6 logistic solvers | unpenalized and L2: `lbfgs` (mf-030); L1: `liblinear` with `l1_ratio=1.0`, `intercept_scaling=100`, `max_iter=10000`, `tol=1e-4`, `random_state=0`, `dual=False` (mf-041 supersedes the `saga` of mf-030) | [mf-041](./mf-041-s6-l1-solver.md) |
| S6 logistic max_iter, tol | 10000, 1e-4 (as S4 lasso); also for the L1 `liblinear` (mf-041) | [mf-030](./mf-030-s6-logistic-solvers.md) |
| S6 logistic random_state, warm_start, fit_intercept | 0 (saga), False, True | [mf-030](./mf-030-s6-logistic-solvers.md) |
| S6 logistic non-convergence | recorded, partial solution used, flagged; point not dropped | [mf-030](./mf-030-s6-logistic-solvers.md) |
| S6 logistic inert library defaults | `intercept_scaling=1` (unpenalized and L2; L1 uses 100, mf-041), `dual=False`, `n_jobs=None`, `verbose=0` | [mf-030](./mf-030-s6-logistic-solvers.md) |
| S6 calibration method | Platt scaling, one per stage-1 classifier (3 calibrations); a <= 0 fit kept and flagged in the results | [mf-031](./mf-031-s6-calibration-method.md) |
| S6 Platt input score | s = z, the log-odds (`decision_function`) of the stage-1 classifier | [mf-038](./mf-038-s6-platt-input-score.md) |
| S6 Platt fitting data | out-of-fold scores of the 5 inner folds (mf-028) with the selected C of the fold; (a, b) fitted on all training events of the fold; the final classifier is refit on the whole training fold | [mf-032](./mf-032-s6-calibration-data.md) |
| S6 Platt fit: penalty, weights, target | no penalty; `class_weight=None`; 0/1 targets | [mf-033](./mf-033-s6-platt-fitting-parameters.md) |
| S6 Platt fit: solver, max_iter, tol, intercept | `lbfgs`, 10000, 1e-4, `fit_intercept=True` | [mf-033](./mf-033-s6-platt-fitting-parameters.md) |
| S6 Platt fit: non-convergence and inert defaults | recorded, partial solution used, flagged; `random_state=None`, `warm_start=False`, `n_jobs=None`, `verbose=0`, `dual=False`, `intercept_scaling=1` | [mf-033](./mf-033-s6-platt-fitting-parameters.md) |
| S6 stage-2 predictions source | the stored S4 out-of-fold predictions (`preds/{ols,ridge,lasso}.parquet`); no refit | [mf-034](./mf-034-s6-stage2-predictions-source.md) |
| S6 alarm rule | alarm if p >= t; t maximizes F2 (beta = 2) on the out-of-fold calibrated p of the training fold; candidates = p of the training HR; ties = median (as mf-012); t stored per fold | [mf-035](./mf-035-s6-combination-alarm-risk.md) |
| S6 predicted risk | stage-2 r_hat as it is (MSE_HR equals the S4 regressor's) | [mf-035](./mf-035-s6-combination-alarm-risk.md) |
| S6 calibration number | Brier, per repetition on all out-of-fold p, averaged over the 5 repetitions; one value per stage-1 classifier | [mf-036](./mf-036-s6-calibration-measure-diagram.md) |
| S6 reliability diagram | equal-count bins, k = 10 (`np.array_split` of the events sorted by p), per repetition then averaged bin by bin; one diagram per classifier | [mf-036](./mf-036-s6-calibration-measure-diagram.md) |
| S6 bootstrap procedure | same as S4 (mf-016..mf-020) for the 9 rows, nothing changed | [mf-037](./mf-037-s6-comparisons-bootstrap.md) |
| S6 paired comparisons | every S6 row vs LRP, CRP and its S4 regressor; plus the 18 pairs among S6 rows that change one stage only; no multiple-comparison correction | [mf-037](./mf-037-s6-comparisons-bootstrap.md) |
| S6 paired L reliability between two rows | not reliable if more than 2.5% of the resamples have F2 = 0 in at least one repetition for A or B; vs LRP and CRP as S4 | [mf-040](./mf-040-s6-paired-l-reliability.md) |
| S7 atlas layout | option C: 6 core case categories + up to 4 optional; cut order O3, O1, O4, O2 | pj-027 |
| S7 core contrast models | LRP vs rf and/or gbdt (S5); S4/S6 preds added to panels when available | pj-027 |
| S7 jump slots (core) | 3 distinct-outcome jump cases (C3–C5) | pj-027 |
| S7 multi-fail slot | ≥2 of {LRP, rf, gbdt} F₂-fail on same true HR (C6) | pj-027 |
| S7 atlas prediction source | OOF on S1 `event_table` / train-val only; not official test for case selection | pj-028 |
| S7 C1/C2 selection among qualifiers | argmax `risk_final` (most severe true HR) | pj-028 |
| S7 OOF row per event (repetition policy) | contrast must hold in ≥3 of 5 seeds (42–46); evaluate each rep separately | pj-029 |
| S7 atlas caption (C1/C2) | report k/5 and mean `r_hat` on qualifying reps for LRP and shown tree | pj-029 |
| S7 jump slots C3–C5, O4 | selection rules deferred until S2 taxonomy ADR | pj-030 |
| S7 C6 qualification | true HR; ≥2 of {LRP, rf, gbdt} F₂-FN in ≥3/5 OOF reps | pj-030 |
| S7 C6 selection among qualifiers | argmax `risk_final`; tie → smallest `event_id` | pj-030 |
| S7 C6 caption | k/5 multi-fail reps; per-model fail count 0–5; mean preds on qualifying reps | pj-030 |
| S7 O1 qualification | ≥3/5 reps: HR + LRP, rf, gbdt all TP; exclude atlas `event_id`s already used | pj-031 |
| S7 O1 selection | argmax `range_risk` on usable CDMs; tie → smallest `event_id` | pj-031 |
| S7 O1 caption | k/5 triple TP; mean preds on k reps; report `range_risk` | pj-031 |
| S7 O2–O4 selection rules | deferred-fog until S6 preds + S2 taxonomy ADRs | pj-032 |
| S7 tie-break equal `risk_final` | deferred-fog (smallest `event_id` suggested in pj-029 for tree tie) | — |

## Fog (not yet sharp)

- S5 tuning when all candidates have F₂ = 0 (L = ∞): tie-break still undefined; R0 in pj-026 reopens c in that case.
- S5 iteration 2 levers still to decide (in order): loss / statistic (e.g. quantile), sample weights on HR, residual on LRP, alarm threshold ≠ −6, classification + magnitude (overlaps S6).
- Rúbrica interna exacta del profe para el project (syllabus describe entregables, no desglose de puntos).
- Papel empírico final de cada familia de modelos (lineal / trees / NN) — se resolverá al implementar; el proposal no lo congela (011).
- Nombres legales / affiliation exactos en el header del PDF (IE formatting).

- Modeling events whose last CDM has `time_to_tca >= 2` (type Z; label CDM is also an input) — needs a different task definition (pj-003).
## Fog addendum (S4)

- Elastic net and KNN: not included in S4 (mf-009; deferred by Mario).
- S4 logistic models (mf-007, mf-009, mf-011): kept for S6, not in the S4 table.
- Source of the ~0.16 F2 gap between training-fold alarm line and an oracle line (mf-012): hypothesis (step-function noise vs scale shift across folds), to contrast with stored t per fold.
- Effect of lasso start point / sweep order on `r_hat` under collinearity (mf-014): not measured.

## Fog addendum (S2)

- Validate c = 1 and the class shares against the real distribution of Δ (mf-003).
- Lead-time and latest_risk bin edges for grouped tables (mf-005, mf-006).

## Out of scope

- Reparto de roles Pedro / Mario en el proposal (no lo pide el enunciado; confirmado usuario).
- Paper final, slides de oral, implementación completa del bake-off.
- Reabrir o rediseñar el form de prioridades (001–006).
- Co-proyecto ESA + PHBench.
- Decidir de nuevo RQ/ángulo/dataset (007–015); este pase solo submission packing (016–024).
