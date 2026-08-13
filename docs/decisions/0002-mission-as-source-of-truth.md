# ADR-0002 — Missions are directories; the mission file is the source of truth

- **Status:** Accepted
- **Date:** 2026-08-13
- **Deciders:** Founding engineering agent
- **Mission:** MISSION-001

## Context
A product mission produces several artifacts (PRD, architecture, tasks, QA and
security reports). These must stay co-located and traceable, and the system must
make it obvious where a mission currently is in the pipeline — from files alone,
without a database (per the "no separate database unless needed" principle).

## Decision
1. Each **product** mission is a directory `missions/MISSION-XXX/` containing a
   `mission.md` control document plus its artifact package.
2. `mission.md` carries a machine-readable metadata block
   (`<!-- AION-MISSION-METADATA ... -->`) with `id`, `title`, `status`, `stage`,
   `owner`, `priority`. This block is the single source of truth for a mission's
   position in the pipeline.
3. `scripts/mission_status.py` parses that block to report state; no database is
   introduced.
4. The foundation meta-mission **MISSION-001 remains a flat file**
   (`missions/MISSION-001.md`) because it produced the repository itself, not a
   product artifact package. New product missions use the directory form.

## Consequences
### Positive
- Full mission history is reconstructable from one directory (auditable).
- Pipeline state is queryable with a dependency-free script.
- No premature database or external tooling.
### Negative / trade-offs
- Two mission shapes exist (flat meta-mission vs. directory product missions);
  documented here to avoid confusion.
- Metadata accuracy depends on agents updating the block at each transition.

## Alternatives considered
- Flat files for everything → artifacts scatter, traceability suffers.
- A database/issue tracker for state → over-engineered for the foundation and
  conflicts with GitHub-as-source-of-truth.
