# Provider Evaluation Framework

A repeatable method for evaluating candidate live data providers **before** any is
chosen. Produces a comparable, evidence-backed scorecard per provider so the CEO
decision rests on facts, not vendor marketing.

> No provider is chosen or endorsed here. This is the how-to; the per-provider
> fill-in lives in `templates/provider-evaluation-template.md`.

## Process
1. Shortlist candidates (desk research only — no signups, no paid trials, no
   credentials; that would trip the YELLOW gate).
2. For each candidate, complete `templates/provider-evaluation-template.md`,
   citing the source (ToS URL, pricing page, docs) for every claim.
3. Score each dimension 1–5 using the rubric below.
4. Flag any **mandatory-fail** (see below) — these disqualify a provider
   regardless of score.
5. Produce a comparison table and a recommendation for the CEO gate.

## Dimensions & weights
| # | Dimension | Weight | What "good" looks like |
|---|-----------|:------:|------------------------|
| 1 | Pricing | 2 | Transparent, predictable, within budget |
| 2 | API limits | 1 | Generous enough for target volume |
| 3 | Permitted use | ⚑ | Explicitly allows commercial prospecting |
| 4 | Data licensing | ⚑ | Permits storage + processing for our use |
| 5 | Terms of Service | ⚑ | No clause we would violate |
| 6 | Geographic coverage | 2 | Covers target markets |
| 7 | Business coverage | 3 | High density of electrical contractors |
| 8 | Freshness | 2 | Records verified recently; freshness stated |
| 9 | Contact availability | 3 | Business contact channels present |
| 10 | Provenance | 3 | Per-record source + timestamp |
| 11 | PII exposure | ⚑ | Business contacts only; no special-category PII |
| 12 | Retention requirements | ⚑ | Compatible with our retention policy |
| 13 | Deletion requirements | ⚑ | Supports deletion/erasure obligations |
| 14 | Security requirements | 3 | Encryption; secret-manager credentials |
| 15 | Reliability | 2 | SLA / track record |
| 16 | Rate limits | 1 | Documented, workable |
| 17 | Cost per qualified lead | 3 | Estimable and acceptable |
| 18 | Scalability | 2 | Grows with volume |

⚑ = **mandatory pass**. Any ⚑ dimension that fails disqualifies the provider
outright, regardless of the weighted score.

## Rubric (1–5)
- **5** Fully meets, evidenced, no concerns.
- **4** Meets with minor caveats.
- **3** Adequate; some gaps to manage.
- **2** Weak; significant gaps.
- **1** Does not meet.

## Scoring
- **Weighted score** = Σ(dimension score × weight) for non-⚑ dimensions,
  normalized to 100.
- **Mandatory gate**: all ⚑ dimensions must be ≥3 with cited evidence.
- **Cost per qualified lead** should be estimated using our baseline
  qualification rate (see `observability.md` / baseline metrics), not the
  provider's raw record count.

## Output
- One completed template per candidate.
- A comparison table (providers × dimensions).
- A written recommendation + residual risks for the CEO gate.
- All artifacts stored in the relevant mission package.
