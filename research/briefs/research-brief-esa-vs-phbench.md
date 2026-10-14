# Research Brief: ESA Collision Avoidance vs PHBench
**Depth**: deep  
**Date**: 2026-10-11  
**Decision**: Pedro × Mario — shortlist final (2 opciones)

**Deep briefs individuales:**
- [`research-brief-esa-collision-avoidance-deep.md`](research-brief-esa-collision-avoidance-deep.md)
- [`research-brief-phbench-deep.md`](research-brief-phbench-deep.md)

## Executive Summary

Dos finalistas ambiciosas y no genéricas. Con peso oral (50%) + ambición (25%), **A (ESA) gana por margen estrecho pero real** (~72% confianza): dato listo, física/UQ alineada con Molina, Pedro a tope; Mario no “pierde” — lidera imbalance, calibración y “cuándo el modelo miente”. **PHBench** es excelente plan B / identidad VC, no un downgrade. Sin acceso HF confirmado esta noche, no puede ser primary.

## Side-by-side

| Criterio (1–10) | ESA CA | PHBench | Notas |
|-----------------|-------:|--------:|-------|
| Ambición / wow | 9 | 9 | Identidades distintas, no el mismo proyecto |
| Calidad / claridad datos | 9 | 8 | ESA Zenodo inmediato; PHBench gated |
| Factibilidad 6 semanas | 8 | 7–8 | PHBench: imbalance + leakage + HF |
| Afinidad Pedro | 10 | 8 | Espacio pleno vs VC innovador OK |
| Afinidad Mario | 7 | 10 | Ranking/finanzas natural en PHBench |
| Articulable con temario | 9 | 9 | Ambas: sklearn + PyTorch + calibración |
| Defendible en oral | 9 | 8 | ESA: física+UQ; PHBench: leakage/lift |
| Portfolio laboral | 9 | 10 | PHBench más puertas VC/product |
| Alineación Molina (insight/UQ/física) | 8–9 | 6–7 | A robá priors/calibración; B = ranking |
| Diferenciación vs genérico | 9 | 8 | A casi único en clase |
| Riesgo de verse genérico *(↑=peor)* | 2 | 4 | A solo si “XGB sin ángulo” |
| Riesgo de no poder empezar mañana *(↑=peor)* | 2 | 7 | **Clave**: acceso PHBench |

**Suma grosera:** A ≈ 86–88, B ≈ 82–84. Con peso oral+ambición → **A**.

## Opción A — ESA Collision Avoidance

### Problema (humano)
Avisos de “casi choque” en órbita (CDM) se actualizan durante días. Hay que anticipar el riesgo final **al menos 2 días antes** del máximo acercamiento para decidir si maniobrar.

### Datos
- Zenodo: https://zenodo.org/records/4463683  
- Kelvins data: https://kelvins.esa.int/collision-avoidance-challenge/data/  
- Train: 162 634 filas, 13 154 eventos (~12 CDMs/evento)  
- Test: 24 484 filas, 2 167 eventos  
- ~103 features; riesgo en log10  
- High-risk \(r \ge 10^{-6}\): ~**3.4%** train overall; test enriquecido ~**6.9%**  
- Umbrales misión típicos de maniobra: \(10^{-5}\)–\(10^{-4}\)  
- Paper: arXiv:2008.03069 · CC BY 4.0 · zip ~221 MB  

### Baselines fuertes
- Constante \(r=-5\): \(L\approx 2.50\)  
- Latest Risk Prediction (LRP): \(L\approx 0.694\) — **85/97 equipos no lo batieron** (solo 12/97)  
- Winners: reglas metric-aware (Honda/sesc) o LSTM siamesa para saltos low→high (Magpies) — no DL genérico  

### Ángulos de originalidad aún abiertos
1. Curvas de **early-warning** (calidad vs lead time)  
2. **Calibración** / uncertainty (no solo score de competición)  
3. Leave-`mission_id`-out (shift documentado)  
4. Features físicas + ablación  
5. Two-stage: clasificar high-risk + regresión de magnitud  
6. Analizar “jump events” que fallaron los top-10

### Riesgos
- Competición ya cerrada → no reinventar sin ángulo  
- Desbalance + test sesgado a high-risk  
- Pocas “fotos”; oral muy técnico  

## Opción B — PHBench (Product Hunt → Series A)

### Problema (humano)
Miles de lanzamientos públicos; ~1 de cada 127 acaba en Series A en 18 meses. Ordenar la cola semanal para no perder el tiempo.

### Datos
- Sitio: https://phbench.com/  
- GitHub: https://github.com/ihlamury/phbench  
- HF gated: https://huggingface.co/datasets/ihlamury/phbench  
- Acceso alternativo: email `benchmark@vela.partners` asunto `PHBench Data Access`  
- 67 292 launches; 528 positivos (0.78%)  
- Train/val/test: 47 071 / 6 753 / 13 468 (test labels privados)  
- 61 features; CC BY 4.0  
- Paper: arXiv:2605.02974  

### Métricas oficiales + champion
- Primaria: **F0.5** (prioriza precisión); también P@k, AP, lift  
- Champion (tree ensemble): test **AP 0.037** (~4.7× random), **F0.5 0.097** vs LR AP 0.024 / F0.5 0.045  
- Val metrics están **infladas** (best-of sobre ~53 positivos) — no cotizar val como logro  

