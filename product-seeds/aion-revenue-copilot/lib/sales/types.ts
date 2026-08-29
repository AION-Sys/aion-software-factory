/**
 * Core domain types for the conversion copilot.
 * Architect-owned contracts — extend as MVP tasks land.
 */

export type Lead = {
  id: string;
  companyName: string;
  contactName?: string;
  source?: string;
  businessContextId?: string;
};

export type BusinessContext = {
  id: string;
  industry: string;
  services: string[];
  likelyPains: string[];
  relevantOffer?: string;
};

export type QualificationState = "unqualified" | "exploring" | "qualified" | "disqualified";

export type CallOutcome = {
  id: string;
  leadId: string;
  painPoints: string[];
  objections: ObjectionRecord[];
  qualification: QualificationState;
  nextAction: string;
  transcriptSummary?: string;
  occurredAt: string;
};

export type ObjectionRecord = {
  objection: string;
  suggestedReframe?: string;
  resolved: boolean;
};

export type LearningEvent = {
  eventType: "call_outcome" | "objection_pattern" | "qualification_shift";
  payload: Record<string, unknown>;
  occurredAt: string;
};

export type CrmEvent = {
  eventType: "lead_updated" | "call_completed" | "next_action_scheduled";
  leadId: string;
  payload: Record<string, unknown>;
  occurredAt: string;
};
