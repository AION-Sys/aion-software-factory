# Revenue Copilot — Product Repo Setup

Mission 002 application code lives in **[AION-Sys/Ceoloo-aion-revenue-copilot](https://github.com/AION-Sys/Ceoloo-aion-revenue-copilot)**.

The factory copy in `product-seeds/aion-revenue-copilot/` is kept in sync until the seed is fully published and removed from this repo.

## Repository

| Item | Value |
|------|-------|
| URL | https://github.com/AION-Sys/Ceoloo-aion-revenue-copilot |
| Status | Created — seed publish pending |
| Default branch | `main` |

## Publish seed (one-time)

If the product repo only has a placeholder README, push the factory seed:

```bash
git clone https://github.com/AION-Sys/Ceoloo-aion-revenue-copilot.git /tmp/aion-revenue-copilot
cd /workspace/product-seeds/aion-revenue-copilot
npm install && npm run lint && npm run typecheck && npm test && npm run build

# Copy seed into clone (exclude node_modules, .next)
cp -r . /tmp/aion-revenue-copilot/
cd /tmp/aion-revenue-copilot
rm -rf node_modules .next
git add -A
git commit -m "feat: bootstrap Mission 002 Revenue Conversion Copilot"
git push origin main
```

Or push from a machine with write access to `AION-Sys/Ceoloo-aion-revenue-copilot`.

## Configure secrets (before production)

In GitHub repo settings → Secrets, and Vercel/Supabase as applicable:

| Secret | Purpose |
|--------|---------|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Client auth |
| `SUPABASE_SERVICE_ROLE_KEY` | Server-side only |
| `AION_AI_GATEWAY_URL` | AI completions |
| `AION_AI_GATEWAY_API_KEY` | Gateway auth |
| `AION_EVENTS_INGEST_URL` | Learning events |
| `AION_EVENTS_API_KEY` | Event ingest auth |

## After seed is published

Delete `product-seeds/aion-revenue-copilot/` from `aion-software-factory` in a follow-up PR so the factory stays governance-only.

## What's in the seed

- Next.js 15 + TypeScript scaffold
- Supabase schema + RLS migration (Task 1)
- `lib/{ai,intelligence,sales,learning,crm,db}/` with domain stubs, mappers, and tests
- `docs/{PRD,ARCHITECTURE,DATA_MODEL,VALIDATION}.md`
- CI workflow (lint, typecheck, test, build)

## Go-live checklist

Full steps: [`REVENUE_COPILOT_GO_LIVE.md`](REVENUE_COPILOT_GO_LIVE.md)

## Next Builder Tasks

In the **product repo** — see `docs/ARCHITECTURE.md` task table. Task 1 (schema + RLS) is in the seed; next is Task 2 (auth + rep session).
