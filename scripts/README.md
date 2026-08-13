# scripts/

Dependency-free tooling (Python 3, stdlib only — no `pip install`). These are the
foundation's first traceability and validation surfaces. Per ADR-0002 they read
version-controlled files; there is no database.

## `mission_status.py`
Reports where every mission sits in the pipeline, read from each mission's
`AION-MISSION-METADATA` block.

```bash
python3 scripts/mission_status.py          # table
python3 scripts/mission_status.py --json   # machine-readable
```

## `validate_repo.py`
Checks the foundation is structurally intact: required governance files, all five
agent contracts (with all nine contract sections), templates, at least one ADR,
and valid mission `status`/`stage` values. Exits non-zero on failure — suitable
for a CI gate later.

```bash
python3 scripts/validate_repo.py
```

## Conventions
- Stdlib only; must run with a bare `python3`.
- Read-only with respect to repository content (they report/validate; they do not
  mutate missions).
- Keep them small. Add tooling only when a concrete need appears.
