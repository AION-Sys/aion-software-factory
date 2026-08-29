import type { CallOutcome, LearningEvent } from "@/lib/sales/types";

export function outcomeToLearningEvent(outcome: CallOutcome): LearningEvent {
  return {
    eventType: "call_outcome",
    payload: {
      leadId: outcome.leadId,
      qualification: outcome.qualification,
      objectionCount: outcome.objections.length,
      painPointCount: outcome.painPoints.length,
      nextAction: outcome.nextAction,
    },
    occurredAt: outcome.occurredAt,
  };
}

export type LearningIngestResult = {
  accepted: boolean;
  eventId?: string;
};

/**
 * Sends learning events to AION learning infrastructure.
 * V1: stub; Builder wires to AION_EVENTS_INGEST_URL.
 */
export async function ingestLearningEvent(
  event: LearningEvent,
  _options?: { ingestUrl?: string; apiKey?: string },
): Promise<LearningIngestResult> {
  if (!event.eventType || !event.occurredAt) {
    return { accepted: false };
  }
  return { accepted: true, eventId: `stub-${Date.now()}` };
}
