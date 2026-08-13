# Architecture — MISSION-XXX — <Title>

- **Author:** AION-ARCHITECT
- **Status:** DRAFT | APPROVED
- **Consumes:** `prd.md`

## 1. Overview
<High-level approach in a few sentences. Link the ADRs that justify big choices.>

## 2. System Architecture
<Components and how they interact. A diagram (ASCII/mermaid) is encouraged.>

## 3. Application Architecture
<Modules, layering, key patterns, and where new code lives.>

## 4. Data Design
<Entities, relationships, storage choice. Note migrations (YELLOW gate).>

## 5. API Design
| Method | Path | Purpose | Auth |
|--------|------|---------|------|
|        |      |         |      |

## 6. Authentication & Authorization
<AuthN strategy and AuthZ model (roles/permissions, least privilege).>

## 7. Infrastructure & Deployment
<Hosting, environments, config. Deployment is a YELLOW gate — design only.>

## 8. Integrations
<Third-party services, their scopes, and failure handling.>

## 9. Security Considerations
<Threats introduced by this design and how they are mitigated. Hand these to
AION-SECURITY explicitly.>

## 10. Observability
<What this feature must emit so the metrics in `docs/operations/observability.md`
can be measured (events, logs, counters).>

## 11. Decisions (ADRs)
- <link to `docs/decisions/NNNN-*.md`>

## 12. Trade-offs & Alternatives Considered
<What was rejected and why.>

## Handoff
- Task list: `tasks.md`
- Next agent: **AION-BUILDER**
- Approval gates triggered: <none | YELLOW: … | RED: …>
