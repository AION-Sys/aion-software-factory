#!/usr/bin/env python3
"""Validate that the AION Software Factory foundation is structurally intact.

Checks required governance files, agent contracts, templates, docs, and mission
metadata. Exits non-zero if any check fails so it can gate CI later.

Stdlib only. Usage:
  python3 scripts/validate_repo.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "AION_ENGINEERING.md",
    "AGENTS.md",
    ".gitignore",
    "agents/README.md",
    "docs/workflows/development-workflow.md",
    "docs/workflows/agent-handoffs.md",
    "docs/architecture/factory-architecture.md",
    "docs/operations/approval-policy.md",
    "docs/operations/security-and-secrets.md",
    "docs/operations/observability.md",
    "scripts/mission_status.py",
]

AGENTS = ["pm", "architect", "builder", "qa", "security"]

REQUIRED_TEMPLATES = [
    "mission-template.md", "prd-template.md", "architecture-template.md",
    "task-list-template.md", "qa-template.md", "security-template.md",
    "adr-template.md",
]

CONTRACT_SECTIONS = [
    "Purpose", "Inputs", "Outputs", "Responsibilities", "Allowed actions",
    "Forbidden actions", "Required context", "Escalation conditions",
    "Completion criteria",
]

VALID_STAGES = {
    "draft", "pm", "prd", "architecture", "tasks", "build",
    "qa", "security", "approval", "pr", "merged", "deployed",
}
VALID_STATUS = {"DRAFT", "ACTIVE", "BLOCKED", "DONE", "ARCHIVED"}

META_RE = re.compile(r"<!--\s*AION-MISSION-METADATA(.*?)-->", re.DOTALL)


def check(cond: bool, ok: str, err: str, errors: list[str]) -> None:
    if cond:
        print(f"  ok   {ok}")
    else:
        print(f"  FAIL {err}")
        errors.append(err)


def main() -> int:
    errors: list[str] = []

    print("Required files:")
    for rel in REQUIRED_FILES:
        p = REPO_ROOT / rel
        check(p.is_file(), rel, f"missing file: {rel}", errors)

    print("\nAgent contracts:")
    for agent in AGENTS:
        p = REPO_ROOT / "agents" / agent / "CONTRACT.md"
        if not p.is_file():
            check(False, "", f"missing contract: agents/{agent}/CONTRACT.md", errors)
            continue
        text = p.read_text(encoding="utf-8")
        missing = [s for s in CONTRACT_SECTIONS if s.lower() not in text.lower()]
        check(not missing, f"agents/{agent}/CONTRACT.md",
              f"agents/{agent}/CONTRACT.md missing sections: {missing}", errors)

    print("\nTemplates:")
    for t in REQUIRED_TEMPLATES:
        p = REPO_ROOT / "templates" / t
        check(p.is_file(), f"templates/{t}", f"missing template: templates/{t}", errors)

    print("\nDecisions (ADRs):")
    adr_dir = REPO_ROOT / "docs" / "decisions"
    adrs = sorted(adr_dir.glob("*.md")) if adr_dir.exists() else []
    check(len(adrs) >= 1, f"{len(adrs)} ADR(s) present",
          "no ADRs found in docs/decisions/", errors)

    print("\nMissions:")
    missions_dir = REPO_ROOT / "missions"
    mission_files = []
    if missions_dir.exists():
        mission_files.extend(sorted(missions_dir.glob("MISSION-*.md")))
        for d in sorted(missions_dir.glob("MISSION-*")):
            if not d.is_dir():
                continue
            for name in ("mission.md", "MISSION.md"):
                if (d / name).is_file():
                    mission_files.append(d / name)
                    break
    check(len(mission_files) >= 1, f"{len(mission_files)} mission(s) present",
          "no missions found", errors)

    for mf in mission_files:
        rel = mf.relative_to(REPO_ROOT)
        text = mf.read_text(encoding="utf-8")
        m = META_RE.search(text)
        if not m:
            check(False, "", f"{rel}: no AION-MISSION-METADATA block", errors)
            continue
        block = m.group(1)
        fields: dict[str, str] = {}
        for line in block.splitlines():
            key, sep, val = line.partition(":")
            if sep:
                fields[key.strip().lower()] = val.split("#", 1)[0].strip()
        status = fields.get("status", "")
        stage = fields.get("stage", "")
        check(status in VALID_STATUS, f"{rel} status={status}",
              f"{rel}: invalid/missing status '{status}'", errors)
        check(stage in VALID_STAGES, f"{rel} stage={stage}",
              f"{rel}: invalid/missing stage '{stage}'", errors)

    print("\n" + "=" * 60)
    if errors:
        print(f"VALIDATION FAILED — {len(errors)} problem(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("VALIDATION PASSED — foundation is structurally intact.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
