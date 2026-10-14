# 002. Captura de tema / dominio

- **Status:** accepted
- **Date:** 2026-10-10
- **Tags:** product | survey
- **Decided by:** human

## Context

Hay que descubrir el espacio temático del compañero sin cerrar demasiado pronto ni perder comparabilidad al cruzar respuestas.

## Options considered

1. **Solo texto libre** — máxima libertad, difícil de cruzar.
2. **Solo menú cerrado** — fácil de cruzar, sesga.
3. **Menú multi-select + otro + top 3** — híbrido corto.
4. **Menú + escala 0–10 por dominio** — rico, más fatiga.
5. **Texto libre primero + escalas 0–10 después (páginas separadas)** — propuesta del usuario.

## Decision

Chose **texto libre unconstrained en página 1**, luego **página 2 con escalas 0–10** del tipo “¿qué problemas / dominios te interesan más?” por cada opción del menú (más “otro” si aplica).

## Why

El texto libre evita anclarse al menú; las escalas dan señal cuantitativa comparable para cruzar prioridades. Separar páginas reduce sesgo de priming del menú sobre el texto libre.

## Consequences

- El form tendrá al menos dos secciones/páginas: open-ended → ratings.
- Hay que definir la lista de dominios/problemas a puntuar (en el diseño final del form, anclada al curso).
- El “otro” del texto libre puede alimentar dominios no listados en el análisis posterior.
