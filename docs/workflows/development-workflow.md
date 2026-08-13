# Development Workflow

The factory turns a CEO objective into deployable software through a fixed,
traceable pipeline. Every stage has one accountable agent and one required
artifact. No stage may be skipped; a stage may send work backward.

## Pipeline

| # | Stage (`stage` value) | Owner | Input | Output artifact | Approval |
|---|-----------------------|-------|-------|-----------------|----------|
| 0 | `draft` | CEO | idea | `mission.md` (skeleton) | — |
| 1 | `pm` → `prd` | AION-PM | mission | `prd.md` | — (GREEN) |
| 2 | `architecture` | AION-ARCHITECT | approved PRD | `architecture.md` + ADRs | YELLOW if infra/auth/migration |
| 3 | `tasks` | AION-ARCHITECT | architecture | `tasks.md` | — |
| 4 | `build` | AION-BUILDER | tasks | code + tests on branch | GREEN; YELLOW to leave branch |
| 5 | `qa` | AION-QA | branch + AC | `qa-report.md` | — |
| 6 | `security` | AION-SECURITY | branch + arch | `security-report.md` | blocks on HIGH/CRIT |
| 7 | `approval` | **Human** | all reports | approval decision | **human gate** |
| 8 | `pr` | AION-BUILDER | approval | pull request | — |
| 9 | `merged` | Human/maintainer | PR | merge | human merges |
| 10 | `deployed` | Human-triggered | merge | deployment | **YELLOW/RED** |

```
CEO ─▶ MISSION ─▶ PM/PRD ─▶ ARCHITECTURE ─▶ TASKS ─▶ BUILD ─▶ QA ─▶ SECURITY
                                                                        │
                                          ┌── fail: back to BUILD ◀─────┤
                                          ▼                             │
                                   HUMAN APPROVAL ◀─────────────────────┘
                                          │
                                          ▼
                                   PR ─▶ MERGE ─▶ DEPLOY
```

## Rules of movement

- **Forward** only when the current stage's completion criteria (see the agent
  contract) are met and the handoff block is written.
- **Backward** whenever a reviewer (QA/Security) finds a blocker: set `stage`
  back to `build` and record the finding IDs the Builder must resolve.
- **Blocked** when a human decision is required: set `status: BLOCKED` and state
  the smallest decision needed.
- The mission metadata block is the single source of truth for `status` and
  `stage`. Update it at every transition. `scripts/mission_status.py` reports it.

## Where a mission lives

Each product mission is a directory:

```
missions/MISSION-XXX/
├── mission.md          # control document (metadata + requirements + AC)
├── prd.md              # AION-PM
├── architecture.md     # AION-ARCHITECT
├── tasks.md            # AION-ARCHITECT
├── qa-report.md        # AION-QA
└── security-report.md  # AION-SECURITY
```

The foundation meta-mission (MISSION-001) is a flat file because it produced the
repository itself, not a product artifact package (see ADR-0002).

## Human approval gates in the pipeline

- Stage 7 is an **explicit human gate** — no agent may self-approve for
  deployment.
- Stages 2 and 10 trigger **YELLOW** gates when they involve infrastructure,
  authentication, migrations, paid services, or production configuration.
- See `../operations/approval-policy.md` for the full GREEN/YELLOW/RED policy.
