# AION Agent Workforce

This directory holds the **contract** for each agent in the factory. A contract
is the authoritative definition of what an agent may and may not do. Agents load
their contract before acting; humans read it to know what to expect.

## The workforce (minimum useful set)

| Agent | Consumes | Produces |
|-------|----------|----------|
| [`AION-PM`](pm/CONTRACT.md) | CEO objective / mission | PRD (`prd.md`) |
| [`AION-ARCHITECT`](architect/CONTRACT.md) | Approved PRD | Architecture (`architecture.md`) + Tasks (`tasks.md`) |
| [`AION-BUILDER`](builder/CONTRACT.md) | Approved architecture + tasks | Implementation (code + tests, branch, PR) |
| [`AION-QA`](qa/CONTRACT.md) | Implementation + acceptance criteria | QA report (`qa-report.md`) |
| [`AION-SECURITY`](security/CONTRACT.md) | Implementation + architecture | Security report (`security-report.md`) |

We deliberately keep the workforce small. New agents are added only when a
concrete, recurring gap is proven — not speculatively.

## Contract schema

Every `CONTRACT.md` uses the same nine sections so agents and humans can rely on
a fixed shape:

1. **Purpose** — the single reason this agent exists.
2. **Inputs** — the artifacts/context it requires before starting.
3. **Outputs** — the artifact(s) it must produce.
4. **Responsibilities** — what it does.
5. **Allowed actions** — what it may do without asking.
6. **Forbidden actions** — hard boundaries it must never cross.
7. **Required context** — files it must read before acting.
8. **Escalation conditions** — when it must stop and ask a human.
9. **Completion criteria** — the definition of "done" for this agent.

## Shared rules (apply to every agent)

- Read `../AION_ENGINEERING.md` and `../AGENTS.md` before acting.
- Communicate through artifacts, never hidden conversational state.
- Obey the approval policy in `../docs/operations/approval-policy.md`.
- Never read, write, log, or commit secrets.
- Operate with least privilege; stay inside the assigned mission scope.
- End every run with the **handoff block** defined in `../AGENTS.md`.
