# 001. Canal del instrumento

- **Status:** accepted
- **Date:** 2026-10-10
- **Tags:** product | survey
- **Decided by:** human

## Context

Necesitamos recopilar prioridades del compañero (y luego las propias) de forma comparable, sin fricción innecesaria. El destino es cruzar respuestas e investigar proyectos.

## Options considered

1. **Solo mensaje** — preguntas en chat. Pros: mínima fricción. Cons: datos irregulares, difíciles de cruzar.
2. **Formulario web + intro** — Google Forms / Typeform + mensaje con link. Pros: datos estructurados. Cons: setup.
3. **Markdown/PDF rellenable** — portable en repo. Pros: versionable. Cons: más fricción.
4. **Form web + markdown dual** — misma estructura en dos sitios. Pros: flexibilidad. Cons: mantenimiento doble.

## Decision

Chose **formulario web** (opción 2). El usuario convertirá las respuestas a markdown a posteriori; no se mantiene un instrumento markdown paralelo como deliverable.

## Why

Prioriza tasa de respuesta y datos comparables. La conversión a markdown es un paso posterior del usuario, no del diseño del instrumento.

## Consequences

- Diseñar el cuestionario listo para Google Forms / Typeform (secciones, tipos de pregunta, opciones).
- Entregar también un mensaje corto de intro + link (placeholder).
- No invertir en app custom ni en versión markdown rellenable obligatoria.
