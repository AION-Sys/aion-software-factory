# AION Software Factory

The operating foundation for AION's agent-driven software development: missions, workflows, standards, and templates that turn CEO objectives into reviewable, shippable code.

## Quick Start

1. Read [`AION_ENGINEERING.md`](AION_ENGINEERING.md) — principles, definition of done, approval gates.
2. Read [`AGENTS.md`](AGENTS.md) — agent contract and roles.
3. Check [`missions/`](missions/) for the active mission.
4. Follow [`docs/workflows/END_TO_END.md`](docs/workflows/END_TO_END.md) for delivery phases.
5. For day-to-day production development: [`docs/workflows/PRODUCTION_DEVELOPMENT_CYCLE.md`](docs/workflows/PRODUCTION_DEVELOPMENT_CYCLE.md).

## Repository Structure

```
aion-software-factory/
├── AION_ENGINEERING.md      # Engineering constitution
├── AGENTS.md                # Agent operating contract (+ Superpowers bridge)
├── missions/                # Scoped work with acceptance criteria
├── docs/
│   ├── architecture/        # Factory & product-repo conventions
│   ├── workflows/           # End-to-end, production cycle, Superpowers overlay
│   ├── standards/           # Testing & security baselines
│   ├── products/            # Mission 002 status, setup, go-live
│   ├── handoffs/            # Cross-repo apply packages
│   └── templates/           # Mission, PRD, architecture, QA, security, release
├── .cursor/
│   ├── rules/               # Always-on agent rules (incl. Superpowers bridge)
│   └── skills/              # Thin AION skills (bridge to Superpowers)
├── product-seeds/           # Retired stubs after product repos publish
└── .github/                 # PR and issue templates
```

## Agent Roles

| Role | Responsibility |
|------|----------------|
| **AION-PM** | Missions, PRDs, acceptance criteria |
| **AION-ARCHITECT** | Technical design, task breakdown |
| **AION-BUILDER** | Implementation and pull requests |
| **AION-QA** | Verification against acceptance criteria |
| **AION-SECURITY** | Review for security-sensitive changes |
| **AION-RELEASE** | Deploy evidence, release record, CEO production gate handoff |

## Product Repositories

This repo defines **how** AION builds. Application code lives in separate product repositories that follow the layout in [`docs/architecture/OVERVIEW.md`](docs/architecture/OVERVIEW.md).

## Current Mission

**[MISSION-001 — Factory Bootstrap](missions/MISSION-001.md)** — Complete.

**[MISSION-002 — Revenue Conversion Copilot](missions/MISSION-002.md)** — Active P0.  
**L1 production development full cycle: READY.** L2 MVP / L3 validation still open.  
Product repo: [Ceoloo-aion-revenue-copilot](https://github.com/AION-Sys/Ceoloo-aion-revenue-copilot) · Status: [`docs/products/MISSION_002_CYCLE_STATUS.md`](docs/products/MISSION_002_CYCLE_STATUS.md)

## Superpowers (agent session discipline)

Install the [obra/superpowers](https://github.com/obra/superpowers) Cursor plugin (`/add-plugin superpowers`) so agents use brainstorm → plan → TDD → verify skills automatically. AION governance still wins on scope and approval gates. Mapping: [`docs/workflows/SUPERPOWERS.md`](docs/workflows/SUPERPOWERS.md).

## Competitive Baseline

The factory is designed for the same delivery patterns fast SaaS teams use: small PRs, tests matched to risk, explicit approval gates, and repeatable templates so each new product starts from a playbook—not a blank page.
