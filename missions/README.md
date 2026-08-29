# Missions

Missions are scoped units of work with explicit acceptance criteria and CEO approval gates. They are the **source of truth for what agents should do next**.

## Active Missions

| ID | Title | Status |
|----|-------|--------|
| [MISSION-001](MISSION-001.md) | AION Software Factory Bootstrap | ACTIVE — FOUNDATION |

## Creating a New Mission

1. Copy [`docs/templates/MISSION.template.md`](../docs/templates/MISSION.template.md) to `missions/MISSION-{NNN}.md`.
2. Fill in CEO objective, scope, acceptance criteria, and approval gates.
3. Set status to `DRAFT` until CEO approves scope.
4. Set status to `ACTIVE` when ready for Architect/Builder execution.
5. Add a row to the table above.
6. Link the product repo in the mission file when applicable.

## Mission Numbering

- `001` — Factory bootstrap (this repo)
- `002+` — Product or revenue-connected work (typically tied to a product repository)

## Workflow

See [`docs/workflows/END_TO_END.md`](../docs/workflows/END_TO_END.md) for PM → Architect → Builder → QA → Security → Human Approval.

## Completion

When all acceptance criteria are satisfied:

1. Check off criteria in the mission file.
2. Set status to `COMPLETE`.
3. Document follow-up in **Next Mission**.
