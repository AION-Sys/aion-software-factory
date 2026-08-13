<!-- AION-MISSION-METADATA
id: MISSION-004
title: Live Data Provider Evaluation (Desk Research)
status: ACTIVE
stage: approval
owner: CEO
priority: P1
-->

# MISSION-004 — Live Data Provider Evaluation (Desk Research)

> **Final status: `READY FOR CEO PROVIDER DECISION`.** GREEN desk research only.
> Nothing was purchased, no account created, no credentials requested, no API
> connected, no real data ingested.

## CEO Decision (input)
Mission 004 approved as a **GREEN desk-research mission**: research public provider
documentation, compare 2–3 candidates, fill the evaluation framework, and produce a
recommendation. Prohibited: signup, purchases, credentials, API keys, real data,
production connections, live credentialed API calls, PII collection, deployment.

## Objective
Determine which external data provider, if any, should be **considered** for a
future AION live-data mission — producing evidence for a future CEO live-provider
approval decision. Do not connect a provider.

## Candidates evaluated
1. **Google Places API (New)** — local business identity, category, location, website, phone.
2. **Data Axle (Infogroup)** — US compiled business database incl. executive contacts; API.
3. **People Data Labs (PDL)** — company + person enrichment API (decision-maker data).

Selection rationale: all three plausibly support US local/small businesses,
business identity, website/domain, category, location, and public contact
channels via an API — the fields our lead-intelligence layer consumes. They span
the tradeoff space (local-directory vs. compiled-SMB vs. person-enrichment).
Candidates were **not** assumed acceptable on database size alone.

## ⚠ Methodology limitation (material — read first)
Direct retrieval of primary vendor pages via the fetch tool was **blocked by this
environment's network egress policy**. All findings therefore rest on
**search-engine-surfaced content** from the cited sources, not on direct primary-
document reading. Consequently:
- Facts attributable to official-domain content are marked **CONFIRMED (via search
  summary of the official source)** — still to be re-read directly before a decision.
- Pricing/limits from third-party blogs are **ESTIMATED**.
- Everything else is **UNKNOWN**.
No pricing or capability was invented. See `PROVIDER-COMPARISON.md` for per-fact provenance.

## Deliverables
| File | Purpose |
|------|---------|
| `MISSION.md` | This control document |
| `PROVIDER-COMPARISON.md` | 25-dimension comparison, per-fact confidence + sources |
| `PROVIDER-SCORES.md` | Weighted scoring methodology + scorecards + ranking |
| `ECONOMIC-MODEL.md` | Parametric cost-per-usable / cost-per-qualified model (assumptions labeled) |
| `RISK-REVIEW.md` | Legal/privacy risk areas: LOW/MEDIUM/HIGH/UNKNOWN |
| `RECOMMENDATION.md` | Single verdict + why/known/unknown/verify/cost/benefit/risks/approvals |
| `HANDOFF.md` | Handoff to the CEO gate |

## Recommendation (summary)
**CONSIDER — Data Axle** as the primary candidate for a future, separately-approved
live-provider pilot, subject to a defined verification list; **Google Places API**
as a complementary identity/verification source only if its caching/storage
restriction can be reconciled; **DO NOT RECOMMEND** PDL as the primary source for
this vertical. Full reasoning in `RECOMMENDATION.md`.

## Approval Gates
- This mission authorizes **nothing** operational. A live-provider mission is a
  separate **YELLOW** gate (see `docs/operations/live-provider-activation-checklist.md`).

## Log
- 2026-08-13 — Mission created from CEO decision. Desk research conducted via web
  search (direct primary fetch blocked by egress policy — documented above).
- 2026-08-13 — Comparison, scores, economic model, risk review, and recommendation
  produced. Status: READY FOR CEO PROVIDER DECISION.
