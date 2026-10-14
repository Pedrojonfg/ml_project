# Research Brief: Ideas de proyecto ML (Pedro × Mario)
**Depth**: deep  
**Date**: 2026-10-11  
**Research time**: ~sesión intensiva (repo + syllabus + intake + web + 8 subagentes en paralelo)  
**Deadline crítico**: Project Proposal — Sunday 11 Oct 2026 (hoy), máx. 2 páginas texto

---

## Executive Summary

El proyecto del curso (ML + Communication Skills, BAM IE, Prof. Nacho Molina) premia **originalidad y ambición (25%)**, implementación reproducible, insights con impacto, y dominio total en oral (50% de la nota ML). El intake cruza dos perfiles asimétricos pero compatibles:

- **Pedro**: deeptech / física / robótica / quantum / aerospace al máximo; odia lo genérico; quiere “dejar boquiabierto” a un investigador; techo = *proponer/adaptar investigación propia*; path fácil = 0.
- **Mario**: finanzas + recommenders; **veto duro salud/omics**; quiere originalidad, buena data, comparación de modelos y análisis limpio; techo = *leer papers y reproducir*; más orientado a portfolio que a paper teórico.

La zona de caza óptima NO es bio (alineada con el profe pero vetada), sino **robar el ADN metodológico de Molina** (probabilístico, estructura física/geométrica, latentes, comparación rigurosa) y aplicarlo a **aerospace / EO / física / robótica / VC innovador / composición-abducción**.

**Veredicto preliminar (top band):**  
1) **ESA Collision Avoidance** *o* **OPS-SAT-AD** (spacecraft ops real; datasets oficiales)  
2) **PHBench** — VC Series A desde Product Hunt (anti-genérico, Mario+Pedro)  
3) **SCAN add-jump** — operacionalizar “can't jump” / composición con bake-off de métodos  
4) **Structured-latent orbital** (ADN Molina sin bio: física en el decoder + ablación)  
5) **Wildfire/EO fusion** o **RODEO-style verification+recommender** (si queréis story CyPhy)  

---

## 1. Constraints duros (del brief oficial + intake)

| Constraint | Implicación |
|------------|-------------|
| Dataset real, manejable en ~6 semanas | Evitar OXE completo, PhysInOne TB-scale, fine-tune LLM gigante |
| ≥1 método del temario + extensiones OK | Siempre anclar a sklearn/PyTorch del curso; ambición = extensión *justificada* |
| Ambición 25% ML | Dataset distintivo + problem framing > “usar XGBoost en Titanic” |
| Oral 50% ML + entender TODO | No black-box que nadie pueda defender |
| Prosa AI prohibida; código AI OK con disclosure | GitHub con historia real de commits |
| Mario: veto **Salud/biomedicina/omics** | Fuera DeepCycle-like, single-cell, breast cancer del curso |
| Pedro: veto **proyecto genérico de estudiante** | Fuera house prices, credit default vanilla, sentiment Twitter |
| Integración multi-fuente valorada | Bonus si se hace con transparencia |

### Temario usable (ancla de nota)

Linear/logistic + regularización, kernels/SVM/kernel PCA, trees/RF/boosting, NN/autoencoders, PCA/clustering; sabor probabilístico del curso (likelihood, bias–variance). Escapes naturales alineados con el profe: **GPs, VAEs, PINNs, dim. reduction no lineal** — pero en dominio no-bio.

### CyPhy Life (IE) — contexto para Pedro

Lab de Eduardo Castelló: swarm robotics, ROBOPRENEUR (blockchain+robots), TUI, AIfred study companion, RODEO. **No hace falta acceso al lab** para un project de curso: se puede (a) usar datasets públicos de swarm/manipulation, (b) modelar un problema *inspirado* en autonomía económica de agentes, (c) contactarles como future work / mentorship, no como dependencia de la proposal.

---

## 2. Perfiles cruzados

### Scores de dominio (intake)

| Dominio | Pedro | Mario | Overlap |
|---------|------:|------:|---------|
| Física / ingeniería / dinámicos | 10 | 8 | ★★★★★ |
| Robótica / control / percepción | 10 | 9 | ★★★★★ |
| Quantum / hard science ML | 10 | 8 | ★★★★★ |
| Aerospace (otro) | 10 | — | ★★★★ (Pedro-led) |
| NLP / texto | 7* | 9 | ★★★★ si problema “guay” |
| Visión / señales | 9 | 7 | ★★★★ |
| Clima / energía | 7 | 7 | ★★★ |
| Finanzas | 7† | 9 | ★★★★ solo si innovador |
| Educación | 9 | 7 | ★★★ |
| Salud / omics | 6 | 3 + **VETO** | ✗ |
| Recommenders (texto libre Mario) | — | alto | ★★★★ vía VC/OSS/papers |

