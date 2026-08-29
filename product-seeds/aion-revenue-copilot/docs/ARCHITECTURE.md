# Architecture — AION Revenue Conversion Copilot

## Status
APPROVED — MVP scaffold

## Mission Link
[aion-software-factory: MISSION-002](https://github.com/Ceoloo/aion-software-factory/blob/main/missions/MISSION-002.md)

## Summary
Next.js sales workspace with Supabase for persistence, AION AI Gateway for conversational intelligence, and AION event infrastructure for CRM + learning signals. V1 is a tight rep workflow — not a platform.

## System Context

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Sales Rep  │────▶│  Next.js App     │────▶│  Supabase       │
│  (browser)  │     │  (this repo)     │     │  Postgres       │
└─────────────┘     └────────┬─────────┘     └─────────────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
      ┌──────────────┐ ┌───────────┐ ┌──────────────────┐
      │ AION AI      │ │ CRM events│ │ Learning events  │
      │ Gateway      │ │ (lib/crm) │ │ (lib/learning)   │
      └──────────────┘ └───────────┘ └──────────────────┘
                                              │
                                              ▼
                                    ┌──────────────────┐
                                    │ AION Learning    │
                                    │ Worker           │
                                    └──────────────────┘
```

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| App framework | Next.js 15 + TypeScript | AION standard stack; fast iteration |
| Data store | Supabase / Postgres | Standard stack; relational lead/call state |
| AI | AION AI Gateway | Centralized model routing, billing, policy |
| Events | HTTP ingest to AION events infra | Decouple product from learning pipeline |
| Deployment | Vercel | Standard for Next.js; CEO gate on prod |
| V1 scope | Assisted workspace, no autonomous calling | Validate workflow before automation |

## Components

| Component | Path | Responsibility |
|-----------|------|----------------|
| App shell | `app/` | Routes, layout, rep UI |
| UI components | `components/` | Workflow phases, call panels |
| Sales domain | `lib/sales/` | Types: Lead, CallOutcome, qualification |
| Intelligence | `lib/intelligence/` | Pre-call brief, objection detection (AI) |
| AI client | `lib/ai/` | AION AI Gateway HTTP client |
| CRM | `lib/crm/` | Persist lead/call state, emit CRM events |
| Learning | `lib/learning/` | Map outcomes → learning events, ingest |

## API / Server Actions (planned tasks)

| Surface | Purpose |
|---------|---------|
| `GET /api/leads/[id]/brief` | Pre-call intelligence |
| `POST /api/calls/[id]/guidance` | During-call suggestions |
| `POST /api/calls/[id]/outcome` | Post-call structured outcome |
| Internal | CRM persist + learning ingest |

Builder tasks implement these as small PRs.

## Security Considerations
- Auth required before any lead/call data (Supabase Auth — task)
- API keys server-side only (`AION_*`, `SUPABASE_SERVICE_ROLE_KEY`)
- Security review mandatory before production deploy
- PII in transcripts — encrypt at rest, minimize retention (document in DATA_MODEL)

## Testing Strategy
| Layer | Location | Required for |
|-------|----------|--------------|
| Unit | `tests/unit/` | lib/intelligence, lib/learning, lib/crm |
| Critical path | `tests/critical-path/` | post-call → CRM + learning pipeline |
| Integration | `tests/integration/` | Supabase, AI Gateway (when wired) |
| Manual | `docs/VALIDATION.md` | Real prospect conversations |

## Deployment
- **Preview:** Vercel preview on PR
- **Production:** CEO release gate; record in factory `RELEASE_RECORD.template.md`
- **Rollback:** Redeploy previous Vercel promotion

## Implementation Tasks

| # | Task | Role | Depends |
|---|------|------|---------|
| 1 | Supabase schema + RLS | Builder | — |
| 2 | Auth + rep session | Builder | 1 |
| 3 | Pre-call brief UI + API | Builder | 1, 2 |
| 4 | AI Gateway client (real) | Builder | — |
| 5 | During-call guidance panel | Builder | 3, 4 |
| 6 | Post-call outcome form | Builder | 3 |
| 7 | CRM persist (Supabase) | Builder | 1, 6 |
| 8 | Learning event ingest (live) | Builder | 6 |
| 9 | E2E critical path tests | Builder | 7, 8 |
| 10 | Production deploy + release record | Release | 9, QA, Security |

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| AI latency during live calls | High | Cache context; async suggestions |
| Learning contract drift | Medium | Version events in payload |
| Scope creep into CRM platform | High | Mission out-of-scope enforced |

## Approval
- [x] Architect scaffold complete
- [ ] Human approved for production architecture changes (before prod deploy)
