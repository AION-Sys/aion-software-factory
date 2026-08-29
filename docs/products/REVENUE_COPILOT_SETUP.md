# Revenue Copilot — Product Repo Setup

Mission 002 product code lives in **`product-seeds/aion-revenue-copilot/`** until the separate GitHub repository is created. This folder is a **one-time bootstrap** — not the long-term home for application code.

## Target Repository
**https://github.com/Ceoloo/aion-revenue-copilot** (public, matches other AION repos)

## CEO / Human Action Required

The Cloud Agent token cannot create new GitHub repositories. A human with org admin access must:

### 1. Create the repository
- Name: `aion-revenue-copilot`
- Org: `Ceoloo`
- Visibility: public
- Do **not** initialize with README (seed includes full scaffold)

### 2. Publish the seed

```bash
cd product-seeds/aion-revenue-copilot
npm install
npm run lint && npm run typecheck && npm test && npm run build
git init -b main
git add -A
git commit -m "feat: bootstrap Mission 002 Revenue Conversion Copilot"
git remote add origin git@github.com:Ceoloo/aion-revenue-copilot.git
git push -u origin main
```

### 3. Configure secrets (before production)
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

### 4. Remove seed from factory (after push)
Delete `product-seeds/aion-revenue-copilot/` from `aion-software-factory` in a follow-up PR so the factory stays governance-only.

## What's in the seed

- Next.js 15 + TypeScript scaffold
- `lib/{ai,intelligence,sales,learning,crm}/` with domain stubs and tests
- `docs/{PRD,ARCHITECTURE,DATA_MODEL,VALIDATION}.md`
- CI workflow (lint, typecheck, test, build)
- Verified locally: all quality checks pass

## Next Builder Tasks

See `product-seeds/aion-revenue-copilot/docs/ARCHITECTURE.md` task table — start with Supabase schema + auth (Tasks 1–2).
