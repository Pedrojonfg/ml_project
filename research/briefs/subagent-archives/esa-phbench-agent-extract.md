# Subagent Archive Extract: ESA · PHBench · Decision Comparison

**Extracted**: 2026-10-11  
**Rule**: facts below are taken only from the named agent transcripts (final assistant messages + research briefs those agents wrote). Nothing invented.

| Label | Transcript UUID | Status |
|-------|-----------------|--------|
| ESA | `192a71d3-fb58-4565-b770-5b59d1c57a61` | Completed; final chat + wrote `research/briefs/research-brief-esa-collision-avoidance-deep.md` |
| PHBench | `b436545a-5b07-46a1-95d4-99f53346d159` | Completed; final chat + wrote `research/briefs/research-brief-phbench-deep.md` |
| Comparison | `76d8cfd8-b107-4136-9d92-43846608586b` | Completed; full decision markdown in chat |

Parent chat: [`5bcdfed7-85f5-4d2a-ad46-7f4ffaf63f32`](5bcdfed7-85f5-4d2a-ad46-7f4ffaf63f32)

---

# PART A — ESA Collision Avoidance (Option A)

## A.0 Final assistant message (verbatim)

> Deep brief written to [`research/briefs/research-brief-esa-collision-avoidance-deep.md`](research/briefs/research-brief-esa-collision-avoidance-deep.md) (all 11 sections).
>
> **Headline:** Predict final collision risk from CDMs truncated ≥2 days before TCA. Data is real ESA ops (2015–2019), CC BY 4.0 on Zenodo (~15.3k events, 103 features/CDM). High-risk at \(10^{-6}\) is only ~**3.4%** overall (~**6.9%** in the enriched test set).
>
> **Trap:** the naive last-risk baseline (LRP) beat **85/97** teams. Winners leaned on metric-aware rules (Honda/sesc) or siamese LSTMs for low→high jumps (Magpies)—not generic deep learning.
>
> **Ambition that grades:** uncertainty / lead-time curves / leave-mission-out / two-stage HR classifier + magnitude regressor—not “we tuned XGBoost on Kelvins.”
>
> **Fit:** Pedro ~9.5 · Mario ~7.5–8 if he owns protocol, imbalance metrics, and calibration.

## A.1 Problem & RQs

- **Plain task:** From CDMs available **≥2 days before TCA**, predict the **final CDM risk** (log₁₀) at closest approach.
- **Unit:** close-approach **event** (`event_id`) = series of CDMs.
- **High-risk (competition):** \(r \geq 10^{-6}\); ops manoeuvre often \(10^{-5}\)–\(10^{-4}\).
- **Competition loss:** \(L = \mathrm{MSE}_{HR} / F_2\) (lower better).
- **Recommended RQs:**
  - **RQ-A:** Which model family beats LRP on \(F_2\) + MSE_HR, and which physical features drive gains?
  - **RQ-B:** Can uncertainty-aware models reduce FNs on “jump” events all top-10 missed?
  - **RQ-C:** How does skill degrade with lead time (−4d/−3d/−2d)?
  - **RQ-D (stretch):** Does leave-mission-out change method ranking?

## A.2 Dataset — numbers & access

| Item | Value |
|------|-------|
| Train | 162,634 CDM rows · 13,154 events · ~12 CDMs/event |
| Test | 24,484 rows · 2,167 events · ~11 CDMs/event |
| Full DB | 199,082 rows · 15,321 events · avg 13 (min 1, max 23) |
| Features | **103** columns/CDM |
| Years | CDMs **2015–2019**, anonymised |
| License | **CC BY 4.0** |
| Zenodo size | ~**221 MB** |
| DOI | 10.5281/zenodo.4463683 |

**URLs**
- Home: https://kelvins.esa.int/collision-avoidance-challenge/
- Data: https://kelvins.esa.int/collision-avoidance-challenge/data/
- Zenodo: https://zenodo.org/records/4463683
- Paper: https://arxiv.org/abs/2008.03069
- Scoring: https://kelvins.esa.int/collision-avoidance-challenge/scoring/
- Leaderboard: https://kelvins.esa.int/collision-avoidance-challenge/leaderboard/

**Imbalance (full DB 15,321 events)**

