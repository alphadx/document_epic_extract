# Hito 7 — Checklist de ejecución y cierre (Post-release & Canal PyPI)

Última actualización: **2026-04-05 (arranque del hito)**

## Objetivo del hito
Cerrar el ciclo posterior al release estable `v0.1.1` con evidencia operativa de estabilidad y una decisión explícita de distribución (`sin publicación`, `TestPyPI` o `PyPI`) para no dejar tareas ambiguas.

## Alcance obligatorio (DoD de Hito 7)

### 1) Seguimiento post-release con señal objetiva
- [x] Consolidar ventana corta de observación post-release (mínimo 3-7 días) con incidencias y acciones (registro activo en `docs/hito7_risk_register.md`).
- [x] Verificar que API, demo y flujo local no reporten regresiones críticas de contrato (checks consolidados en `docs/hito7_cierre.md`).
- [x] Publicar registro de riesgos residuales y estado (`abierto`, `mitigado`, `aceptado`) en `docs/hito7_risk_register.md`.

### 2) Decisión formal del canal de distribución
- [x] Definir estrategia oficial: `No publicar aún`, `Publicar en TestPyPI`, o `Publicar en PyPI` (acta en `docs/hito7_distribution_decision.md`).
- [x] Si se elige publicación: validar credenciales/tokens, owner del paquete y naming definitivo (N/A por decisión actual de diferimiento de publicación).
- [x] Si se difiere publicación: documentar criterio de re-evaluación (fecha/trigger técnico).

### 3) Paquete y release hygiene
- [x] Ejecutar build reproducible del paquete (`python -m build`) y validar metadata (evidencia: `docs/hito7_packaging_validation.md`).
- [x] Ejecutar verificación de artefactos (`twine check dist/*`) (evidencia: `docs/hito7_packaging_validation.md`).
- [x] Adjuntar evidencia de comandos y resultados en documento de cierre del hito (`docs/hito7_cierre.md`).

### 4) Gobernanza documental de cierre
- [x] Actualizar `docs/milestone_decisions.md` con decisiones finales del hito.
- [x] Actualizar `README.md` y `plan.md` con estado final y próximo paso habilitado.
- [x] Publicar acta de cierre (`docs/hito7_cierre.md` o equivalente) con checks ejecutados.

## Avance técnico del hito
- [x] Estabilizado entorno de pruebas async con fallback en `tests/conftest.py` para ejecutar `pytest -q` aun cuando `pytest-asyncio` no esté cargado en el entorno.

## Riesgos a controlar en Hito 7
- Publicar paquete sin ownership/credenciales validadas.
- Confundir “release estable Git” con “distribución PyPI”.
- Cerrar hito sin evidencia de estabilidad post-release.

## Criterio para avanzar al siguiente hito
Hito 7 se considera cerrado solo cuando exista evidencia de seguimiento post-release, decisión explícita de canal de distribución y trazabilidad documental completa (README + plan + milestone decisions).
