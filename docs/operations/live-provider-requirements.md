# Live Data Provider — Requirements

The requirements any live data provider MUST satisfy before it can be connected
to the lead-intelligence system. Meeting these is necessary but **not sufficient**
— activation also requires the CEO gate in `live-provider-activation-checklist.md`.

> Status: no provider selected or approved. Live acquisition is a **YELLOW gate**
> (ADR-0005). This document defines the bar; it does not authorize anything.

## 1. Legal & licensing (mandatory)
- **Terms of Service** explicitly permit our use (B2B lead research + storage).
- **Data licensing** permits storing and processing returned data for our purpose.
- **Permitted use** covers commercial prospecting; no clause we would violate.
- **No scraping in violation** of any site's ToS or robots directives.
- Written confirmation retained in `docs/decisions/` or the mission package.

## 2. Privacy & PII (mandatory)
- Returns **business** contact information; any personal data is limited to
  legitimately-available, business-role contacts.
- Supports our obligations for **retention** and **deletion** of personal data.
- Provides a lawful basis / data-processing terms (DPA) where applicable.
- Never requires us to store special-category personal data.

## 3. Data quality
- **Geographic coverage** includes our target markets.
- **Business coverage** includes electrical contractors at useful density.
- **Freshness** stated and acceptable (how recently records are verified).
- **Contact information availability** sufficient for qualification.
- **Provenance**: each record traceable to a source + retrieval time.

## 4. Technical & operational
- **API limits / rate limits** documented and workable for our volume.
- **Reliability / uptime** stated (SLA or track record).
- **Security**: encrypted transport; credentials via secret manager only.
- **Scalability**: can grow with our volume without renegotiation surprises.

## 5. Commercial
- **Pricing** transparent; **cost per qualified lead** estimable.
- No commitment exceeding the CEO-approved budget.

## Mapping to the system
When a provider is approved, it is implemented as a `ResearchProvider` behind the
existing seam (`leadintel/providers/live.py`). Nothing downstream
(normalizer → enrichment → qualification → output) changes: the provider only
supplies `RawBusiness` records. Real records will be labeled `is_synthetic=false`
and must satisfy the provenance and PII rules above.
