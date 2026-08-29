# AION Software Factory

The operating foundation for AION's agent-driven software development: missions, workflows, standards, and templates that turn CEO objectives into reviewable, shippable code.

## Quick Start

1. Read [`AION_ENGINEERING.md`](AION_ENGINEERING.md) — principles, definition of done, approval gates.
2. Read [`AGENTS.md`](AGENTS.md) — agent contract and roles.
3. Check [`missions/`](missions/) for the active mission.
4. Follow [`docs/workflows/END_TO_END.md`](docs/workflows/END_TO_END.md) for delivery phases.

## Repository Structure

```
aion-software-factory/
├── AION_ENGINEERING.md      # Engineering constitution
├── AGENTS.md                  # Agent operating contract
├── missions/                  # Scoped work with acceptance criteria
├── docs/
│   ├── architecture/          # Factory & product-repo conventions
│   ├── workflows/             # End-to-end delivery process
│   ├── standards/             # Testing & security baselines
│   └── templates/             # Mission, PRD, architecture, QA, security
└── .github/                   # PR and issue templates
```

## Agent Roles

| Role | Responsibility |
|------|----------------|
| **AION-PM** | Missions, PRDs, acceptance criteria |
| **AION-ARCHITECT** | Technical design, task breakdown |
| **AION-BUILDER** | Implementation and pull requests |
| **AION-QA** | Verification against acceptance criteria |
| **AION-SECURITY** | Review for security-sensitive changes |

## Product Repositories

This repo defines **how** AION builds. Application code lives in separate product repositories that follow the layout in [`docs/architecture/OVERVIEW.md`](docs/architecture/OVERVIEW.md).

## Current Mission

**[MISSION-001 — Factory Bootstrap](missions/MISSION-001.md)** — Establish the minimum operating foundation. Next: select a revenue-connected product for MISSION-002 (CEO approval required before production access).

## Competitive Baseline

The factory is designed for the same delivery patterns fast SaaS teams use: small PRs, tests matched to risk, explicit approval gates, and repeatable templates so each new product starts from a playbook—not a blank page.
