# Plan de trabajo por tramos — TODO de prioridad media

Fecha base: 2026-04-05.

Este plan descompone los 3 ítems abiertos de prioridad media en tramos amplios y secuenciales.
Cada tramo termina con un punto de control para validar avance antes de pasar al siguiente.

## Alcance de trabajo

1. Implementar `FlanT5Adapter` (mini/base) y hardening de colas asíncronas del worker local.
2. Cerrar integración SDK cloud real (AWS/GCP/Azure) con pruebas de credenciales, timeout y proveedor caído.
3. Definir política operativa de circuit breaker distribuido para despliegues multi-réplica.

## Tramo 1 — Descubrimiento y diseño técnico (sin cambios de riesgo)

### Objetivos
- Confirmar arquitectura actual de adapters LLM y worker local.
- Definir contrato del nuevo `FlanT5Adapter` y su estrategia de fallback.
- Diseñar casos de prueba para colas asíncronas (concurrencia, backpressure, errores).
- Levantar matriz de escenarios cloud reales para AWS/GCP/Azure.
- Proponer borrador de política operativa de circuit breaker distribuido.

### Entregables
- Documento corto de diseño con decisiones y trade-offs.
- Lista de pruebas (unitarias/integración) que se agregarán por tramo.
- Lista de variables de entorno/configuración necesarias.

### Criterio de salida
- Diseño aprobado y alcance cerrado para implementación incremental.

## Tramo 2 — Implementación local (`FlanT5Adapter` + hardening worker)

### Objetivos
- Implementar `FlanT5Adapter` con soporte explícito para variantes mini/base.
- Integrar adapter al registro/ruteo existente.
- Endurecer colas asíncronas del worker local (reintentos acotados, límites de cola, manejo de cancelación/timeout).

### Entregables
- Código funcional en adapters/worker.
- Cobertura de pruebas unitarias para parser, adapter y cola.
- Ajustes de documentación técnica mínima de uso local.

### Criterio de salida
- Tests locales verdes para la parte local, sin regresiones en rutas existentes.

## Tramo 3 — Integración cloud real y resiliencia verificable

### Objetivos
- Completar pruebas de integración para AWS/GCP/Azure con:
  - credenciales válidas/ausentes,
  - timeout configurable,
  - caída simulada/real del proveedor.
- Homogeneizar manejo de errores y evidencia en logs.

### Entregables
- Suite de integración actualizada + evidencia de ejecución.
- Ajustes de configuración/documentación para entornos reales.

### Criterio de salida
- Evidencia reproducible de los 3 escenarios por proveedor (o evidencia explícita de limitación de entorno).

## Tramo 4 — Política operativa de circuit breaker distribuido

### Objetivos
- Definir política para multi-réplica: estado compartido, ventanas, umbrales y recuperación.
- Alinear la política con las decisiones de resiliencia existentes.
- Establecer runbook de operación y observabilidad mínima.

### Entregables
- Documento de política operativa versionado en `docs/`.
- Checklist operativo de despliegue.

### Criterio de salida
- Política aprobada y referenciada desde decisiones de hito.

## Tramo 5 — Cierre del TODO de prioridad media

### Objetivos
- Vincular evidencia en `TODO.md` y/o documentos de hito.
- Completar owner, fecha objetivo y evidencia por cada ítem medio.
- Verificar definición de done del backlog consolidado.

### Entregables
- TODO actualizado sin ambigüedades en prioridad media.
- Resumen final de cierre técnico-operativo.

### Criterio de salida
- Ítems de prioridad media cerrados o replanificados con fecha/owner/evidencia.

## Cadencia de interacción propuesta

Para avanzar “con cuidado”, usaremos control por etapas:
1. Yo ejecuto un tramo.
2. Te reporto evidencia y riesgos.
3. Te pido confirmación explícita para pasar al siguiente tramo.
