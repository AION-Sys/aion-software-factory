# Handoff — Confirm secrets + disable demo auth (Mission 002)

## Status
**PARTIAL — HUMAN UNBLOCKS REQUIRED**

| Check | Result (2026-09-16) |
|-------|---------------------|
| Production login demo mode | **ON** — `/login` shows Preview rep + `ENABLE_DEMO_AUTH=false` hint |
| `NEXT_PUBLIC_SUPABASE_*` in client build | **Likely unset** — no `*.supabase.co` host in production JS bundles (Next inlines `NEXT_PUBLIC_*` at build) |
| Vercel env var listing (names only) | **Blocked** — Composio Vercel connection pending; native Vercel MCP has no env API |
| GitHub Actions secrets listing | **Blocked** — `gh` 403; Composio GitHub connection pending |
| Supabase project / API keys | **Blocked** — Composio Supabase connection pending |
| Apply demo-auth disable in product repo | **Blocked** — `cursor[bot]` **403** push to `AION-Sys/Ceoloo-aion-revenue-copilot` |

Local patch prepared and unit-tested (`tests/unit/demo-auth.test.ts` — 5 passed).

## Required secrets (presence only — never paste values into chat)

Set on **Vercel** project `ceoloo-aion-revenue-copilot` (Production + Preview) **and** GitHub Actions secrets:

| Name | Required for |
|------|----------------|
| `NEXT_PUBLIC_SUPABASE_URL` | Auth + data (rebuild after set) |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Client auth |
| `SUPABASE_SERVICE_ROLE_KEY` | Server persistence / seed |
| `AION_AI_GATEWAY_URL` | AI brief/guidance |
| `AION_AI_GATEWAY_API_KEY` | Gateway auth |
| `AION_EVENTS_INGEST_URL` | Learning events |
| `AION_EVENTS_API_KEY` | Event ingest auth |
| `ENABLE_DEMO_AUTH` | Set to `false` on Production (belt-and-suspenders with code change) |

After setting `NEXT_PUBLIC_*`, **redeploy** so they are baked into the client bundle.

## Disable demo auth (product repo)

### Option A — apply patch (CEO / machine with write access)

```bash
git clone git@github.com:AION-Sys/Ceoloo-aion-revenue-copilot.git
cd Ceoloo-aion-revenue-copilot
git apply /path/to/aion-software-factory/docs/handoffs/patches/0002-fix-disable-demo-auth-by-default.patch
npm test -- tests/unit/demo-auth.test.ts
git checkout -b cursor/disable-demo-auth-1bd1
git add -A && git commit -m "fix: disable demo auth by default for production"
git push -u origin cursor/disable-demo-auth-1bd1
```

Patch file: [`patches/0002-fix-disable-demo-auth-by-default.patch`](patches/0002-fix-disable-demo-auth-by-default.patch)

### Option B — grant `cursor[bot]` write access on the product repo

Then re-run an agent to push the same branch.

### What the patch does

- `isDemoAuthEnabled()` defaults to **false**; only `ENABLE_DEMO_AUTH=true|1` enables demo
- Updates `.env.example`, README, login copy, unit tests

## Unblock agent confirmation (optional but recommended)

Complete these Composio OAuth links (expire ~10 minutes; re-request if expired):

- [Connect Vercel](https://connect.composio.dev/link/lk_hJ4-_QN10G7Y)
- [Connect Supabase](https://connect.composio.dev/link/lk_b5xf12jro66A)
- [Connect GitHub](https://connect.composio.dev/link/lk_owUJtXkEVmCG)

Once active, an agent can list env/secret **names**, set `ENABLE_DEMO_AUTH=false` on Vercel, and confirm Supabase project status — without printing secret values.

## Manual verify after apply

1. Production `/login` no longer shows Preview rep credentials.
2. Sign-in requires a real Supabase Auth user.
3. Client bundle contains your `*.supabase.co` host (public URL only).
4. Brief/guidance APIs work with gateway secrets set.

## Mission linkage

Unblocks Mission 002 Phase 0 / L2 item: confirm Supabase + secrets; disable demo auth.
