# ADR-0004 — Lead Intelligence built in Python (stdlib only)

- **Status:** Accepted
- **Date:** 2026-08-13
- **Deciders:** AION-ARCHITECT (MISSION-002)
- **Mission:** MISSION-002

## Context
The lead-intelligence V1 is a CLI/library that transforms input data into a
scored lead list. It has no UI requirement and must run anywhere with minimal
friction. The repository's existing tooling (`scripts/`) is Python stdlib.

## Decision
Implement `products/lead-intel/` in Python 3 using the **standard library only**
(no third-party packages). Tests use `unittest`.

## Consequences
### Positive
- Runs with a bare `python3` — zero install, matches AC-7 (no credentials/network).
- Consistent with the repo's dependency-free ethos and existing scripts.
- Pure functions are easy to unit-test and reason about.
### Negative / trade-offs
- No rich data/HTTP libraries; a future live provider will add a dependency then,
  under review — deferred deliberately.

## Alternatives considered
- **TypeScript/Next.js** (standard-stack default) — rejected: no UI; heavier
  toolchain for a library/CLI.
- **Python with third-party deps (requests, pydantic)** — rejected for V1: not
  needed without network calls; adds install friction.
