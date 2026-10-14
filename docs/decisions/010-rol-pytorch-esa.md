# 010. Rol de PyTorch en el proposal (ESA)

- **Status:** accepted
- **Date:** 2026-10-11
- **Tags:** tech | research
- **Decided by:** human

## Context

El curso usa sklearn + PyTorch; en datos tabulares/series CDM a menudo ganan trees. El equipo aún no ha visto redes en clase (solo hasta PCA). Hay que fijar qué promete el proposal sobre deep learning sin fingir expertise.

## Options considered

1. **A** — PyTorch como modelo principal del claim. Pros: ambición visible. Cons: frágil; contradice el nivel actual del curso.
2. **B** — PyTorch como ablación stretch bajo el mismo protocolo; resultado principal puede ser trees/GBDT + two-stage. Pros: señal de stack + honestidad. Cons: hay que redactarlo como plan, no como garantía.
3. **C** — Casi solo sklearn; PyTorch invisible. Pros: seguro. Cons: poca ambición técnica del syllabus.
4. **D** — Trees y NN como claims iguales. Pros: simétrico. Cons: diluye y exige más certeza de la que hay.

## Decision

Chose **B**.

## Why

El usuario eligió B y aclaró que, a estas alturas, todo lo posterior a PCA es desconocido: están dispuestos a adelantarse al temario para el proyecto, pero no pueden fijar al 100% el papel de cada método. PyTorch queda como brazo previsto de comparación, no como estrella asegurada.

## Consequences

- Proposal: ladder “baselines → modelos del temario (cuando se den) → stretch NN”; verbo = *planeamos / exploraremos*, no *demostraremos SOTA con LSTM*.
- Si NN no aporta, se reporta como ablación negativa (válido bajo criterio de éxito 009).
- Detalle de arquitectura PyTorch no se congela ahora.
