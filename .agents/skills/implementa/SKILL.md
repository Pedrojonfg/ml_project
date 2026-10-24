---
name: implementa
description: >-
  Implementa todo lo ya decidido en paralelo cuando sea posible. Haz lista
  efímera de lo secuencial vs paralelizable, emite subagentes para lo paralelo,
  aplica principios ponytail, y pregunta ante cualquier duda. Usa cuando el
  usuario diga implementa, /implementa, implementa todo, ship it, o cuando
  diga que ya está decidido y quiere ejecución (no planificación).
disable-model-invocation: true
---

# Implementa

Ejecuta lo **ya decidido**. No replanifiques, no reabras diseño, no escribas
docs de plan en el repo. Si algo no está claro → pregunta y para.

**Anuncia al empezar:** "Usando `/implementa`."

## Mandato (verbatim)

implementa todo. haz una lista primero de lo que es paralelizable y secuencial
y emite subagentes para lo que sea paralelizable (así acabamos antes). no sé
si tienes que incluir tests o algo, en caso de que tengas que hacerlo, que un
subagente cree los tests y otro los resuelva para evitar que se creen solo
los tests que se saben resolver. si emites subagentes, evita opus 5, mejor
algún grok/composer/sonnet. si tienes cualquier duda, pregúntame.

## Ponytail (obligatorio)

Aplica los principios de `/ponytail` (full) en cada cambio y en cada prompt a
subagente. Si la skill `ponytail` está disponible, léela; si no, usa esta
escalera y para en el primer peldaño que aguante:

1. ¿Hace falta que exista? (YAGNI)
2. ¿Stdlib?
3. ¿Feature nativa de la plataforma?
4. ¿Dependencia ya instalada?
5. ¿Cabe en una línea?
6. Solo entonces: el mínimo código que funciona.

Reglas: sin abstracciones no pedidas, diff más corto, pocos archivos, alcance
quirúrgico, aburrido > clever. No simplifiques validación en boundaries,
seguridad, ni lo explícitamente pedido.

Marca simplificaciones deliberadas con `// ponytail: …` / `# ponytail: …`.

## Flujo

### 0. Dudas

Si falta una decisión que cambia el diseño, el contrato o el alcance →
**pregunta y espera**. No inventes. Máximo claridad, cero replanificación
espontánea.

### 1. Lista efímera (chat only)

Haz una lista corta de trabajo: qué es **secuencial** y qué es **paralelizable**.

- Muéstrala en el chat (texto o ASCII de dependencias).
- **NUNCA** la guardes en el repo ni en archivos del proyecto (nada de
  `TASKS.md`, `ROADMAP.md`, `plan.md`, checklists, ni scratch en disco).
- No commits de esa lista. Vive solo en el hilo.

Criterio de paralelizable: no comparte archivos conflictivos, no depende del
output de otra tarea, interfaces ya fijadas.

### 2. Ejecutar

1. Haz primero lo secuencial (tú o un subagente), en orden de dependencias.
2. Emite **varios subagentes en paralelo** (una sola tanda de `Task`) para
   todo lo paralelizable listo.
3. Integra resultados; repite waves si quedan frentes desbloqueados.
4. Si una tarea es trivial (pocos archivos, sin riesgo de colisión), hazla
   tú sin subagente — ponytail también aplica al proceso.

Cada prompt a subagente debe incluir: objetivo concreto, archivos/contratos
tocados, constraints ponytail, y qué devolver al padre (diff summary +
bloqueos).

### 3. Tests (solo si hace falta)

Decide si hay que testear:

| Situación | Acción |
|-----------|--------|
| Trivial / one-liner / pediste no tests | No tests (YAGNI) |
| El repo/CI ya exige tests para lo tocado | Sí |
| Lógica no trivial (rama, parser, dinero, seguridad) y no hay cobertura | Sí — el check más pequeño que falle si se rompe |
| El usuario pide tests / TDD | Sí |

Si hay que incluir tests:

1. **Subagente A (autor):** escribe los tests / checks a partir del contrato
   decidido. **No implementa** la feature. Entrega tests que fallen o queden
   rojos contra el código actual.
2. **Subagente B (solver):** recibe los tests ya escritos e implementa el
   mínimo para pasarlos. **No reescribe** los tests para hacerlos fáciles
   salvo bug obvio en el test (entonces reporta al padre).

Autor y solver = modelos distintos cuando sea posible. El padre no debe ser
quien invente tests y código en el mismo paso si se puede separar.

### 4. Cierre

- Verifica que lo decidido quedó hecho (tests/CI del proyecto si aplica).
- Respuesta corta al estilo ponytail: qué se hizo; qué se saltó y cuándo
  añadirlo. Sin ensayos ni tours de diseño.
- No abras PR ni commits salvo que el usuario lo pida.

## Modelos de subagente

Al emitir `Task` / subagentes:

- **Prohibido:** Opus 5 / cualquier slug `opus`.
- **Preferidos (elige de los disponibles en la sesión):** `grok-*`,
  `composer-*`, `claude-sonnet-*` (p. ej. `grok-4.7-high-fast`,
  `composer-2.5` / `composer-2.5-fast`, `claude-sonnet-5-5-high`).
- Si el usuario pide un modelo concreto listado → úsalo.
- Si un slug no está en la lista de la sesión → elige otro preferido; no
  reintentes el inválido.

Default razonable: `composer-2.5-fast` o `grok-4.7-high-fast` para
implementación; `claude-sonnet-5-5-high` si hace falta más rigor en el
autor de tests. Tipo: `generalPurpose` salvo que explore/búsqueda pura
encaje mejor.

## Anti-patrones

- Reabrir el diseño o “mejorar” el plan sin que lo pidan
- Escribir la lista paralelo/secuencial a disco
- Un solo subagente que escribe tests e implementación juntos
- Scaffolding “por si acaso”, deps nuevas evitables, refactor de vecinos
- Usar Opus 5 en subagentes
- Seguir con dudas sin preguntar
