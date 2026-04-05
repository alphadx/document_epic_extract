# Política Operativa — Circuit Breaker Distribuido (multi-réplica)

Fecha: 2026-04-05  
Estado: Implementada (fases A/B/C completadas)
Owner: Equipo Core OmniExtract (API/Plataforma)

## 1. Objetivo

Definir una política operativa única para circuit breaker en despliegues con múltiples réplicas de API, evitando decisiones divergentes por instancia y reduciendo cascadas de fallos hacia proveedores LLM/OCR.

## 2. Alcance

Esta política aplica a:
- llamadas salientes de `llm_router`;
- llamadas salientes OCR cloud (AWS/GCP/Azure) cuando operen en modo SDK real;
- cualquier provider externo con riesgo de degradación transitoria.

No aplica a fallas de validación local de request (4xx de cliente).

## 3. Principios operativos

1. **Estado compartido**: el estado del circuito debe vivir en backend compartido (Redis) y no sólo en memoria local.
2. **Fail-fast controlado**: cuando un circuito esté abierto, rechazar temprano nuevas llamadas al proveedor afectado.
3. **Half-open con cupo limitado**: permitir reapertura gradual con un número bajo de solicitudes de prueba.
4. **Observabilidad obligatoria**: cada transición de estado debe emitirse con métrica + log estructurado.
5. **Configuración por proveedor**: thresholds y cooldowns ajustables por tipo de proveedor/modelo.

## 4. Modelo de estados

- **CLOSED**: operación normal.
- **OPEN**: se bloquean llamadas por ventana de enfriamiento.
- **HALF_OPEN**: se habilita un cupo de prueba; si falla, regresa a OPEN; si pasa, vuelve a CLOSED.

## 5. Claves y consistencia distribuida

## 5.1 Clave de circuito

Formato recomendado:

`cb:{provider}:{model_or_endpoint}`

Ejemplos:
- `cb:llm_router:gpt-4o`
- `cb:aws:textract`
- `cb:azure:prebuilt-invoice`

## 5.2 Campos mínimos por clave

- `state`: `closed|open|half_open`
- `failures`: contador de fallos en ventana
- `opened_until_ms`: timestamp epoch ms
- `half_open_tokens`: cupo de pruebas disponible
- `updated_at_ms`

## 5.3 Reglas de concurrencia

- Transiciones de estado deben hacerse con operación atómica (script Lua o transacción Redis).
- Réplicas no deben sobrescribir estado sin control de versión (`updated_at_ms`/CAS).

## 6. Umbrales iniciales (baseline)

Valores de arranque sugeridos (ajustables por proveedor):

- `failure_threshold`: 5
- `cooldown_ms`: 10000
- `half_open_max_calls`: 2
- `rolling_window_ms`: 30000

Ajustes por sensibilidad:
- Proveedores más inestables: reducir `failure_threshold` o aumentar `cooldown_ms`.
- Proveedores críticos de baja latencia: `half_open_max_calls=1` para minimizar ráfagas de reintento.

## 7. Clasificación de errores para contabilizar fallo

Contabilizan para abrir circuito:
- timeout,
- errores de autenticación transitoria (token vencido, revocación temporal),
- errores 5xx/provider unavailable,
- errores de red (connect/reset).

No contabilizan:
- validaciones 4xx causadas por payload del cliente,
- errores de contrato interno (schema parse) no atribuibles al proveedor externo.

## 8. Comportamiento en degradación

Cuando circuito esté OPEN:
- API responde error homogéneo con mensaje de indisponibilidad temporal de proveedor;
- se evita consumir cuota/costo en proveedor degradado;
- se recomienda fallback de modelo/proveedor alterno si está habilitado en el router.

## 9. Observabilidad mínima obligatoria

## 9.1 Métricas

- `cb_state{provider,key}` (gauge: 0 closed, 1 open, 2 half_open)
- `cb_open_total{provider,key}`
- `cb_reject_total{provider,key}`
- `cb_half_open_probe_total{provider,key,result}`

## 9.2 Logs estructurados

Evento por transición:
- `event=cb_transition`
- `provider`, `key`, `from_state`, `to_state`
- `reason` (timeout/auth/provider_error)
- `cooldown_ms`, `failures`

## 10. Runbook operativo

1. Verificar métricas de apertura/rechazo por provider.
2. Correlacionar con latencia y errores upstream.
3. Si OPEN persiste > 3 ventanas de cooldown:
   - activar proveedor alterno en configuración,
   - escalar incidente al owner de plataforma,
   - documentar postmortem con timestamps y causas.
4. Para cierre manual excepcional: ejecutar comando administrado con auditoría (quién/cuándo/por qué).

## 11. Plan de implementación incremental

### Fase A (rápida)
- Mantener store en memoria actual como fallback.
- Agregar interfaz de store con implementación Redis opcional.
 - Estado: **completada**.

### Fase B
- Activar Redis en entornos staging/prod.
- Añadir pruebas de concurrencia multi-réplica simulada.
 - Estado: **completada** (atomicidad + CAS + pruebas de concurrencia).

### Fase C
- Activar half-open con cupo y métricas completas.
- Ajustar umbrales con datos reales de operación.
 - Estado: **completada** (half-open con cupo + métricas + logs de transición).

## 12. Criterio de aceptación

Se considera implementada esta política cuando:
- exista store distribuido activo en despliegue multi-réplica,
- exista evidencia de pruebas de transición CLOSED→OPEN→HALF_OPEN→CLOSED,
- métricas y logs estén visibles en tablero operativo,
- runbook esté enlazado en documentación de release.

## 13. Evidencia de implementación (cierre 2026-04-05)

- Hito 1 (base/fallback): `docs/circuit_breaker_hito1_2026-04-05.md`.
- Hito 2 (atomicidad/CAS): `docs/circuit_breaker_hito2_2026-04-05.md`.
- Hito 3 (observabilidad/tablero): `docs/circuit_breaker_hito3_2026-04-05.md`.
- Hito 4 (cierre final): `docs/circuit_breaker_hito4_cierre_2026-04-05.md`.
