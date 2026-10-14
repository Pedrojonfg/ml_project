# 007. RQ primaria del proyecto ESA

- **Status:** accepted
- **Date:** 2026-10-11
- **Tags:** product | research
- **Decided by:** human

## Context

Hay que fijar el claim científico del proposal (~2 páginas) para ESA Kelvins Collision Avoidance, evitando “rehacer la competición” sin ángulo. Fuentes: user input (primary = ESA); `research/briefs/research-brief-esa-collision-avoidance-deep.md` §1 (RQ-A…D).

## Options considered

1. **A** — Bake-off: qué familia de modelos (lineal/trees vs sequence) mejora LRP en \(F_2\) / \(\mathrm{MSE}_{HR}\) y qué features físicas importan. Pros: curso-natural, factible. Cons: menos señal de originalidad.
2. **B** — Uncertainty-aware: distribución / \(P(\mathrm{HR})\) calibrada reduce FN en eventos “jump” vs LRP/GBDT. Pros: oral/UQ. Cons: más riesgo si el protocolo base no está sólido.
3. **A+B** — A primaria + B secundaria. Pros: nota + ambición. Cons: hay que acotar B.
4. **A+C** — A + curvas de lead-time (−4/−3/−2 d). Pros: ops-relevante. Cons: menos UQ explícita.
5. **C** — Solo lead-time / early warning. Pros: ángulo limpio. Cons: menos comparación de familias.

## Decision

Chose **A+B**.

## Why

El usuario eligió A+B. Encaja con el curso (comparación honesta vs LRP) y con ambición/oral (calibración e incertidumbre; Mario puede liderar esa mitad) sin diluir el problema en un segundo dataset.

## Consequences

- Proposal: RQ primaria = bake-off vs LRP + features; secundaria = uncertainty / calibración / “cuándo el modelo miente”.
- El diferenciador concreto (siguiente decisión) debe servir sobre todo a B, sin contradecir A.
- No claim de “ganar Kelvins” ni de despliegue en ESOC.
