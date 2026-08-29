import { describe, expect, it } from "vitest";
import {
  businessContextRowToDomain,
  callOutcomeRowToDomain,
  callOutcomeToRow,
  domainLeadToInsert,
  leadRowToDomain,
} from "@/lib/crm/mappers";
import type { CallOutcome } from "@/lib/sales/types";

describe("crm mappers", () => {
  it("maps lead row to domain", () => {
    const lead = leadRowToDomain({
      id: "lead-1",
      organization_id: "org-1",
      business_context_id: "ctx-1",
      company_name: "Acme HVAC",
      contact_name: "Jane",
      source: "outbound",
      status: "new",
      created_at: "2026-08-29T00:00:00Z",
      updated_at: "2026-08-29T00:00:00Z",
    });
    expect(lead.companyName).toBe("Acme HVAC");
    expect(lead.businessContextId).toBe("ctx-1");
  });

  it("maps domain lead to insert row", () => {
    const insert = domainLeadToInsert(
      { id: "lead-1", companyName: "Acme HVAC" },
      "org-1",
    );
    expect(insert.organization_id).toBe("org-1");
    expect(insert.company_name).toBe("Acme HVAC");
  });

  it("round-trips call outcome through row mapper", () => {
    const outcome: CallOutcome = {
      id: "outcome-1",
      leadId: "lead-1",
      painPoints: ["slow response"],
      objections: [{ objection: "price", resolved: false }],
      qualification: "exploring",
      nextAction: "follow up",
      occurredAt: "2026-08-29T00:00:00Z",
    };
    const row = callOutcomeToRow(outcome, "call-1");
    expect(row.call_id).toBe("call-1");
    const domain = callOutcomeRowToDomain(
      {
        id: row.id!,
        call_id: row.call_id,
        qualification: row.qualification,
        pain_points: row.pain_points ?? [],
        objections: row.objections ?? [],
        next_action: row.next_action,
        transcript_summary: row.transcript_summary ?? null,
        created_at: outcome.occurredAt,
      },
      outcome.leadId,
    );
    expect(domain.qualification).toBe("exploring");
    expect(domain.painPoints).toEqual(["slow response"]);
  });

  it("maps business context jsonb arrays", () => {
    const ctx = businessContextRowToDomain({
      id: "ctx-1",
      organization_id: "org-1",
      industry: "home-services",
      services: ["HVAC"],
      likely_pains: ["slow follow-up"],
      relevant_offer: "trial",
      created_at: "2026-08-29T00:00:00Z",
      updated_at: "2026-08-29T00:00:00Z",
    });
    expect(ctx.likelyPains).toEqual(["slow follow-up"]);
  });
});