| Threshold | Events | Rate |
|-----------|-------:|-----:|
| \(r \geq 10^{-4}\) | 30 | 0.20% |
| \(r \geq 10^{-5}\) | 131 | 0.85% |
| \(r \geq 10^{-6}\) (HR) | **515** | **~3.4%** |

- **9,505** events have final risk \(\leq -30\) (log₁₀) — extreme low-risk mass.
- Eligible HR after filters: **216** of 515 → **150 test / 66 train**.
- Test HR rate ≈ **150/2167 ≈ 6.9%** (enriched).
- Paper FP/FN analysis: **150 positives / 2017 negatives** on test.

**Schema highlights:** `event_id`, `mission_id`, `time_to_tca`, `risk` (log₁₀); miss_distance, relative_speed, covariances, OD quality, space weather (`F10`, `AP`, …); target/chaser prefixes `t_`/`c_`.

## A.3 Baselines, winners, open angles

| Rank / baseline | Score \(L\) | Notes |
|-----------------|------------:|-------|
| CRP constant \(\hat r=-5\) | 2.5 | Weak |
| **LRP** (last known risk) | **0.694** | Beat by only **12/97** teams |
| 1 — sesc (Honda RI) | **0.556** | Metric-aware **rule cascade** |
| 2 — dietmarw | 0.571 | Best F₂ on Pareto with sesc |
| 3 — Magpies | 0.585 | Manhattan-LSTM siamese on 7 physics features |

- Competition: Oct–Dec 2019 · **96–97 teams** · **862 submissions**.
- Survey: 65% framed as **static**; 30% admitted test probing.
- Post-comp LightGBM residual \(h=r-r_{-2}\): ~**+1.27% F₂** vs LRP under their CV — fragile OOD.
- **11/150** HR events were FNs for **all top-10** (large jumps + high uncertainty).
- **Still open:** uncertainty-first models; lead-time curves; leave-mission-out; physics ablations; two-head HR classifier + regressor; controlled static vs sequence.

## A.4 Methods / metrics / 6-week plan (summary)

- **Ladder:** CRP/LRP → classical (logreg, RF, GBDT) + residual \(h\) → physics features → imbalance toolkit → PyTorch MLP/LSTM → uncertainty **or** lead-time **or** leave-mission-out.
- **Metrics:** \(F_2\), MSE_HR, \(L\); plus PR-AUC, recall@k, Brier/reliability, lead-time curves, leave-mission-out. **Not** accuracy / overall MSE.
- **W1** Zenodo + LRP reproduce · **W2** classical · **W3** physics + calibration · **W4** PyTorch fair compare · **W5** differentiator · **W6** polish + oral.
- **Roles:** Pedro = domain features / hard events / narrative; Mario = CV, metrics, calibration, comparison tables.
- **Recommended differentiators:** two-stage + lead-time curves; failure atlas as oral centerpiece.

## A.5 Fit, risks, ambition

| Dimension | Pedro | Mario |
|-----------|------:|------:|
| Aggregate | **9.5/10** | **7.5–8/10** |
| Domain passion | 10 | 7 |
| Data/comparison | 7 | 9 |
| Anti-generic | 10 | 7 |
| Oral | 9 | 8 |
| Feasibility 6w | 8 | 8 |

**Risks:** LRP bar; train≠test; tiny HR counts; manoeuvre selection bias; metric gaming; mission shift; Mario boredom if not given metrics ownership.

**Fake ambition:** architecture zoo, accuracy headlines, Autogluon without analysis, claiming ops readiness.

---

# PART B — PHBench (Option B)

## B.0 Final assistant message (verbatim)

