# Revenue Copilot — Product Repo

## Repository (live)
**https://github.com/Ceoloo/Ceoloo-aion-revenue-copilot**

Mission 002 application code lives in this repo — not in the factory.

## Publish bootstrap (one-time)

The factory seed at `product-seeds/aion-revenue-copilot/` must be pushed to the product repo once. The repo currently contains only the default GitHub README.

From a machine with **push access** to `Ceoloo/Ceoloo-aion-revenue-copilot`:

```bash
git clone https://github.com/Ceoloo/Ceoloo-aion-revenue-copilot.git
cd Ceoloo-aion-revenue-copilot

# Copy seed from factory clone (or use product-seeds/ in aion-software-factory)
cp -r /path/to/aion-software-factory/product-seeds/aion-revenue-copilot/* .
cp -r /path/to/aion-software-factory/product-seeds/aion-revenue-copilot/.[!.]* . 2>/dev/null || true

npm install
npm run lint && npm run typecheck && npm test && npm run build

git add -A
git commit -m "feat: bootstrap Mission 002 Revenue Conversion Copilot"
git push origin main
```

After push succeeds, delete `product-seeds/` from `aion-software-factory` (factory stays governance-only).

## Agent access (required for Builder PRs)

Adding `cursor[bot]` as a collaborator is **not sufficient** for Cloud Agents. You must also grant the **Cursor GitHub App** access to this repository:

1. GitHub → **Settings** → **Applications** → **Installed GitHub Apps**
2. Click **Cursor** → **Configure**
3. Under **Repository access**, add **`Ceoloo-aion-revenue-copilot`** (or enable all repositories)
4. Save — then reply here so the agent can push

Org owners may need to approve third-party app access for new repos.

## Secrets (before production)

Configure in GitHub repo settings → Secrets, plus Vercel/Supabase:

| Secret | Purpose |
|--------|---------|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Client auth |
| `SUPABASE_SERVICE_ROLE_KEY` | Server-side only |
| `AION_AI_GATEWAY_URL` | AI completions |
| `AION_AI_GATEWAY_API_KEY` | Gateway auth |
| `AION_EVENTS_INGEST_URL` | Learning events |
| `AION_EVENTS_API_KEY` | Event ingest auth |

## Next Builder tasks

See product repo `docs/ARCHITECTURE.md` — start with **Task 1: Supabase schema + RLS**.
