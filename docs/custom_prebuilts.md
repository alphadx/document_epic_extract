# Guía — Custom Prebuilts

Última actualización: **2026-04-05**

## Objetivo
Permitir que cualquier integrador defina un tipo documental propio sin tocar código del core, reutilizando el motor de plantillas.

## Estructura recomendada

Un custom prebuilt debe definir:

- `id`: identificador único en `snake_case` (ej. `insurance_claim`).
- `display_name`: nombre legible para UI/usuarios.
- `version`: versión interna del prebuilt (ej. `1.0`).
- `system_prompt`: instrucción principal para el motor.
- `required_fields`: lista mínima de campos esperados.
- `output_schema`: para este proyecto, `StandardizedExtraction`.

Ejemplo:

```yaml
id: insurance_claim
display_name: "Siniestro de Seguro"
version: "1.0"
system_prompt: |
  Extrae los campos clave del documento y responde SOLO JSON válido.
required_fields:
  - claim_id
  - policy_number
  - incident_date
  - insured_name
  - total_claimed
output_schema: "StandardizedExtraction"
```

## Reglas de diseño

1. Mantener prompts deterministas y sin texto ambiguo.
2. Definir `required_fields` orientados a negocio (no genéricos tipo `field_1`).
3. Versionar cambios incompatibles incrementando major (`2.0`, `3.0`, ...).
4. Evitar incluir secretos o datos sensibles en prompts de ejemplo.

## Flujo de validación recomendado

1. Crear prebuilt custom en entorno local.
2. Ejecutar extracción con al menos 2 documentos reales/anónimos.
3. Verificar:
   - presencia de campos obligatorios
   - formato consistente por proveedor
   - estabilidad de nombres de keys
4. Ajustar prompt hasta obtener salida estable.

## Criterios de aceptación para PR

- Documentar caso de uso y campos requeridos.
- Incluir ejemplo de payload de extracción.
- No romper contrato `StandardizedExtraction`.
- Pasar quality gates:

```bash
ruff check .
pytest -q
```
