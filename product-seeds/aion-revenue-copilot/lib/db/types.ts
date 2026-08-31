/**
 * Database row types — keep aligned with supabase/migrations and docs/DATA_MODEL.md
 */

export type DbOrganization = {
  id: string;
  name: string;
  created_at: string;
  updated_at: string;
};

export type DbOrganizationMember = {
  id: string;
  organization_id: string;
  user_id: string;
  role: "owner" | "admin" | "rep";
  created_at: string;
};

export type DbBusinessContext = {
  id: string;
  organization_id: string;
  industry: string;
  services: string[];
  likely_pains: string[];
  relevant_offer: string | null;
  created_at: string;
  updated_at: string;
};

export type DbLead = {
  id: string;
  organization_id: string;
  business_context_id: string | null;
  company_name: string;
  contact_name: string | null;
  source: string | null;
  status: "new" | "contacted" | "qualified" | "closed";
  created_at: string;
  updated_at: string;
};

export type DbCall = {
  id: string;
  lead_id: string;
  rep_user_id: string;
  phase: "pre" | "active" | "post" | "completed";
  started_at: string;
  ended_at: string | null;
};

export type DbObjectionRecord = {
  objection: string;
  suggested_reframe?: string;
  resolved: boolean;
};

export type DbCallOutcome = {
  id: string;
  call_id: string;
  qualification: "unqualified" | "exploring" | "qualified" | "disqualified";
  pain_points: string[];
  objections: DbObjectionRecord[];
  next_action: string;
  transcript_summary: string | null;
  created_at: string;
};

export type DbEventLog = {
  id: string;
  organization_id: string;
  call_id: string | null;
  lead_id: string | null;
  event_type: "crm" | "learning";
  payload: Record<string, unknown>;
  external_id: string | null;
  created_at: string;
};