> Deep research brief written to [`research/briefs/research-brief-phbench-deep.md`](research/briefs/research-brief-phbench-deep.md) (all 12 sections).
>
> **Verdict:** Strong yes for Pedro×Mario **if data access lands in week 0–1**. Ranking / deal-flow framing fits Mario; anti-generic VC story fits Pedro. Do **not** dual-core with VCBench.
>
> **Day-0 actions**
> 1. Request HF access: https://huggingface.co/datasets/ihlamury/phbench (gated, CC BY 4.0)
> 2. Email `benchmark@vela.partners` — subject `PHBench Data Access`
> 3. Clone https://github.com/ihlamury/phbench
>
> **Key facts**
> - 67,292 featured launches · 528 Series A ≤18mo · **0.78%** positives  
> - Splits: 47k / 6.7k / 13.5k (test labels private) · company-grouped stratification  
> - Champion test: AP **0.037**, F₀.₅ **0.097** (~4.7× random); val metrics are inflated  
> - Public data is **anonymized tabular** (no raw tagline/description) — don’t pitch SBERT week 1  
> - Documented leakage: maker follower counts scraped in 2026  
>
> **Best originality angles:** temporal holdout (authors’ own future work), nested calibration, lift@k budget metrics, follower ablation, one PyTorch tabular arm.
>
> **Fit:** Pedro ~8.5 · Mario ~9.5. **Backup:** VCBench (https://vcbench.com/, ~9% positives, easier CSV) only if PHBench gate fails.

## B.1 Problem & RQs

- **Task:** Featured Product Hunt launch → **Series A within 18 months**; ranking / deal-flow prioritization (~**1 in 127**).
- **RQ1:** Best precision-weighted ranking (AP, P@50/100) under official split **and** temporal holdout (train≤2023, eval 2024–25).
- **RQ2:** Do topics + surface text add lift beyond engagement/rank?
- **RQ3:** Calibration, leakage sensitivity, lift@k for fixed review budget.
- Optional: ML top-k vs LLM picks complementarity (~**6%** top-50 overlap on val; all TPs in that overlap).

## B.2 Dataset — access, splits, features

| Resource | URL |
|----------|-----|
| Site / leaderboard | https://phbench.com/ |
| Paper | https://arxiv.org/abs/2605.02974 |
| GitHub | https://github.com/ihlamury/phbench |
| HF (gated) | https://huggingface.co/datasets/ihlamury/phbench |
| Email access | `benchmark@vela.partners` subject `PHBench Data Access` |
| License | **CC BY 4.0** (~29.3 MB on HF) |

| Split | Posts | Positives | Rate | Labels |
|-------|------:|----------:|-----:|--------|
| Train | 47,071 | 372 | 0.79% | Public |
| Val | 6,753 | 53 | 0.78% | Public |
| Test | 13,468 | 103 | 0.76% | **Withheld** |
| **Total** | **67,292** | **528** | **0.78%** | |

- Split ~70/10/20 stratified on `year_bucket × topic_bucket × label`, **company-grouped** (`cb_permalink`), seed 42.
- Year buckets: pre_covid ≤2019; covid_boom 2020–21; vc_winter 2022–23; ai_era 2024–25.
- Official split is **IID across years**, not temporal — temporal holdout is authors’ **future work**.
- Public release: **61** engineered features (+ unused `maker_tier`); **no** product name/tagline/description/makers/CB fields/`days_to_series_a`.
- Strong signals (authors): daily rank (~**3.5×** lift top-3 day rank), votes×rank, maker followers (⚠ leakage), votes-per-comment, B2B, AI×year, reviews.
- **Leakage:** maker followers scraped ~2026; CB FN (~**12%** featured match rate); right-censoring 2025; featured-only (288k → 67k).

## B.3 Baselines / leaderboard

| Model | Val F₀.₅ | Val AP | Test F₀.₅ | Test AP |
|-------|---------:|-------:|----------:|--------:|
| Top-3 Ensemble (champion) | 0.284 | 0.126 | **0.097** | **0.037** |
| LR FS4 (official baseline) | 0.127 | 0.047 | **0.045** | **0.024** |
| Random | — | ~0.008 | — | — |

- Champion ≈ **4.7×** random on test AP; val inflated (best-of-144 on 53 positives).
- Trees + isotonic + `scale_pos_weight ≈ 125.5` dominate.
- Ops read: top-50 from ~2,400 quarterly posts → ~**5** true Series A (~**10%** precision).
- Authors: ML AP drops ~**42×** from 2021→2024 cohorts (regime story).

## B.4 Methods / 6-week / differentiators

- **Ladder:** reproduce LR/XGB → classical bake-off → imbalance/ranking → **temporal holdout** → topics/surface text + PyTorch tabular → nested calibration → error analysis.
- **Metrics:** AP/PR-AUC primary; F₀.₅; P@50/100; lift@k; ECE/reliability; bootstrap CIs. Avoid accuracy/macro-F1 as primary.
- **W0** access+proposal · **W1** EDA+leakage · **W2** classical · **W3** temporal+calibration · **W4** PyTorch · **W5** error analysis · **W6** report+oral.
- **Killers:** temporal holdout; lift@k budget metrics; follower ablation; nested calibration; PT vs trees; boom/bust regimes.

## B.5 Fit, risks, VCBench backup

| | Pedro | Mario |
|--|------:|------:|
| Overall | **8.5** | **9.5** |

**Blocker risk:** HF/email denial → pivot VCBench by end of week 1. **Do not dual-core.**

| | PHBench | VCBench |
|--|---------|---------|
| URL | phbench.com | https://vcbench.com/ |
| Paper | arXiv:2605.02974 | arXiv:2509.14448 |
| Label | Series A ≤18mo | Mega-success >$500M |
| N / rate | 67k / **0.78%** | 9k / **~9%** |
| Access | HF gate + email | Starter CSV (easier) |

**Ambition sweet spot cited:** 7.5–8.5 with Feasibility ≥7.

---

# PART C — Decision Comparison (A vs B)

## C.0 Final assistant message (verbatim)

# Decisión: ESA Collision Avoidance vs PHBench  
**Pedro × Mario · BAM ML · proposal hoy (~2 pág.) · horizonte ~6 semanas**

---

## 1. Tabla lado a lado

Escala 1–10. Lectura: **más alto = mejor**, excepto *Riesgo de verse genérico* (más alto = peor).

| Criterio | **A) ESA CDM risk forecasting** | **B) PHBench (PH → Series A)** | Notas |
|---|---:|---:|---|
| **Ambition** | **9** | **9** | Ambos en banda correcta (7.5–9). A = ops espacial real; B = benchmark VC fresco (2025–26). |
| **Dataset quality** | **9** | **8** | A: Zenodo ESA, documentado, acceso inmediato. B: ~67k launches / ~0.78% positivos, excelente si HF gate abre; si no, F baja. |
| **Feasibility 6w** | **8** | **7–8** | A más predecible (tabla+series). B: imbalance extremo + leakage temporal + posible delay HF. |
| **Pedro joy** | **10** | **8** | A = aerospace/SSA pleno. B = VC innovador (OK para Pedro), pero sin física. |
| **Mario joy** | **7** | **10** | B = finanzas + ranking/recommender. A: Mario brilla en métricas/desbalance, menos “su” dominio narrativo. |
| **Course articulability** | **9** | **9** | Ambos anclan sklearn (LR/trees/boosting) + PyTorch (MLP/seq o embeddings) + calibración. |
| **Oral defendability** | **9** | **8** | A: física + incertidumbre + “cuándo no usar el modelo” = oro oral (50%). B: defensa fuerte en leakage/lift@k; más fácil quedar en “black-box ranking”. |
| **Portfolio signal** | **9** | **10** | A: entrevistas aerospace/deeptech. B: VC/product/ops más amplio y “explicable en 30s”. |
| **Molina-alignment** | **8–9** | **6–7** | A robá ADN: priors físicos (miss distance, covarianza), UQ, insight mecánico. B es prediction/ranking limpio; insight = features, no física/latentes. |
| **Differentiability** | **9** | **8** | A casi único en clase. B anti-crédito/bolsa, pero “startup ML” es identidad más común fuera del aula. |
| **Riesgo de verse genérico** | **2** (bajo) | **4** (medio-bajo) | A: genérico solo si “XGBoost en CDMs sin ángulo”. B: genérico si parece credit scoring o “Predecir unicornios” sin rigor temporal. |

