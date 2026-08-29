# Architecture — {Product / Feature Name}

## Status
DRAFT | APPROVED | SUPERSEDED

## Mission Link
{Link to mission file}

## Summary
{2–4 sentences: technical approach and key tradeoffs.}

## Context
- **PRD:** {link}
- **Constraints:** {timeline, stack, compliance, etc.}

## System Context

```
{ASCII or mermaid diagram: users, app, DB, external services}
```

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| {Topic} | {Option chosen} | {Why} |

For significant decisions, add an ADR in `docs/adr/`.

## Components

| Component | Responsibility | Notes |
|-----------|----------------|-------|
| {Name} | {What it does} | {Stack, boundaries} |

## Data Model
{High-level entities and relationships, or link to schema migration.}

## API / Interface
{Public routes, events, or contracts — or "N/A for this change."}

## Security Considerations
{Auth model, data classification, trust boundaries — flag if Security review required.}

## Testing Strategy
{Which layers: unit, integration, E2E — per docs/standards/TESTING.md}

## Deployment
{How this ships; feature flags; rollback plan.}

## Tasks
Break into small, PR-sized units:

| # | Task | Owner role | Depends on |
|---|------|------------|------------|
| 1 | {Description} | Builder | — |
| 2 | {Description} | Builder | 1 |

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| {Risk} | {H/M/L} | {Plan} |

## Approval
- [ ] Architect complete
- [ ] Human approved (if material architecture change)
