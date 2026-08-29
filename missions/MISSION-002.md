# Mission 002 — AION Revenue Conversion Copilot

## Status
ACTIVE — VALIDATION → MVP

## Lifecycle
Validation → MVP

## Priority
P0

## Mission Type
Revenue-connected product build

## CEO Objective
Prove the AION Software Factory can ship a revenue-connected product end-to-end: **Factory → Code → User → Economic Signal → Learning**.

Build and validate the first production version of **AION Revenue Conversion Copilot** — an AI-assisted sales workspace that turns lead/business context into adaptive discovery, objection handling, recommended actions, structured call intelligence, and learning signals.

## Product Thesis
Small and local businesses do not primarily need "more AI." They need more leads converted into actual conversations, appointments, applications, and sales.

AION already has underlying IP across the conversion loop:

```
business context → lead intelligence → pain discovery → adaptive conversation
→ objection handling → next-best action → outcome → learning loop
```

Mission 002 productizes that loop — not another isolated script generator.

## ICP and Buyer
| Dimension | Detail |
|-----------|--------|
| **Initial ICP** | Home-service contractors and SMB sales teams |
| **Problem** | Revenue leaks between initial contact and conversion: slow response, inconsistent follow-up, reps lack context, conversations are not systematically learned from |
| **Buyer** | Owner/operator, sales manager, or revenue leader |
| **Why they pay** | Faster response + better conversations + better follow-up → more qualified opportunities → more closed revenue |
| **Distribution** | AION's existing outbound contractor pipeline (dogfood while selling) |

## Outcome
A production MVP used on **real prospect conversations** with evidence collected on whether it improves the sales workflow — and structured outcome events feeding AION learning infrastructure.

Mission 002 is **not complete** when the app deploys. It is complete when reality validates it.

## Scope — MVP

### Before conversation
- Lead → company intelligence → likely pains → relevant offer → recommended questions

### During conversation
- Context-aware script guidance
- Discovery checklist
- Objection detection → suggested reframe
- Qualification capture
- Next-best question/action

### After conversation
- Notes/transcript → structured outcome
- Pain points, objections, qualification state captured
- Next action defined
- CRM event emitted
- Learning event emitted

## Out of Scope (V1 — downstream)
- Autonomous calling
- Giant CRM replacement
- Giant agent workforce
- Unnecessary workflow builder

## Acceptance Criteria

### Build and quality gates
| Gate | Criterion | Status |
|------|-----------|--------|
| **Build** | Production deployment succeeds | [ ] |
| **Quality** | lint + typecheck + tests + build pass in CI | [ ] |
| **UX** | Rep can complete pre-call → call → post-call workflow | [ ] |
| **Context** | Recommendations use stored business/lead context | [ ] |
| **Intelligence** | Objections, pain, and qualification can be captured | [ ] |
| **Data** | Outcomes generate structured events | [ ] |
| **Learning** | Outcome can feed AION learning infrastructure | [ ] |
| **CRM** | Lead/call state persists correctly | [ ] |

### Commercial validation gates (required for mission complete)
| Gate | Criterion | Status |
|------|-----------|--------|
| **Revenue** | Product is used on real prospect conversations | [ ] |
| **Validation** | Evidence collected showing whether it improves the sales workflow | [ ] |

## Success Metric
Demonstrate the full loop once:

**Factory → Code → User → Economic Signal → Learning**

Evidence includes: real usage on prospect conversations, structured outcome/learning events, and documented validation findings in the product repo (`docs/VALIDATION.md`).

## Product Repository
https://github.com/Ceoloo/aion-revenue-copilot

Bootstrap seed (until repo is created): [`product-seeds/aion-revenue-copilot/`](../product-seeds/aion-revenue-copilot/) — see [`docs/products/REVENUE_COPILOT_SETUP.md`](../docs/products/REVENUE_COPILOT_SETUP.md).

## Standard Stack
- **Application:** Next.js / TypeScript
- **Database:** Supabase / Postgres
- **AI:** AION AI Gateway
- **Events:** AION event/learning infrastructure
- **Hosting:** Vercel (where appropriate)
- **Agents:** Cursor Cloud Agents — bounded tasks via small PRs

## Factory Execution Flow

```
CEO
 │
 │ Mission 002 approval
 ▼
AION SOFTWARE FACTORY
 │
 ├── AION-PM          → PRD + acceptance criteria
 ├── AION-ARCHITECT   → architecture + data contracts
 ├── AION-BUILDER     → implementation PRs
 ├── AION-QA          → tests + validation
 ├── AION-SECURITY    → risk review
 └── AION-RELEASE     → deployment evidence
              │
              ▼
      CEO RELEASE GATE
              │
              ▼
        Production MVP
              │
              ▼
      Real Sales Usage
              │
              ▼
       Outcome Events
              │
              ▼
       Learning Worker
              │
              ▼
      Product Improvements
```

## CEO Approval Gates
- [ ] **Mission scope approval** — required before Architect begins material design (this document)
- [ ] **Production deployment** — required before first production release
- [ ] **Release gate** — CEO confirms deployment evidence before declaring MVP live
- [ ] **Validation complete** — CEO reviews `docs/VALIDATION.md` evidence before mission close

## Dependencies
- Mission 001 complete (factory foundation)
- Product repo `aion-revenue-copilot` bootstrapped
- AION AI Gateway access (product repo secrets)
- AION event/learning infrastructure endpoints (Architect to document contracts)
- Supabase project for product data (human-approved provisioning)

## Governance — Mission 003 Block
**Mission 003 cannot become another major product build until Mission 002 reaches its defined validation gate** (Revenue + Validation acceptance criteria satisfied, or explicitly cancelled with CEO approval).

See `AION_ENGINEERING.md` — Sequential Mission Governance.

## Next Mission (blocked until validation)
Mission 003 — TBD. Scope depends on Mission 002 validation outcomes and learning signals. Do not initiate until validation gate is met.
