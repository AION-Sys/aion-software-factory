import type {
  DbBusinessContext,
  DbCallOutcome,
  DbLead,
  DbObjectionRecord,
} from "@/lib/db/types";
import type {
  BusinessContext,
  CallOutcome,
  Lead,
  ObjectionRecord,
} from "@/lib/sales/types";

export function leadFromDb(row: DbLead): Lead {
  return {
    id: row.id,
    companyName: row.company_name,
    contactName: row.contact_name ?? undefined,
    source: row.source ?? undefined,
    businessContextId: row.business_context_id ?? undefined,
  };
}

export function leadToDbInsert(
  lead: Pick<Lead, "companyName" | "contactName" | "source" | "businessContextId">,
  organizationId: string,
): Pick<
  DbLead,
  "organization_id" | "company_name" | "contact_name" | "source" | "business_context_id"
> {
  return {
    organization_id: organizationId,
    company_name: lead.companyName,
    contact_name: lead.contactName ?? null,
    source: lead.source ?? null,
    business_context_id: lead.businessContextId ?? null,
  };
}

export function businessContextFromDb(row: DbBusinessContext): BusinessContext {
  return {
    id: row.id,
    industry: row.industry,
    services: row.services,
    likelyPains: row.likely_pains,
    relevantOffer: row.relevant_offer ?? undefined,
  };
}

function objectionFromDb(row: DbObjectionRecord): ObjectionRecord {
  return {
    objection: row.objection,
    suggestedReframe: row.suggested_reframe,
    resolved: row.resolved,
  };
}

function objectionToDb(row: ObjectionRecord): DbObjectionRecord {
  return {
    objection: row.objection,
    suggested_reframe: row.suggestedReframe,
    resolved: row.resolved,
  };
}

export function callOutcomeFromDb(row: DbCallOutcome, leadId: string): CallOutcome {
  return {
    id: row.id,
    leadId,
    painPoints: row.pain_points,
    objections: row.objections.map(objectionFromDb),
    qualification: row.qualification,
    nextAction: row.next_action,
    transcriptSummary: row.transcript_summary ?? undefined,
    occurredAt: row.created_at,
  };
}

export function callOutcomeToDbInsert(
  outcome: CallOutcome,
  callId: string,
): Pick<
  DbCallOutcome,
  "call_id" | "qualification" | "pain_points" | "objections" | "next_action" | "transcript_summary"
> {
  return {
    call_id: callId,
    qualification: outcome.qualification,
    pain_points: outcome.painPoints,
    objections: outcome.objections.map(objectionToDb),
    next_action: outcome.nextAction,
    transcript_summary: outcome.transcriptSummary ?? null,
  };
}
