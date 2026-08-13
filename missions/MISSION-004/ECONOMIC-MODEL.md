# Economic Model — MISSION-004

> **These are ASSUMPTIONS, not measured performance.** No real data has been
> ingested and no conversion has been observed. The MISSION-003 baseline is on
> **synthetic** data and is **not** evidence of real-world conversion. Real
> cost-per-qualified-lead can only be known from a bounded, CEO-approved pilot.

## Model
```
cost_per_record        = provider price ÷ 1,000                (from pricing; ESTIMATED)
cost_per_usable_lead   = cost_per_record ÷ usable_rate         (usable_rate = ASSUMED)
cost_per_qualified_ec  = cost_per_record ÷ qualified_rate      (qualified_rate = ASSUMED)
```
- **usable lead** = record with business identity + category + location + ≥1 contact channel.
- **qualified electrical contractor** = classified ELECTRICAL and complete enough to
  score QUALIFIED by our engine (MISSION-003).
- `usable_rate` / `qualified_rate` are fractions of *paid* records that clear each bar,
  **after** any pre-filtering the provider supports (NAICS / place type).

## Inputs (pricing = ESTIMATED; rates = ASSUMED, no measured basis)
| Provider | cost/record | Pre-filter available | usable_rate (ASSUMED) | qualified_rate (ASSUMED) |
|----------|:-----------:|----------------------|:---------------------:|:------------------------:|
| Google Places | $0.020 (Enterprise Details only) | `electrician` type | 0.90 | 0.70 |
| Data Axle (Standard) | $0.050 | NAICS 238210 | 0.85 | 0.65 |
| Data Axle (Enhanced) | $0.075 | NAICS 238210 | 0.85 | 0.65 |
| People Data Labs | $0.100 (Pro company) | industry filter | 0.35 | 0.20 |

Rate rationale (still ASSUMPTIONS): Data Axle/Google support tight pre-filtering, so
most paid records should be on-target; PDL's coverage bias against small local
trades implies a low match/usable rate for this vertical.

## Outputs (illustrative — ASSUMPTIONS)
| Provider | cost / usable lead | cost / qualified EC | cost for 1,000 qualified ECs |
|----------|:------------------:|:-------------------:|:----------------------------:|
| Google Places (Details only) | ≈ $0.022 | ≈ $0.029 | ≈ $29 |
| Data Axle (Standard) | ≈ $0.059 | ≈ $0.077 | ≈ $77 |
| Data Axle (Enhanced) | ≈ $0.088 | ≈ $0.115 | ≈ $115 |
| People Data Labs | ≈ $0.286 | ≈ $0.500 | ≈ $500 |

## Critical caveats (do not read the table without these)
1. **Google's figure is understated and misleading for our use.** It counts only the
   Enterprise Place Details step. A real workflow also pays for a **search step**
   (Text/Nearby Search, billed separately — exact SKU **UNKNOWN** here), and, more
   importantly, **Google's terms forbid permanently storing the place content**
   (30-day cache; only `place_id` persists). A stored lead pipeline would require
   **re-fetching** data, multiplying cost and breaking the "organize/store" model.
2. **Data Axle** cost is a licensed **internal-use** cost; resale/redistribution is
   prohibited. Figures are pay-as-you-go API list prices (ESTIMATED); a negotiated or
   subscription quote may differ.
3. **PDL** effective cost is dominated by low match rate for this vertical; the $0.50
   figure could be far higher if the real match rate is below the assumed 0.35.
4. All conversion rates are **assumptions**. Do not present these as measured KPIs.

## How to replace assumptions with evidence (future, gated)
Run a **bounded pilot** (CEO-approved, within a spend cap) on one metro:
buy/query N records, run them through the MISSION-003 pipeline, and **measure**
usable_rate and qualified_rate on a human-labeled sample. Then recompute this model
with real numbers before scaling. Until then, treat every figure here as directional.
