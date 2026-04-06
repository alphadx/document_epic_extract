---
name: security-reviewer-lite
description: Ejecutar revisión de seguridad ligera en cambios de extracción documental y APIs. Usar cuando se modifiquen endpoints, manejo de archivos, integraciones OCR o configuración sensible.
---

# security-reviewer-lite

## Focos de revisión

1. Validación de entradas en endpoints de extracción.
2. Manejo seguro de archivos y contenido OCR.
3. Exposición accidental de secretos/tokens en código y logs.
4. Manejo de errores sin filtrar datos sensibles.
5. Dependencias nuevas con riesgo operativo.

## Guardrails

- No permitir secretos hardcodeados.
- No loggear payloads sensibles completos.
- Documentar cualquier riesgo residual con mitigación y dueño.
