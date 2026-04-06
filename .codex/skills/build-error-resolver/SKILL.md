---
name: build-error-resolver
description: Resolver fallos de build, lint o tests con cambios mínimos y verificables. Usar cuando falle CI local/remota o aparezcan errores tras refactors.
---

# build-error-resolver

## Protocolo

1. Reproducir error con comando exacto.
2. Aislar causa raíz al archivo o módulo mínimo.
3. Corregir con diff pequeño y sin mezclar mejoras no relacionadas.
4. Reejecutar el mismo comando y registrar resultado.
5. Correr chequeo adyacente para evitar regresión inmediata.

## Regla de oro

- Corregir primero estabilidad; optimizaciones o limpieza van en PR separado.
