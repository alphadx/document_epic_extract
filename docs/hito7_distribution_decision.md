# Hito 7 — Acta de decisión de distribución

Estado: **Propuesta de decisión lista para aprobación**  
Fecha objetivo de decisión: **2026-04-05**

## Contexto
Con release estable `v0.1.1` ya publicado en repositorio, Hito 7 exige decisión explícita del canal de distribución para evitar backlog indefinido de publicación.

## Opciones evaluadas

### Opción A — No publicar aún
- Pros: menor riesgo operativo inmediato.
- Contras: fricción para adopción externa vía `pip`.
- Cuándo elegirla: credenciales, ownership o proceso de soporte aún no listos.

### Opción B — Publicar en TestPyPI
- Pros: validación de packaging/distribución con riesgo controlado.
- Contras: canal no productivo para consumidores finales.
- Cuándo elegirla: primer ciclo de hardening de empaquetado.

### Opción C — Publicar en PyPI
- Pros: disponibilidad pública directa.
- Contras: mayor impacto ante errores de metadata/versionado.
- Cuándo elegirla: artefactos validados + owner/token + estrategia de soporte definida.

## Criterios de decisión (Go/No-Go)
- `python -m build` en verde.
- `twine check dist/*` en verde.
- Owner del paquete y credenciales verificados (preflight: `make publish-testpypi-preflight`).
- Plan de rollback/comunicación definido para incidentes de publicación.

## Estado actual de criterios
- Build de paquete (`python -m build`): **Cumplido (2026-04-05)**.
- Validación de artefactos (`twine check dist/*`): **Cumplido (2026-04-05)**.
- Owner/credenciales de publicación: **Pendiente**.
- Plan de rollback/comunicación: **Pendiente**.

## Recomendación actual
**Recomendado:** Opción A — **No publicar aún** con diferimiento controlado hasta disponer de credenciales/owner y ventana de comunicación.

**Bloqueadores para ejecutar upload:**
- Credenciales TestPyPI (`TWINE_API_TOKEN` o `TWINE_USERNAME`/`TWINE_PASSWORD`).
- Confirmación de owner responsable y ventana de comunicación.

**Fecha de reevaluación:** 2026-04-19 (o antes si se habilitan credenciales).

## Decisión final
- **Canal elegido:** No publicar aún en PyPI/TestPyPI (diferimiento controlado).
- **Responsable:** Release Manager (Equipo Core OmniExtract).
- **Fecha:** 2026-04-05.
- **Racional breve:** preservar control operativo hasta contar con credenciales/owner y ventana de comunicación; evitar publicación parcial.

## Evidencia requerida al cerrar
- Salida de comandos (`build`, `twine check`).
- Referencia a commit/tag asociado.
- Actualización de `README.md`, `plan.md` y `docs/milestone_decisions.md`.
