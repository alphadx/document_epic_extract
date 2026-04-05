## Summary

- Describe what changed and why.

## Validation

- [ ] `ruff check .`
- [ ] `pytest -q`
- [ ] `make release-readiness` (or explain why not applicable)

## Documentation / Governance checks

- [ ] Updated docs impacted by this change (README/docs/TODO if applicable)
- [ ] If circuit breaker behavior/state changed, ran `make cb-consistency` and resolved any drift
- [ ] If milestone/hito status changed, updated `docs/milestone_decisions.md`

## Risk and Rollback

- Risk level: Low / Medium / High
- Rollback plan:
