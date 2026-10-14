# 009. Criterio de éxito del proyecto (ESA)

- **Status:** accepted
- **Date:** 2026-10-11
- **Tags:** product | research
- **Decided by:** human

## Context

El proposal necesita un claim de éxito que no dependa de batir el baseline LRP (solo 12/97 equipos lo hicieron en Kelvins) ni suene a análisis vacío. Depende de 007 (A+B) y 008 (two-stage + atlas).

## Options considered

1. **A** — Éxito = superar LRP en \(L\) / \(F_2\). Pros: claro. Cons: frágil.
2. **B** — Éxito = protocolo limpio + dashboard rare-events + two-stage/calibración + atlas; beat LRP = bonus. Pros: defendible y ambicioso en evaluación. Cons: hay que redactar ambición visible.
3. **C** — Igualar LRP con modelo interpretable + mejor calibración. Pros: conservador. Cons: poca señal de ambición.
4. **D** — Beat LRP **o** demostrar por qué no, con evidencia. Pros: flexible. Cons: puede parecer excusa.

## Decision

Chose **B**.

## Why

El usuario eligió B. Encaja con un estudio académico sobre el dataset ESA: la nota/oral premia rigor, calibración y failure modes; mejorar LRP es deseable pero no es la condición del claim.

## Consequences

- Proposal: objetivos medibles = reproducir baselines, bake-off, calibración, atlas; “intentamos mejorar LRP” como meta aspiracional.
- Si no se bate LRP, el entregable sigue siendo válido si el análisis es sólido.
- No prometer “deployment” ni “resolver colisiones en órbita”.
