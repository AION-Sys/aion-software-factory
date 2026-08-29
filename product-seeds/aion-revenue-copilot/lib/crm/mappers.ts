import type { Database, BusinessContextRow, CallOutcomeRow, LeadRow } from "@/lib/supabase/database.types";
import type {
  BusinessContext,
  CallOutcome,
  Lead,
  ObjectionRecord,
  QualificationState,
} from "@/lib/sales/types";

function asStringArray(value: unknown): string[] {
  if (!Array.isArray(value)) return [];
  return value.filter((item): item is string => typeof item === "string");
}

function asObjections(value: unknown): ObjectionRecord[] {
  if (!Array.isArray(value)) return [];
  return value.flatMap((item) => {
    if (typeof item !== "object" || item === null) return [];
    const record = item as Record<string, unknown>;
    if (typeof record.objection !== "string") return [];
    return [{
      objection: record.objection,
      suggestedReframe:
        typeof record.suggestedReframe === "string" ? record.suggestedReframe : undefined,
      resolved: Boolean(record.resolved),
    }];
  });
}

export function leadRowToDomain(row: LeadRow): Lead {
  return {
    id: row.id,
    companyName: row.company_name,
    contactName: row.contact_name ?? undefined,
    source: row.source ?? undefined,
    businessContextId: row.business_context_id ?? undefined,
  };
}

export function businessContextRowToDomain(row: BusinessContextRow): BusinessContext {
  return {
    id: row.id,
    industry: row.industry,
    services: asStringArray(row.services),
    likelyPains: asStringArray(row.likely_pains),
    relevantOffer: row.relevant_offer ?? undefined,
  };
}

export function callOutcomeToRow(
  outcome: CallOutcome,
  callId: string,
): Database["public"]["Tables"]["call_outcomes"]["Insert"] {
  return {
    id: outcome.id,
    call_id: callId,
    qualification: outcome.qualification,
    pain_points: outcome.painPoints,
    objections: outcome.objections,
    next_action: outcome.nextAction,
    transcript_summary: outcome.transcriptSummary ?? null,
  };
}

export function callOutcomeRowToDomain(row: CallOutcomeRow, leadId: string): CallOutcome {
  return {
    id: row.id,
    leadId,
    painPoints: asStringArray(row.pain_points),
    objections: asObjections(row.objections),
    qualification: row.qualification as QualificationState,
    nextAction: row.next_action,
    transcriptSummary: row.transcript_summary ?? undefined,
    occurredAt: row.created_at,
  };
}

export function domainLeadToInsert(
  lead: Lead,
  organizationId: string,
): Database["public"]["Tables"]["leads"]["Insert"] {
  return {
    id: lead.id,
    organization_id: organizationId,
    business_context_id: lead.businessContextId ?? null,
    company_name: lead.companyName,
    contact_name: lead.contactName ?? null,
    source: lead.source ?? null,
  };
}
