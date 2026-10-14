# Spec: formulario de prioridades — proyecto ML (grupo)

**Curso:** Machine Learning · BAM · IE University · Prof. Nacho Molina  
**Uso:** mismo form para el compañero y para ti → export / convertir a 2 markdowns.  
**Herramienta sugerida:** Google Forms (secciones = páginas) o Typeform.

Basado en: syllabus (project 25%, datos reales, report tipo paper + oral), lecture notes (paradigmas), y decisiones en `docs/decisions/`.

---

## Mensaje de intro (copiar/pegar)

> Hey — para el project de ML quiero pillar bien qué te motiva antes de ponernos a buscar ideas.  
> Son ~8–10 min, todo en un form (nada de horas ni “nivel técnico”: eso ya lo hablamos).  
> Hay texto libre al principio para que te explayes sin filtros; luego escalas.  
> Link: [PEGAR_LINK]  
> Cuando lo tengas, yo lo relleno también y a partir de ahí investigamos opciones juntos.

---

## Config del form

| Setting | Valor |
|--------|--------|
| Idioma UI | Español |
| Recoger email | Opcional (o pregunta “Nombre”) |
| Una respuesta por persona | Sí |
| Progress bar | Sí |
| Secciones | 6 (ver abajo) |
| Escalas | Linear scale **0–10** (etiquetar 0 = nada / 10 = muchísimo), salvo donde se diga otra cosa |

**Pregunta 0 (todas las secciones):** Nombre o alias — Short answer, required.

---

## Sección 1 — Temáticas (texto libre)

*Sin menús todavía (evitar priming).*

1. **¿Qué temas, dominios o tipos de problemas te interesan para el project de ML?**  
   - Long answer · required  
   - Hint: “Puede ser vago (‘algo de salud’, ‘física’, ‘finanzas’) o concreto. No hace falta proponer el proyecto todavía.”

2. **¿Hay alguna idea a medias, dataset o paper que ya te dé curiosidad?**  
   - Long answer · optional  
   - Hint: “Si no, déjalo vacío.”

---

## Sección 2 — Interés por dominio (0–10)

*Página nueva. Enunciado:*  
“Aunque hayas escrito arriba, puntúa de 0 a 10 cuánto te interesa cada dominio como **contexto** del project (no como problema concreto).”

Usar **una pregunta linear scale por fila** (o grid si la herramienta lo permite).

| ID | Dominio | Por qué está en la lista |
|----|---------|---------------------------|
| D1 | Salud / biomedicina / omics | Ejemplos del curso + línea del profe |
| D2 | Neurociencia / comportamiento / cognición | Adjacent a bio + datos ricos |
| D3 | Clima / energía / sostenibilidad | Dominio aplicado clásico con datos abiertos |
| D4 | Finanzas / economía / riesgo | Demanda laboral + regresión/clasificación naturales |
| D5 | Física / ingeniería / sistemas dinámicos | Encaja con PINNs / modelos con estructura |
| D6 | Robótica / control / percepción | Escape ambicioso; a menudo híbrido |
| D7 | Computación cuántica / ML para ciencia “hard” | Mencionada como interés posible; niche |
| D8 | Texto / lenguaje / redes sociales (NLP) | Datos abundantes; fuera del core del temario |
| D9 | Imagen / visión / señales | Natural para redes; más allá de tabular típico |
| D10 | Movilidad / ciudades / logística | Problemas aplicados + series temporales |
| D11 | Deporte / rendimiento / wearables | Motivador, datos reales frecuentes |
| D12 | Educación / learning analytics | Impacto + datos institucionales/públicos |
| D13 | Música / audio / creativo | Motivación alta si encaja con hobbies |
| D14 | Metodológico / benchmarks (menos “dominio”, más método) | Si priorizan investigación de modelos |

3. **Otro dominio no listado (nombre + interés 0–10)**  
   - Short answer para el nombre + scale (o una sola long: “Dominio: X — 8/10”) · optional

---

## Sección 3 — Intención y definición de éxito (0–10)

*Página nueva. Separada a propósito de las temáticas.*

Enunciado: “Asumimos que queremos buena nota. Esto mide **hacia dónde** empujas el project.”

| ID | Escala (0–10) |
|----|----------------|
| P1 | Orientación **laboral / portfolio** (algo enseñable en entrevistas) |
| P2 | Orientación **investigación / profundidad teórica** |
| P3 | **Impacto real / aplicado** (que el problema “importe” fuera del aula) |
| P4 | **Aprendizaje técnico ambicioso** (salir de la zona cómoda) |
| P5 | Preferencia por un path **fácil de articular con el temario** (menos riesgo de nota) |

