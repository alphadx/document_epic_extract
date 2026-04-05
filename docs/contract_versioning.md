# Versionado de Contrato API (OpenAPI)

Última actualización: **2026-04-05**

## Objetivo
Definir reglas claras para evolucionar el contrato sin romper integraciones de consumidores.

## Política SemVer aplicada al contrato

### Cambios **PATCH** (`X.Y.Z`)
No cambian estructura ni semántica del contrato, por ejemplo:
- correcciones de documentación/descripciones
- ejemplos más precisos
- aclaraciones de errores sin cambiar códigos ni payload

### Cambios **MINOR** (`X.Y.0`)
Agregan capacidades backward-compatible, por ejemplo:
- nuevos campos opcionales en responses
- nuevos endpoints no obligatorios para clientes existentes
- nuevos valores permitidos compatibles con defaults

### Cambios **MAJOR** (`X.0.0`)
Rompen compatibilidad y requieren migración, por ejemplo:
- renombrar/eliminar campos existentes
- volver obligatorio un campo antes opcional
- cambiar shape de payload en request/response
- eliminar endpoint público

## Proceso mínimo antes de merge

1. Ejecutar tests de contrato y snapshot:

```bash
pytest -q tests/integration/test_openapi_contract.py tests/integration/test_openapi_signature_snapshot.py
make openapi-signature
git diff --exit-code tests/fixtures/openapi_signature.json
```

2. Si hay ruptura detectada, documentar explícitamente:
- impacto a consumidores
- versión objetivo (major/minor)
- guía de migración breve en PR/README/docs

3. Actualizar `docs/openapi.md` cuando cambie comportamiento observable.
