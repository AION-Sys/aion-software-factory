# PRD — MISSION-002 — Electrical Contractor Lead Intelligence (V1)

- **Author:** AION-PM
- **Status:** APPROVED
- **Source mission:** `mission.md`

## 1. Summary
Build the smallest usable system that turns a `(target market, location)` input
into a structured, scored list of electrical-contractor leads with
decision-maker intelligence captured only when legitimately available. V1 proves
the intelligence layer; it does not perform outreach.

## 2. Problem & Opportunity
Prospecting for electrical contractors today is manual and inconsistent: an
operator searches, copies data into a spreadsheet by hand, and guesses at
priority. There is no repeatable, explainable way to produce a qualified lead
list. A reliable intelligence layer is the prerequisite for any later outreach or
revenue automation — and is where the leverage begins.

## 3. Target Users
| User | Needs | Context |
|------|-------|---------|
| AION operator (sales/BD) | A qualified, structured lead list from a market input | Wants to skip manual research; needs to trust the scores |
| AION-BUILDER (future missions) | A clean intelligence API to extend | Will add live providers/outreach later |

## 4. Goals & Success Metrics
| Goal | Metric | Target |
|------|--------|--------|
| Turn input into usable leads | Required fields populated or explicitly "not available" | 100% of leads |
| Trustworthy prioritization | Score is explainable (per-signal breakdown) | Every lead |
| Immediately usable output | Valid CSV + JSON produced | Every run |
| Zero-friction proof | Runs with no credentials/network in V1 | Always |

## 5. MVP Scope
The pipeline **INPUT → RESEARCH → ENRICH → QUALIFY → ORGANIZE → OUTPUT**, backed
by a deterministic fixture research provider, transparent scoring, file-based
storage, and a CLI. A live-provider seam is defined but disabled.

## 6. Non-Goals
- Automated cold outreach (email, calls, messaging) — deferred.
- Live/paid data-provider integration — YELLOW gate, not in V1.
- Web UI, CRM sync, database.
- Any capture or invention of personal data beyond legitimate business contacts.

## 7. User Stories
- As an operator, I provide a market ("electrical contractors") and a location
  ("Austin, TX") and receive a scored lead list, so I can prioritize outreach later.
- As an operator, I can see *why* a lead scored as it did, so I can trust the ranking.
- As an operator, I can open the results in a spreadsheet (CSV), so I can work immediately.
- As a compliance-conscious operator, I can rely on the system to mark missing
  decision-maker info as unavailable rather than guessing, so I don't act on fabricated data.

## 8. Acceptance Criteria
> The contract QA verifies against. Mirrors `mission.md` § Acceptance Criteria.
- [ ] AC-1 CLI with `(market, location)` produces a lead list (CSV + JSON).
- [ ] AC-2 Every lead has all required fields; missing data is explicit `null`/"not available", never fabricated.
- [ ] AC-3 Qualification score is 0–100 with a per-signal breakdown.
- [ ] AC-4 Each lead has status ∈ {NEW, QUALIFIED, NEEDS_REVIEW, DISQUALIFIED}.
- [ ] AC-5 Estimated opportunity ∈ {LOW, MEDIUM, HIGH}.
- [ ] AC-6 Decision-maker info appears only when present in source; absence is marked.
- [ ] AC-7 Runs with zero credentials and zero network.
- [ ] AC-8 Automated tests cover qualification, pipeline, and output; all pass.

## 9. Required lead schema (output contract)
Each lead must expose:
`company, website, location, service_type, estimated_opportunity,
decision_makers, contact_channels, qualification_score, score_breakdown,
research_notes, source, status`.
Field-level definitions are specified in `architecture.md` § Data model.

## 10. Risks & Assumptions
| Item | Type | Impact | Mitigation |
|------|------|--------|------------|
| Operators treat synthetic sample data as real | risk | High | Label fixtures synthetic; live provider gated |
| Scoring feels arbitrary | risk | Med | Ship explainable breakdown + docs |
| Fixture data is enough to prove the layer | assumption | — | Intelligence = enrich/qualify/organize/output; data acquisition is a separate seam |

## 11. Open Questions
- Which live data provider (and budget) will back real acquisition? → CEO decision at the YELLOW gate for a future mission.
- Target scoring thresholds may need tuning against real data → revisit after first live run.

## Handoff
- Next agent: **AION-ARCHITECT**
- Approval required before build: none (GREEN — code generation + local tests on a branch).
