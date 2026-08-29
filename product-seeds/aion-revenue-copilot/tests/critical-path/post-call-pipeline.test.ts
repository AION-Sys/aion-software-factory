import { describe, expect, it } from "vitest";
import { outcomeToLearningEvent, ingestLearningEvent } from "@/lib/learning/events";
import type { CallOutcome } from "@/lib/sales/types";

const outcome: CallOutcome = {
  id: "outcome-1",
  leadId: "lead-1",
  painPoints: ["slow response"],
  objections: [{ objection: "too expensive", resolved: false }],
  qualification: "exploring",
  nextAction: "send proposal",
  occurredAt: new Date().toISOString(),
};

describe("learning events", () => {
  it("maps call outcome to learning event", () => {
    const event = outcomeToLearningEvent(outcome);
    expect(event.eventType).toBe("call_outcome");
    expect(event.payload.leadId).toBe("lead-1");
  });

  it("accepts valid learning events", async () => {
    const event = outcomeToLearningEvent(outcome);
    const result = await ingestLearningEvent(event);
    expect(result.accepted).toBe(true);
  });
});
