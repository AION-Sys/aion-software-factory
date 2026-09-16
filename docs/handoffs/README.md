# Agent Handoffs

Cross-repo work that Cloud Agents cannot push directly (403 / missing repo access) is documented here for human apply.

| Handoff | Target repo | Status |
|---------|-------------|--------|
| [REVENUE_FACTORY_LIVE_EMISSION.md](REVENUE_FACTORY_LIVE_EMISSION.md) | [AION-Sys/AION-Revenue-Factory](https://github.com/AION-Sys/AION-Revenue-Factory) | Applied locally 2026-08-31 — 67 tests passed; `git push` still **403** for `cursor[bot]` |
| [SECRETS_AND_DEMO_AUTH.md](SECRETS_AND_DEMO_AUTH.md) | [AION-Sys/Ceoloo-aion-revenue-copilot](https://github.com/AION-Sys/Ceoloo-aion-revenue-copilot) + Vercel/GitHub secrets | Partial 2026-09-16 — demo still ON in prod; Supabase public env likely unset; patch ready; agent push **403** |

When a handoff is applied and merged on the target repo, update the status row and link the resulting PR.