**Suma grosera (sin peso oral):** A ≈ **86–88**, B ≈ **82–84**.  
Con peso oral 50% + ambición 25%: **A gana por margen estrecho pero real.**

---

## 2. Escenarios: cuándo elegir A vs B

### Elegid **A (ESA)** si…
- Queréis que el oral suene a *sistema físico + incertidumbre + decisión operativa*, no a producto.
- Pedro necesita máxima energía 6 semanas (aerospace es su combustible).
- Queréis alineación Molina (priors, calibración, “insight > leaderboard”) sin tocar salud.
- Preferís **dato listo hoy** (Zenodo) vs gate HF.
- El pitch de 2 páginas puede decir: *“CDM parcial → riesgo final; ablations con/sin features físicas; PR-AUC + reliability.”*

### Elegid **B (PHBench)** si…
- La identidad de portfolio que queréis es **VC / early-stage / ranking**, no satélites.
- Mario debe liderar narrativa + definición de éxito + comparación limpia (su zona de excelencia).
- Confirmáis **acceso HF esta noche** (o tenéis VCBench CSV como plan B inmediato).
- Os emociona más *leakage control + lift@k + calibración de rare events* que covarianza orbital.
- Preferís historia de entrevista “product hunt → Series A” en fintech/ops/VC.