4. **Para ti, ¿qué sería un 10 en este trabajo de grupo?**  
   - Long answer · required

---

## Sección 4 — Fuera de temario y métodos (preferencia a priori)

*No fija el paradigma del proyecto; solo preferencias.*

5. **¿Cuánto estás dispuesto/a a estudiar material fuera del temario para este project?** (0–10)

6. **Techo de compromiso fuera de temario** — Multiple choice, required  
   - Solo leer blogs/docs/tutoriales cortos  
   - Implementar siguiendo tutoriales / repos existentes  
   - Leer papers e intentar reproducir ideas  
   - Intentar proponer / adaptar algo con sabor a investigación propia  

7. **Preferencia a priori por familia de métodos** — por cada fila:  
   *Me interesa* / *Me da igual* / *Preferiría evitar*  
   (Multiple choice grid)

| ID | Familia | Ancla |
|----|---------|--------|
| M1 | Modelos clásicos del temario (regresión, logistic, regularización, validación) | Core syllabus |
| M2 | Trees / random forests / boosting | Syllabus + labs |
| M3 | Kernels / SVM / kernel PCA | Syllabus |
| M4 | Redes neuronales feedforward / autoencoders (PyTorch del curso) | Syllabus Neural Methods |
| M5 | Probabilístico / Bayesian / Gaussian processes | Énfasis del curso + notas |
| M6 | Unsupervised “rico” (mezclas, embeddings no lineales, etc.) | Notas (más allá de k-means/PCA básico) |
| M7 | Deep learning “heavy” (CNN, transformers, pipelines grandes) | Escape frecuente |
| M8 | Physics-informed / modelos que respetan estructura física (PINNs, etc.) | Perfil investigación profe / escape |
| M9 | Reinforcement learning | Mencionado en notas; no núcleo del curso |
| M10 | Generative (VAEs, difusión, LLMs como modelo, etc.) | Notas: building blocks, no foco del curso |

---

## Sección 5 — Vetos

8. **¿Qué quieres evitar sí o sí en este project?**  
   - Long answer · required  
   - Hint: “Dominios, tipos de problema, estilo (‘otro Kaggle genérico’, ‘solo deep learning’, ‘nada de bio’…).”

9. **Marca dominios que serían veto duro** (aunque arriba hayas puesto interés medio) — Checkboxes, optional  
   - Misma lista D1–D14 + “Ninguno”

10. **Marca métodos que serían veto duro** — Checkboxes, optional  
    - Misma lista M1–M10 + “Ninguno”

---

## Sección 6 — Cómo preferirías trabajar

*Colaboración entre amigos; sin preguntas de horas ni skills.*

11. **Estilo de trabajo preferido** — Multiple choice  
    - Bastante juntos (pair / sesiones compartidas)  
    - Dividir partes claras y juntar  
    - Mixto según la fase  

12. **Ritmo de coordinación** — Multiple choice  
    - Check-ins frecuentes y cortos  
    - Bloques menos frecuentes pero más largos  
    - Flexible / según ruede  

13. **Si hay desacuerdo (tema, método, enfoque), ¿qué prefieres?** — Multiple choice  
    - Discutir hasta consenso  
    - Probar rápido un spike y decidir con evidencia  
    - Que uno lidere esa decisión y el otro apoye  
    - Otro (short text)

14. **Cualquier otra cosa que deba saber antes de buscar ideas**  
    - Long answer · optional

---

## Mapa de secciones (Google Forms)

1. Temáticas (libre)  
2. Dominios 0–10  
3. Intención / éxito  
4. Fuera de temario + métodos  
5. Vetos  
6. Colaboración  

Orden fijado en [003](./decisions/003-dimensiones-prioridad.md) y [002](./decisions/002-captura-tema-dominio.md): **temáticas antes que definición de éxito**.

---

## Después del form (fuera de scope; recordatorio)

1. Exportar respuestas → 2 markdowns (`partner.md`, `me.md`).  
2. Ahí sí: deep research / cruzar / shortlist / hablar la decisión final.

---

## Fuentes

- Syllabus ML-AM.2.S.A (project 25%, teams 2–3, real-world data, scientific-paper report + oral; stack Python/sklearn/PyTorch).  
- Lecture notes Molina: paradigmas (supervised/unsupervised/hybrid/RL bridge), ejemplos salud/single-cell/housing.  
- `docs/decisions/LEDGER.md` (001–006).
