# ESA Early Collision Risk — Plan de trabajo (Shape Up)

Ventana: mié 14 oct → mié 25 nov 2026 (Final Report) + oral (sesiones ML 27–28, fecha por confirmar)
Personas: **Pedro** y **Mario** (cada uno elige paquete) | Tipo: software + LaTeX, git (por crear)

Etiquetas: **[Book]** = Shape Up dice esto. **[Inference]** = adaptación mía (el libro no da fórmula de reparto para N personas ni habla de git).

---

## 1. Supuestos y preguntas abiertas

- **[Material]** Disponibilidad ≈ **7 h/semana por persona** para el proyecto (no lo dice nada del repo). Si es otra cifra, se reescala la sección 2 y el cut list, no las fechas.
- **[Material]** El repo **todavía no es git**. El enunciado exige GitHub público con "meaningful history" → se crea hoy (Fase 0). Sin esto se pierde nota de *Quality of Implementation*.
- **[Material]** La **plantilla BAM Project LaTeX** del final ("supplied with the assignment") no está en el repo (solo `bam-proposal.cls`). Conseguirla antes del 16 nov.
- Fecha exacta del oral sin confirmar (sesiones 27–28; probablemente finales nov / principios dic).
- Estimaciones en horas con etiqueta de confianza; las desconocidas son **appetite** (tope), no estimación **[Book ch02, ch12]**.

## 2. Appetite y capacidad

- Fijo: las 4 fechas del curso. Variable: scope. **Sin extensiones** (circuit breaker) **[Book ch07]**.
- Se trata como **3 mini-ciclos**, uno por entrega, cada uno con su ventana final reservada **[Inference]**:

| Ciclo | Ventana | Entrega | Build | Ventana final (sin scope nuevo) |
|---|---|---|---|---|
| C1 | 14 → 25 oct | Progress Report (2 pág., 5% ML) | 14–22 oct | 23–25 oct |
| C2 | 26 oct → 15 nov | Sentence Outline + resultados casi finales (20% ML / 40% CS) | 26 oct–10 nov | 11–15 nov |
| C3 | 16 → 25 nov | Final Report 10–12 pág. (20% ML / 40% CS) | 16–21 nov | 22–25 nov |
| Oral | 26 nov → sesión 27/28 | 10 min + 10 min Q&A (**50% ML**) | slides | 2 ensayos |

- Capacidad **[Inference]**: 2 personas × 6 semanas × 7 h × 0.85 ≈ **71 h**. Reserva de ventanas finales ≈ 20%. Experimentos ≈ 45 h, escritura + oral ≈ 26 h.

## 3. Problema, outcomes, no-gos

- Problema (ya cerrado en el proposal, ADR 007–016): con CDMs de time-to-TCA ≥ 2 d, ¿qué enfoque mejora a **LRP** en F₂ / MSE_HR? ¿Un **two-stage calibrado** caracteriza mejor los *jumps*?
- Must-have outcomes:
  1. Protocolo de validación por `event_id` (el test oficial solo para la evaluación final).
  2. ≥1 método del temario (logística / ridge) vs LRP bajo el mismo protocolo.
  3. Trees (RF/GBDT) vs LRP.
  4. Two-stage: P(HR) calibrada + magnitud, con reliability diagram.
  5. Atlas de fallos (jumps / FN duros) para paper y oral.
  6. Repo público reproducible con historia real; ambos saben explicar **todo** (en el oral se evalúa a cada uno).
- **No-gos**: ganar/replicar el leaderboard Kelvins; seleccionar modelos sobre el test oficial; deployment u operación; PHBench (ADR 015); conformal/intervalos completos; generar prosa con IA (prohibido por el enunciado §5.1: la IA ayuda a estructurar, el texto es vuestro); arquitectura NN como claim principal (ADR 010).

## 4. Rabbit holes y spikes

