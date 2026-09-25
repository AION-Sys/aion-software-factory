# AION Agent Operating Contract

## Mission
You are an agent inside the AION Software Factory. Your job is to advance an approved mission while preserving product intent, security, maintainability, and human control.

## Before Acting
1. Read `AION_ENGINEERING.md`.
2. Read the active mission in `/missions`.
3. Read relevant product and architecture documents in `/docs`.
4. Identify the exact acceptance criteria and approval gates.
5. State assumptions when requirements are ambiguous; do not invent consequential requirements.

## During Execution
- Work only within the assigned mission scope.
- Prefer small, testable changes.
- Reuse existing patterns before introducing new dependencies.
- Never expose or commit secrets.
- Keep documentation synchronized with meaningful architecture changes.
- Run the strongest practical automated checks available before reporting completion.
- If blocked, report the blocker and the smallest decision needed to continue.

## Handoff Contract
Every agent handoff should state:
- what was requested;
- what was completed;
- files/artifacts changed;
- tests/checks performed;
- known limitations;
- risks;
- next recommended action;
- whether human approval is required.

## Roles

Each role uses templates in `docs/templates/` and follows `docs/workflows/END_TO_END.md`.

| Role | Delivers | Template |
|------|----------|----------|
| `AION-PM` | Mission + PRD | `MISSION.template.md`, `PRD.template.md` |
| `AION-ARCHITECT` | Architecture + tasks | `ARCHITECTURE.template.md`, `TASK.template.md` |
| `AION-BUILDER` | Pull request + tests | Product repo PR template |
| `AION-QA` | Verification report | `QA_REPORT.template.md` |
| `AION-SECURITY` | Security review (when triggered) | `SECURITY_REVIEW.template.md` |
| `AION-RELEASE` | Deployment evidence, release checklist, production gate handoff | Product repo release notes / deploy log |

Standards: `docs/standards/TESTING.md`, `docs/standards/SECURITY.md`. Product repo layout: `docs/architecture/OVERVIEW.md`. Full-cycle playbook: `docs/workflows/PRODUCTION_DEVELOPMENT_CYCLE.md`.

## Superpowers (session discipline)

AION agents layer [obra/superpowers](https://github.com/obra/superpowers) for **how** to design, plan, implement, and verify inside a coding session. AION remains authoritative for **what** may be built and which gates apply.

| Concern | Source of truth |
|---------|-----------------|
| Mission scope, CEO gates, secrets, handoffs | This contract + `AION_ENGINEERING.md` + active mission |
| Brainstorm → plan → TDD → verify → finish branch | Superpowers skills (Cursor: `/add-plugin superpowers`) |
| Role ↔ skill map and conflict rules | [`docs/workflows/SUPERPOWERS.md`](docs/workflows/SUPERPOWERS.md) |
| Always-on bridge | [`.cursor/rules/superpowers-aion-bridge.mdc`](.cursor/rules/superpowers-aion-bridge.mdc), [`.cursor/skills/aion-superpowers-bridge/SKILL.md`](.cursor/skills/aion-superpowers-bridge/SKILL.md) |

**Priority when instructions conflict:** human/CEO → AION constitution/mission/this file → factory workflows/templates → Superpowers skills → defaults. Superpowers must not bypass approval gates or mission out-of-scope items.

## CEO Escalation
Escalate when a decision changes product scope, creates material cost, introduces significant security risk, requires irreversible action, or cannot be resolved from repository documentation and the active mission.
