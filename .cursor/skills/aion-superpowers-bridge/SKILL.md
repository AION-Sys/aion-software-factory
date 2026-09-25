---
name: aion-superpowers-bridge
description: Use at session start and whenever choosing between Superpowers skills and AION roles — maps obra/superpowers workflows onto AION missions, templates, and approval gates without bypassing governance.
---

# AION × Superpowers bridge

## When to use

- Starting any AION factory or product-repo coding session
- Choosing which Superpowers skill fits the current AION role/phase
- Resolving conflict between "build it now" impulses and AION gates

## Instructions

1. **Load AION context first:** `AION_ENGINEERING.md` → active mission in `missions/` → relevant `docs/`. State assumptions; do not invent consequential product requirements.

2. **If Superpowers is installed**, follow `using-superpowers` for skill invocation. If it is **not** installed, still follow the discipline below using this bridge and `docs/workflows/SUPERPOWERS.md`.

3. **Pick the skill by phase:**

| Situation | Superpowers skill | AION output |
|-----------|-------------------|-------------|
| New feature / unclear intent | `brainstorming` | Mission update, PRD section, or architecture note |
| Multi-step approved design | `writing-plans` | Architect `TASK` rows + optional plan under product `docs/` |
| Implementing a bounded task | `executing-plans` or `subagent-driven-development` | PR in the **product** repo (or factory for process-only) |
| Logic change | `test-driven-development` | Tests per `docs/standards/TESTING.md` |
| About to claim done | `verification-before-completion` | Evidence in PR / QA report |
| Bug / failing CI | `systematic-debugging` | Fix + regression test |
| Branch complete | `finishing-a-development-branch` | PR using factory/product PR template |
| Independent parallel failures | `dispatching-parallel-agents` | Only if no shared mutable state |

4. **Plan file location:** Prefer AION artifacts (`missions/`, product `docs/ARCHITECTURE.md`, task files). If writing a Superpowers-style plan file, put it in the **product** repo under `docs/plans/` (or the human's preferred path)—not as a substitute for Architect tasks.

5. **Handoff:** Always emit the `AGENTS.md` handoff fields. Note whether human approval is required.

6. **Factory-only vs product:** Process/tooling work may proceed in this repo in parallel with Mission 002. Do not implement Mission 002 application features here.

## Anti-patterns

- Skipping CEO gates because a Superpowers plan says "merge"
- Brainstorming a new product mission while Mission 002 validation is open (blocked unless factory-only)
- Claiming tests pass without running them this session
- Vendoring or rewriting upstream Superpowers skill files in this repo