### Desempate de identidad (1 frase)
¿Queréis que digan *“hostia, ESA”* o *“hostia, VC real”*? No son el mismo proyecto con otro dataset: son marcas distintas.

---

## 3. Híbridos / falsos compromisos a evitar

| Tentación | Por qué es mala idea |
|---|---|
| **“ESA + PHBench en un solo proyecto”** | Dos dominios, dos RQs, oral diluido. Parece indecisión, no ambición. |
| **“PHBench features + embeddings satelitales / EO”** | Cosplay interdisciplinar sin mecanismo compartido. |
| **“Collision risk como analogía de Series A”** | Metáfora de deck, no ciencia. Molina la olfatea. |
| **Mitad aerospace + mitad VC “por equidad Pedro/Mario”** | Equidad de roles ≠ equidad de tema. Mejor: un tema + roles asimétricos claros. |
| **Añadir VCBench + PHBench + Crunchbase** | Scope explosion; ToS/leakage landmine. |
| **Transformer “porque SOTA” en CDMs o taglines** | Oral risk alto; ambición falsa. Extensión mínima, no núcleo. |
| **OPS-SAT + ESA + PHBench “exploramos y ya vemos”** | Matáis la proposal de 2 páginas. Primary + backup, no zoológico. |

**Compromiso sano (sí):** un primary, un backup documentado en 3 líneas, roles fijos (quién lidera data / models / oral Q&A).

---

## 4. Recomendación

### Veredicto: **A — ESA Collision Avoidance**  
**Confianza: 72%** (no 90%: el gap es de identidad/portfolio, no de calidad).

**Por qué (opinión):** Con ambición 25% y oral 50%, A maximiza lo que el curso *paga*: dataset institucional, problema raro, story física defendible, ADN Molina (priors + UQ + comparación honesta), y Pedro a tope sin vetar a Mario. Mario no “pierde”: lidera imbalance, calibración, PR-AUC, reliability diagrams y la parte “cuándo el modelo miente al operador” — eso es nota alta, no consolación.

PHBench es **excelente plan B / identidad alternativa**, no un downgrade intelectual. Pierde ligeramente en Molina-alignment, riesgo de gate HF, y en que Pedro se aburra a la semana 3 si el proyecto se vuelve “tabular + texto + lift”.

### Vista disidente (28%)
Si esta noche Pedro dice en serio “el portfolio VC me importa más que el wow espacial”, o el acceso Zenodo/ESA se atasca, o Mario necesita el dominio para no desengancharse: **B gana**. En ese mundo, A se vuelve el backup. Un disenso fuerte también aplica si queréis maximizar *señal laboral genérica* (más puertas VC/product) sobre *señal deeptech*.

---

## 5. Checklist de decisión — esta noche (proposal)

Marcad **sí/no** en orden; no avanzéis si falla un gate duro.

**Gates duros**
- [ ] ¿Primary elegido? (A o B — una letra)
- [ ] ¿Backup escrito en 3 líneas? (el otro, u OPS-SAT / VCBench)
- [ ] ¿RQ en una frase falsable?
- [ ] ¿Dataset URL + “ya lo tenemos / request enviado”?
- [ ] ¿Unidad de análisis clara? (A: *evento* de conjunción; B: *launch* el día 0)
- [ ] ¿Métrica primaria de rare events? (PR-AUC / recall@k / Brier — no accuracy)
- [ ] ¿Split que no filtre futuro? (A: por evento/TCA; B: temporal estricto)
- [ ] ¿Ángulo propio ≠ “reproducir winner del challenge/benchmark”?
- [ ] ¿Ancla temario explícita? (≥1 sklearn + 1 extensión PyTorch justificada)
- [ ] ¿Roles: Pedro / Mario / oral joint?
- [ ] ¿Veto salud respetado? (trivial aquí, pero confirmd)
- [ ] ¿Proposal ≤2 páginas, prosa humana, sin relleno AI?