| Unknown | Por qué es riesgo | Resolución | Dueño | Timebox |
|---|---|---|---|---|
| Etiqueta de train y truncado | Train trae CDMs < 2 d; si se usa mal hay leakage | **Patch**: label = `risk` del último CDM del evento; inputs = solo CDMs ≥ 2 d; filtrar eventos como Uriot et al. (verificar en el paper) | dueño de S1 | dentro de S1 |
| Validación que se parezca al test | Train/test no i.i.d., mezcla de misiones distinta | **Spike**: GroupKFold por `event_id` + chequear que LRP en val da L parecido al test (~0.69). Si no, documentarlo como limitación, no perseguirlo | dueño de S1 | 2 h |
| Two-stage "funciona" | Nadie lo ha hecho; puede no ganar a LRP | **Cut back**: el éxito es caracterizar, no ganar (ADR 009). Empezar con logística + isotonic; GBDT se enchufa después | dueño de S6 | appetite 9 h |
| Métodos post-PCA no vistos aún | Trees (ses. 16–18), NN (22–26) llegan tarde | **Patch**: adelantarse con docs de sklearn; NN queda `~` | dueños S5/S8 | — |
| HR = 150 eventos en test | Métricas ruidosas, rankings inestables | **Patch**: reportar bootstrap / varianza entre folds, no un número solo | dueño de S4 (en `src/evaluation.py`, no en `metrics.py`) | 1 h |

## 5. Scopes (rebanadas verticales: datos → modelo → métrica → figura → párrafo)

| ID | Scope | Hecho = | Must/~ | h | Confianza | Depende de |
|---|---|---|---|---|---|---|
| S1 | **Protocolo de eventos** | `event_table` (1 fila/evento, label, inputs ≥2 d) + folds por evento + LRP/CRP en val + spike validación | Must | 6 | partial | — |
| S2 | **EDA profunda + taxonomía de jumps** | figuras misiones/imbalance; etiqueta `stable-low/stable-high/jump-up/jump-down` por evento | Must | 6 | known | datos crudos |
| S3 | **Features de evento** | latest CDM + deltas + agregados; función `build_features(event_table)` documentada | Must | 5 | known | S1 (contrato) |
| S4 | **Modelos del temario vs LRP** | logística (HR) + ridge/lasso (magnitud) [+ KNN] en folds; tabla vs LRP; bootstrap | Must | 6 | partial | S1, S3 (stub) |
| S5 | **Árboles vs LRP** | RF + GBDT tuneados; importancias; tabla | Must | 7 | partial | S1, S3 |
| S6 | **Two-stage calibrado** | P(HR) calibrada (isotonic/Platt) + regresor de magnitud; reliability diagram; F₂/MSE_HR vs single-stage | Must | 9 (appetite) | unknown | S1, contrato de modelos |
| S7 | **Atlas de fallos** | 5–10 casos (FN duros, jumps) con timelines CDM + qué modelo falla y por qué | Must | 6 | partial | S2, preds de S4–S6 |
| S8 | ~ **Ablación PyTorch** (MLP/secuencia) | misma tabla, mismos folds | ~ | 6 | unknown | S3 |
| S9 | ~ **Lead-time / leave-mission-out** | curva skill vs días a TCA o L por misión | ~ | 4 | partial | S1, S5 |
| S10 | ~ **Kernel ridge** (temario ses. 19–21) | fila extra en la tabla | ~ | 3 | known | S3 |
| S11 | **Repo reproducible** | README, script que regenera tablas+figs, MLA bib, Declaración IA (el entorno pinneado lo hace Pedro en Fase 0) | Must | 3 | known | — |

Escritura (cada dueño escribe la parte de lo que construyó; integrador une):

| ID | Entrega | Integrador (main.tex, formato) | Secciones |
|---|---|---|---|
| W1 | Progress Report (25 oct) | Mario | resultados S1/S3/S5 → Pedro; S2/S4 → Mario |
| W2 | Sentence Outline (15 nov) | Pedro | intro+data → Mario; method+results → Pedro; discusión → ambos |
| W3 | Final Report (25 nov) | Mario | cada scope = su subsección de Methods/Results; intro/conclusiones a medias |
| W4 | Oral | ambos | **cada uno presenta y defiende scopes del otro** en ensayos |

## 6. Dependencias