### Trampas documentadas
- Fuga temporal en `maker_followers` (scrape 2026, no al launch)  
- Cohort 2025 parcialmente resuelto  
- Sesgo: PH featured ≠ universo startups  
- Datos públicos = **tabular anonimizado** (sin tagline/descripción cruda) → no pitch SBERT en week 1  
- Company-level grouping ya está en splits (bien)  

### Ángulos de originalidad
1. Framing **rank-the-weekly-queue** + lift@k / budget  
2. Ablation honesta de features con fuga  
3. Holdout temporal (train ≤2023, eval 2024–25) — future work de los autores  
4. Calibración anidada + curvas precisión-capacidad  
5. Topics / surface stats (no embeddings de texto crudo)  

### Riesgos
- **Acceso no inmediato** (HF gated + email)  
- Desbalance brutal  
- Leaderboard ya existe → no solo “subir XGB”  
- Oral: causalidad, ética, sesgo de plataforma  
- **Fallback si gate falla:** VCBench (~9% positivos, CSV más fácil) — no dual-core con PHBench  

## Escenarios de decisión

| Situación | Elegir |
|-----------|--------|
| Queréis identidad “espacio / ESA / deeptech” | **ESA** |
| Queréis identidad “VC / portfolio / ranking” | **PHBench** (si hay datos) |
| Proposal hoy y PHBench aún sin acceso | **ESA primary**, PHBench reserva |
| Mario debe brillar en métricas de negocio | **PHBench** *o* ESA con Mario en rare-events/UQ |
| Queréis maximizar alineación Molina (física/UQ) | **ESA** |
| Teméis parecer “otra competición Kelvins” | PHBench* o ESA con ángulo early-warning/calibración |
| Portfolio VC os importa más que wow espacial | **PHBench*** |

\*Solo con acceso a datos confirmado.

### Desempate de identidad (1 frase)
¿Queréis que digan *“hostia, ESA”* o *“hostia, VC real”*? No son el mismo proyecto con otro dataset.

## Híbridos / falsos compromisos a evitar

| Tentación | Por qué es mala idea |
|-----------|----------------------|
| ESA + PHBench en un solo proyecto | Dos RQs, oral diluido |
| Metáfora “Series A ≈ riesgo orbital” | Deck, no ciencia |
| Mitad-mitad “por equidad” Pedro/Mario | Equidad de **roles**, no de tema |
| Transformer “porque SOTA” como núcleo | Ambición falsa; oral risk |
| Explorar 3 datasets “y ya vemos” | Mata la proposal de 2 páginas |

**Compromiso sano:** un primary + un backup en 3 líneas + roles asimétricos claros.

## Recomendación (opinada)

**Default: A (ESA), backup B (PHBench).**  
**Confianza: ~72%** (el gap es de identidad/portfolio + acceso, no de “calidad intelectual”).

Vista disidente (~28%): si Pedro prioriza portfolio VC esta noche, o HF abre ya, o Mario necesita el dominio para no desengancharse → **B primary**.

Mario en ESA no es consolación: lidera imbalance, PR-AUC/F2, reliability diagrams y “cuándo el modelo miente al operador”.

## Checklist proposal (esta noche)

**Gates duros**
- [ ] Primary elegido (A o B)
- [ ] Backup en 3 líneas
- [ ] RQ falsable en una frase
- [ ] Dataset URL + “ya lo tenemos / request enviado”
- [ ] Unidad de análisis (A: evento; B: launch día 0)
- [ ] Métrica de rare events (no accuracy)
- [ ] Split sin filtrar futuro
- [ ] Ángulo propio ≠ reproducir winner
- [ ] Ancla temario (≥1 sklearn + 1 extensión PyTorch)
- [ ] Roles Pedro / Mario / oral

**Si A:** CDMs truncados → riesgo final; baseline LRP/trees; ablation física; early-warning o UQ.  
**Si B:** features solo al launch; lift@k / F0.5; anti-leakage; HF confirmado o fallback nombrado.

## Spike 48h (si empatáis)

| Ventana | ESA | PHBench |
|---------|-----|---------|
| 0–2h | Zenodo + schema + tasa high-risk | Request HF + email + % Series A |
| 2–6h | 3 plots (riesgo→TCA, miss distance, missingness) | 3 plots (imbalance, votes vs label, timeline) |
| 6–12h | Baseline event-level + 5 fallos | Baseline temporal + lift@50 + 5 fallos |
| 12–24h | 1 pág RQ + ángulo + riesgo oral | Idem + anti-leakage |
| 24–48h | Peer review cruzado → scorecard → voto | Idem |

**Reglas:** nada fancy; si B sin CSV a las 12h → B pierde el empate; criterio final = ¿defendible 20 min sin sudar?

## Sources
- https://zenodo.org/records/4463683  
- https://kelvins.esa.int/collision-avoidance-challenge/  
- https://arxiv.org/abs/2008.03069  
- https://phbench.com/  
- https://github.com/ihlamury/phbench  
- https://arxiv.org/abs/2605.02974  
- https://huggingface.co/datasets/ihlamury/phbench  
- Archive extract (agents): `research/briefs/subagent-archives/esa-phbench-agent-extract.md`  