**Si primary = A — rellenar en la proposal**
- [ ] Predicción: riesgo *final* desde CDMs *truncados* (ej. 2 días antes TCA)
- [ ] Baseline: logística/RF/boosting en features agregadas
- [ ] Stretch: seq model pequeña **o** GP/calibración — no ambos como must
- [ ] Ablation: con/sin features físicas (miss distance, covarianza, proxies Pc)
- [ ] Limitación: imbalance + papers de competición → vuestro ángulo es early warning + UQ

**Si primary = B — rellenar en la proposal**
- [ ] Solo features disponibles *al launch*
- [ ] Baseline popularidad (votos/rank) vs LR/XGB vs texto
- [ ] Métrica: lift@k / precision@budget de sourcing
- [ ] HF access confirmado **o** fallback VCBench nombrado
- [ ] Disclaimer: no es consejo de inversión; ranking empírico con error

---

## 6. Si hay empate: protocolo spike 48h

Objetivo: **decidir con evidencia**, no con gusto abstracto. Cada uno lidera un spike; el otro revisa.

| Hora | A — ESA | B — PHBench |
|---|---|---|
| **0–2h** | Descarga Zenodo; schema CDM; contar eventos vs filas; tasa de “alto riesgo” | Request HF + clone repo; schema; % Series A; verificar labels train |
| **2–6h** | 3 plots: evolución de riesgo hacia TCA; hist miss distance; missingness | 3 plots: imbalance; votes vs label; timeline de launches |
| **6–12h** | Baseline sklearn event-level; PR-AUC; 5 fallos legibles | Baseline LR/XGB temporal split; lift@50; 5 fallos legibles |
| **12–24h** | 1 página: RQ + ángulo propio + riesgo oral | 1 página: RQ + anti-leakage + riesgo oral |
| **24–36h** | Peer review cruzado (Mario revisa A, Pedro revisa B) | Idem |
| **36–48h** | Scorecard 10 min (misma rúbrica §1) → **voto**; si empate, gana quien tenga **dato end-to-end + plot en proposal** |

**Reglas del spike**
1. Nada de arquitectura fancy; solo EDA + 1 baseline + narrativa.
2. Si B no tiene acceso a datos a las 12h → **B pierde el empate automáticamente**.
3. Si A no produce un plot interpretable de secuencia CDM → A pierde.
4. El criterio final no es “más accuracy”: es **¿podemos defender esto 20 minutos sin sudar?**

---

### Cierre (una línea para esta noche)

**Default: A (ESA), backup B (PHBench).** Escribid la proposal de A; dejáis B como párrafo “alternativa si…” solo si aún dudáis — mejor ni mencionarlo en el PDF y guardarlo en el ledger interno.

---

# PART D — Cross-source decision numbers (quick reference)

| Number | Source | Meaning |
|-------:|--------|---------|
| **72%** | Comparison | Confidence for primary = ESA |
| Score sum ~**86–88** vs **82–84** | Comparison | A edges B |
| LRP \(L=0.694\); only **12/97** beat it | ESA | Hard baseline |
| HR ~**3.4%** overall / ~**6.9%** test | ESA | Imbalance |
| **15,321** events · **103** feats · Zenodo CC BY | ESA | Dataset |
| **0.78%** Series A · **67,292** launches | PHBench | Imbalance |
| Champion test AP **0.037** / F₀.₅ **0.097** | PHBench | SOTA bar (~4.7× random) |
| LR test AP **0.024** / F₀.₅ **0.045** | PHBench | Official baseline |
| Pedro ESA **9.5** / PHBench **8.5** | Both briefs | Fit |
| Mario ESA **7.5–8** / PHBench **9.5** | Both briefs | Fit |
| VCBench ~**9%** positives | PHBench §12 | Backup if HF fails |

**Full deep briefs (agent Write outputs):**
- `research/briefs/research-brief-esa-collision-avoidance-deep.md`
- `research/briefs/research-brief-phbench-deep.md`
