# Superpowers × AION Integration

Layer [obra/superpowers](https://github.com/obra/superpowers) onto the AION Software Factory without replacing governance, templates, or approval gates.

**Pinned reference:** Superpowers `v6.4.2` (study date 2026-09-25). Install from the Cursor marketplace for live updates; do not vendor skill bodies into this repo.

## Why this layer exists

AION already defines **who** acts and **what artifacts** are required (`AGENTS.md`, missions, templates). Superpowers defines **how** an agent should think and execute inside a coding session (brainstorm → plan → TDD → verify → finish branch).

Together:

| Layer | Owns |
|-------|------|
| AION | Mission scope, CEO gates, role handoffs, PRD/architecture/QA/security templates, DoD |
| Superpowers | Session discipline: design before code, bite-sized plans, red/green TDD, evidence before claims |

## Install (humans / Cursor Desktop)

In Cursor Agent chat:

```text
/add-plugin superpowers
```

Or search the plugin marketplace for **superpowers**. Restart the agent session after install so the `sessionStart` bootstrap (`using-superpowers`) loads.

**Cloud Agents / environments without the marketplace plugin:** this repo’s bridge rule and skill still apply the AION↔Superpowers mapping. Full auto-trigger of upstream skill bodies requires the plugin.

Optional telemetry opt-out (visual companion): `SUPERPOWERS_DISABLE_TELEMETRY=1`.

## Priority stack (non-negotiable)

When instructions conflict, resolve in this order:

1. **Explicit human / CEO instruction for this session**
2. **`AION_ENGINEERING.md` + active mission + `AGENTS.md`** (scope, gates, secrets, handoffs)
3. **Factory workflows and templates** (`docs/workflows/`, `docs/templates/`, `docs/standards/`)
4. **Superpowers skills** (process for design/plan/build/verify)
5. **Default agent behavior**

Never use Superpowers to bypass: CEO approval gates, security review triggers, production deploy rules, or mission out-of-scope items.

## Role → skill map

| AION role | Primary Superpowers skills | AION artifact still required |
|-----------|---------------------------|------------------------------|
| `AION-PM` | `brainstorming` (intent → design chunks) | Mission + PRD from templates |
| `AION-ARCHITECT` | `brainstorming` → `writing-plans` | `ARCHITECTURE.md` + `TASK` files |
| `AION-BUILDER` | `using-git-worktrees` → `executing-plans` / `subagent-driven-development` + `test-driven-development` | Small PR; tests per `docs/standards/TESTING.md` |
| `AION-QA` | `verification-before-completion` + `requesting-code-review` | `QA_REPORT` vs acceptance criteria |
| `AION-SECURITY` | `systematic-debugging` (for suspected vulns); review still template-driven | `SECURITY_REVIEW` when triggered |
| `AION-RELEASE` | `verification-before-completion` (smoke evidence) | Release record + CEO gate — **not** auto-merge |

Cross-cutting: `systematic-debugging` on failures; `receiving-code-review` when addressing review; `finishing-a-development-branch` when ready to PR/merge options; `dispatching-parallel-agents` only for independent domains that do not share mutable state.

## End-to-end overlay

```
CEO objective
    │
    ▼
AION-PM ──────────── Superpowers: brainstorming
    │                 → mission + PRD (AION templates win)
    ▼
AION-ARCHITECT ───── brainstorming → writing-plans
    │                 → ARCHITECTURE + ordered tasks (AION templates win)
    ▼
AION-BUILDER ─────── worktrees → execute plan → TDD → verify
    │                 → PR in product repo
    ▼
AION-QA / SECURITY ─ verification-before-completion (+ review skills)
    │
    ▼
Human / CEO gates ── Superpowers does not replace these
    │
    ▼
AION-RELEASE ─────── verify smoke; fill release record
```

Day-to-day Builder loop remains [`PRODUCTION_DEVELOPMENT_CYCLE.md`](PRODUCTION_DEVELOPMENT_CYCLE.md); Superpowers sharpens steps 2–5 (implement, test, verify) without changing where code lives.

## Practical use cases (best fit for AION)

1. **New feature / behavior change in a product repo** — Brainstorm against the active mission + PRD; write a plan that maps to existing Architect tasks; implement with TDD; verify before claiming done.
2. **Factory process/tooling changes** (this repo) — Allowed in parallel with Mission 002 per Sequential Mission Governance; keep PRs small; still use verification-before-completion.
3. **Bug / CI failure** — `systematic-debugging` before speculative fixes; then TDD for the regression.
4. **Multi-task Architect plan** — Prefer `executing-plans` for a single Builder session on one task; use `subagent-driven-development` only when the human explicitly wants per-task subagents and cost is accepted.
5. **QA handoff** — Do not claim criteria pass without fresh command output (`verification-before-completion`).

## What we deliberately do not do

- **Do not** copy or fork Superpowers skill markdown into this repo (drift + license sync burden).
- **Do not** add npm/runtime dependencies for Superpowers (it is a Cursor plugin, not an app dependency).
- **Do not** treat Superpowers brainstorming as a substitute for CEO mission approval.
- **Do not** implement Mission 002 product features in this factory repo.

## Agent checklist (session start)

1. Read `AION_ENGINEERING.md`, active mission, relevant `docs/`.
2. If Superpowers plugin is available, follow `using-superpowers` (invoke applicable skills).
3. Apply [`.cursor/skills/aion-superpowers-bridge/SKILL.md`](../../.cursor/skills/aion-superpowers-bridge/SKILL.md) mapping.
4. Produce AION handoff fields on completion (`AGENTS.md`).

## Attribution

Superpowers is © Jesse Vincent / contributors, MIT License — https://github.com/obra/superpowers
