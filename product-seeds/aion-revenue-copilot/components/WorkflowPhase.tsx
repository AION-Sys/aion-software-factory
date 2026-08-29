type WorkflowPhaseProps = {
  title: string;
  items: readonly string[];
};

export function WorkflowPhase({ title, items }: WorkflowPhaseProps) {
  return (
    <article className="card">
      <h2>{title}</h2>
      <ul>
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </article>
  );
}
