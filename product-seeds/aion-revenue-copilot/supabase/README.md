# Supabase — Revenue Conversion Copilot

## Apply migration

### Option A — Supabase CLI (recommended)

```bash
# From repo root, after linking project: supabase link --project-ref <ref>
supabase db push
```

### Option B — Dashboard

1. Open Supabase project → **SQL Editor**
2. Paste contents of `migrations/20250831000000_initial_schema.sql`
3. Run

## Verify

After applying, confirm tables exist:

- `organizations`, `organization_members`
- `business_contexts`, `leads`, `calls`, `call_outcomes`, `event_log`

RLS should be **enabled** on all public tables.

## Bootstrap a tenant (manual, post-auth)

Once Task 2 (auth) lands, seed the first org for a rep:

```sql
insert into public.organizations (name) values ('AION Sales') returning id;
-- Link auth user via organization_members (user_id from auth.users)
```

## Service role

Use `SUPABASE_SERVICE_ROLE_KEY` only in server-side code (API routes, server actions). Never expose to the browser.