| Par | Clase | Manejo |
|---|---|---|
| S1 → S3/S4/S5/S6 | Shared foundation | S1 primero (Fase 0), un dueño |
| S3 ↔ S4/S5/S6 | Contract-coupled | contrato de columnas en `src/features.py` el día 1; antes usar stub = solo `latest risk` + 5 columnas |
| S4/S5 → S6 | Contract-coupled | interfaz común `fit(X,y)/predict_proba/predict`; S6 empieza con logística, enchufa GBDT luego |
| S4/S5/S6 → S7 | Strictly sequential (blando) | atlas lee `preds/<modelo>.parquet`; mientras, usa LRP + taxonomía de S2 |
| S2 ↔ S1 | Independent | S2 lee CSV directamente |
| main.tex | Hotspot | un integrador por entrega; secciones en archivos `\input{}` separados |

## 7. Fases y timeline

- **Fase 0 (mié 14 → sáb 17 oct)**, en paralelo **[Book ch10]**:
  - Pedro: `requirements.txt` + estructura `src/` + S1 (protocolo, folds, spike validación, regla de etiquetado) + propuesta de contratos (sección 9). (`git init` + GitHub: hecho el 14 oct.)
  - Mario: S2 EDA profunda + propuesta de definición de jump + esqueleto LaTeX del Progress Report.
  - Decisiones y reuniones (R0 kickoff, R1 contratos): ver [`dependencias-y-reuniones.md`](./dependencias-y-reuniones.md).
  - **Exit (sáb 17)**: primera rebanada integrada en `main`: logística sobre features stub, evaluada en folds vs LRP, números en `results/`. *Core, small, novel* **[Book ch10]**.
- **C1 build (dom 18 → jue 22 oct)**: Pedro → S3 + empieza S5. Mario → S4 (+ bootstrap). Merge continuo.
- **C1 final (vie 23 → dom 25)**: congelar tabla LRP vs logística/ridge vs RF/GBDT preliminar; escribir y entregar Progress Report.
- **C2 build (lun 26 oct → mar 10 nov)**: Pedro → S5 tuning + S7 atlas. Mario → S6 two-stage. `~` S8/S9/S10 solo si el dueño tiene su must cuesta abajo.
- **C2 final (mié 11 → dom 15 nov)**: resultados "casi finales" congelados; Sentence Outline.
- **C3 (lun 16 → mié 25 nov)**: 16–21 redacción por secciones; 22–25 integración, twocolumn, MLA, Declaración, link GitHub. **Desde el 18 nov: cero experimentos nuevos**, solo arreglar figuras.
- **Oral**: slides 26–28 nov; 2 ensayos con preguntas hostiles cruzadas.

Ruta crítica: S1 → S3 → S5/S6 → S7 → Results del Final Report.

## 8. Asignación (paquetes balanceados; cada persona elige uno)

| Paquete | Scopes | Carga (h, solo must) | Variedad | Buddy |
|---|---|---|---|---|
| **Pedro** | S1 Protocolo, S3 Features, S5 Árboles, S7 Atlas; integra W2 | 6+5+7+6 = **24** + escritura ~13 | infra de datos + modelo fuerte + narrativa oral | revisa S6 |
| **Mario** | S2 EDA/taxonomía, S4 Temario, S6 Two-stage, S11 Repo/bib; integra W1 y W3 | 6+6+9+3 = **24** + escritura ~13 | EDA + modelos del curso + la apuesta arriesgada (RQ secundaria) | revisa S1 |

- `~` S8/S9/S10 fuera de la carga: los coge quien tenga sus must cuesta abajo primero.
- Mario tiene el unknown principal (S6) → slack explícito (appetite 9 h) y Pedro como buddy **[Inference]**.
- Cada uno se reparte sus tareas dentro del scope; nadie hace de taskmaster **[Book ch09]**.
- Nadie espera al otro para empezar: Pedro arranca en S1, Mario en S2 (independiente).

## 9. Ownership map y reglas anti-colisión

