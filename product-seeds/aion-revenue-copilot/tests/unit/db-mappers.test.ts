import { describe, expect, it } from "vitest";
import {
  businessContextFromDb,
  callOutcomeFromDb,
  callOutcomeToDbInsert,
  leadFromDb,
  leadToDbInsert,
} from "@/lib/db/mappers";
import type { CallOutcome } from "@/lib/sales/types";

describe("db mappers", () => {
  it("maps lead rows to domain", () => {
    const lead = leadFromDb({
      id: "lead-1",
      organization_id: "org-1",
      business_context_id: "ctx-1",
      company_name: "Acme HVAC",
      contact_name: "Jane Doe",
      source: "outbound",
      status: "new",
      created_at: "2026-08-31T00:00:00.000Z",
      updated_at: "2026-08-31T00:00:00.000Z",
    });

    expect(lead.companyName).toBe("Acme HVAC");
    expect(lead.contactName).toBe("Jane Doe");
    expect(lead.businessContextId).toBe("ctx-1");
  });

  it("maps domain lead to insert shape", () => {
    const insert = leadToDbInsert(
      {
        companyName: "Acme HVAC",
        contactName: "Jane Doe",
        source: "outbound",
      },
      "org-1",
    );

    expect(insert.organization_id).toBe("org-1");
    expect(insert.company_name).toBe("Acme HVAC");
    expect(insert.business_context_id).toBeNull();
  });

  it("maps business context rows to domain", () => {
    const context = businessContextFromDb({
      id: "ctx-1",
      organization_id: "org-1",
      industry: "home-services",
      services: ["HVAC install"],
      likely_pains: ["slow response"],
      relevant_offer: "AI follow-up",
      created_at: "2026-08-31T00:00:00.000Z",
      updated_at: "2026-08-31T00:00:00.000Z",
    });

    expect(context.likelyPains).toEqual(["slow response"]);
    expect(context.relevantOffer).toBe("AI follow-up");
  });

  it("round-trips call outcomes", () => {
    const outcome: CallOutcome = {
      id: "outcome-1",
      leadId: "lead-1",
      painPoints: ["slow response"],
      objections: [{ objection: "too expensive", resolved: false }],
      qualification: "exploring",
      nextAction: "send proposal",
      occurredAt: "2026-08-31T00:00:00.000Z",
    };

    const insert = callOutcomeToDbInsert(outcome, "call-1");
    const restored = callOutcomeFromDb(
      {
        id: outcome.id,
        call_id: "call-1",
        qualification: insert.qualification,
        pain_points: insert.pain_points,
        objections: insert.objections,
        next_action: insert.next_action,
        transcript_summary: null,
        created_at: outcome.occurredAt,
      },
      outcome.leadId,
    );

    expect(restored.qualification).toBe("exploring");
    expect(restored.objections[0]?.objection).toBe("too expensive");
    expect(restored.nextAction).toBe("send proposal");
  });
});
