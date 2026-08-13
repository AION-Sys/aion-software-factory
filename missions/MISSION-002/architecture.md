# Architecture — MISSION-002 — Electrical Contractor Lead Intelligence (V1)

- **Author:** AION-ARCHITECT
- **Status:** APPROVED
- **Consumes:** `prd.md`

## 1. Overview
A small, dependency-free Python package implementing a linear pipeline
`INPUT → RESEARCH → ENRICH → QUALIFY → ORGANIZE → OUTPUT`. Research is behind a
provider interface so data acquisition can evolve (fixture now, live later)
without touching the intelligence logic. Enrichment and qualification are pure
functions — deterministic and unit-testable. Storage is file-based. See ADR-0004
(Python + stdlib) and ADR-0005 (fixture-first, gated live acquisition).

## 2. System Architecture
```
CLI (market, location, provider)
        │
        ▼
   pipeline.run()
        │
  ┌─────┴───────────────────────────────────────────────┐
  │ RESEARCH   provider.search(query) -> [RawBusiness]    │  ← pluggable
  │ ENRICH     enrich(RawBusiness)    -> Lead (canonical)│  ← pure
  │ QUALIFY    qualify(Lead, query)   -> score+status    │  ← pure
  │ ORGANIZE   store JSONL                                │
  │ OUTPUT     export CSV + JSON                          │
  └───────────────────────────────────────────────────── ┘
        │
        ▼
  out/<run-id>.{jsonl,csv,json}
```

## 3. Application Architecture
```
products/lead-intel/
├── leadintel/
│   ├── models.py        # Lead, DecisionMaker, ContactChannels, enums, Query
│   ├── providers/
│   │   ├── base.py      # ResearchProvider (ABC), RawBusiness
│   │   ├── fixture.py   # FixtureProvider (deterministic, synthetic data)
│   │   └── live.py      # LiveProvider seam — disabled, needs API key (YELLOW)
│   ├── enrich.py        # RawBusiness -> Lead (normalize, no fabrication)
│   ├── qualify.py       # scoring, opportunity tier, status
│   ├── pipeline.py      # orchestration
│   └── output.py        # JSONL / CSV / JSON writers
├── data/fixtures/electrical_contractors.json   # labeled synthetic sample
├── cli.py               # entry point (python cli.py ... / -m)
├── tests/               # unittest (stdlib)
└── examples/            # committed sample output (evidence)
```
Key patterns: dependency inversion at the provider boundary; pure core; explicit
"unknown" over inference.

## 4. Data model
`Lead` (canonical output contract):

| Field | Type | Notes |
|-------|------|-------|
| `id` | str | stable slug of company+location |
| `company` | str | business name |
| `website` | str \| null | null if not available |
| `location` | {city, region, country} | normalized |
| `service_type` | list[str] | e.g. ["residential electrical", "commercial"] |
| `estimated_opportunity` | enum LOW/MEDIUM/HIGH | derived from size signals |
| `estimated_opportunity_basis` | str | why that tier (transparency) |
| `decision_makers` | list[DecisionMaker] | empty if none legitimately available |
| `contact_channels` | {phone, email, contact_form_url, socials[]} | nulls when absent |
| `qualification_score` | int 0–100 | from `qualify()` |
| `score_breakdown` | dict[signal→points] | explainability (AC-3) |
| `status` | enum NEW/QUALIFIED/NEEDS_REVIEW/DISQUALIFIED | from score |
| `research_notes` | str | human-readable notes |
| `source` | {provider, url, retrieved_at} | provenance |

`DecisionMaker` = {name, title, source, contact?}. Only populated when the
provider legitimately supplies it; never inferred.

## 5. Scoring model (transparent heuristic, total 100)
| Signal | Max points | Rule |
|--------|-----------|------|
| Service relevance | 25 | matches electrical service intent |
| Location match | 15 | matches target location |
| Has website | 15 | website present |
| Has contact channel | 15 | ≥1 of phone/email/form |
| Opportunity signal | 20 | scaled from size signals (employees/reviews/years) |
| Decision-maker identified | 10 | ≥1 legitimately-available decision maker |

Status thresholds: **≥60 QUALIFIED**, **40–59 NEEDS_REVIEW**, **<40 DISQUALIFIED**.
`NEW` is the pre-scoring state. Opportunity tier: HIGH if strong size signals,
MEDIUM if moderate, LOW/unknown otherwise. All rules are unit-tested and tunable
via constants in `qualify.py`.

## 6. API (internal, not networked)
- `providers.base.ResearchProvider.search(query: Query) -> list[RawBusiness]`
- `enrich.enrich(raw: RawBusiness, query: Query) -> Lead`
- `qualify.qualify(lead: Lead, query: Query) -> Lead` (sets score/breakdown/status/opportunity)
- `pipeline.run(query, provider, out_dir) -> RunResult`

## 7. Authentication & Authorization
V1 has no network calls and no auth. The `LiveProvider` seam reads an API key
from an environment variable only and is disabled by default; enabling it is a
YELLOW gate (see approval policy).

## 8. Infrastructure & Deployment
None. A local CLI writing files under `out/` (git-ignored). No deployment in this
mission.

## 9. Security Considerations (handed to AION-SECURITY)
- No secrets in code; live key via env only.
- No PII fabrication: decision-maker fields populated only from source data.
- Fixture data must be clearly synthetic to avoid operators acting on fake leads.
- Future live provider must respect ToS/robots and undergo security review before enablement.
- Output files may contain business contact data → keep out of git via `.gitignore`.

## 10. Observability
`pipeline.run()` returns a `RunResult` summary (counts by status, average score,
timing) and writes a `run-summary.json`. These feed MISSION metrics
(`docs/operations/observability.md`): leads produced, qualified rate, avg score.

## 11. Decisions (ADRs)
- `docs/decisions/0004-lead-intel-python-stdlib.md`
- `docs/decisions/0005-fixture-first-gated-live-acquisition.md`

## 12. Trade-offs & Alternatives Considered
- **TypeScript/Next.js** — rejected: no UI needed; heavier toolchain for a CLI/library.
- **Database (Supabase/Postgres)** — rejected for V1: file output is sufficient; no concurrency/scale need yet.
- **Immediate live scraping** — rejected: paid + PII + ToS risk; gated behind human approval by design.

## Handoff
- Task list: `tasks.md`
- Next agent: **AION-BUILDER**
- Approval gates triggered: none for V1 (all GREEN). Live acquisition = future YELLOW.
