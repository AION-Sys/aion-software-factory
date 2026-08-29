# Security Review — {PR or Feature Title}

## References
- **Mission:** {link}
- **PR:** {link}
- **Date:** {YYYY-MM-DD}
- **Reviewer:** AION-SECURITY

## Scope of Review
{What was examined: auth, data, infra, dependencies, etc.}

## Trigger Checklist
- [ ] Authentication / authorization
- [ ] Secrets / credentials
- [ ] User data handling
- [ ] External integrations
- [ ] Infrastructure / IAM
- [ ] Dependency changes

## Findings

| ID | Severity | Location | Description | Recommendation |
|----|----------|----------|-------------|----------------|
| {1} | Blocker / High / Medium / Low | {file or area} | {Issue} | {Fix} |

## Secrets Scan
- [ ] No secrets in diff
- [ ] No credentials in logs or error messages introduced

## Dependency Notes
{New packages, versions, known CVE status.}

## Data Classification
{What data is touched; retention; access controls.}

## Verdict
APPROVE | APPROVE WITH CONDITIONS | BLOCK

## Conditions (if any)
{Must-fix items before merge or deploy.}

## Residual Risk (if accepted)
{Document for human approval when issues are deferred.}