| Área | Dueño | El otro puede |
|---|---|---|
| `src/protocol.py`, `src/metrics.py` (hoy `scripts/esa_kelvins_metrics.py`), folds | Pedro | leer; cambios vía PR pequeño |
| `src/features.py` | Pedro | pedir columnas |
| `src/eda/`, `src/taxonomy.py`, `src/evaluation.py` (bootstrap) | Mario | leer |
| `src/models/linear.py`, `src/models/two_stage.py` | Mario | leer |
| `src/models/trees.py`, `src/atlas/` | Pedro | leer |
| `requirements.txt` / env, `.gitignore` | Pedro | pedir dependencias |
| `report/<entrega>/main.tex` | integrador de esa entrega | editar solo su `sections/*.tex` |
| `data/` | nadie la commitea (`.gitignore`) | — |

- **Contratos a commitear antes de paralelizar (sáb 17)**: esquema de `event_table` (columnas + tipos), interfaz de modelo, formato `results/<modelo>.json` (= el de `prelim_results.json`), `preds/<modelo>.parquet` = `event_id, p_hr, r_hat, fold`.
- Ramas **[Inference]**: trunk-based, `scope/<id>-<nombre>`, vida ≤ 2–3 días, merge a `main` en cuanto funciona; `main` siempre ejecutable; merge de `main` en tu rama a diario.
- **PR revisado por el otro** = no es control de calidad, es el mecanismo para que ambos entiendan todo el código (el oral lo exige) **[Inference]**. Commits pequeños y frecuentes = historia creíble.

## 10. Checkpoints y seguimiento

| Fecha | Check | Pasa si | Si falla |
|---|---|---|---|
| sáb 17 oct | Fin Fase 0 | repo público + 1ª rebanada en `main` | Pedro y Mario en pareja hasta que salga; recortar features stub |
| jue 22 oct | Freeze C1 | tabla preliminar ≥3 modelos vs LRP | PR con lo que haya (logística + RF), no extender |
| mié 4 nov | Midpoint C2 | S6 y S5 **cuesta abajo** en el hill | S6 → cut back: solo logística calibrada + reliability; matar `~` |
| mar 10 nov | Freeze resultados | tablas/figuras finales regenerables con un comando | lo que no esté, va a *Future Work* |
| mié 18 nov | Freeze experimentos | — | ninguno nuevo |
| ensayo 1 | Comprensión cruzada | cada uno explica los scopes del otro sin notas | sesión de walkthrough de código |

- **Hill chart** **[Book ch12]**: en la sync (2×/semana, 15 min) cada uno coloca sus scopes: subiendo (aún averiguando) / bajando (solo ejecutar). Un punto que no se mueve en 3–4 días = mano levantada → partir el scope o pairing.

## 11. Cut list (en orden)

1. S10 Kernel ridge
2. S9 Lead-time / leave-mission-out
3. S8 PyTorch (el proposal lo dejó "si está justificado"; se reporta como trabajo futuro)
4. KNN dentro de S4 (queda logística + ridge)
5. Tuning fino de GBDT (dejar defaults razonables + 1 búsqueda pequeña)
6. Atlas reducido a 5 casos
- **Nunca se corta**: protocolo, comparación vs LRP, ≥1 método del temario, two-stage + calibración (RQ secundaria), historia git, Declaración de IA.

Preguntas para *scope hammering* **[Book ch13]**: ¿responde a una RQ? ¿sin esto el paper se sostiene? ¿se compara con el baseline (LRP), no con lo ideal?

## 12. Riesgos y notas

- LRP puede no batirse: ya está cubierto (ADR 009: el éxito es protocolo + calibración + atlas).
- 50% de la nota ML es el oral y evalúa comprensión individual → el reparto **no** puede convertirse en "cada uno sabe solo lo suyo". PRs cruzados + ensayo con preguntas cruzadas son obligatorios.
- IA: puede ayudar con código; **la prosa la escribís vosotros** y cada entrega declara herramienta, uso, modificaciones y verificación.
- **Del libro**: scopes verticales con un dueño, unknowns primero, una pieza integrada temprano, tiempo fijo / scope variable, sin extensión, hill chart, cortar `~` antes que must-haves, QA en los bordes.
- **Inferencias a validar**: 7 h/semana, 3 mini-ciclos por entrega, balance de 24 h por paquete, ramas trunk-based, PR cruzado como mecanismo de comprensión.
