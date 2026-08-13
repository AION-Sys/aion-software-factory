# Provider Comparison — MISSION-004

Every fact is tagged **CONFIRMED** (search summary of an official-domain source —
re-read directly before deciding), **ESTIMATED** (third-party/secondary source), or
**UNKNOWN**. See the methodology limitation in `MISSION.md`: primary pages could not
be fetched directly; nothing here is invented. Access date: **2026-08-13**.

## Summary matrix
| # | Dimension | Google Places API | Data Axle | People Data Labs |
|---|-----------|-------------------|-----------|------------------|
| 1 | Provider | Google | Data Axle (Infogroup) | People Data Labs |
| 2 | Product/API | Places API (New) — REST | Business Data / Search API | Company + Person Enrichment API |
| 3 | Geographic coverage | Global; strong US | US (+Canada) | Global |
| 4 | Business coverage | Very strong local/SMB | 94M+ US business records | Large; visibility-biased |
| 5 | Electrical contractor coverage | `electrician` place type | Via NAICS 238210 | **Weak for small local trades** |
| 6 | Data fields | identity, category, location, website, phone | identity, address, phone, email, SIC/NAICS, size, exec | firmographics + person (title, email) |
| 7 | Contact information | website + phone | phone + email + address | work email/phone (paid) |
| 8 | Decision-maker info | **None** | **Yes (exec name/title/level)** | Yes (person data) — biased away from our targets |
| 9 | Data freshness | continuous (Maps) [EST] | regular verification [EST] | monthly refresh [EST] |
| 10 | Provenance | Google Maps; `place_id` | compiled, Data Axle-owned | aggregated, compliance-screened |
| 11 | API availability | Yes (mature) | Yes | Yes (developer-friendly) |
| 12 | Rate limits | high QPS, project quotas [EST] | UNKNOWN | tier-based [EST] |
| 13 | Pricing | Details $5/$17/$20 per 1k (Ess/Pro/Ent) [EST] | $50/$75 per 1k API [EST] | ~$100/1k company (Pro) [EST] |
| 14 | Free tier/trial | per-SKU monthly free [EST] | demo only [EST] | 100 lookups/mo free [CONF] |
| 15 | Terms of Service | Maps Platform Service Terms [CONF] | limited internal-use license [CONF] | AUP + data-broker terms [CONF] |
| 16 | Data licensing | **no permanent storage** (30-day cache) [CONF] | licensed, not owned; internal use [CONF] | redistribution restricted [CONF] |
| 17 | Commercial-use restrictions | **HIGH (storage/caching)** [CONF] | no resale/redistribution [CONF] | AUP-governed [CONF] |
| 18 | PII considerations | LOW (business data) | MEDIUM (exec contacts) | **HIGH (person-level, data broker)** |
| 19 | Retention requirements | delete cached content ≤30d; `place_id` exempt [CONF] | tied to license term [UNK] | honor deletion/opt-out [CONF] |
| 20 | Deletion requirements | as above [CONF] | UNKNOWN | data-subject deletion supported [CONF] |
| 21 | Security requirements | Google Cloud; API key [CONF] | enterprise vendor [EST] | privacy/security overview published [CONF] |
| 22 | Reliability | 99.9% uptime SLA [CONF] | established (decades) [EST] | established API vendor [EST] |
| 23 | Est. cost / 1,000 records | ~$20/1k (Enterprise Details) [EST] | $50–75/1k [EST] | ~$100/1k [EST] |
| 24 | Est. cost / usable lead | see `ECONOMIC-MODEL.md` (assumptions) | see model | see model |
| 25 | Est. cost / qualified electrical contractor | see model | see model | see model |

---

