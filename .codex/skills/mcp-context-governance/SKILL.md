---
name: mcp-context-governance
description: Definir gobierno de MCPs para mantener contexto saludable y acceso a fuentes externas sin degradar rendimiento. Usar cuando se habiliten MCPs, se investigue información externa o se requiera decidir qué servidores MCP activar por tarea.
---

# mcp-context-governance

## Objetivo

Usar MCPs con criterio: activar solo lo necesario para la tarea, minimizar ruido en contexto y asegurar trazabilidad de fuentes.

## Cuándo activar MCP

- Cuando se necesite información externa verificable (APIs, repos remotos, documentación oficial).
- Cuando reduzca pasos manuales repetitivos durante investigación o validación.
- Cuando el costo de contexto sea menor que el beneficio operacional.

## Cuándo desactivar MCP

- Si no aporta señal directa a la tarea actual.
- Si agrega demasiadas herramientas y degrada velocidad/calidad del razonamiento.
- Si duplica información ya disponible localmente en el repo.

## MCPs sugeridos por tipo de tarea

1. **Código/PR remoto**: MCP de GitHub.
2. **Investigación guiada**: MCP de búsqueda/documentación (solo dominios oficiales cuando aplique).
3. **Razonamiento paso a paso**: MCP de sequential-thinking para planes complejos.

## Política de uso

- Activar pocos MCPs por sesión (mínimo viable).
- Registrar en la respuesta final qué MCP se usó y para qué.
- Preferir fuentes primarias y acotar consultas por dominio/objetivo.
- Desactivar MCPs no usados al cerrar la tarea.

## Estado de uso de MCP

- MCPs incluidos en esta skill: **GitHub**, **búsqueda/documentación**, **sequential-thinking** (recomendados por patrón).
- Uso efectivo en este repositorio (al momento): **guía documentada**, **sin configuración MCP versionada dentro de `Skills/`**.
