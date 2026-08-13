<!-- AION-MISSION-METADATA
id: MISSION-XXX
title: <short title>
status: DRAFT            # DRAFT | ACTIVE | BLOCKED | DONE | ARCHIVED
stage: draft            # draft|pm|prd|architecture|tasks|build|qa|security|approval|pr|merged|deployed
owner: CEO
priority: P2            # P0 | P1 | P2 | P3
-->

# MISSION-XXX — <Title>

> Machine-readable status lives in the metadata block above. Keep `status` and
> `stage` accurate — `scripts/mission_status.py` reads them.

## Business Objective
<The CEO-level outcome, in business terms.>

## Problem
<The concrete problem being solved and why it matters now.>

## Target User
<Who this is for. Be specific.>

## Expected Outcome
<What "good" looks like once this ships.>

## Success Metrics
- <Measurable metric 1>
- <Measurable metric 2>

## Scope
- <In scope>

## Non-Goals
- <Explicitly out of scope>

## Requirements
- <Functional requirement>

## Acceptance Criteria
- [ ] <Objectively verifiable criterion>

## Technical Requirements
<Filled/expanded by AION-ARCHITECT. Constraints known up front go here.>

## Security Requirements
<Non-negotiable security constraints (authz, data handling, secrets, compliance).>

## Risks
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
|      |           |        |            |

## Dependencies
- <Upstream missions, services, credentials, or decisions this depends on>

## Milestones
1. <Milestone>

## Approval Gates
- **YELLOW (needs human approval):** <e.g. deployment, migration, new paid service>
- **RED (human-only):** <e.g. production data deletion, financial commitment>

## Definition of Done
See `AION_ENGINEERING.md` § Definition of Done. This mission additionally requires:
- <Mission-specific completion condition>

## Artifact Package
| Artifact | Path | Produced by |
|----------|------|-------------|
| PRD | `prd.md` | AION-PM |
| Architecture | `architecture.md` | AION-ARCHITECT |
| Tasks | `tasks.md` | AION-ARCHITECT |
| QA Report | `qa-report.md` | AION-QA |
| Security Report | `security-report.md` | AION-SECURITY |

## Log
- YYYY-MM-DD — created.
