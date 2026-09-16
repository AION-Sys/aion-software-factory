# Revenue Copilot — Go-Live Checklist

Move Mission 002 through **L1 development cycle → L2 production MVP → L3 validation**.

Living board: [`MISSION_002_CYCLE_STATUS.md`](MISSION_002_CYCLE_STATUS.md)  
Full-cycle playbook: [`../workflows/PRODUCTION_DEVELOPMENT_CYCLE.md`](../workflows/PRODUCTION_DEVELOPMENT_CYCLE.md)

## Phase 0 — CEO / Human

| Step | Owner | Done |
|------|-------|------|
| Approve Mission 002 scope | CEO | [x] |
| Create GitHub repo [AION-Sys/Ceoloo-aion-revenue-copilot](https://github.com/AION-Sys/Ceoloo-aion-revenue-copilot) | Org admin | [x] |
| Create Supabase project (prod + optional staging) | CEO / infra | [ ] — public URL **not** detected in prod client build (2026-09-16) |
| Confirm AION AI Gateway access + model routing | Architect / platform | [ ] — see [`../handoffs/SECRETS_AND_DEMO_AUTH.md`](../handoffs/SECRETS_AND_DEMO_AUTH.md) |
| Confirm AION events ingest URL + API key | Architect / platform | [ ] — see [`../handoffs/REVENUE_FACTORY_LIVE_EMISSION.md`](../handoffs/REVENUE_FACTORY_LIVE_EMISSION.md) |
| Link Vercel project to product repo | CEO / infra | [x] — `ceoloo-aion-revenue-copilot` |
| Disable demo auth on production | CEO / Builder | [ ] — patch ready; prod still shows demo login |

## Phase 1 — Product repo (published)

| Step | Done |
|------|------|
| Seed published to product `main` | [x] (PR #3 bootstrap + follow-ons) |
| GitHub Actions CI (lint/typecheck/test/build) | [x] |
| Work only in product repo (factory seed retired) | [x] — see [`../../product-seeds/README.md`](../../product-seeds/README.md) |

Configure secrets in **GitHub Actions** and **Vercel** (never commit):

| Secret | Required for |
|--------|----------------|
| `NEXT_PUBLIC_SUPABASE_URL` | App + CI integration tests (later) |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Client auth |
| `SUPABASE_SERVICE_ROLE_KEY` | Server-side persistence |
| `AION_AI_GATEWAY_URL` | Pre-call / during-call AI |
| `AION_AI_GATEWAY_API_KEY` | Gateway auth |
| `AION_EVENTS_INGEST_URL` | Learning pipeline |
| `AION_EVENTS_API_KEY` | Event ingest auth |

## Phase 2 — Database schema

In the **product repo**:

```bash
supabase login
supabase link --project-ref <your-project-ref>
supabase db push
```

Or apply `supabase/migrations/` via SQL Editor / product `npm run db:apply-migration` helper.

Verify RLS enabled on all tables.

## Phase 3 — Vercel

| Step | Done |
|------|------|
| Import product repo in Vercel | [x] |
| Preview deploys on PR | [x] |
| `main` deploys to production target | [x] — mechanical; CEO release gate still required for Mission “MVP live” |
| Env vars set (same as GitHub secrets) | [ ] — confirm |
| Demo auth disabled for real-auth-only prod | [ ] when Supabase Auth ready |

## Phase 4 — Builder task order

Tracked in product `docs/ARCHITECTURE.md` and [`MISSION_002_CYCLE_STATUS.md`](MISSION_002_CYCLE_STATUS.md):

| # | Task | Status |
|---|------|--------|
| 1 | Supabase schema + RLS | Done |
| 2 | Auth + rep session | Done |
| 3 | Pre-call brief UI + API | Done |
| 4 | AI Gateway client (real) | Done |
| 5 | During-call guidance panel | Done |
| 6 | Post-call outcome form | Open PR #10 |
| 7 | CRM persist (Supabase) | Next |
| 8 | Learning event ingest (live) | |
| 9 | E2E critical path tests | |
| 10 | Production deploy + release record | CEO gate |

## Phase 5 — Factory cleanup

| Step | Done |
|------|------|
| Retire factory `product-seeds/aion-revenue-copilot/` application tree | [x] |
| Mission 002 points at product repo | [x] |
| Quality gate reflected when CI green | [x] — see cycle status |

## Phase 6 — Validation (mission complete)

Not at deploy — after real usage:

- [ ] 5+ real prospect conversations (`docs/VALIDATION.md` in product repo)
- [ ] CRM + learning events confirmed in ingest logs
- [ ] CEO validation sign-off → Mission 002 close → Mission 003 unblocked

## Quick status commands (product repo)

```bash
npm run lint
npm run typecheck
npm test
npm run build
```

All four must pass before every Builder handoff.
