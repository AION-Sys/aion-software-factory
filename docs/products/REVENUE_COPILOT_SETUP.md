# Revenue Copilot — Product Repo

## Repository (live)
**https://github.com/Ceoloo/Ceoloo-aion-revenue-copilot**

## Agent access — still required

Cloud Agent push returns **403** until the **Cursor GitHub App** has write access to this repo.

For **org repos**, configure at:
**https://github.com/organizations/Ceoloo/settings/installations**

1. Open **Cursor** → **Configure**
2. Add **`Ceoloo-aion-revenue-copilot`** under Repository access (or all repos)
3. Org owner may need to approve

Personal settings (`github.com/settings/installations`) do not apply to `Ceoloo/*` org repos.

## Manual push (if agent access is delayed)

Bootstrap + Task 1 (Supabase schema) are in `product-seeds/aion-revenue-copilot/`:

```bash
git clone https://github.com/Ceoloo/Ceoloo-aion-revenue-copilot.git
cd Ceoloo-aion-revenue-copilot
cp -r /path/to/aion-software-factory/product-seeds/aion-revenue-copilot/* .
cp -r /path/to/aion-software-factory/product-seeds/aion-revenue-copilot/.[!.]* . 2>/dev/null || true
npm install && npm run lint && npm run typecheck && npm test && npm run build
git checkout -b cursor/supabase-schema-rls-be3c
git add -A && git commit -m "feat: bootstrap + Supabase schema (Task 1)"
git push -u origin cursor/supabase-schema-rls-be3c
# Also push main if repo is still empty README-only:
git checkout main && git merge cursor/supabase-schema-rls-be3c && git push origin main
```

## Secrets (before production)

| Secret | Purpose |
|--------|---------|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Client auth |
| `SUPABASE_SERVICE_ROLE_KEY` | Server-side only |
| `AION_AI_GATEWAY_URL` | AI completions |
| `AION_AI_GATEWAY_API_KEY` | Gateway auth |
| `AION_EVENTS_INGEST_URL` | Learning events |
| `AION_EVENTS_API_KEY` | Event ingest auth |

## Next Builder task

Task 2 — Auth + rep session (after Task 1 PR merges).
