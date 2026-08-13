# Provider Scores — MISSION-004

## Methodology
Each provider is scored **1–5** per dimension (5 = fully meets, evidenced; 1 = does
not meet). The weighted score = Σ(score × weight) ÷ 5, normalized to 0–100. Weights
follow the mission's suggested dimensions. Scores reflect fit **for AION's specific
use case** (US local electrical contractors → structured, stored, qualified leads
with decision-makers where legitimate), not generic quality.

> Scores are **judgments over ESTIMATED/CONFIRMED-via-search evidence** (see the
> methodology limitation in `MISSION.md`). They rank candidates for further
> verification — they are not a purchase decision.

| Dimension | Weight |
|-----------|:------:|
| Data Quality | 20% |
| Electrical Coverage | 15% |
| Business Coverage | 10% |
| Provenance | 10% |
| API Quality | 10% |
| Pricing / Economics | 15% |
| Commercial Rights | 10% |
| Privacy / Security | 5% |
| Operational Reliability | 5% |

## Scorecard
| Dimension (weight) | Google Places | Data Axle | PDL |
|--------------------|:-------------:|:---------:|:---:|
| Data Quality (20) | 4 | 4 | 3 |
| Electrical Coverage (15) | 4 | 5 | 2 |
| Business Coverage (10) | 5 | 5 | 4 |
| Provenance (10) | 4 | 4 | 3 |
| API Quality (10) | 5 | 3 | 5 |
| Pricing/Economics (15) | 3 | 4 | 3 |
| Commercial Rights (10) | **1** | 3 | 3 |
| Privacy/Security (5) | 5 | 3 | 2 |
| Operational Reliability (5) | 5 | 4 | 4 |
| **Weighted score /100** | **77.0** | **80.0** | **63.0** |

### Weighted calculation
- **Google:** (4·20+4·15+5·10+4·10+5·10+3·15+1·10+5·5+5·5)/5 = 385/5 = **77.0**
- **Data Axle:** (4·20+5·15+5·10+4·10+3·10+4·15+3·10+3·5+4·5)/5 = 400/5 = **80.0**
- **PDL:** (3·20+2·15+4·10+3·10+5·10+3·15+3·10+2·5+4·5)/5 = 315/5 = **63.0**

## Ranking
1. **Data Axle — 80.0**
2. **Google Places API — 77.0** (see override below)
3. **People Data Labs — 63.0**

## Rationale highlights
- **Data Axle** leads on the dimensions that matter most for our vertical:
  electrical-contractor selectability (NAICS), SMB depth, decision-maker contacts,
  and transparent pay-as-you-go pricing with an internal-use license that appears
  compatible with storing leads for internal use.
- **Google Places** scores well on data/API/reliability but carries a
  **mandatory-concern override**: Commercial Rights = 1 because its terms **prohibit
  permanently storing place content** (30-day cache; only `place_id` may persist).
  For a system whose purpose is to *store* a structured lead pipeline, this is close
  to disqualifying for the **primary** role — the weighted score alone understates
  it. Google remains viable only as a **live identity/verification lookup**, not a
  storage source.
- **PDL** is strong technically but its person/company data is **biased toward
  online-visible white-collar profiles**, underrepresenting small local electrical
  contractors — the exact population we target — and carries the **highest PII
  burden** (registered data broker; person-level data). Weakest fit as primary.

## Sensitivity
The scores are stable to reasonable weight changes among Data Axle and Google; PDL
stays last under any plausible weighting because its two lowest scores
(Electrical Coverage, Privacy) sit on non-trivial weights. **Pricing/Economics**
scores rest on ESTIMATED figures; if Data Axle's real quote is materially higher, it
could compress the Data Axle–Google gap.
