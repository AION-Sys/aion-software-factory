# ADR-0005 — Fixture-first intelligence; live data acquisition is gated

- **Status:** Accepted
- **Date:** 2026-08-13
- **Deciders:** AION-ARCHITECT + AION-SECURITY (MISSION-002)
- **Mission:** MISSION-002

## Context
MISSION-002 asks us to "prove the intelligence layer" (enrich → qualify →
organize → output) before outreach. Real prospect data acquisition means paid
search/places APIs and handling business — and potentially personal — data, which
carries cost, Terms-of-Service, and privacy/compliance risk.

## Decision
1. V1 ships a deterministic **`FixtureProvider`** with clearly-labeled *synthetic*
   sample businesses. The intelligence layer is fully exercised and tested on it.
2. Data acquisition sits behind a **`ResearchProvider`** interface. A
   **`LiveProvider`** seam is defined but **disabled**: it reads an API key from an
   environment variable and raises a clear "requires approval + credentials" error
   until enabled.
3. Enabling any live/paid provider, acquiring real data, or storing real prospect
   PII is a **YELLOW gate** requiring human approval and a security review.
4. Enrichment never fabricates data: absent fields (website, decision-makers,
   contacts) are marked unavailable, never inferred.

## Consequences
### Positive
- Proves the intelligence layer with zero cost, credentials, or privacy exposure.
- Clean seam to add real providers later without touching scoring logic.
- Compliance posture is explicit and reviewable before any real data is touched.
### Negative / trade-offs
- Sample data is not real market data; scoring thresholds will need tuning against
  a first live run (tracked as an open question in the PRD).

## Alternatives considered
- **Scrape/collect real data now** — rejected: paid + ToS + PII risk without
  approval; violates progressive-autonomy gates.
- **No provider abstraction** — rejected: would couple intelligence logic to a
  specific data source and block future evolution.
