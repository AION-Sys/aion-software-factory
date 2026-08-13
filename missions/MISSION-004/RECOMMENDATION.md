# Recommendation — MISSION-004

## Verdict: **CONSIDER — Data Axle** (primary candidate for a future, separately-approved pilot)

Secondary positions:
- **Google Places API — CONSIDER (complementary only)**, as a live identity/verification
  lookup, **not** a storage source, and only if its storage/caching restriction is
  reconciled with legal review.
- **People Data Labs — DO NOT RECOMMEND** as the primary source for this vertical
  (coverage bias against small local contractors + highest PII burden). Optional as a
  later decision-maker enrichment layer.

Why **CONSIDER** and not **RECOMMEND**: the fit case for Data Axle is strong, but the
deciding facts — exact pricing, API rate limits, retention/redistribution specifics,
and **actual electrical-contractor data quality** — are ESTIMATED or UNKNOWN, and
primary sources could not be read directly (egress policy). That is enough to advance
to verification, not enough to commit.

---

## For the recommended provider — Data Axle

### WHY
- Best fit for the target population: **selectable by NAICS 238210** across **94M+ US
  business records**, with SMB depth — the small local electrical contractors we want.
- **Only candidate that cleanly supplies decision-makers** for SMBs (primary-contact
  name, title, management level) alongside phone/email.
- **Internal-use license appears compatible with storing** a lead pipeline (unlike
  Google's storage prohibition) — critical for our "organize/store leads" model.
- **Transparent, pay-as-you-go API pricing** enabling a small bounded pilot.

### WHAT WE KNOW (CONFIRMED via search of official/library sources)
- 94M+ US business records; NAICS/SIC selectability; API with primary-contact fields;
  fields incl. name/address/phone/email/employees/sales/exec contact.
- License is limited, internal-use, non-transferable; **redistribution prohibited**
  without written authorization; Data Axle owns the data.

### WHAT WE DO NOT KNOW (ESTIMATED or UNKNOWN)
- Exact API pricing (ESTIMATED $50–75/1k from secondary sources).
- API rate limits (UNKNOWN).
- Retention/deletion terms for stored records (UNKNOWN).
- **Real electrical-contractor coverage %, accuracy, and freshness** for target metros
  (UNKNOWN — no data measured).
- Match/qualified conversion rates (ASSUMED in the economic model).

### WHAT MUST BE VERIFIED (before a live mission)
1. Written pricing quote + rate limits (primary source / sales).
2. License terms confirming **internal storage + internal lead-gen** are permitted,
   and the retention/deletion obligations.
3. A **small labeled sample** for one metro to measure real usable/qualified rates,
   accuracy, and freshness against the MISSION-003 pipeline.
4. Legal review of the HIGH-flagged items in `RISK-REVIEW.md`.

### EXPECTED COST (illustrative — ASSUMPTIONS, not measured)
- ≈ **$0.05–0.075 per record**; ≈ **$77–$115 per 1,000 qualified electrical
  contractors** under assumed conversion (see `ECONOMIC-MODEL.md`). A verification
  pilot could be bounded to a **low three-figure** spend.

### EXPECTED BENEFIT
- Replaces manual prospecting with a repeatable, filterable feed of on-target,
  decision-maker-bearing leads that our qualification engine can score — the first
  real input to the MISSION-002/003 intelligence layer.

### RISKS
- Compiled-data accuracy/staleness (mitigate: measure on a sample first).
- Pricing/licensing differ from estimates (mitigate: get a written quote).
- PII/compliance obligations on exec contacts (mitigate: legal review; no outreach yet).
- Redistribution prohibition (mitigate: internal use only; never resell lists).

### REQUIRED CEO APPROVALS (to move to a live mission — all per the activation checklist)
1. Approve **Data Axle** as the provider to pilot.
2. Approve a **spend cap** for a bounded verification pilot.
3. Approve **target metro + record volume** for the pilot.
4. Approve **PII handling** (retention window + deletion/opt-out process).
5. Authorize **storing real prospect data** in a defined, access-controlled,
   non-repo location.
(Plus legal sign-off on `RISK-REVIEW.md` HIGH items.)

---

## Why Google Places is complementary-only
Excellent data/API/reliability and the best local coverage, but its terms **prohibit
permanently storing place content** (30-day cache; only `place_id` persists). Our
system's purpose is to *store* a structured lead pipeline, so Google cannot be the
primary source without breaking its terms. It is valuable as a **live verification /
enrichment lookup** (e.g., confirm a business exists, current website/phone) if legal
review confirms that pattern — otherwise skip.

## Why not PDL (primary)
Its data reflects **online visibility**, systematically underrepresenting small local
electrical contractors — the exact targets — and it is a **registered data broker**
with person-level data, the **highest PII burden** of the three. Reconsider only as an
optional decision-maker enrichment layer once a core provider is proven.

## Confidence
**Moderate.** Fit reasoning is well-grounded; the commercial and quality specifics
are not yet primary-verified. Advancing to a bounded verification pilot is the
correct next step — not a full commitment.
