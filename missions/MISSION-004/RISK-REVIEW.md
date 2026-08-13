# Legal / Privacy Risk Review — MISSION-004

> **Not legal advice and not a legal conclusion.** This flags risk areas by level
> (**LOW / MEDIUM / HIGH / UNKNOWN**) for qualified legal review before any
> live-provider mission. Based on publicly available terms surfaced via search
> (direct primary-document review still required). Access date: 2026-08-13.

## Risk matrix
| Risk area | Google Places | Data Axle | People Data Labs |
|-----------|:-------------:|:---------:|:----------------:|
| Terms of Service (general) | MEDIUM | MEDIUM | MEDIUM |
| Commercial-use permission | MEDIUM | LOW–MEDIUM | MEDIUM |
| **Data storage / retention** | **HIGH** | MEDIUM | MEDIUM |
| Redistribution / resale | HIGH | HIGH | HIGH |
| Data licensing / ownership | MEDIUM | MEDIUM | MEDIUM |
| PII exposure | LOW | MEDIUM | **HIGH** |
| Deletion / data-subject rights | LOW | UNKNOWN | MEDIUM |
| Scraping / acquisition legality (upstream) | LOW | LOW–MEDIUM | MEDIUM |
| Outreach compliance (future, out of scope) | MEDIUM | HIGH | HIGH |

## Notes by provider

### Google Places API
- **Storage / retention = HIGH.** Terms prohibit permanent storage of place content
  (30-day cache; only `place_id` persists). A persistent lead database built on
  Google place data appears **outside** permitted use. *This is the dominant legal
  risk and the main reason Google is not a primary-source candidate.* **Requires legal
  review** if any storage beyond `place_id` is contemplated.
- **Redistribution = HIGH:** sharing/reselling Google-sourced content is restricted.
- **PII = LOW:** business-level data; minimal personal data.

### Data Axle
- **Commercial use = LOW–MEDIUM:** license grants internal-use rights that appear to
  cover internal lead generation; **resale/redistribution prohibited without written
  authorization** (HIGH if we ever share/sell lists).
- **PII = MEDIUM:** executive contact names/titles (and possibly emails) are personal
  data → CCPA/state-law obligations; **outreach** would add CAN-SPAM/DNC/TCPA
  exposure (future mission, out of scope now).
- **Retention/deletion = UNKNOWN:** license-term-dependent; **must be clarified** with
  Data Axle before storing records.

### People Data Labs
- **PII = HIGH:** person-level data from a **registered California data broker**
  (reg. #190662). Licensee inherits data-subject-rights obligations (access,
  deletion, opt-out) under CCPA/CPRA and, for any EU data, GDPR.
- **Acceptable Data Use Policy** governs permitted uses (prohibited-use list);
  redistribution restricted. PDL states it does not sell GDPR Art. 9 / CPRA sensitive
  PII.
- **Deletion = MEDIUM:** PDL provides opt-out/deletion mechanisms, but our system
  would need a process to honor downstream deletion/opt-out for stored records.

## Cross-cutting items requiring legal review before any live mission
1. Whether **storing** provider data in our lead pipeline is permitted (per-provider).
2. Retention limits and a **deletion/opt-out honoring** process for stored PII.
3. Redistribution boundaries (we must not resell/share lists).
4. A written **Data Processing Agreement** where personal data is involved.
5. Outreach-time compliance (deferred, but scope it before collecting contact data).

**No provider is legally cleared by this review.** All carry at least one HIGH-flagged
area needing legal sign-off.
