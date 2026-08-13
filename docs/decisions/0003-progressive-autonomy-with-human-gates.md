# ADR-0003 — Progressive autonomy with explicit human gates

- **Status:** Accepted
- **Date:** 2026-08-13
- **Deciders:** Founding engineering agent / CEO direction
- **Mission:** MISSION-001

## Context
The factory should reduce manual engineering while never risking irreversible or
high-impact actions being taken autonomously. Full autonomy is unsafe; zero
autonomy defeats the purpose.

## Decision
Adopt a three-tier progressive-autonomy model, enforced by agent contracts and
`docs/operations/approval-policy.md`:

- **GREEN** — agents act automatically (research, planning, code generation,
  local tests, lint, refactor, branch creation, non-destructive analysis).
- **YELLOW** — agents must request human approval (production deployment, data
  migrations, infrastructure changes, new paid services, major architecture
  changes, authentication changes, production configuration changes).
- **RED** — human-only (deleting production data, destructive production ops,
  financial/legal commitments, credential/secret disclosure, irreversible infra,
  major resource allocation).

Deployment is never triggered autonomously. A separate reviewer verifies
consequential work before the human gate.

## Consequences
### Positive
- Safety by default; humans retain control of high-impact actions.
- Autonomy can expand later by moving specific actions GREEN with evidence.
### Negative / trade-offs
- Some throughput is traded for safety at YELLOW gates (accepted deliberately).

## Alternatives considered
- Full autonomy → unacceptable irreversible-action risk.
- Human approval for everything → no leverage; defeats the factory's purpose.
