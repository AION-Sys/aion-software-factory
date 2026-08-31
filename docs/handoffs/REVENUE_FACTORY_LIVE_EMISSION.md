# Handoff — Revenue Factory live `lead.qualified` telemetry

## Status
**BLOCKED** — Cloud Agent (`cursor[bot]`) cannot push to target repos (403).

| Target | Permission | Error |
|--------|------------|-------|
| [AION-Sys/AION-Revenue-Factory](https://github.com/AION-Sys/AION-Revenue-Factory) | none | `403 Permission denied` |
| [AION-Sys/Ceoloo-aion-revenue-copilot](https://github.com/AION-Sys/Ceoloo-aion-revenue-copilot) | none | `403 Permission denied` (historical) |

**Human with org write access must apply** the artifacts below.

## Source of truth (company-os)

Draft **company-os PR #20** contains:

| Artifact | Purpose |
|----------|---------|
| `docs/migration/REVENUE_FACTORY_LIVE_EMISSION.md` | Live wiring runbook |
| `docs/migration/patches/0001-feat-live-lead.qualified-telemetry-to-health-aggrega.patch` | Code change for `lead.qualified` → health aggregator |

> The `company-os` repository is not accessible to the Cloud Agent token in this environment. Treat PR #20 as canonical; this document is the factory-side mirror and apply checklist.

## What the change does (intent)

Wire **live telemetry emission** when the Revenue Factory qualifies a lead:

1. Orchestrator emits `lead.qualified` (already implemented in `AION-Revenue-Factory` `orchestrator.py`).
2. `HttpTelemetrySink` POSTs the AION envelope when `AION_TELEMETRY_URL` is set (`config.py` → `_build_event_sink`).
3. The patch routes / enriches that event for the **health aggregator** (AION learning / ops telemetry path) so Mission 002 validation can observe economic signals.

No change to offline default: without env vars, `NullSink` keeps runs side-effect free.

## Human apply procedure

### Step 1 — Merge company-os PR #20

Review and merge PR #20 in **company-os** so the runbook and patch are on that repo's default branch.

### Step 2 — Apply patch to AION-Revenue-Factory

From a machine with **push access** to `AION-Sys/AION-Revenue-Factory`:

```bash
git clone git@github.com:AION-Sys/AION-Revenue-Factory.git
cd AION-Revenue-Factory

# Copy patch from company-os after PR #20 merges:
#   docs/migration/patches/0001-feat-live-lead.qualified-telemetry-to-health-aggrega.patch
git apply /path/to/0001-feat-live-lead.qualified-telemetry-to-health-aggrega.patch

# Or use git am if the patch includes commit metadata:
# git am /path/to/0001-feat-live-lead.qualified-telemetry-to-health-aggrega.patch

python -m pytest -q
git checkout -b feat/live-lead-qualified-telemetry
git add -A
git commit -m "feat: live lead.qualified telemetry to health aggregator"
git push -u origin feat/live-lead-qualified-telemetry
```

Open a PR on `AION-Revenue-Factory`; reference company-os PR #20 in the description.

### Step 3 — Configure live env (staging first)

From `AION-Revenue-Factory` `config.py` / README:

| Variable | Purpose |
|----------|---------|
| `AION_TELEMETRY_URL` | POST target for envelope events |
| `AION_TELEMETRY_KEY` | Bearer token (optional) |

Use **staging / canary** endpoints first. Do not point at production ingest until CEO release gate (Mission 002).

### Step 4 — Verify

```bash
# Offline still works (no env)
python -m pytest -q

# With telemetry URL set (staging), run a workflow slice that qualifies leads
# Confirm lead.qualified appears in health aggregator / ingest logs
```

Checklist:

- [ ] `lead.qualified` envelope received by telemetry endpoint
- [ ] Revenue workflow does not fail when telemetry is down (`HttpTelemetrySink` captures failures)
- [ ] No secrets in logs or commits

## Mission linkage

| Mission | Connection |
|---------|------------|
| **MISSION-002** (Revenue Copilot) | Learning + validation gates require structured outcome events; Revenue Factory `lead.qualified` feeds the same AION event spine |
| **AION-Revenue-Factory** | Emits canonical events; this handoff enables **live** emission |
| **Ceoloo-aion-revenue-copilot** | Rep workflow emits CRM + learning events on post-call (Task 8); separate product repo |

## Unblock options (pick one)

1. **Human apply** — follow steps above (recommended now).
2. **Grant `cursor[bot]` write** on `AION-Revenue-Factory` (and product repos) so Cloud Agents can push handoff PRs.
3. **Pat transfer** — CEO pushes the local commit that failed with 403 using the commands in Step 2.

## Agent handoff record

| Field | Value |
|-------|-------|
| Requested | Live `lead.qualified` telemetry wiring to health aggregator |
| Completed (factory) | Blocker documented; apply runbook mirrored here |
| Blocked on | 403 push to `AION-Revenue-Factory`; company-os PR #20 not readable by agent |
| Human approval | Required for live telemetry URLs and production ingest |
| Next action | Merge company-os #20 → human apply patch → PR on Revenue Factory |
