import type { BusinessContext, Lead } from "@/lib/sales/types";

export type PreCallBrief = {
  lead: Lead;
  context: BusinessContext;
  recommendedQuestions: string[];
};

/**
 * Builds pre-call intelligence from lead + stored business context.
 * V1: rule-based stub; Builder tasks replace with AI Gateway calls.
 */
export function buildPreCallBrief(lead: Lead, context: BusinessContext): PreCallBrief {
  const recommendedQuestions = [
    `What is the biggest operational bottleneck at ${lead.companyName}?`,
    ...context.likelyPains.slice(0, 2).map((pain) => `How are you handling ${pain} today?`),
    context.relevantOffer
      ? `Would ${context.relevantOffer} be relevant if we solved that?`
      : "What would a successful outcome look like in the next 90 days?",
  ];

  return { lead, context, recommendedQuestions };
}
