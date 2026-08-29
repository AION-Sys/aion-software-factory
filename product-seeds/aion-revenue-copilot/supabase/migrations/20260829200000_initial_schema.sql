-- Mission 002 Task 1: initial schema + RLS for Revenue Conversion Copilot
-- Tables: organizations, organization_members, business_contexts, leads,
--         calls, call_outcomes, event_log

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

-- ---------------------------------------------------------------------------
-- Business context + leads
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

-- ---------------------------------------------------------------------------
-- Calls + outcomes
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
create index event_log_lead_id_idx on public.event_log (lead_id);
create index event_log_call_id_idx on public.event_log (call_id);

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
-- RLS helper: orgs the current user belongs to
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

-- ---------------------------------------------------------------------------
-- Enable RLS
-- ---------------------------------------------------------------------------
alter table public.organizations enable row level security;
alter table public.organization_members enable row level security;
alter table public.business_contexts enable row level security;
alter table public.leads enable row level security;
alter table public.calls enable row level security;
alter table public.call_outcomes enable row level security;
alter table public.event_log enable row level security;

-- organizations
create policy "members read own organizations"
  on public.organizations for select
  using (id in (select public.user_organization_ids()));

create policy "owners create organizations"
  on public.organizations for insert
  with check (true);

create policy "admins update own organizations"
  on public.organizations for update
  using (
    id in (
      select organization_id from public.organization_members
      where user_id = auth.uid() and role in ('owner', 'admin')
    )
  );

-- organization_members
create policy "members read org membership"
  on public.organization_members for select
  using (organization_id in (select public.user_organization_ids()));

create policy "admins manage org membership"
  on public.organization_members for all
  using (
    organization_id in (
      select organization_id from public.organization_members
      where user_id = auth.uid() and role in ('owner', 'admin')
    )
  )
  with check (
    organization_id in (
      select organization_id from public.organization_members
      where user_id = auth.uid() and role in ('owner', 'admin')
    )
  );

create policy "users join org as rep"
  on public.organization_members for insert
  with check (user_id = auth.uid() and role = 'rep');

-- business_contexts
create policy "members read business contexts"
  on public.business_contexts for select
  using (organization_id in (select public.user_organization_ids()));

create policy "members write business contexts"
  on public.business_contexts for all
  using (organization_id in (select public.user_organization_ids()))
  with check (organization_id in (select public.user_organization_ids()));

-- leads
create policy "members read leads"
  on public.leads for select
  using (organization_id in (select public.user_organization_ids()));

create policy "members write leads"
  on public.leads for all
  using (organization_id in (select public.user_organization_ids()))
  with check (organization_id in (select public.user_organization_ids()));

-- calls (via lead org)
create policy "members read calls"
  on public.calls for select
  using (
    lead_id in (
      select l.id from public.leads l
      where l.organization_id in (select public.user_organization_ids())
    )
  );

create policy "reps manage own calls"
  on public.calls for all
  using (
    rep_user_id = auth.uid()
    and lead_id in (
      select l.id from public.leads l
      where l.organization_id in (select public.user_organization_ids())
    )
  )
  with check (
    rep_user_id = auth.uid()
    and lead_id in (
      select l.id from public.leads l
      where l.organization_id in (select public.user_organization_ids())
    )
  );

-- call_outcomes (via call → lead → org)
create policy "members read call outcomes"
  on public.call_outcomes for select
  using (
    call_id in (
      select c.id from public.calls c
      join public.leads l on l.id = c.lead_id
      where l.organization_id in (select public.user_organization_ids())
    )
  );

create policy "reps write call outcomes"
  on public.call_outcomes for all
  using (
    call_id in (
      select c.id from public.calls c
      where c.rep_user_id = auth.uid()
        and c.lead_id in (
          select l.id from public.leads l
          where l.organization_id in (select public.user_organization_ids())
        )
    )
  )
  with check (
    call_id in (
      select c.id from public.calls c
      where c.rep_user_id = auth.uid()
        and c.lead_id in (
          select l.id from public.leads l
          where l.organization_id in (select public.user_organization_ids())
        )
    )
  );

-- event_log
create policy "members read event log"
  on public.event_log for select
  using (organization_id in (select public.user_organization_ids()));

create policy "members write event log"
  on public.event_log for insert
  with check (organization_id in (select public.user_organization_ids()));
