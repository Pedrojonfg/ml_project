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

## Fog (not yet sharp)

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
