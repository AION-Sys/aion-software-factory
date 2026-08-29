# PRD — AION Revenue Conversion Copilot

## Status
APPROVED

## Mission Link
[aion-software-factory: MISSION-002](https://github.com/Ceoloo/aion-software-factory/blob/main/missions/MISSION-002.md)

## Problem
Home-service contractors and SMB sales teams generate leads, but revenue leaks between initial contact and conversion. Response is slow, follow-up is inconsistent, reps lack context, and sales conversations are not systematically learned from.

## Goals
- Productize AION's conversion loop: context → intelligence → conversation → outcome → learning
- Give reps an AI-assisted workspace for pre-call, during-call, and post-call workflows
- Emit structured events for CRM persistence and AION learning infrastructure
- Validate on real prospect conversations via AION's contractor outbound pipeline

## Non-Goals (V1)
- Autonomous calling
- Full CRM replacement
- Multi-agent workforce orchestration
- Generic workflow builder

## Users and Use Cases

| User | Use case | Success looks like |
|------|----------|-------------------|
| Sales rep | Prepare for a contractor lead call | Brief with pains, offer, and questions in &lt; 2 min |
| Sales rep | Run discovery on live call | Checklist, objection reframe, qualification captured |
| Sales rep | Close out call | Structured outcome, next action, CRM + learning events |
| Sales manager | Review team usage | Evidence that workflow improves conversion signals |
| Owner/operator | Buy based on outcomes | Faster response, better conversations, more closed revenue |

## Requirements

### Must Have
- Pre-call brief from lead + business context
- During-call guidance surfaces (checklist, objections, next-best action)
- Post-call structured outcome capture
- CRM persistence for lead/call state
- Learning event emission on outcomes
- CI: lint, typecheck, tests, build

### Should Have
- Transcript/notes ingestion for post-call structuring
- Objection pattern tagging for learning worker

### Won't Have (V1)
- Autonomous dialer
- Custom workflow designer
- Enterprise multi-tenant admin

## Acceptance Criteria
Aligned with Mission 002 — see mission file for gate table. Mission complete requires **Revenue** and **Validation** gates.

## Metrics

| Metric | Target (validation) | How measured |
|--------|---------------------|--------------|
| Rep workflow completion | Reps complete pre → call → post on real leads | Usage logs + `docs/VALIDATION.md` |
| Time to pre-call brief | &lt; 2 minutes | Timed sessions |
| Outcome event rate | 100% of completed calls emit CRM + learning events | Event ingest logs |
| Workflow improvement signal | Qualitative + quantitative evidence | Validation interviews + before/after notes |

## Open Questions
- [ ] Supabase project provisioning — owner: CEO/infra
- [ ] AION AI Gateway model routing defaults — owner: Architect
- [ ] Learning worker contract version — owner: Architect + platform team

## Approval
- [x] PM complete (Mission 002)
- [ ] CEO production deploy approval (pending MVP)
