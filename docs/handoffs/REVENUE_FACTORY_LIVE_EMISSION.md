# Handoff — Revenue Factory live `lead.qualified` telemetry

## Status
**APPLIED LOCALLY — PUSH BLOCKED** — Cloud Agent applied the patch on `AION-Revenue-Factory` `main` (`f237b0c`), installed `.[dev]`, and ran pytest. **67 passed.** `git push -u origin feat/live-lead-qualified-telemetry` still returns **403** for `cursor[bot]`.

Use CEO credentials to push the local commit, or grant the bot write access and re-run the apply.

## Apply verification (2026-08-31)

| Step | Result |
|------|--------|
| Clone `AION-Sys/AION-Revenue-Factory` | OK (`main` @ `f237b0c`) |
| `git apply` patch `0001-feat-live-lead.qualified-telemetry-to-health-aggrega.patch` | OK (`git apply --check` clean) |
| `pip install -e ".[dev]"` | OK |
| `python3 -m pytest -q` | **67 passed**, 0 failed (0.50s) |
| Branch `feat/live-lead-qualified-telemetry` | Created locally |
| Commit `feat: live lead.qualified telemetry to health aggregator` | Local SHA `f74924f` |
| `git push -u origin feat/live-lead-qualified-telemetry` | **403** — `Permission to AION-Sys/AION-Revenue-Factory.git denied to cursor[bot]` |

Local clone (agent VM, not on GitHub): `/home/ubuntu/AION-Revenue-Factory` on `feat/live-lead-qualified-telemetry`.

## Apply (human or bot with write access)

```bash
git clone git@github.com:AION-Sys/AION-Revenue-Factory.git
cd AION-Revenue-Factory
git apply /path/to/aion-software-factory/docs/handoffs/patches/0001-feat-live-lead.qualified-telemetry-to-health-aggrega.patch
pip install -e ".[dev]"
python3 -m pytest -q
git checkout -b feat/live-lead-qualified-telemetry
git add -A && git commit -m "feat: live lead.qualified telemetry to health aggregator"
git push -u origin feat/live-lead-qualified-telemetry
```

Or from factory repo root:

```bash
git -C AION-Revenue-Factory apply docs/handoffs/patches/0001-feat-live-lead.qualified-telemetry-to-health-aggrega.patch
```

## Artifacts (in this repo)

| File | Purpose |
|------|---------|
| [`migration/REVENUE_FACTORY_LIVE_EMISSION.md`](migration/REVENUE_FACTORY_LIVE_EMISSION.md) | Live wiring runbook |
| [`patches/0001-feat-live-lead.qualified-telemetry-to-health-aggrega.patch`](patches/0001-feat-live-lead.qualified-telemetry-to-health-aggrega.patch) | Code change (67 tests pass when applied) |

company-os PR #20 may contain the canonical copy; this factory mirror is ready to apply now.

## What changed

- `FilteredSink` + `CompositeSink` in `event_sink.py`
- `AION_HEALTH_AGGREGATOR_URL` env → POST **only** `lead.qualified` envelopes
- `AION_TELEMETRY_URL` unchanged (all events)
- Offline default unchanged (`NullSink`)

## Env vars (staging first)

| Variable | Purpose |
|----------|---------|
| `AION_HEALTH_AGGREGATOR_URL` | Health aggregator ingest |
| `AION_HEALTH_AGGREGATOR_KEY` | Bearer token (optional) |
| `AION_TELEMETRY_URL` | Full event spine (optional) |
| `AION_TELEMETRY_KEY` | Bearer token (optional) |

## Unblock agent push

Grant **`cursor[bot]`** write access on `AION-Sys/AION-Revenue-Factory` (Settings → Collaborators or org team). Personal CEO access does not apply to the Cloud Agent token.

Re-verified 2026-08-31: apply + tests succeed; only the push is blocked. After write access, re-run the apply block below (or cherry-pick local `f74924f` if the clone is still available).

## Mission linkage

Feeds Mission 002 **Learning** and **Validation** gates via live `lead.qualified` signals on the health aggregator / event spine.
