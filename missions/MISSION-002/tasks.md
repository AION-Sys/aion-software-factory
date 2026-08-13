# Engineering Tasks — MISSION-002 — Electrical Contractor Lead Intelligence (V1)

- **Author:** AION-ARCHITECT
- **Consumes:** `architecture.md`
- **Implemented by:** AION-BUILDER

| # | Task | AC covered | Risk | Status |
|---|------|-----------|------|--------|
| 1 | Data models + enums (`models.py`) | AC-2,4,5 | GREEN | DONE |
| 2 | Provider interface + `RawBusiness` (`providers/base.py`) | AC-2 | GREEN | DONE |
| 3 | Synthetic fixture data + `FixtureProvider` | AC-1,7 | GREEN | DONE |
| 4 | `LiveProvider` seam (disabled, env-key only) | AC-7 | GREEN | DONE |
| 5 | Enrichment `enrich()` (no fabrication) | AC-2,6 | GREEN | DONE |
| 6 | Qualification `qualify()` (score+breakdown+status+opportunity) | AC-3,4,5 | GREEN | DONE |
| 7 | Output writers JSONL/CSV/JSON + run summary | AC-1 | GREEN | DONE |
| 8 | Pipeline orchestration (`pipeline.py`) | AC-1 | GREEN | DONE |
| 9 | CLI entry point | AC-1,7 | GREEN | DONE |
| 10 | Tests: qualify, pipeline, output, enrich | AC-8 | GREEN | DONE |
| 11 | Product README + example run | AC-1 | GREEN | DONE |

## Task detail

### Task 6 — Qualification
- **Goal:** deterministic 0–100 score with per-signal breakdown, status, opportunity tier.
- **Files:** `leadintel/qualify.py`
- **Tests:** high-signal → QUALIFIED; sparse → DISQUALIFIED; mid → NEEDS_REVIEW; breakdown sums to score; thresholds at boundaries.
- **Done when:** scoring is deterministic and explainable; all tests pass.
- **Approval gate:** none.

### Task 5 — Enrichment (no fabrication)
- **Goal:** map raw provider data to canonical `Lead`, marking missing fields explicitly.
- **Done when:** absent website/decision-makers become `null`/empty, never invented (AC-6).

### Task 4 — Live provider seam
- **Goal:** define the interface for real acquisition without enabling it.
- **Done when:** `LiveProvider.search` raises a clear "requires approval + API key" error; no network in default path.
- **Approval gate:** enabling it later = YELLOW.

## Sequencing notes
1 → 2 → (3,4) → 5 → 6 → 7 → 8 → 9 → 10 → 11. Core (5,6) is pure and testable before wiring the CLI.
