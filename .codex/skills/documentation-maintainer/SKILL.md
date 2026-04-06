---
name: documentation-maintainer
description: Mantener y reorganizar documentación técnica y de producto de este repositorio. Usar cuando pidan actualizar README, ordenar docs/, consolidar pendientes en TODO.md, o alinear documentación con cambios en API, pruebas, releases e hitos.
---

# documentation-maintainer

## Ejecutar este flujo

1. Revisar `README.md`, `docs/README.md`, `TODO.md` y archivos nuevos en `docs/`.
2. Separar contenido por nivel:
   - Producto y navegación rápida en `README.md`.
   - Procedimientos técnicos, contratos y troubleshooting en `docs/`.
   - Pendientes accionables en `TODO.md`.
3. Mantener trazabilidad: cada tarea o decisión relevante debe enlazar su documento fuente.
4. Si hay cambios de endpoints/modelos, sincronizar `docs/openapi.md`, `docs/custom_prebuilts.md` y `docs/adding_models.md`.
5. Verificar enlaces internos y consistencia de nombres de archivos.

## Lecciones operativas incorporadas

- No sobrecomplicar: priorizar documentos cortos enlazados entre sí, no mega-documentos.
- Cuidar contexto: editar solo archivos documentales necesarios para la tarea pedida.
- Automatizar repetitivo: reutilizar plantillas/checklists existentes en `docs/` antes de crear formatos nuevos.

## Reglas de calidad

- Escribir cambios concretos, no texto genérico.
- Evitar duplicar contenido: enlazar en vez de copiar.
- Usar fechas explícitas (`YYYY-MM-DD`) en actas o evidencia operativa.
- Cuando se cierre un hito, dejar evidencia en `docs/` y reflejar estado en `TODO.md`.

## Hooks relacionados y uso

- Hook sugerido: recordatorio al finalizar para validar enlaces y actualizar `docs/README.md` cuando cambie la estructura documental.
- Estado de uso en esta skill: **propuestos**, **no instrumentados aún** en configuración local.

