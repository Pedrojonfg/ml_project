# 006. Vetos y preferencias de colaboración (sin constraints técnicos)

- **Status:** accepted
- **Date:** 2026-10-10
- **Tags:** product | survey
- **Decided by:** human

## Context

El compañero es un amigo; constraints de tiempo, nivel técnico y tipo de dato sobran. Sí interesa fricción social/temática: qué evitar y cómo trabajar juntos.

## Options considered

1. Nada más además de temáticas / prioridades / métodos.
2. Bloque constraints técnicos (horas, skills, datos, roles).
3. Bloque amplio (técnico + profe + dataset + estilo).
4. Ultra-mínimo: solo vetos + horas.
5. **Vetos + cómo preferiría trabajar** (sin bloque técnico) — propuesta del usuario.

## Decision

Chose **vetos + preferencias de colaboración**. Explicitamente **fuera del form**: horas/semana, nivel Python/sklearn/PyTorch, tipos de dato, roles técnicos, dataset público vs propio.

Incluir:

- Qué quiere evitar (vetos): texto libre + opcional multi-select de “no gracias” sobre dominios/métodos ya listados.
- Cómo preferiría trabajar: estilo de colaboración (sync/async, dividir vs hacer juntos, frecuencia de check-ins, cómo decidir si hay desacuerdo).

## Why

Entre amigos la viabilidad técnica se negocia fácil; los vetos y el estilo de trabajo son lo que realmente evita rozaduras y shortlists inútiles.

## Consequences

- Form más corto y personal.
- El research posterior no tendrá señal explícita de capacidad técnica/tiempo; se asume conversación offline si hace falta.
