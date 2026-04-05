# Acta de consistencia documental — Circuit Breaker Distribuido

Fecha: 2026-04-05  
Estado: Cerrada  
Owner: Equipo Core OmniExtract (API/Plataforma)

## Objetivo

Dejar una referencia única que alinee el estado del circuito breaker distribuido entre backlog, decisiones, avances de hitos y documentación operativa.

## Estado canónico (único)

- **Implementación:** completada.
- **Hitos:** 0/1/2/3/4 completados.
- **Riesgo técnico específico de circuit breaker:** cerrado.
- **Modo de operación actual:** monitoreo continuo y ajuste de umbrales por proveedor.

## Mapa de documentos fuente de verdad

1. **Política y diseño operativo (canónico técnico):**  
   `docs/circuit_breaker_distribuido.md`
2. **Evidencia por fases/hitos (canónico de ejecución):**  
   `docs/circuit_breaker_hito1_2026-04-05.md`  
   `docs/circuit_breaker_hito2_2026-04-05.md`  
   `docs/circuit_breaker_hito3_2026-04-05.md`  
   `docs/circuit_breaker_hito4_cierre_2026-04-05.md`
3. **Backlog actual (canónico de pendientes):**  
   `TODO.md` (circuit breaker fuera de deuda abierta y en cierres recientes)
4. **Estado ejecutivo de hitos (canónico de seguimiento):**  
   `docs/hitos_avances.md`
5. **Registro de decisiones (canónico de gobernanza):**  
   `docs/milestone_decisions.md`

## Regla de mantenimiento

Cuando cambie el estado operativo del circuit breaker:

1. Actualizar primero `docs/circuit_breaker_distribuido.md`.
2. Actualizar evidencia del hito/acta correspondiente.
3. Sincronizar `TODO.md`, `docs/hitos_avances.md` y `docs/milestone_decisions.md`.
4. Validar que `README.md` no contradiga el estado.

## Verificación de consistencia ejecutada

- Se verificó que el circuit breaker ya no aparece como deuda abierta en `TODO.md`.
- Se verificó que `README.md` lo reporta como cierre técnico reciente.
- Se verificó que `docs/hitos_avances.md` y `docs/milestone_decisions.md` no lo listan como pendiente.
- Se añadió verificador automatizable: `python scripts/check_circuit_breaker_consistency.py`.
- Se integró el verificador al gate `make release-readiness`.
- Se integró también al workflow CI (`.github/workflows/ci.yml`) vía `make cb-consistency`.