\*Pedro: NLP-filosofía solo si el problema es suficientemente ambicioso (abducción / LLMs can't jump).  
†Pedro: fintech solo si no es “lo de siempre”; VC le interesa.

### Intención

| Escala | Pedro | Mario |
|--------|------:|------:|
| Portfolio / laboral | 10 | 7 |
| Investigación / teoría | 10 | 5 |
| Impacto real | 9 | 5 |
| Aprendizaje ambicioso | 10 | 7 |
| Path fácil temario | **0** | 4 |

**Tensión productiva:** Pedro empuja wow-research; Mario ancla definición, datos y comparación. El sweet spot es un problema **ambicioso pero bien acotado**, con dataset limpio y story defendible en oral — no un paper de Nature incompleto.

### Métodos a priori

Ambos abiertos a trees, NN, deep, PINNs, RL. Pedro más Bayesian/GP; Mario más clásico + unsupervised + generative. **Ningún veto de método duro.**

---

## 3. Rubrica de scoring (para rankear ideas)

Pesos propuestos (suma 100):

| Criterio | Peso | Qué mide |
|----------|-----:|----------|
| Ambition / wow | 20 | ¿Sorprende a Molina y a un entrevistador? |
| Dataset quality | 15 | Real, documentado, no toy; multi-source bonus |
| Differentiability | 15 | ¿No es genérico de estudiante? |
| Pedro joy | 12 | Deeptech / física / space / robotics / weird |
| Mario joy | 12 | Finanzas innovadoras / recommenders / NLP / comparación limpia |
| Feasibility 6w | 12 | Proposal hoy + progress + report |
| Course articulability | 8 | ¿Se ve el temario? |
| Oral defendability | 6 | ¿Ambos pueden explicar cada línea? |

**Banda de ambición recomendada:** 7.5–9/10. Por debajo = genérico. Por encima = riesgo de no cerrar o no defender.

---

## 4. Catálogo de ideas (ambicioso)

Leyenda de scores: **A**mbition, **D**ataset, **P**edro, **M**ario, **F**easibility (0–10). **Score** = weighted rough.

---

### CLUSTER A — Aerospace / SSA / orbital (máximo overlap deeptech)

#### A1. ESA Collision Avoidance Challenge — predecir riesgo final de conjunción
- **Pitch:** Series temporales de CDMs (Conjunction Data Messages) reales de ESA; predecir el riesgo de colisión final a partir de CDMs truncados (setup del Kelvins challenge).
- **RQ:** ¿Qué familia de modelos (baseline lineal/trees vs NN sobre secuencias vs *survival*/hazard framing) mejor anticipa el riesgo final dos días antes del TCA, y qué features físicas dominan?
- **Datos:** [Zenodo ESA CA Challenge](https://zenodo.org/records/4463683); paper [arXiv:2008.03069](https://arxiv.org/abs/2008.03069). ~103 features/CDM, eventos con series.
- **Métodos:** logistic/regression baselines, RF/XGBoost, NN (MLP/seq), feature engineering orbital; opcional GP sobre riesgo; calibración de probabilidades.
- **Por qué ambicioso:** dataset de agencia espacial, problema operativo real, imbalance extremo, paper de competición citables, wow en entrevistas aerospace/ML.
- **Trade-offs:** +impacto +diferenciación; −desbalance severo, hay literature de winners (hay que aportar *ángulo propio*: uncertainty, interpretability, physics features).
- **Fit:** A9 D9 P10 M7 F8 → **TOP TIER**

#### A2. SOCRATES / CelesTrak conjunctions — tendencias de riesgo LEO
- **Pitch:** Analizar near-misses públicos (miss distance, Pc upper bound) y modelar régimen orbital / crecimiento de riesgo.
- **Datos:** [HF satellite-conjunctions](https://huggingface.co/datasets/juliensimon/satellite-conjunctions) (SOCRATES).
- **Métodos:** clustering de regímenes, supervised risk ranking, time-series.
- **Trade-offs:** +datos vivos/actualizados; −Pc es cota de screening no operacional; menos “challenge oficial” que A1.
- **Fit:** A8 D7 P10 M6 F7

#### A3. Hamiltonian / PINN orbital reconstruction (Kepler + datos reales RV/TLE)
- **Pitch:** Comparar NN vanilla vs PINN vs Hamiltonian NN en reconstrucción/extrapolación orbital; anclar a física (energía, momento angular) — *no* Burgers 1D.
- **Datos:** simulación controlada + NASA Exoplanet Archive RV / TLEs; refs tipo [PINN-Kepler](https://github.com/SwarnadeepSeth/Physics_Informed_NN-Kepler).
- **Métodos:** PyTorch PINN/HNN + baselines sklearn; métricas de conservación.
- **Trade-offs:** +alineado con ADN Molina (physics-informed) + Pedro joy máximo; −riesgo de parecer “demo PINN” si no hay dato real + story fuerte; Mario puede ver menos “producto”.
- **Fit:** A9 D6 P10 M6 F7 → **TOP si se ancla a dato real**

#### A4. CubeSat / satellite telemetry anomaly detection
- **Pitch:** Anomalías en telemetría (public cubesat / OPS-SAT si accesible) con unsupervised rico + supervised.
- **Trade-offs:** +aerospace; −encontrar dataset limpio etiquetado es el cuello.
- **Fit:** A7 D5 P9 M5 F5

#### A5. ADS-B aviation trajectories — anomaly / intent / congestion
- **Pitch:** Trayectorias abiertas ADS-B; clustering + predicción de desviaciones.
- **Trade-offs:** datos abundantes pero proyectos de estudiante frecuentes → hay que pillar ángulo (uncertainty, multi-airport transfer).
- **Fit:** A6 D8 P8 M6 F7

---

### CLUSTER B — Earth Observation / satellites imaging

#### B1. OSCD / Sentinel-2 urban change detection
- **Pitch:** Change detection multi-espectral Sentinel-2; comparar features clásicas + RF vs CNN siamesa ligera.
- **Datos:** [OSCD](https://ieee-dataport.org/open-access/oscd-onera-satellite-change-detection).
- **Trade-offs:** +EO real + multi-band; −24 pares (pequeño) → énfasis en metodología/generalización, no en SOTA.
- **Fit:** A7 D7 P9 M6 F8

#### B2. Wildfire / burnt area — Sentinel-1+2 fusion
- **Pitch:** Fusión óptico+SAR para burnt area; RF (como openEO example) vs boosting vs NN; importancia de SAR bajo nubes.
- **Datos:** Copernicus EMS + Sentinel vía CDSE; CLMS burnt area products.
- **Trade-offs:** +impacto clima + multi-source (valorado en brief); −pipeline EO pesado (cloud API, tiles).
- **Fit:** A8 D8 P8 M7 F6

#### B3. OPTIMUS-style change time series (subset)
- **Datos:** [OPTIMUS HF](https://huggingface.co/datasets/optimus-change/optimus-dataset) (~600k series; eval 300 labeled).
- **Trade-offs:** +escala moderna; −cómputo/storage; usar **subset** estricto.
- **Fit:** A8 D8 P9 M6 F5

---

### CLUSTER C — Physics-informed / materials / hard science (no bio)

#### C1. Matbench band gap — composition/structure → gap
- **Pitch:** Benchmark Materials Project; comparar featurization clásica + trees vs NN; uncertainty; error analysis por familia química.
- **Datos:** [Matbench](https://matbench.materialsproject.org/) (`matbench_expt_gap` 4.6k o `mp_gap` 106k).
- **Trade-offs:** +hard science + leaderboard citable + muy defendible; −menos “sexy aerospace”; Mario menos afinidad emocional; Pedro quantum/materials OK.
- **Fit:** A8 D9 P8 M5 F9 → **excelente plan B “nota alta segura-ambiciosa”**

#### C2. Learning conservation laws / Lagrangian NN on dynamical systems
- **Pitch:** Sistemas conocidos (pendulum, orbital, multi-body); comparar data-driven vs structure-preserving.
- **Trade-offs:** +teoría elegante; −fácil caer en toy; necesita dato/experimento real o al menos ruido medido.
- **Fit:** A8 D5 P10 M5 F6

#### C3. Quantum-inspired / classical ML on quantum chemistry surrogates
- **Pitch:** Predecir propiedades moleculares (QM9) con kernels/GPs vs NN; *sin* hardware cuántico.
- **Trade-offs:** “quantum” en el título es marketing si no hay ángulo claro; mejor Matbench o orbital.
- **Fit:** A7 D8 P9 M5 F7

#### C4. Grid / energy as dynamical system — ENTSO-E load & prices
- **Pitch:** Forecast multi-zona con régimen (spike prices), comparación models + uncertainty.
- **Datos:** [ENTSO-E snapshots HF](https://huggingface.co/datasets/hsilvosa/entsoe-day-ahead); OpenSTEF Liander 2024.
- **Trade-offs:** +clima/energía overlap; −forecasting eléctrico es común → ángulo: transfer entre zonas, extreme events, conformal prediction.
- **Fit:** A7 D9 P7 M7 F8

---

### CLUSTER D — Robotics / CyPhy-adjacent (sin lab access)

#### D1. Swarm / multi-agent coordination from public sim datasets
- **Pitch:** Predecir éxito de tarea / congestión / roles emergentes; unsupervised structure + supervised.
- **Inspiración CyPhy:** swarm line — pero datos de simulación pública (ARGoS/SwarmLab datasets, OpenAI Multi-Agent Particle si se reframa).
- **Trade-offs:** +encaje narrativo IE; −datasets fragmentados; RL full es peligroso para oral si nadie lo domina.
- **Fit:** A8 D5 P10 M7 F5

#### D2. Manipulation policy residual / success prediction on OXE **subset**
- **Pitch:** No entrenar VLA: predecir success/failure o next-action residual con features + small NN; BridgeData V2 subset.
- **Datos:** Open X-Embodiment subsets (Bridge, streaming GCS) — **nunca** full TB.
- **Trade-offs:** +robótica real; −infra TFDS/RLDS pesada; riesgo scope creep.
- **Fit:** A8 D7 P10 M8 F5

#### D3. “Robopreneur” economic peer — ML sobre decisiones de agentes económicos (inspirado RODEO)
- **Pitch:** Simular o usar datos on-chain/robot-economy proxies; clasificar estrategias sostenibles; recommender de “contratos”.
- **Trade-offs:** +única + IE story; −puede parecer hand-wavy sin datos sólidos; blockchain ≠ ML rigor.
- **Fit:** A9 D4 P9 M7 F4 → solo si construís dataset propio limpio en semana 1

#### D4. Perception uncertainty for robotics (depth/pose error) — vision
- **Pitch:** Calibración de incertidumbre de un estimator; trees vs NN vs temperature scaling.
- **Fit:** A7 D6 P9 M6 F6

---

### CLUSTER E — Finance innovador / VC / recommenders (anti-genérico)

#### E1. PHBench — Product Hunt launch → Series A
- **Pitch:** 67k launches, 0.78% positivos; predecir Series A en 18 meses; comparar LR/XGB vs embeddings de tagline vs LLM-zero-shot (como feature, no como prosa).
- **Datos:** [PHBench](https://phbench.com/) / [GitHub](https://github.com/ihlamury/phbench) / HF access.
- **Métodos:** class imbalance (focal, undersample, ranking metrics), trees, NN on text embeddings, calibration, lift@k.
- **Por qué NO genérico:** no es credit scoring ni stock price; es **VC deal-flow** con benchmark 2026, leaderboard, story de portfolio brutal.
- **Trade-offs:** +Mario joy + Pedro VC interest + portfolio; −extreme imbalance; acceso HF puede requerir request; leakage temporal hay que cuidarlo.
- **Fit:** A9 D9 P8 M10 F8 → **TOP TIER**

#### E2. VCBench — founder profiles → major success
- **Pitch:** 4.5k perfiles anonimizados; ML tabular + texto; F0.5 precision-oriented.
- **Datos:** [VCBench starter](https://github.com/Vela-Engineering/VCBench-Starter-Kit).
- **Trade-offs:** similar a E1; menor N; buen complemento o alternativa.
- **Fit:** A8 D8 P8 M10 F8

#### E3. Recommender de issues / repos open-source “where to contribute”
- **Pitch:** Matching developer→issue (o paper→code); collaborative filtering + content models.
- **Por qué:** Pedro mencionó OSS como signal CV; Mario likes recommenders.
- **Trade-offs:** +portfolio; −construir dataset lleva tiempo; cold-start.
- **Fit:** A7 D5 P8 M9 F5

#### E4. Earnings call NLP → short-horizon market move (con MUCHA cautela)
- **Trade-offs:** común + ethical/leakage; Pedro lo verá “visto”.
- **Fit:** A4 D7 P3 M8 F6 → **deprioritize**

#### E5. Limit order book microstructure ML
- **Trade-offs:** datos caros/complejos; genérico en quant shops.
- **Fit:** A6 D5 P5 M8 F4

#### E6. Systemic risk / financial network contagion
- **Pitch:** Grafos de correlaciones/holdings; unsupervised + supervised distress.
- **Trade-offs:** ambicioso; datos macro limitados.
- **Fit:** A8 D6 P6 M8 F5

---

### CLUSTER F — Abducción / “LLMs can't jump” / composición (Pedro curiosity × Mario NLP)

#### F1. SCAN add-jump — operacionalizar “can't jump”
- **Pitch:** Lake & Baroni SCAN: el split `addprim_jump` es literalmente el experimento “aprende jump aislado, ¿compone jump twice?”. Comparar seq2seq NN vs modelos clásicos (SVM sobre bag-of-ngrams, nearest neighbor en embedding space, kernel methods) y medir **dónde** falla la composición.
- **Datos:** [brendenlake/SCAN](https://github.com/brendenlake/SCAN).
- **Métodos del curso + stretch:** feature baselines, kernels, small RNN/Transformer, error analysis compositional.
- **Por qué ambicioso:** conecta filosofía/ML foundations con experimento controlado; oral espectacular si contáis bien la historia; paper ICML canónico.
- **Trade-offs:** +diferenciación intelectual; −dataset sintético (¿“real-world”? — argumentar: benchmark estándar de generalización, como ImageNet lo es para visión; brief acepta Kaggle/repos). Mario necesita ver comparación de modelos y análisis, no solo chat con GPT.
- **Fit:** A9 D7 P10 M8 F8 → **TOP TIER intelectual**

#### F2. SCAR — scientific analogy structure abduction
- **Pitch:** Benchmark de analogías científicas con structure abduction; embeddings + matching vs LLM few-shot (evaluación, no generación de prosa del report).
- **Datos:** SCAR (Findings EMNLP 2023).
- **Trade-offs:** +muy on-theme “abducción”; −NLP heavy; oral sobre embeddings/matching.
- **Fit:** A9 D7 P9 M9 F6

#### F3. CFQ / compositional QA divergence splits
- **Pitch:** Keysers et al. compound divergence; medir correlación accuracy vs compositional distance.
- **Trade-offs:** dataset grande; riesgo de ser “otro paper reproduction” sin twist.
- **Fit:** A8 D8 P8 M8 F6

#### F4. UniADILR — abductive vs deductive vs inductive OOD
- **Pitch:** Comparar generalización por tipo lógico.
- **Fit:** A8 D7 P9 M8 F6

#### F5. ARC-AGI lite
- **Trade-offs:** demasiado abierto/competitivo; difícil aportar en 6 semanas sin parecer toy.
- **Fit:** A7 D6 P8 M5 F3 → evitar como core

---

### CLUSTER G — Educación / movilidad / visión / wildcards

#### G1. Learning analytics — early warning (si datos institucionales/públicos)
- **Trade-offs:** Pedro 9 edu; ética/privacy; a menudo genérico.
- **Fit:** A5 D5 P8 M6 F5

#### G2. Urban mobility — bike/metro demand multi-source
- **Fit:** A6 D7 P7 M5 F7

#### G3. Music source separation / genre — solo si motivación hobby fuerte
- **Fit:** A5 D7 P5 M5 F6 → bajo

#### G4. Sport wearables — similarly low priority unless passion
- **Fit:** A5 D6 P5 M5 F6

#### G5. Contribuir ML a open-source científico (wrapper de project)
- **Pitch:** El “proyecto” es un análisis + PR a un repo (p.ej. mejora de baseline en PHBench o matbench notebook reproducible).
- **Trade-offs:** +CV signal Pedro; −grading puede no entender “PR” como deliverable — mejor como *bonus*, no como núcleo.
- **Fit:** A7 D8 P9 M7 F7 as bonus track

---

### CLUSTER H — Ideas locas / alta ambición / alto riesgo

#### H1. Multi-agent market + satellite weather → crop/insurance proxy
- Demasiado multi-hop para 6 semanas.

#### H2. Train a tiny world-model on embodied physics trajectories (subset HF)
- Cool; storage/compute risk.

#### H3. Detect “greenwashing” in ESG reports with classical+NN
- NLP+financiero; datos labeling difíciles.

#### H4. Soft-robot continuum dynamics learning
- Niche; datasets escasos.

#### H5. Philosophy argument mining + stance (Corpus of arguments)
- Solo si F-cluster no convence.

---

## 5. Matriz resumida (selección ~25 ideas principales)

| ID | Idea | Amb | Data | Pedro | Mario | Feas | Notas |
|----|------|----:|-----:|------:|------:|-----:|-------|
| A1 | ESA Collision Avoidance | 9 | 9 | 10 | 7 | 8 | ★★★ |
| E1 | PHBench Series A | 9 | 9 | 8 | 10 | 8 | ★★★ |
| F1 | SCAN “can't jump” | 9 | 7 | 10 | 8 | 8 | ★★★ |
| A3 | HNN/PINN orbital real | 9 | 6 | 10 | 6 | 7 | ★★ |
| B2 | Wildfire S1+S2 | 8 | 8 | 8 | 7 | 6 | ★★ |
| C1 | Matbench gap | 8 | 9 | 8 | 5 | 9 | ★★ plan B |
| E2 | VCBench founders | 8 | 8 | 8 | 10 | 8 | ★★ |
| B1 | OSCD change | 7 | 7 | 9 | 6 | 8 | ★ |
| C4 | ENTSO-E energy | 7 | 9 | 7 | 7 | 8 | ★ |
| D2 | OXE subset success | 8 | 7 | 10 | 8 | 5 | riesgo infra |
| F2 | SCAR abduction | 9 | 7 | 9 | 9 | 6 | NLP heavy |
| A2 | SOCRATES conjunctions | 8 | 7 | 10 | 6 | 7 | |
| D1 | Swarm coordination | 8 | 5 | 10 | 7 | 5 | CyPhy story |
| E3 | OSS issue recommender | 7 | 5 | 8 | 9 | 5 | |
| C2 | Conservative NN dynamics | 8 | 5 | 10 | 5 | 6 | toy risk |
| A5 | ADS-B aviation | 6 | 8 | 8 | 6 | 7 | algo visto |
| E4 | Earnings calls | 4 | 7 | 3 | 8 | 6 | genérico |
| G1 | Learning analytics | 5 | 5 | 8 | 6 | 5 | |
| D3 | Robopreneur economy | 9 | 4 | 9 | 7 | 4 | datos flacos |
| F5 | ARC-AGI | 7 | 6 | 8 | 5 | 3 | no |

---

## 6. Trade-offs por perfil

### Si maximizáis **Pedro (wow research / deeptech)**
1. A1 ESA CA  
2. F1 SCAN jump  
3. A3 HNN orbital  
4. B2 wildfire fusion  
Riesgo: Mario se desengancha si no hay story de “buen análisis + comparación”.

### Si maximizáis **Mario (original + data + models + finance/NLP)**
1. E1 PHBench  
2. E2 VCBench  
3. F1 SCAN (análisis sólido)  
4. F2 SCAR  
Riesgo: Pedro siente “fintech de siempre” si no destacáis rareza del benchmark VC / compositionality.

### Si maximizáis **nota segura articulable con temario**
1. C1 Matbench  
2. E1 PHBench (trees + calibration)  
3. B1 OSCD + RF  
4. C4 ENTSO-E  
Riesgo: Pedro path-fácil=0 → aburrimiento; compensar con uncertainty / physics features / multi-source.

### Si maximizáis **alineación con Molina sin bio**
Physics-informed + probabilistic + latent geometry:
- A3 HNN/PINN orbital  
- C1 Matbench + GP uncertainty  
- A1 con calibración bayesiana / GP  
- F1 con kernel methods + geometric view of composition  

### Si maximizáis **portfolio laboral**
- E1/E2 (VC)  
- A1 (aerospace ops)  
- B2 (EO climate)  
- E3 OSS recommender as side  

---

## 7. Ranking del autor de este brief (likes)

### Me gustan más (haría yo con vosotros)

1. **A1 — ESA Collision Avoidance**  
   Ambitious, real, rare, aerospace, model comparison natural, oral gold. Mario puede brillar en imbalance/metrics; Pedro en física orbital/features.

2. **E1 — PHBench VC**  
   Resuelve la tensión finanzas-de-Pedro: es innovador, benchmark fresco (2026), extreme class imbalance = ML serio, portfolio nuclear.

3. **F1 — SCAN add-jump / “LLMs can't jump” operacionalizado**  
   Intelectualmente más afilado; diferencia al grupo de 95% de projects; conecta curiosidad filosófica de Pedro con NLP de Mario. Cuidar argumentación “dataset real/relevante”.

4. **A3 — HNN/PINN orbital con ancla real**  
   ADN Molina sin bio. Solo si en la proposal ya fijáis dato real + baselines.

5. **B2 — Wildfire Sentinel fusion**  
   Impacto + multi-source. Feasibility media por pipeline EO.

### Me gustan con condiciones

- **C1 Matbench** — excelente craftsmanship, menos “boca abierta” en entrevista deeptech.  
- **E2 VCBench** — casi E1; elegid uno.  
- **F2 SCAR** — si queréis abducción más “research NLP”.  
- **B1 OSCD** — sólido, un poco más pequeño/clásico.  
- **D2 OXE subset** — solo con freeze brutal de scope día 1.

### Me gustan menos / evitar

- Earnings calls, credit scoring, house prices, sentiment Twitter, breast cancer, single-cell, Burgers PINN toy, full OXE/PhysInOne, ARC-AGI como core, Robopreneur sin datos, learning analytics genérico, stock prediction.

---

## 8. Arquitecturas de proyecto recomendadas (plantillas)

### Plantilla “Agency dataset”
Dataset de institución (ESA/Copernicus) → EDA fuerte → 3+ model families → uncertainty + limitations → impact paragraph.  
**Ejemplos:** A1, B2.

### Plantilla “Fresh benchmark”
Benchmark 2025–26 con leaderboard → reproduce baseline → beat with honest ablation → insight sobre qué features importan.  
**Ejemplos:** E1, E2, C1.

### Plantilla “Foundations experiment”
Benchmark cognitivo/ML foundations → hipótesis sobre generalización → comparación paradigmática (kernel vs NN) → discusión filosófica *acotada por evidencia*.  
**Ejemplos:** F1, F2.

### Plantilla “Physics structure”
Inductive bias físico → comparar con/without structure → conservación como métrica.  
**Ejemplos:** A3, C2.

---

## 9. Shortlist de decisión (próximo paso humano)

Discutid y elegid **1 primary + 1 backup** hoy (proposal):

| Priority | Primary candidates | Backup |
|----------|--------------------|--------|
| Deeptech aerospace | **A1** | A3 o B2 |
| VC/portfolio | **E1** | E2 |
| Intellectual wow | **F1** | F2 |
| Hard-science safe-ambitious | **C1** | C4 |

**Pregunta de desempate:** ¿Queréis que un entrevistador diga “hostia, ESA/espacio”, “hostia, VC real”, o “hostia, composición/abducción”? Las tres son ambiciosas; son *identidades* distintas.

---

## 10. Riesgos globales y open questions

1. **Proposal hoy:** hace falta RQ + dataset + EDA preliminar — elegir esta noche e ir a datos mañana temprano si no antes.  
2. **¿Contactar CyPhy?** Valioso como future work / consejo, peligroso como dependencia.  
3. **PHBench acceso HF:** verificar acceso inmediato.  
4. **Definición “real-world data”** para SCAN: preparar defensa (benchmark canónico de generalización).  
5. **Desacuerdo Pedro-Mario:** spike de 48h en top-2 y decidir con evidencia (estilo preferido en form).  
6. **RL / heavy DL:** ambos “me interesa”, pero oral-risk alto — usar como extensión, no como único pilar.  
7. **Fog del ledger:** rúbrica interna exacta de Molina desconocida → maximizar ambición *demostrable* + claridad.

---

## 11. Suggested phases

1. **Hoy:** elegir primary+backup; clonar datos; EDA plots para proposal; escribir RQ.  
2. **→ 25 Oct (progress):** baselines + 1 modelo avanzado + comparación preliminar.  
3. **→ 15 Nov (outline):** resultados casi finales + sentence outline.  
4. **→ 25 Nov:** report LaTeX BAM + GitHub historia real.  
5. **Sessions 27–28:** oral — ambos dominan pipeline completo.

---

## 12. Sources

### Repo / curso
- `project_ML_commskills_2026(1).pdf` — brief oficial deliverables/rúbrica  
- `SyllabusPDF_…pdf` — Molina profile, stack, sessions  
- `MachineLearning_IEUniversity (3).pdf` — paradigms, examples  
- `docs/partner-priority-form-spec.md`, `docs/decisions/001–006`, intake CSV (Pedro, Mario)

### Labs / IE
- https://cyphy.life/  
- https://www.ie.edu/school-science-technology/the-pulse/the-pulse-articles/ie-university-cyphy-life-periscope-future/

### Datasets / benchmarks
- ESA CA: https://zenodo.org/records/4463683 — arXiv:2008.03069  
- SOCRATES HF: https://huggingface.co/datasets/juliensimon/satellite-conjunctions  
- OSCD: https://ieee-dataport.org/open-access/oscd-onera-satellite-change-detection  
- OPTIMUS: https://huggingface.co/datasets/optimus-change/optimus-dataset  
- Matbench: https://matbench.materialsproject.org/  
- PHBench: https://phbench.com/ — https://github.com/ihlamury/phbench  
- VCBench: https://github.com/Vela-Engineering/VCBench-Starter-Kit  
- SCAN: https://github.com/brendenlake/SCAN  
- ENTSO-E HF: https://huggingface.co/datasets/hsilvosa/entsoe-day-ahead  
- Open X-Embodiment: https://github.com/google-deepmind/open_x_embodiment  

### Papers / themes
- Lake & Baroni SCAN (ICML 2018)  
- SCAR scientific analogies (EMNLP Findings 2023)  
- Compositional generalization CFQ (Keysers et al.)  
- UniADILR abductive/deductive/inductive (COLING 2025)

---

## 13. Fusión de subagentes (net-new)

Investigaciones en paralelo: robotics/CyPhy, satellite/EO, quantum/PINNs, fintech/VC, LLM-abduction, climate/vision/edu, Molina alignment, fit-matrix. Ideas **añadidas** tras fusionar:

### A6. OPS-SAT CubeSat telemetry anomaly detection (NEW ★★★)
- **Pitch:** Benchmark oficial ESA OPS-SAT-AD con anomalías etiquetadas por operadores; ~2.1k fragmentos; 30 baselines publicadas → “explicar/superar el benchmark”.
- **Datos:** https://zenodo.org/records/15108715 · https://github.com/kplabs-pl/OPS-SAT-AD · Nature Scientific Data 2025.
- **Métodos:** IsolationForest / OCSVM / RF features vs AE/LSTM-AE; interpretabilidad por canal; lead-time.
- **Fit:** Pedro 10 · Mario 8–9 · Feas **alta** (dataset pequeño).
- **Por qué sube al top:** aerospace puro + reproducible + papers citables + no genérico.

### A7. TrajAir — predicción social de trayectorias aéreas (NEW ★★)
- ADS-B + METAR, 111 días; comparar GP/boosting/seq NN vs constant-velocity.
- https://theairlab.org/trajair/
- Pedro 10 · Mario 6–7 · Feas alta.

### A8. ALFA UAV fault detection (NEW ★★)
- Telemetría real con 8 tipos de fault inyectados; CSV (sin ROS).
- https://theairlab.org/alfa-dataset/
- Unsupervised AE/PCA + supervised; calibración.

### D5. RODEO-flavored marketplace verification + recommender (refined ★★)
- Verificación de “proof-of-work” físico desde logs (voraus-AD / BotFails) + recommender robot↔tarea.
- Mejor balance Pedro/Mario que swarm sim puro; riesgo “gimmick” si el mercado es fake → protocolo + ablations.

### B4. YieldSAT multimodal crop yield (NEW ★)
- https://yieldsat.github.io/ — fusion S2+weather+soil; subset estricto.
- Mario climate alto; Pedro EO medio; storage risk.

### B5. Sen2Fire / SAR flood (NEW)
- Sen2Fire Zenodo; SEN12-FLOOD / S1GFloods — clima + física radar.

### Molina DNA (sin bio) — framing obligatorio en proposal
Pregunta plantilla: *“Given high-dim observations of a dynamical system, can we recover interpretable latent structure + parameters that a pure black-box misses?”*
- Ablation: hybrid vs no-physics vs no-latent.
- Preferir insight + UQ sobre SOTA.
- Fake ambition: Burgers toy PINN, 12 models sin tesis, transformer “porque SOTA”.

### Fit-matrix (proceso)
- Pedro veto genérico; Mario veto undefined/health; joint veto Feasibility <6.
- Effort shape: 20–30% research hook · 40–50% evaluation spine · 20–30% packaging.
- Check-ins frecuentes (preferencia Mario).

### Top tier actualizado (post-fusión)

1. **A1 ESA Collision Avoidance** o **A6 OPS-SAT-AD** (elegir uno SSA/spacecraft)
2. **E1 PHBench VC**
3. **F1 SCAN can't jump**
4. **A3 / Molina-orbital structured latent** (P1 del subagente Molina)
5. **D5 RODEO marketplace** (si queréis historia IE CyPhy + Mario recommender)

### Subagentes aún enriqueciéndose al cerrar este archivo
quantum/PINNs, fintech detalle, LLM-abduction, climate wildcards — revisar si aportan contradicciones; el núcleo de decisión ya está arriba.



## 14. Segunda fusión (quantum / abduction / climate wildcards)

### Physics / quantum (añadidos)
- **HNN/LNN + disipación/UQ** sobre péndulo real + dysts (mejor que Burgers toy) — top del cluster quantum.
- **MD17/QM9** energy–force surrogates con \(F=-\nabla E\) + UQ.
- **Circuit outcomes clásicos** (PennyLane/Qiskit sim → sklearn/NN) sin hardware.
- **Gravity Spy** solo con ángulo calibration/open-set (accuracy saturada).
- Evitar: Burgers-only PINN, Lorenz+LSTM único, Matbench clone sin UQ.

### Abducción / composición (añadidos)
- **SCAN + COGS/ReCOGS** como par (responde a “SCAN is solved”).
- **ART αNLI** con *hard split propio* = originalidad.
- **ARCT adversarial** (warrant recovery; accuracy ≠ understanding).
- ARC/LiveCodeBench: satélite, no spine.

### Climate / vision / edu wildcards (añadidos)
- **SolarCube** PV nowcasting (cloud motion) — climate×vision ambicioso.
- **WildfireSpreadTS** next-day spread multimodal (ojo: ~48GB).
- Educación: cross-course knowledge transfer / PEEK topics (si education es priority).
- Depriorizar mobility puro (Mario 5) salvo spice clima.

### Archivos de subagentes
Salidas completas en [`subagent-archives/`](./subagent-archives/).

### Cluster briefs dedicados (subagentes)
- [`research-brief-innovative-finance-vc-recommenders.md`](./research-brief-innovative-finance-vc-recommenders.md)
- [`research-brief-quantum-physics-ml-ideas.md`](./research-brief-quantum-physics-ml-ideas.md)
- [`research-brief-llm-limits-compositionality-abduction.md`](./research-brief-llm-limits-compositionality-abduction.md)

## 15. Cierre final de subagentes (net-new residual)

Confirmado por [Research LLM abduction](373e845a-bc1b-46fd-a2be-f7e0ef5712e6), [Research climate energy vision edu](0e433743-3336-43ba-9590-5f663219f0e7), [Research quantum physics PINNs](57fe02d3-5ae2-4f30-bb4b-39c51657b6ef), [Research innovative fintech VC](7a7a209b-12f8-4e0e-bc81-3ca2b4ad7390):

### Fintech (ángulo nuevo vs PHBench solo)
- **Founder ↔ investor matching recommender** — Open Funding Data / VCSheets / Form D; CF→embeddings→GNN opcional. Mejor joint Mario(rec)+Pedro(VC).
- **Polymarket calibration / mispricing** — Brier vs precio de mercado; no equity LSTM.
- Backup: Form D private-markets nowcasting.

### Climate/vision/edu (ángulo nuevo)
- **Fields of the World (FTW)** — domain generalization Europe→Africa field boundaries.
- **SolarCube** PV cloud-motion nowcasting (± Open Climate Fix PR stretch).
- **PTADisc / EdNet cross-course KT** si education es priority.
- WildfireSpreadTS solo si hay disco/GPU (≈48GB).

### Quantum/physics (ángulo nuevo)
- **HNN/LNN + disipación/UQ + conservation discovery** (péndulo real + dysts) > Burgers PINN.
- **MD17/QM9** force–energy consistency + UQ.
- **Circuit outcomes** clásicos sin hardware.

### Top band (sin cambio de veredicto; opción VC refinada)
1. ESA CA **o** OPS-SAT-AD  
2. PHBench/VCBench **o** founder↔investor matching  
3. SCAN+COGS **o** ART αNLI hard-split  
4. HNN/LNN structured-physics **o** orbital structured-latent  
5. FTW / SolarCube / RODEO-recommender según identidad deseada  

**Estado:** oleada de research **completa**. Decisión humana: primary + backup.

