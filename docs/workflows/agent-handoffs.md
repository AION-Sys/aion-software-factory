# Agent Handoffs

Agents coordinate through **artifacts**, not conversational memory. A handoff is
complete only when (a) the required artifact exists and passes its completion
criteria, and (b) a handoff block is recorded.

## The handoff block

Every agent ends its run by appending this block to the mission `Log` (or its
output artifact):

```
### Handoff — <FROM-AGENT> → <TO-AGENT> (YYYY-MM-DD)
- Requested: <what this stage was asked to do>
- Completed: <what was actually done>
- Artifacts changed: <paths>
- Checks performed: <tests/lint/scans + results, verbatim>
- Known limitations: <what is not covered>
- Risks: <material risks discovered>
- Next recommended action: <for the next agent>
- Human approval required: <yes/no + which gate>
```

## Consumption contract (who reads what)

```
AION-PM         reads: mission            writes: prd.md
AION-ARCHITECT  reads: prd.md             writes: architecture.md, tasks.md, ADRs
AION-BUILDER    reads: architecture.md,   writes: code, tests, implementation notes
                       tasks.md
AION-QA         reads: branch, prd AC     writes: qa-report.md
AION-SECURITY   reads: branch,            writes: security-report.md
                       architecture.md
HUMAN           reads: all reports        writes: approval decision
```

## Failure handoffs

- **QA FAIL / SECURITY FAIL** → set `stage: build`, list the finding IDs, hand
  back to AION-BUILDER. The Builder resolves and re-hands off; the reviewer
  re-verifies (does not rubber-stamp).
- **Untestable AC / product ambiguity** → hand back to AION-PM.
- **Plan cannot be implemented** → hand back to AION-ARCHITECT.

## Traceability requirement

Because handoffs are file-based, any agent (or human) can reconstruct the full
history of a mission from its directory alone — no chat transcript required. This
is what makes the factory auditable.
