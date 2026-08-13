# Lead Intelligence (V1) — `lead-intel`

Built by the AION Software Factory for **MISSION-002**. Turns a
`(market, location)` input into a structured, scored electrical-contractor lead
list. **Intelligence layer only — no outreach.**

> V1 runs fully **offline** on **synthetic** sample data (no credentials, no
> network). Real/paid data acquisition is a disabled, human-gated seam. See
> `../../missions/MISSION-002/` for the full mission package and
> `../../docs/decisions/0005-fixture-first-gated-live-acquisition.md`.

## Pipeline
`INPUT → RESEARCH → ENRICH → QUALIFY → ORGANIZE → OUTPUT`

## Run it
```bash
cd products/lead-intel
python3 cli.py --market "electrical contractors" --location "Austin, TX"
# options: --limit N  --out DIR  --run-id NAME  --fixture PATH  --provider fixture|live
```
Outputs (per run) in the chosen `--out` dir: `<run>.csv`, `.json`, `.jsonl`, and
`.run-summary.json`. A committed sample lives in `examples/`.

## Output fields (per lead)
`company, website, location, service_type, estimated_opportunity (+basis),
decision_makers, contact_channels (phone/email/form/socials),
qualification_score, score_breakdown, status, research_notes, source`.

## Qualification model (transparent, tunable)
Score 0–100 = service relevance (25) + location match (15) + has website (15) +
has contact (15) + opportunity signal (20) + decision-maker identified (10).
Status: **≥60 QUALIFIED**, **40–59 NEEDS_REVIEW**, **<40 DISQUALIFIED**. Every
lead carries a `score_breakdown` explaining its score. Weights/thresholds are
constants in `leadintel/qualify.py`.

## Tests
```bash
cd products/lead-intel
python3 -m unittest discover -s tests
```

## Layout
```
leadintel/            core package (stdlib only)
  models.py           canonical Lead schema + enums
  providers/          base interface, fixture (default), live (disabled seam)
  enrich.py           raw -> Lead (never fabricates)
  qualify.py          scoring / status / opportunity
  output.py           JSONL / JSON / CSV writers
  pipeline.py         orchestration + run summary
cli.py                command-line entry point
data/fixtures/        SYNTHETIC sample data
tests/                unittest suite
examples/             committed sample run
```

## Not in V1 (by design)
Automated outreach · live/paid data provider · web UI · CRM sync · database.
Enabling live acquisition requires human approval (YELLOW) and a security review.
