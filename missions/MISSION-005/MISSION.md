<!-- AION-MISSION-METADATA
id: MISSION-005
title: Data Axle Verification Pilot — Plan
status: ACTIVE
stage: approval
owner: CEO
priority: P1
-->

# MISSION-005 — Data Axle Verification Pilot (PLAN)

> **This mission produces the bounded-pilot PLAN only — not an API integration.**
> No provider connection, no credentials, no data acquisition, and no spend occur
> under this mission. Execution is a separate step that begins only after the CEO
> authorizes the parameters below and legal signs off.
>
> **Final status: `READY FOR CEO PILOT AUTHORIZATION`.**

## Purpose
Prove — with a small amount of **real** Data Axle data — whether real
electrical-contractor data produces **acceptable economics and qualification
accuracy** for AION. Not "does Data Axle look good on paper" (Mission 004 answered
that); rather, does it work in practice, cheaply and accurately, through our
existing intelligence engine.

## The one metric that matters
> **How much does it cost AION to produce one genuinely qualified
> electrical-contractor opportunity?**

Everything else in the pilot exists to compute and trust that number.

## Flow (what the pilot does — and where it stops)
```
Provider (Data Axle)  →  Intelligence (existing MISSION-003 engine)  →  Verified lead dataset
   [bounded]                    [no new logic]                              [measured]
                                                                              │
                                          STOP HERE ── no outreach, no CRM, no sales
                                                                              │
                                                                              ▼
                                                                 AION Intelligence Evaluation
                                                                              │
                                                                              ▼
                                                                        CEO DECISION
                                                                     ┌────────┴────────┐
                                                                     ▼                 ▼
                                                              APPROVE provider   REJECT / ITERATE
```

## Scope (deliberately minimal — "almost boring")
Acquire a bounded dataset → run it through the **existing** engine unchanged →
measure → decide. The only new code (built **after** approval) is a thin Data Axle
adapter implementing the existing `ResearchProvider` seam.

## Explicit non-goals (do NOT build these here)
- ❌ No outreach (email/call/message) of any kind.
- ❌ No CRM, no enrichment beyond the existing engine, no autonomous workflows.
- ❌ No lead-generation "platform." This is a measurement pilot, not a product.
- ❌ No production deployment.
- ❌ No unbounded data pull; no spend beyond the hard cap.

## Deliverables (this planning mission)
| File | Purpose |
|------|---------|
| `MISSION.md` | This control document |
| `PILOT-PLAN.md` | Bounded parameters, methodology, stop conditions, exit |
| `MEASUREMENT-PLAN.md` | Metric definitions, labeling protocol, pre-registered thresholds |
| `DATA-HANDLING-PLAN.md` | Storage, PII rules, retention/deletion, security, legal items |
| `DECISION-FRAMEWORK.md` | APPROVE / REJECT / ITERATE criteria for the CEO gate |
| `APPROVALS.md` | Exact CEO approvals + legal sign-off required before execution |
| `HANDOFF.md` | Handoff to the CEO authorization gate |

## Gate
Real-data acquisition is a **YELLOW gate** (see
`docs/operations/live-provider-activation-checklist.md`). This mission authorizes
nothing; it prepares the authorization decision.

## Log
- 2026-08-13 — Mission created from CEO decision (Data Axle selected for a bounded
  verification pilot). Pilot plan authored. Status: READY FOR CEO PILOT AUTHORIZATION.
