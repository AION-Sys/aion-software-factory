# AION Software Factory — Architecture Overview

## Purpose
The Software Factory is AION's operating system for turning product objectives into shipped software. It is not a product itself; it is the **governance, workflow, and artifact layer** that product repositories inherit.

## Two-Layer Model

```
┌─────────────────────────────────────────────────────────────┐
│  AION Software Factory (this repo)                          │
│  Missions · Workflows · Standards · Templates · Agent rules │
└──────────────────────────┬──────────────────────────────────┘
                           │ governs
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  Product repositories (one per product or bounded domain) │
│  Application code · CI/CD · infra · tests · deployments     │
└─────────────────────────────────────────────────────────────┘
```

**Factory repo** holds process truth. **Product repos** hold runtime truth. Agents always read the active mission and relevant factory docs before changing product code.

## Repository Map

| Path | Purpose |
|------|---------|
| `AION_ENGINEERING.md` | Engineering constitution: principles, DoD, approval gates, stack |
| `AGENTS.md` | Agent operating contract and role definitions |
| `missions/` | Scoped work units with acceptance criteria and CEO gates |
| `docs/workflows/` | End-to-end delivery process |
| `docs/standards/` | Testing, security, and quality baselines |
| `docs/templates/` | Repeatable artifacts for PM, Architect, Builder, QA, Security |
| `docs/architecture/` | Factory and cross-repo architectural guidance |

## Agent Roles and Artifacts

| Role | Primary output | Stored in |
|------|----------------|-----------|
| AION-PM | Mission + PRD | `missions/`, product repo `docs/` |
| AION-ARCHITECT | Architecture doc + task breakdown | product repo `docs/` |
| AION-BUILDER | Pull request + implementation | product repo |
| AION-QA | QA report vs acceptance criteria | product repo `docs/` or PR |
| AION-SECURITY | Security review (when triggered) | product repo `docs/` or PR |
| CEO / Human | Approval at defined gates | GitHub PR review, mission status |

## Product Repo Conventions

Every product repository created under AION should include at minimum:

```
product-repo/
├── README.md              # What it is, how to run locally, deploy notes
├── docs/
│   ├── PRD.md             # Current product requirements (from template)
│   ├── ARCHITECTURE.md    # Current technical design (from template)
│   └── adr/                 # Architecture Decision Records (optional, recommended)
├── src/ or app/           # Application code (stack-specific)
├── tests/                 # Automated tests appropriate to risk
├── .github/
│   ├── workflows/         # CI: lint, test, build on every PR
│   └── PULL_REQUEST_TEMPLATE.md
└── AGENTS.md              # Symlink or copy pointing agents to factory contract
```

Agents must not invent a new layout per mission. Extend this baseline only when the Architect documents a reason.

## Standard Stack

Prefer unless documented deviation (`AION_ENGINEERING.md`):

| Layer | Default |
|-------|---------|
| Source control | GitHub |
| Application | TypeScript, Next.js where appropriate |
| Database | Supabase / Postgres where appropriate |
| Cloud | AWS |
| Frontend hosting | Vercel where appropriate |
| Agents | AI coding agents (Cursor Cloud Agents, etc.) |
| Observability | Standard tooling per product (to be defined at product bootstrap) |

## Delivery Principles (Competitive Baseline)

These patterns match what fast-moving SaaS teams optimize for:

1. **Small PRs** — One mission task or one vertical slice per PR; reviewable in minutes.
2. **Tests match risk** — Critical paths and auth/data flows always tested; UI polish may be lighter.
3. **Explicit gates** — Autonomous work stops at production, migrations, new paid services, and permission changes.
4. **Artifact trail** — No "tribal knowledge"; every handoff uses templates in `docs/templates/`.
5. **Reversible changes** — Feature flags, migrations with rollback plans, no big-bang releases without approval.
6. **Same playbook every product** — Mission 002+ reuses templates; speed comes from repetition, not reinvention.

## What Lives Outside This Repo

- Application runtime, databases, and production credentials
- Product-specific CI/CD secrets and deployment targets
- Customer data and billing integrations

The factory defines *how* to build; product repos define *what* is built and *where* it runs.

## Evolution

Material changes to this model (new roles, new gates, new required artifacts) require Architect documentation and human approval per `AION_ENGINEERING.md`.
