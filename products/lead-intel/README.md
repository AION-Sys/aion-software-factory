# Lead Intelligence — `lead-intel`

Built by the AION Software Factory (MISSION-002, hardened in MISSION-003). Turns a
`(market, location)` input into a structured, **scored, explainable**
electrical-contractor lead list. **Intelligence layer only — no outreach.**

> Runs fully **offline** on **synthetic** data (no credentials, no network). Every
> synthetic lead is labeled `is_synthetic` end-to-end and is **NOT real-world
> evidence**. Real/paid data acquisition is a disabled, human-gated seam — see
> `../../docs/operations/live-provider-activation-checklist.md`.

## Pipeline (clean stage separation)
```
Data Provider → Raw Data → Normalizer → Enrichment → Qualification Engine → Lead → Output
providers/*     RawBusiness  normalize.py  enrich.py    scoring/engine.py            output.py
```
The **qualification engine is provider-independent**: it consumes an enriched
`Lead` + a `ScoringConfig`, never provider-specific shapes.

## Run it
```bash
cd products/lead-intel
python3 cli.py --market "electrical contractors" --location "Denver, CO" \
    --fixture data/fixtures/synthetic_leads.json
# options: --limit N  --out DIR  --run-id NAME  --config scoring.json  --provider fixture|live
```

## Measure it (baseline metrics on the labeled dataset)
```bash
python3 evaluate.py            # precision / FP / FN / completeness (SYNTHETIC)
python3 evaluate.py --json     # machine-readable
```

## Scoring model — explicit, configurable, explainable (ADR-0006)
Two parts:
1. **Category validation (gate).** Each business is classified `ELECTRICAL`,
   `ADJACENT`, `NON_ELECTRICAL`, or `AMBIGUOUS`. Only `ELECTRICAL` can be
   `QUALIFIED`; non-electrical trades (handyman/plumber/HVAC/GC-without-electrical)
   are gated out.
2. **Weighted signals.** Positive add, negative subtract; every lead records a
   `why` (per-signal points + reasons).

All weights, thresholds, and keyword lists live in
`leadintel/scoring/default_config.json` — tune there, not in code. Provide your
own with `--config`.

## Output fields (per lead)
`company, synthetic, category_verdict, status, qualification_score,
estimated_opportunity, website, location, service_type, decision_makers,
contact channels, score_breakdown, why, category_reason, data_completeness,
provenance_complete, research_notes, source, scoring_config_version`.

## Tests
```bash
python3 -m unittest discover -s tests    # 50 tests
```
Includes data-driven category/qualification regression tests
(`tests/test_category.py`) over the labeled dataset.

## Layout
```
leadintel/
  models.py            canonical schema, enums, NormalizedBusiness, contributions
  providers/           base interface, fixture (synthetic default), live (disabled seam)
  normalize.py         Normalizer: clean/standardize (provider-independent)
  enrich.py            Enrichment: completeness + provenance, honest notes
  scoring/             config.py + engine.py + default_config.json (the model)
  output.py            CSV / JSON / JSONL writers (+ synthetic labels)
  pipeline.py          orchestration + data-quality run summary
  metrics.py           baseline metrics over the labeled dataset
cli.py                 run the pipeline
evaluate.py            compute baseline metrics
data/fixtures/         synthetic_leads.json (labeled) + electrical_contractors.json
tests/                 unittest suite (50 tests)
examples/              committed sample runs
```

## Not in V1 (by design)
Live/paid data provider · real data · automated outreach · web UI · CRM · database
· deployment. Enabling live acquisition requires the CEO gate (activation checklist).
