# Handoff — Revenue Factory live `lead.qualified` telemetry

## Status
**PATCH READY** — apply from this repo. Agent push to `AION-Revenue-Factory` still returns **403** for `cursor[bot]` as of last check; use CEO credentials or grant the bot write access.

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

## Mission linkage

Feeds Mission 002 **Learning** and **Validation** gates via live `lead.qualified` signals on the health aggregator / event spine.
