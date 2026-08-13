# ADR-0001 — Record architecture decisions as ADRs

- **Status:** Accepted
- **Date:** 2026-08-13
- **Deciders:** Founding engineering agent
- **Mission:** MISSION-001

## Context
The factory must be auditable and its reasoning reconstructable by future agents
and humans without access to any chat transcript. Decisions made only in
conversation are lost when the session ends.

## Decision
Record every consequential technical or structural decision as a lightweight
Architecture Decision Record (ADR) in `docs/decisions/`, using
`templates/adr-template.md`. ADRs are numbered sequentially and immutable once
accepted (supersede rather than edit).

## Consequences
### Positive
- Decisions and their rationale are version-controlled and greppable.
- New agents can learn "why" before changing "what".
### Negative / trade-offs
- Small overhead per decision; requires discipline to keep ADRs current.

## Alternatives considered
- Decisions in commit messages only → not discoverable or structured.
- A wiki / external doc tool → violates the "GitHub is source of truth" principle.
