# Revenue Copilot — Product Repo Setup

Mission 002 application code lives **only** in:

**https://github.com/AION-Sys/Ceoloo-aion-revenue-copilot**

The factory no longer carries an application seed for this product. Agents implement features in the product repo; this factory holds mission status, go-live checklists, and cross-repo handoffs.

## Repository

| Item | Value |
|------|-------|
| URL | https://github.com/AION-Sys/Ceoloo-aion-revenue-copilot |
| Status | Published — active Builder loop |
| Default branch | `main` |
| Vercel | `ceoloo-aion-revenue-copilot` (team `ceoloos-projects`) |
| Cycle status | [`MISSION_002_CYCLE_STATUS.md`](MISSION_002_CYCLE_STATUS.md) |
| Go-live | [`REVENUE_COPILOT_GO_LIVE.md`](REVENUE_COPILOT_GO_LIVE.md) |
| Full-cycle playbook | [`../workflows/PRODUCTION_DEVELOPMENT_CYCLE.md`](../workflows/PRODUCTION_DEVELOPMENT_CYCLE.md) |

## Clone and develop

```bash
git clone https://github.com/AION-Sys/Ceoloo-aion-revenue-copilot.git
cd Ceoloo-aion-revenue-copilot
cp .env.example .env.local   # fill secrets locally; never commit
npm install
npm run lint && npm run typecheck && npm test && npm run build
npm run dev
```

## Configure secrets (before production-capable MVP)

In GitHub → Settings → Secrets and variables → Actions, and in Vercel project env:

| Secret | Purpose |
|--------|---------|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Client auth |
| `SUPABASE_SERVICE_ROLE_KEY` | Server-side only |
| `AION_AI_GATEWAY_URL` | AI completions |
| `AION_AI_GATEWAY_API_KEY` | Gateway auth |
| `AION_EVENTS_INGEST_URL` | Learning events |
| `AION_EVENTS_API_KEY` | Event ingest auth |

## What's in the product repo

- Next.js + TypeScript sales workspace
- Supabase schema + RLS migrations
- Auth (Supabase SSR) + demo rep path for preview
- Pre-call, during-call, dashboard shell; post-call in flight
- AI Gateway client, CRM/learning stubs → live wiring tasks
- CI workflow (lint, typecheck, test, build)
- Docs: PRD, ARCHITECTURE, DATA_MODEL, VALIDATION

## Next Builder tasks

See product `docs/ARCHITECTURE.md` and [`MISSION_002_CYCLE_STATUS.md`](MISSION_002_CYCLE_STATUS.md). Priority: land Task 6, then Tasks 7–9.
