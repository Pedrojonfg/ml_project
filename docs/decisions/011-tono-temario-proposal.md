# 011. Tono del proposal respecto al temario

- **Status:** accepted
- **Date:** 2026-10-11
- **Tags:** product | process
- **Decided by:** human

## Context

A la fecha de la proposal, el curso solo ha cubierto material hasta **PCA**. Árboles, boosting, calibración, redes, etc. aún no se han visto. El proposal debe sonar ambicioso pero no como si el equipo ya dominara ese stack.

## Options considered

1. **Proposal como expertos** — métodos y roles fijados con certeza. Cons: poco creíble y rígido.
2. **Proposal solo con lo ya visto** — PCA + lineal como techo. Cons: mata ambición del project.
3. **Plan de aprendizaje + ladder** — declarar disposición a avanzar con el temario (y algo fuera si hace falta); métodos como hipótesis de trabajo, no commitments cerrados. Pros: honesto e implícitamente alineado al curso.
4. **Disclaimer explícito largo** — “no sabemos nada de X”. Cons: debilita el documento.

## Decision

Chose **opción 3**: tono de **plan** (ladder metodológica + hitos), con disposición a seguir el temario y estudiar lo necesario; **sin fingir dominio** ni congelar el papel exacto de cada técnica.

## Why

Input explícito del usuario: están dispuestos a avanzar, pero no pueden saber al 100% qué papel jugará cada cosa. Eso debe notarse *implícitamente* en el proposal (verbos, estructura por fases, “candidate methods”), no con un mea culpa.

## Consequences

- Redacción: “compararemos familias…”, “incluiremos calibración cuando dispongamos del material / estudio dirigido…”, no “nuestro LSTM siamesa batirá LRP”.
- Two-stage (008) y métricas (ledger) se mantienen como **diseño de evaluación** (eso sí se puede decidir ya); la implementación concreta de cada brazo se afina en W1–W4.
- Fog aceptado: ranking final trees vs NN vs lineal = resultado empírico, no promesa.
