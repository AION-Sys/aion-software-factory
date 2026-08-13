# AION Software Factory

An AI-native engineering organization. The CEO/founder defines business and
product objectives at a high level; specialized AI agents handle product
planning, architecture, implementation, testing, security review, and
documentation — under explicit human approval gates.

This repository is the **engineering source of truth** for the factory itself.
It is version-controlled, agent-readable, and vendor-neutral by design.

> **Status:** Foundation (Mission 001). The factory can take a structured CEO
> mission and produce a complete, reviewable development package. Autonomous
> production deployment is **not** enabled.

---

## How it works

A CEO objective flows through a fixed, traceable pipeline. Each stage is owned
by one agent and produces a concrete artifact that the next stage consumes.

```
CEO OBJECTIVE
   ↓
MISSION            (structured objective — missions/MISSION-XXX/)
   ↓  AION-PM
PRD                (product requirements — prd.md)
   ↓  AION-ARCHITECT
ARCHITECTURE       (technical plan — architecture.md)
   ↓  AION-ARCHITECT
ENGINEERING TASKS  (task list — tasks.md)
   ↓  AION-BUILDER
IMPLEMENTATION     (code + tests on a branch)
   ↓  AION-QA
QA REPORT          (verification vs. acceptance criteria — qa-report.md)
   ↓  AION-SECURITY
SECURITY REPORT    (risk review — security-report.md)
   ↓
HUMAN APPROVAL GATE
   ↓
PULL REQUEST → MERGE → DEPLOYMENT
```

Agents communicate **through artifacts, not conversational memory**. Any agent
can pick up a mission, read its files, and determine what must happen next.

## Repository layout

```
├── README.md               ← you are here
├── AION_ENGINEERING.md     ← the engineering constitution (rules, DoD, gates)
├── AGENTS.md               ← the agent operating contract + handoff rules
│
├── agents/                 ← per-agent contracts (inputs/outputs/allowed/forbidden)
│   ├── pm/  architect/  builder/  qa/  security/
│
├── missions/               ← one directory per product mission
│   ├── MISSION-001.md       (foundation meta-mission — flat file)
│   └── MISSION-XXX/         (product missions — mission.md + artifact package)
│
├── templates/              ← blank templates for every artifact
│   ├── mission-template.md      prd-template.md         architecture-template.md
│   ├── task-list-template.md    qa-template.md          security-template.md
│   └── adr-template.md
│
├── docs/
│   ├── architecture/       ← how the factory itself is built
│   ├── decisions/          ← Architecture Decision Records (ADRs)
│   ├── workflows/          ← the development workflow + agent handoffs
│   └── operations/         ← approval policy, security/secrets, observability
│
└── scripts/                ← traceability & validation tooling (stdlib only)
    ├── mission_status.py    (where is each mission in the pipeline?)
    └── validate_repo.py     (is the foundation structurally intact?)
```

## Start here (reading order)

1. `AION_ENGINEERING.md` — the rules everything else obeys.
2. `AGENTS.md` — how agents operate and hand off.
3. `docs/workflows/development-workflow.md` — the end-to-end pipeline.
4. `agents/<role>/CONTRACT.md` — the contract for a specific agent.
5. `missions/MISSION-001.md` — the mission that produced this foundation.

## Quick commands

```bash
python3 scripts/validate_repo.py     # check the foundation is intact
python3 scripts/mission_status.py    # show every mission's pipeline stage
```

## Creating a new product mission

```bash
mkdir -p missions/MISSION-002
cp templates/mission-template.md missions/MISSION-002/mission.md
# fill it in, then hand off to AION-PM
```

See `docs/workflows/development-workflow.md` for the full lifecycle.

## Human control & safety

Progressive autonomy is enforced. Agents act freely on **GREEN** work
(research, planning, code generation, local tests, branches). They **must stop
and request approval** for **YELLOW** work (deployment, migrations, infra, auth,
paid services). **RED** actions (destructive production ops, financial/legal
commitments, secrets disclosure) are **human-only**. Full policy in
`docs/operations/approval-policy.md`.
