import { WorkflowPhase } from "@/components/WorkflowPhase";

const phases = [
  {
    id: "pre-call",
    title: "Before conversation",
    items: [
      "Lead intelligence",
      "Likely pains",
      "Relevant offer",
      "Recommended questions",
    ],
  },
  {
    id: "during-call",
    title: "During conversation",
    items: [
      "Script guidance",
      "Discovery checklist",
      "Objection detection",
      "Qualification capture",
      "Next-best action",
    ],
  },
  {
    id: "post-call",
    title: "After conversation",
    items: [
      "Structured outcome",
      "CRM event",
      "Learning event",
      "Next action",
    ],
  },
] as const;

export default function HomePage() {
  return (
    <main className="page">
      <header className="header">
        <p className="eyebrow">AION · Mission 002</p>
        <h1>Revenue Conversion Copilot</h1>
        <p className="subtitle">
          AI-assisted sales workspace — pre-call → call → post-call
        </p>
      </header>
      <section className="grid">
        {phases.map((phase) => (
          <WorkflowPhase key={phase.id} title={phase.title} items={phase.items} />
        ))}
      </section>
    </main>
  );
}
