-- Mission 002 Task 1: initial schema + RLS
-- Apply with Supabase CLI: supabase db push
-- Or paste into Supabase Dashboard → SQL Editor

-- Extensions
create extension if not exists "pgcrypto";

-- ---------------------------------------------------------------------------
-- Organizations (tenant boundary)
-- ---------------------------------------------------------------------------
create table public.organizations (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.organization_members (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations (id) on delete cascade,
  user_id uuid not null references auth.users (id) on delete cascade,
  role text not null default 'rep' check (role in ('owner', 'admin', 'rep')),
  created_at timestamptz not null default now(),
  unique (organization_id, user_id)
);

create index organization_members_user_id_idx on public.organization_members (user_id);
create index organization_members_organization_id_idx on public.organization_members (organization_id);

-- ---------------------------------------------------------------------------
-- Business context
-- ---------------------------------------------------------------------------
create table public.business_contexts (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations (id) on delete cascade,
  industry text not null,
  services jsonb not null default '[]'::jsonb,
  likely_pains jsonb not null default '[]'::jsonb,
  relevant_offer text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index business_contexts_organization_id_idx on public.business_contexts (organization_id);

-- ---------------------------------------------------------------------------
-- Leads
-- ---------------------------------------------------------------------------
create table public.leads (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations (id) on delete cascade,
  business_context_id uuid references public.business_contexts (id) on delete set null,
  company_name text not null,
  contact_name text,
  source text,
  status text not null default 'new' check (status in ('new', 'contacted', 'qualified', 'closed')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index leads_organization_id_idx on public.leads (organization_id);
create index leads_business_context_id_idx on public.leads (business_context_id);
create index leads_status_idx on public.leads (status);

-- ---------------------------------------------------------------------------
-- Calls
-- ---------------------------------------------------------------------------
create table public.calls (
  id uuid primary key default gen_random_uuid(),
  lead_id uuid not null references public.leads (id) on delete cascade,
  rep_user_id uuid not null references auth.users (id) on delete restrict,
  phase text not null default 'pre' check (phase in ('pre', 'active', 'post', 'completed')),
  started_at timestamptz not null default now(),
  ended_at timestamptz
);

create index calls_lead_id_idx on public.calls (lead_id);
create index calls_rep_user_id_idx on public.calls (rep_user_id);
create index calls_phase_idx on public.calls (phase);

-- ---------------------------------------------------------------------------
-- Call outcomes (one per call)
-- ---------------------------------------------------------------------------
create table public.call_outcomes (
  id uuid primary key default gen_random_uuid(),
  call_id uuid not null unique references public.calls (id) on delete cascade,
  qualification text not null check (
    qualification in ('unqualified', 'exploring', 'qualified', 'disqualified')
  ),
  pain_points jsonb not null default '[]'::jsonb,
  objections jsonb not null default '[]'::jsonb,
  next_action text not null,
  transcript_summary text,
  created_at timestamptz not null default now()
);

create index call_outcomes_call_id_idx on public.call_outcomes (call_id);

-- ---------------------------------------------------------------------------
-- Event audit trail (CRM + learning)
-- ---------------------------------------------------------------------------
create table public.event_log (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations (id) on delete cascade,
  call_id uuid references public.calls (id) on delete set null,
  lead_id uuid references public.leads (id) on delete set null,
  event_type text not null check (event_type in ('crm', 'learning')),
  payload jsonb not null default '{}'::jsonb,
  external_id text,
  created_at timestamptz not null default now()
);

create index event_log_organization_id_idx on public.event_log (organization_id);
create index event_log_call_id_idx on public.event_log (call_id);
create index event_log_lead_id_idx on public.event_log (lead_id);
create index event_log_event_type_idx on public.event_log (event_type);

-- ---------------------------------------------------------------------------
-- updated_at trigger
-- ---------------------------------------------------------------------------
create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create trigger organizations_set_updated_at
  before update on public.organizations
  for each row execute function public.set_updated_at();

create trigger business_contexts_set_updated_at
  before update on public.business_contexts
  for each row execute function public.set_updated_at();

create trigger leads_set_updated_at
  before update on public.leads
  for each row execute function public.set_updated_at();

-- ---------------------------------------------------------------------------
-- RLS helpers
-- ---------------------------------------------------------------------------
create or replace function public.user_organization_ids()
returns setof uuid
language sql
stable
security definer
set search_path = public
as $$
  select organization_id
  from public.organization_members
  where user_id = auth.uid();
$$;

create or replace function public.lead_organization_id(p_lead_id uuid)
returns uuid
language sql
stable
security definer
set search_path = public
as $$
  select organization_id from public.leads where id = p_lead_id;
$$;

-- ---------------------------------------------------------------------------
-- Row Level Security
-- ---------------------------------------------------------------------------
alter table public.organizations enable row level security;
alter table public.organization_members enable row level security;
alter table public.business_contexts enable row level security;
alter table public.leads enable row level security;
alter table public.calls enable row level security;
alter table public.call_outcomes enable row level security;
alter table public.event_log enable row level security;

-- organizations: members can read their org
create policy "organizations_select_member"
  on public.organizations for select
  using (id in (select public.user_organization_ids()));

-- organization_members: members see co-members in shared orgs
create policy "organization_members_select_member"
  on public.organization_members for select
  using (organization_id in (select public.user_organization_ids()));

-- business_contexts
create policy "business_contexts_select_member"
  on public.business_contexts for select
  using (organization_id in (select public.user_organization_ids()));

create policy "business_contexts_insert_member"
  on public.business_contexts for insert
  with check (organization_id in (select public.user_organization_ids()));

create policy "business_contexts_update_member"
  on public.business_contexts for update
  using (organization_id in (select public.user_organization_ids()))
  with check (organization_id in (select public.user_organization_ids()));

-- leads
create policy "leads_select_member"
  on public.leads for select
  using (organization_id in (select public.user_organization_ids()));

create policy "leads_insert_member"
  on public.leads for insert
  with check (organization_id in (select public.user_organization_ids()));

create policy "leads_update_member"
  on public.leads for update
  using (organization_id in (select public.user_organization_ids()))
  with check (organization_id in (select public.user_organization_ids()));

-- calls: org membership via lead
create policy "calls_select_member"
  on public.calls for select
  using (public.lead_organization_id(lead_id) in (select public.user_organization_ids()));

create policy "calls_insert_member"
  on public.calls for insert
  with check (
    rep_user_id = auth.uid()
    and public.lead_organization_id(lead_id) in (select public.user_organization_ids())
  );

create policy "calls_update_member"
  on public.calls for update
  using (public.lead_organization_id(lead_id) in (select public.user_organization_ids()))
  with check (public.lead_organization_id(lead_id) in (select public.user_organization_ids()));

-- call_outcomes: org membership via call → lead
create policy "call_outcomes_select_member"
  on public.call_outcomes for select
  using (
    exists (
      select 1 from public.calls c
      where c.id = call_id
        and public.lead_organization_id(c.lead_id) in (select public.user_organization_ids())
    )
  );

create policy "call_outcomes_insert_member"
  on public.call_outcomes for insert
  with check (
    exists (
      select 1 from public.calls c
      where c.id = call_id
        and public.lead_organization_id(c.lead_id) in (select public.user_organization_ids())
    )
  );

create policy "call_outcomes_update_member"
  on public.call_outcomes for update
  using (
    exists (
      select 1 from public.calls c
      where c.id = call_id
        and public.lead_organization_id(c.lead_id) in (select public.user_organization_ids())
    )
  );

-- event_log
create policy "event_log_select_member"
  on public.event_log for select
  using (organization_id in (select public.user_organization_ids()));

create policy "event_log_insert_member"
  on public.event_log for insert
  with check (organization_id in (select public.user_organization_ids()));

-- Service role bypasses RLS by default in Supabase (server-side only).
