# 008. Diferenciador de originalidad (ESA)

- **Status:** accepted
- **Date:** 2026-10-11
- **Tags:** product | research | method
- **Decided by:** human

## Context

Con RQ A+B (007), hace falta un ángulo propio para que el proposal no se lea como replay del leaderboard Kelvins 2019. Brief ESA §11 lista diferenciadores; el usuario pidió claridad de que usamos el dataset + RQ medianamente similar, no “replicar el concurso”.

## Options considered

1. **Two-stage + calibración** — cabeza \(P(\mathrm{HR})\) calibrada + regresor de magnitud. Pros: alinea con \(F_2\)+MSE_HR y con B. Cons: menos “ops timeline” que lead-time.
2. **Lead-time curves** — skill vs días a TCA. Pros: ops. Cons: solapa menos con UQ.
3. **Uncertainty intervals** — cuantiles/conformal. Pros: UQ fuerte. Cons: más carga en 6 semanas.
4. **Mission-OOD** — leave-`mission_id`-out. Pros: gap del paper. Cons: oral más niche.
5. **Failure atlas alone** — taxonomía de jumps/FNs. Pros: oral. Cons: débil como única contribución metodológica.

## Decision

Chose **1 + atlas oral**: two-stage (clasificación HR calibrada + regresión de magnitud) como diferenciador metodológico; atlas de fallos (jumps / FNs duros) como pieza narrativa del oral, no como RQ única.

## Why

El usuario eligió 1 tras entender las dos cabezas, más atlas para el oral. Encaja con A+B: bake-off de métodos en un protocolo honesto + calibración/incertidumbre sin pretender ganar Kelvins.

## Consequences

- Proposal claim: estudio académico supervised en dos etapas sobre CDMs ESA; baselines incluyen LRP; no “deployment ESOC”.
- Métodos candidatos (logreg, trees/GBDT, stretch NN) compiten bajo el mismo protocolo; “fancy” = comparación + calibración + análisis, no un único modelo mágico.
- Atlas: figuras/casos en oral y paper; no sustituye métricas.
- Lead-time / mission-OOD / intervals quedan backlog stretch, no claim principal del proposal.
