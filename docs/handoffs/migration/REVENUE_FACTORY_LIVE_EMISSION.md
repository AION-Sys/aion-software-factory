# Revenue Factory — live `lead.qualified` telemetry

## Purpose

When qualifying leads in a live run, forward `lead.qualified` envelope events to the
AION **health aggregator** so Mission 002 validation can observe economic signals
without breaking offline simulation.

## Environment

| Variable | Required | Purpose |
|----------|----------|---------|
| `AION_TELEMETRY_URL` | No | POST all envelope events (event spine) |
| `AION_TELEMETRY_KEY` | No | Bearer token for telemetry |
| `AION_HEALTH_AGGREGATOR_URL` | No | POST **only** `lead.qualified` events |
| `AION_HEALTH_AGGREGATOR_KEY` | No | Bearer token for health aggregator |

Offline default unchanged: no env vars → `NullSink` (no network I/O).

## Wiring

`build_factory_from_env()` composes sinks:

- `AION_TELEMETRY_URL` → all events via `HttpTelemetrySink`
- `AION_HEALTH_AGGREGATOR_URL` → `FilteredSink(..., {"lead.qualified"})`
- Both set → `CompositeSink` fan-out

Transport failures are captured in `HttpTelemetrySink.failures` and **never**
propagate into the revenue workflow.

## Verify (staging)

```bash
export AION_HEALTH_AGGREGATOR_URL=https://<staging-health-aggregator>/ingest
export AION_HEALTH_AGGREGATOR_KEY=<staging-key>   # if required
python -m pytest -q
python -m aion_revenue_factory.cli run-day --prospects 5   # or project entrypoint
# Confirm lead.qualified envelopes in aggregator logs
```

## Rollback

Unset `AION_HEALTH_AGGREGATOR_URL` / `AION_TELEMETRY_URL` and redeploy. No schema
changes.

## Approval

Live production URLs require CEO release gate (Mission 002).
