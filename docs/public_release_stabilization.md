# Estabilización y Release Público

Última actualización: **2026-04-05**

## Objetivo
Definir un proceso corto, verificable y repetible para pasar del estado “documentación cerrada” a un release público con riesgo controlado.

## Alcance de estabilización

### 1) Congelamiento de alcance (Scope Freeze)
- Congelar cambios funcionales no críticos.
- Aceptar únicamente fixes de bugs, documentación y hardening.
- Registrar explícitamente cambios diferidos al siguiente ciclo.

### 2) Calidad y regresión
- Ejecutar quality gates (recomendado en comando único):
  - `make release-readiness`
  - o `scripts/release_readiness.sh`
- Comandos equivalentes:
  - `ruff check .`
  - `pytest -q`
- Ejecutar validación de contrato OpenAPI:
  - `pytest -q tests/integration/test_openapi_contract.py tests/integration/test_openapi_signature_snapshot.py`
  - `make openapi-signature`
  - `git diff --exit-code tests/fixtures/openapi_signature.json`

### 3) Smoke de operación local
- API local levanta y responde `/health`.
- Demo Streamlit ejecuta flujo base (upload + extract + render JSON).
- Worker local responde `/infer` en modo CPU (mínimo).

### 4) Triage de riesgo antes de release
- Clasificar issues abiertos en:
  - **Bloqueantes** (rompen contrato/flujo principal)
  - **Altos** (degradan experiencia principal)
  - **Medios/Bajos** (post-release)
- Release público solo sin bloqueantes abiertos.

## Proceso sugerido de release

1. Crear release candidate (`vX.Y.Z-rc1`).
2. Ejecutar checklist de `docs/release_checklist.md`.
3. Hacer validación rápida manual de API + demo.
4. Si pasa, promover a `vX.Y.Z`.
5. Publicar notas de release con:
   - cambios principales
   - incompatibilidades (si aplica)
   - riesgos conocidos
   - plan de mitigación

## Criterio Go / No-Go

**Go**:
- Quality gates en verde.
- Contrato OpenAPI estable.
- Sin bloqueantes abiertos.
- Documentación de operación actualizada.

**No-Go**:
- Regresiones en contrato API.
- Demo o flujo `/extract` no reproducible.
- Incertidumbre sobre compatibilidad de release.

## Ejecución más reciente

- RC ejecutado: `v0.1.1-rc1` (**GO**).
- Release estable ejecutado: `v0.1.1` (**GO**).
- Evidencias: `docs/release_rc_0.1.1-rc1.md` y `docs/release_v0.1.1.md`.
