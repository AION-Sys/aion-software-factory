# Revenue Copilot — Go-Live Checklist

Use this checklist to move Mission 002 from factory seed → product repo → first Builder PRs.

## Phase 0 — CEO / Human (before Builder scale-up)

| Step | Owner | Done |
|------|-------|------|
| Approve Mission 002 scope | CEO | [x] |
| Create GitHub repo [AION-Sys/Ceoloo-aion-revenue-copilot](https://github.com/AION-Sys/Ceoloo-aion-revenue-copilot) | Org admin | [x] |
| Create Supabase project (prod + optional staging) | CEO / infra | [ ] |
| Confirm AION AI Gateway access + model routing | Architect / platform | [ ] |
| Confirm AION events ingest URL + API key | Architect / platform | [ ] |

## Phase 1 — Publish product repo

Repo exists at **https://github.com/AION-Sys/Ceoloo-aion-revenue-copilot**. Push the factory seed if the remote still only has a placeholder README:

```bash
git clone https://github.com/AION-Sys/Ceoloo-aion-revenue-copilot.git /tmp/aion-revenue-copilot
cd product-seeds/aion-revenue-copilot
npm install && npm run lint && npm run typecheck && npm test && npm run build
cp -r . /tmp/aion-revenue-copilot/
cd /tmp/aion-revenue-copilot && rm -rf node_modules .next
git add -A && git commit -m "feat: bootstrap Mission 002 Revenue Conversion Copilot"
git push origin main
```

Then in GitHub repo settings → **Secrets and variables → Actions**:

| Secret | Required for |
|--------|----------------|
| `NEXT_PUBLIC_SUPABASE_URL` | App + CI integration tests (later) |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Client auth |
| `SUPABASE_SERVICE_ROLE_KEY` | Server-side persistence |
| `AION_AI_GATEWAY_URL` | Pre-call / during-call AI |
| `AION_AI_GATEWAY_API_KEY` | Gateway auth |
| `AION_EVENTS_INGEST_URL` | Learning pipeline |
| `AION_EVENTS_API_KEY` | Event ingest auth |

## Phase 2 — Apply database schema

In the **product repo** (after publish):

```bash
# Install Supabase CLI if needed: https://supabase.com/docs/guides/cli
supabase login
supabase link --project-ref <your-project-ref>
supabase db push
```

Or paste `supabase/migrations/20250831000000_initial_schema.sql` into Supabase SQL Editor.

Verify RLS is enabled on all tables (Dashboard → Authentication → Policies).

## Phase 3 — Vercel (preview first)

1. Import [AION-Sys/Ceoloo-aion-revenue-copilot](https://github.com/AION-Sys/Ceoloo-aion-revenue-copilot) in Vercel
2. Set environment variables (same as GitHub secrets)
3. Confirm preview deploy succeeds on PR
4. **Do not** promote to production until CEO release gate

## Phase 4 — Builder task order

From `docs/ARCHITECTURE.md` in the product repo:

| # | Task | Status after this PR |
|---|------|----------------------|
| 1 | Supabase schema + RLS | ✅ Migration in seed |
| 2 | Auth + rep session | Next PR |
| 3 | Pre-call brief UI + API | |
| 4 | AI Gateway client (real) | |
| 5 | During-call guidance panel | |
| 6 | Post-call outcome form | |
| 7 | CRM persist (Supabase) | |
| 8 | Learning event ingest (live) | |
| 9 | E2E critical path tests | |
| 10 | Production deploy + release record | CEO gate |

## Phase 5 — Factory cleanup (after product repo live)

In **aion-software-factory**, open a PR to:

- [ ] Remove `product-seeds/aion-revenue-copilot/` (product code lives in product repo only)
- [ ] Update `missions/MISSION-002.md` product repo link if needed
- [ ] Check off **Quality** gate when CI green on product repo

## Phase 6 — Validation (mission complete)

Not at deploy — after real usage:

- [ ] 5+ real prospect conversations (`docs/VALIDATION.md`)
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
