<!-- AION-MISSION-METADATA
id: MISSION-005
title: Data Axle Verification Pilot — Plan
status: ACTIVE
stage: approval
owner: CEO
priority: P1
-->

# MISSION-005 — Data Axle Verification Pilot (PLAN)

> **Parameters ratified by the CEO (2026-08-13). AION preparation complete.**
> No provider connection, no credentials, no data acquisition, and no spend have
> occurred. **Current status: `NOT CLEARED TO EXECUTE` — 7 items across gates 1–6 & 8
> require CEO / legal / procurement action (see `GATE-STATUS.md`).**

## Ratified parameters (CEO, 2026-08-13)
| Parameter | Value |
|-----------|-------|
| Provider | Data Axle |
| Market | Denver–Aurora–Lakewood, Colorado (one metro) |
| Max records | **500** |
| Hard spend cap | **$100 USD** absolute not-to-exceed |
| Human ground-truth sample | 100 records |
| Retention | ≤30 days (or shorter per license); longer needs CEO + legal review |
| Storage | Encrypted, access-controlled, **non-repository** only |
| Credentials | Secret manager only; never committed |

Out of scope (ratified): no cold outreach, email, SMS, calling, CRM, automated sales,
production deployment, resale/redistribution, market expansion, >500 records, or
additional provider purchases.

## Preparation completed by AION (this turn, GREEN only)
- Built `DataAxleProvider` adapter — **disabled by default**, technically enforcing the
  500-record and $100 caps and the Denver-only market guard; credentials from secret
  manager/env only; **no live-call path reachable** (gate 7 prep, gates 9 & 10).
- AION-SECURITY review of the adapter → `SECURITY-REVIEW-ADAPTER.md` (gate 7).
- Froze the measurement baseline before acquisition → `MEASUREMENT-BASELINE.md` (gate 11),
  incl. the precise **cost-per-usable-qualified-opportunity** definition.
- Confirmed synthetic regression + adapter tests pass — **60 tests green** (gate 12).
- Verification packet for the human/legal gates → `PRE-EXECUTION-VERIFICATION.md`.
- Gate tracker → `GATE-STATUS.md`; controlled `EXECUTION-RUNBOOK.md`.

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
| `GATE-STATUS.md` | Live status of the 12 pre-execution gates |
| `PRE-EXECUTION-VERIFICATION.md` | Verification packet for the human/legal gates (1–6, 8) |
| `MEASUREMENT-BASELINE.md` | FROZEN baseline: metric defs, thresholds, config pin (gate 11) |
| `SECURITY-REVIEW-ADAPTER.md` | AION-SECURITY review of the adapter (gate 7) |
| `EXECUTION-RUNBOOK.md` | Controlled run procedure — only after all gates pass |
| `HANDOFF.md` | Handoff to the CEO authorization gate |
| adapter | `products/lead-intel/leadintel/providers/dataaxle.py` (+ tests) |

## Gate
Real-data acquisition is a **YELLOW gate** (see
`docs/operations/live-provider-activation-checklist.md`). This mission authorizes
nothing; it prepares the authorization decision.

## Log
- 2026-08-13 — Mission created from CEO decision (Data Axle selected for a bounded
  verification pilot). Pilot plan authored. Status: READY FOR CEO PILOT AUTHORIZATION.
- 2026-08-13 — CEO ratified pilot parameters (500 records, $100 cap, Denver metro,
  30-day retention, secret-manager credentials). AION completed GREEN preparation:
  disabled cap-enforcing adapter + security review, frozen baseline, 60 tests green,
  gate tracker + verification packet + runbook. **Did not execute.** Gates 1–6 & 8
  (quote, ToS/licensing/retention/PII confirmation, legal sign-off, credentials)
  require CEO/legal/procurement. Status: NOT CLEARED TO EXECUTE.
