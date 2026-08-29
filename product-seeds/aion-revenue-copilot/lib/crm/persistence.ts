import type { CallOutcome, CrmEvent } from "@/lib/sales/types";

export function outcomeToCrmEvent(outcome: CallOutcome): CrmEvent {
  return {
    eventType: "call_completed",
    leadId: outcome.leadId,
    payload: {
      qualification: outcome.qualification,
      nextAction: outcome.nextAction,
      outcomeId: outcome.id,
    },
    occurredAt: outcome.occurredAt,
  };
}

export type CrmPersistResult = {
  ok: boolean;
  recordId?: string;
};

/**
 * Persists lead/call state. V1 stub; Builder wires Supabase.
 */
export async function persistCallOutcome(outcome: CallOutcome): Promise<CrmPersistResult> {
  if (!outcome.leadId || !outcome.id) {
    return { ok: false };
  }
  return { ok: true, recordId: outcome.id };
}
