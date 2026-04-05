# Checklist de Release OSS

Última actualización: **2026-04-05**

> Complementar con `docs/public_release_stabilization.md` para criterio Go/No-Go.

## 1) Pre-release técnico
- [x] Ejecutar gate único: `make release-readiness` (o `scripts/release_readiness.sh`).
- [ ] Ejecutar workflow manual "Release Readiness" en GitHub Actions (opcional recomendado).
- [x] `ruff check .`
- [x] `pytest -q`
- [x] `make openapi-signature`
- [x] `git diff --exit-code tests/fixtures/openapi_signature.json`

## 2) Revisión documental
- [x] README actualizado con estado real del roadmap.
- [x] `docs/milestone_decisions.md` actualizado con decisiones del hito.
- [x] `CHANGELOG.md` actualizado (Unreleased y versión objetivo).
- [x] Guías nuevas enlazadas desde README (`docs/`).

## 3) Versionado y tag
- [x] Definir versión (SemVer) para release.
- [x] Actualizar versión en `pyproject.toml`.
- [x] Crear tag anotado (`git tag -a vX.Y.Z -m "release vX.Y.Z"`).

## 4) Publicación (opcional)
- [ ] Construir distribución (`python -m build`).
- [ ] Verificar artefactos (`twine check dist/*`).
- [ ] Publicar (TestPyPI/PyPI) según estrategia del equipo.

## 5) Post-release
- [ ] Publicar notas de release/changelog.
- [ ] Registrar riesgos conocidos y mitigaciones.
- [ ] Confirmar que main queda en verde tras merge.
- [ ] Abrir plan de estabilización siguiente ciclo (si quedan riesgos altos/medios).

## Evidencia de ejecución (RC actual)
- Log de ejecución y decisión GO/No-GO: `docs/release_rc_0.1.1-rc1.md`.
