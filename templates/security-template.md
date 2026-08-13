# Security Report — MISSION-XXX — <Title>

- **Reviewer:** AION-SECURITY (independent of Builder)
- **Consumes:** implementation branch/PR + `architecture.md` + `qa-report.md`
- **Verdict:** PASS | PASS WITH CONDITIONS | FAIL
- **Date:** YYYY-MM-DD

## 1. Review checklist
| Area | Result | Notes |
|------|--------|-------|
| Authentication | OK / ISSUE | |
| Authorization / least privilege | OK / ISSUE | |
| Secrets handling (none hardcoded/committed/logged) | OK / ISSUE | |
| API exposure & abuse/rate limiting | OK / ISSUE | |
| Database permissions | OK / ISSUE | |
| Input validation / injection | OK / ISSUE | |
| Dependency risks | OK / ISSUE | |
| Common app security (OWASP-style) | OK / ISSUE | |
| Infrastructure / operational risk | OK / ISSUE | |

## 2. Findings
| ID | Severity (LOW/MED/HIGH/CRIT) | Location (no secret values) | Description | Remediation |
|----|------------------------------|------------------------------|-------------|-------------|
| S1 |                              |                              |             |             |

## 3. Secret scan
- Tooling used: <e.g. secret scanning>
- Result: <clean / findings — report location only, never the value>

## 4. Verdict & handoff
- **Verdict:** <PASS → Human Approval Gate | FAIL → return to AION-BUILDER>
- **Blocking conditions:** <finding IDs that must be resolved before approval>
- **Notes for the human approver:** <residual risk they should weigh>