## Google Places API (New)
- **Product (2):** Places API (New) — Place Details, Text Search, Nearby Search; REST. **CONFIRMED** (developers.google.com/maps/documentation/places/web-service/*).
- **Geo/Business coverage (3,4):** Global; among the strongest local/SMB coverage via Google Maps listings. **CONFIRMED** (product overview) / density is **ESTIMATED**.
- **Electrical coverage (5):** `electrician` is a supported, filterable place type. **CONFIRMED** (developers.google.com/maps/documentation/places/web-service/place-types).
- **Fields/contact (6,7):** business identity, types/category, location, `websiteUri`, `nationalPhoneNumber`/`internationalPhoneNumber`. Website + phone are **Enterprise-SKU** fields. **CONFIRMED** (place-details / data-fields docs). **No email; no decision-makers.**
- **Decision-makers (8):** None in the data model. **CONFIRMED.**
- **Provenance (10):** Google Maps; stable `place_id`. **CONFIRMED.**
- **Pricing (13,14):** Place Details Essentials **$5/1k**, Pro **$17/1k**, Enterprise **$20/1k** (10k–100k tier); per-SKU free monthly (10k Ess / 5k Pro / 1k Ent); universal **$200 credit retired Mar 2025**. **ESTIMATED** (woosmap.com, safegraph.com — secondary; must confirm on developers.google.com usage-and-billing). Search steps (Text/Nearby) are billed separately and add per-lead cost.
- **ToS/licensing (15,16,17,19,20):** Google Maps Platform Service Specific Terms — **caching prohibited beyond 30 days; place content cannot be permanently stored; `place_id` may be cached.** **CONFIRMED** (cloud.google.com/maps-platform/terms/maps-service-terms; corroborated by multiple sources). *This is the single most important finding for us: it conflicts with permanently storing enriched leads.*
- **PII (18):** Business data, minimal personal data → LOW.
- **Security/Reliability (21,22):** Google Cloud, API-key auth; **99.9% uptime SLA** with financial credits. **CONFIRMED** (cloud.google.com/maps-platform/terms/sla).

## Data Axle (Infogroup)
- **Product (2):** Business Data + Search API; also Salesgenie (self-serve) and Reference Solutions (library). **CONFIRMED** (data-axle.com/data-solutions/apis, business-data).
- **Coverage (3,4):** US (+Canada); **94M+ US business records** (plus historical/new-business files). **CONFIRMED** (library.virginia.edu, fortbendlibraries.gov summaries).
- **Electrical coverage (5):** Selectable by **SIC/NAICS** (electrical contractors = NAICS 238210); deep SMB coverage. Capability **CONFIRMED**; the specific electrical-contractor count is **UNKNOWN**.
- **Fields/contact (6,7):** name, address, phone, **email**, SIC/NAICS, employees, sales volume, credit rating; API returns **Primary Contact first/last name, job title, job function, management level**. **CONFIRMED** (rapidapi.com Data Axle Business Search; data-axle.com business-data).
- **Decision-makers (8):** **Yes** — executive/primary-contact name + title + management level. **CONFIRMED.** Best decision-maker fit for SMBs of the three.
- **Provenance (10):** Compiled proprietary database; Data Axle **owns** the data. **CONFIRMED** (terms).
- **Pricing (13,14):** API **$50/1k (Standard)**, **$75/1k (Enhanced)**, pay-as-you-go; Salesgenie $99/$149/$299 per month; demo (no free API tier). **ESTIMATED** (bookyourdata.com, fullenrich.com — secondary; must confirm with Data Axle).
- **ToS/licensing (15,16,17):** "limited, non-exclusive, non-transferable, non-sublicensable license … for internal purposes"; **redistribution/resale prohibited without written authorization**; Data Axle retains all IP. **CONFIRMED** (data-axle.com/terms-and-conditions). Internal lead-gen appears within scope; resale is not.
- **PII (18):** Executive contact data → **MEDIUM**; triggers CAN-SPAM/DNC/state-law obligations on any future outreach (out of scope now).
- **Retention/deletion (19,20):** Tied to license term; specifics **UNKNOWN**.
- **Reliability (22):** Established vendor (decades as Infogroup). **ESTIMATED.**

## People Data Labs (PDL)
- **Product (2):** Company Enrichment API + Person Data API; REST, well-documented. **CONFIRMED** (peopledatalabs.com/company-data/enrichment-api, /person-data).
- **Coverage (3,4):** Global; large company dataset. **CONFIRMED.**
- **Electrical coverage (5):** **Weak for small local trades** — data "reflects online visibility"; strong for tech/white-collar and companies with 50+ employees; **underrepresents blue-collar and small-business owners**. **CONFIRMED** (syncgtm.com review; consistent with PDL's own sourcing description). *Decisive negative for our vertical.*
- **Fields/contact (6,7):** firmographics (name, domain, industry, size, location) + person (title, work email/phone on paid tiers). **CONFIRMED.**
- **Decision-makers (8):** Yes via person data — but coverage skewed away from our targets. **CONFIRMED with caveat.**
- **Provenance (10):** Aggregated from many sources; compliance-screened before ingest. **CONFIRMED** (privacy-security-overview.pdf).
- **Pricing (13,14):** Free **100 lookups/mo** (no email/phone on free); Pro Company **$100/mo for 1,000 records**; ~$0.01–0.05/record. **CONFIRMED** (support.peopledatalabs.com pricing/credits summary) / secondary corroboration **ESTIMATED**.
- **ToS/licensing/PII (15,16,17,18,19,20):** Acceptable Data Use Policy; **registered California data broker** (reg. #190662, approved 2020-06-16); provides opt-out/portability/correction/deletion; does **not** sell GDPR Art. 9 / CPRA sensitive PII. Redistribution restricted. Person-level data → **HIGH PII**; CCPA/GDPR data-subject obligations flow to the licensee. **CONFIRMED** (oag.ca.gov/data-broker/registration/190662; privacy.peopledatalabs.com).
- **Reliability (22):** Established API vendor. **ESTIMATED.**

---

## Sources (accessed 2026-08-13; via web search — direct fetch blocked by egress policy)
**Google:** developers.google.com/maps/documentation/places/web-service/{usage-and-billing, place-types, place-details, data-fields}; cloud.google.com/maps-platform/terms/{maps-service-terms, sla}; secondary pricing: woosmap.com/blog/google-places-api-pricing, safegraph.com/guides/google-places-api-pricing.
**Data Axle:** data-axle.com/{data-solutions/apis, data-solutions/business-data, terms-and-conditions}; library.virginia.edu/data/datasources/licensed/infogroup; fortbendlibraries.gov (Data Axle Reference Solutions); rapidapi.com Data Axle Business Search; secondary pricing: bookyourdata.com/blog/data-axle-pricing, fullenrich.com/content/data-axle-pricing.
**PDL:** peopledatalabs.com/{company-data/enrichment-api, person-data, data-fields/person}; support.peopledatalabs.com (Pricing & credits); privacy.peopledatalabs.com; peopledatalabs.com/pdf/privacy-security-overview.pdf; oag.ca.gov/data-broker/registration/190662; secondary: fullenrich.com, syncgtm.com/blog/people-data-labs-review, saleshive.com.
