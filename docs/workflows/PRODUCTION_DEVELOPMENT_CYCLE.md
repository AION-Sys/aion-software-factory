# Production Development Full Cycle

Operational playbook for running Mission 002 (and future product missions) end-to-end:

**Factory → Code → Preview → QA → Security → Release → Real usage → Validation → Learning**

This is the companion to [`END_TO_END.md`](END_TO_END.md). Use that doc for role phases; use this doc for readiness levels and day-to-day execution.

## Readiness Levels

| Level | Meaning | Mission 002 (as of 2026-09-16) |
|-------|---------|--------------------------------|
| **L0 — Factory governance** | Missions, templates, gates, agent contract exist | **READY** (Mission 001 complete) |
| **L1 — Product development cycle** | Product repo, CI, preview deploys, Builder loop works | **READY** |
| **L2 — Production-capable MVP** | Auth, data, AI, CRM, learning wired; QA + Security signed; CEO release gate | **IN PROGRESS** |
| **L3 — Validated** | Real prospect usage + evidence in `docs/VALIDATION.md` | **NOT STARTED** |

**"Ready for production development full cycle"** = **L1**. Agents may run the full Builder → PR → CI → preview → QA path without inventing process. L2/L3 still require human infra and CEO gates.

## Where Work Happens

| Concern | Location |
|---------|----------|
| Process truth (missions, gates, templates) | This factory repo |
| Application code, CI, Vercel, Supabase migrations | [AION-Sys/Ceoloo-aion-revenue-copilot](https://github.com/AION-Sys/Ceoloo-aion-revenue-copilot) |
| Learning telemetry patch (cross-repo) | [`docs/handoffs/REVENUE_FACTORY_LIVE_EMISSION.md`](../handoffs/REVENUE_FACTORY_LIVE_EMISSION.md) |

**Do not implement Mission 002 features in this factory repo.** The former `product-seeds/aion-revenue-copilot/` tree is retired; see [`product-seeds/README.md`](../../product-seeds/README.md).

## Cycle Loop (every Builder change)

```
1. Read missions/MISSION-002.md + product docs/ARCHITECTURE.md task row
2. Branch in product repo → implement one task (small PR)
3. npm run lint && typecheck && test && build
4. Open PR (product PR template) → CI + Vercel Preview
5. AION-QA: acceptance vs task + mission criteria
6. AION-SECURITY: if auth/secrets/data/integrations touched
7. Human merge
8. Vercel deploys main (preview always; production target when configured)
9. If release-bound: AION-RELEASE fills RELEASE_RECORD + CEO gate
10. After live usage: VALIDATION.md → learning events → mission close
```

## Role checklist (full cycle)

| Role | Artifact | Gate |
|------|----------|------|
| AION-PM | Mission + PRD | CEO scope approval |
| AION-ARCHITECT | Architecture + ordered tasks | Human approval for material/paid changes |
| AION-BUILDER | PR + tests | No prod secrets in git; CI green |
| AION-QA | QA report vs criteria | Failures blocked or CEO-deferred |
| AION-SECURITY | Security review (when triggered) | Blockers fixed before merge/prod |
| AION-RELEASE | Release record + deploy evidence | **CEO production / release gate** |
| Sales / founders | Real conversations | Revenue + Validation gates |

Templates: [`docs/templates/`](../templates/).

## Mission 002 — L1 evidence (development cycle ready)

| Capability | Evidence |
|------------|----------|
| Product repo live | [Ceoloo-aion-revenue-copilot](https://github.com/AION-Sys/Ceoloo-aion-revenue-copilot) |
| CI on every PR/push | GitHub Actions `CI` — green on `main` |
| Preview + production targets | Vercel project `ceoloo-aion-revenue-copilot` (team `ceoloos-projects`) |
| Builder tasks in flight | Tasks 1–5 merged; Task 6 open ([PR #10](https://github.com/AION-Sys/Ceoloo-aion-revenue-copilot/pull/10)); 7–10 remaining |
| Demo path for preview | Demo rep auth documented in product README |
| Factory → product pointer | Mission 002 + go-live docs point at product repo only |

Living status: [`docs/products/MISSION_002_CYCLE_STATUS.md`](../products/MISSION_002_CYCLE_STATUS.md).

## Remaining for L2 (production-capable MVP)

Human / platform (CEO or infra owner):

1. Confirm Supabase project + schema applied (prod; optional staging).
2. Confirm secrets on Vercel + GitHub Actions (Supabase, AI Gateway, events ingest).
3. Push/merge Revenue Factory live `lead.qualified` telemetry ([handoff](../handoffs/REVENUE_FACTORY_LIVE_EMISSION.md)) — agent push currently **403**.
4. Disable demo auth when real Supabase Auth is sole path (`ENABLE_DEMO_AUTH=false`).
5. Security review before declaring production MVP.
6. CEO **Production deployment** + **Release gate** checkboxes on Mission 002 + release record.

Builder (product repo):

7. Merge Task 6 (post-call) if still open.
8. Tasks 7–9: CRM persist, learning ingest, E2E critical path.
9. Task 10: production release record after CEO gate.

## Remaining for L3 (mission complete)

1. ≥5 real prospect conversations tracked in product `docs/VALIDATION.md`.
2. CRM + learning events confirmed in ingest logs.
3. CEO validation sign-off → Mission 002 `COMPLETE` → Mission 003 unblocked.

## Explicit non-goals of L1

- Declaring Mission 002 complete
- Skipping CEO release / validation gates
- Treating Vercel `production` target alone as formal release approval (still record CEO gate + release record)
- Starting Mission 003 while Mission 002 validation is open

## Related docs

- [`END_TO_END.md`](END_TO_END.md) — phase-by-phase roles
- [`REVENUE_COPILOT_GO_LIVE.md`](../products/REVENUE_COPILOT_GO_LIVE.md) — infra checklist
- [`MISSION_002_CYCLE_STATUS.md`](../products/MISSION_002_CYCLE_STATUS.md) — current board
- [`AION_ENGINEERING.md`](../../AION_ENGINEERING.md) — approval gates + sequential governance
