#!/usr/bin/env python3
"""Report where every mission sits in the AION pipeline.

Reads the machine-readable metadata block from each mission and prints a table.
Stdlib only — no dependencies, no database (see ADR-0002).

Mission locations recognised:
  - missions/MISSION-XXX.md            (flat meta-missions, e.g. MISSION-001)
  - missions/MISSION-XXX/mission.md    (product missions with artifact packages)

Usage:
  python3 scripts/mission_status.py            # human-readable table
  python3 scripts/mission_status.py --json     # machine-readable JSON
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MISSIONS_DIR = REPO_ROOT / "missions"

# Ordered pipeline stages (see docs/workflows/development-workflow.md).
STAGES = [
    "draft", "pm", "prd", "architecture", "tasks",
    "build", "qa", "security", "approval", "pr", "merged", "deployed",
]
META_RE = re.compile(r"<!--\s*AION-MISSION-METADATA(.*?)-->", re.DOTALL)
FIELD_RE = re.compile(r"^\s*([A-Za-z_]+)\s*:\s*(.*?)\s*$")


def parse_metadata(text: str) -> dict:
    """Extract fields from the AION-MISSION-METADATA comment block, if present."""
    meta: dict[str, str] = {}
    match = META_RE.search(text)
    if not match:
        return meta
    for line in match.group(1).splitlines():
        line = line.split("#", 1)[0]  # strip inline comments
        m = FIELD_RE.match(line)
        if m:
            meta[m.group(1).lower()] = m.group(2)
    return meta


def find_mission_files() -> list[Path]:
    files: list[Path] = []
    if not MISSIONS_DIR.exists():
        return files
    # Flat mission files: missions/MISSION-*.md
    files.extend(sorted(MISSIONS_DIR.glob("MISSION-*.md")))
    # Directory missions: missions/MISSION-*/mission.md
    for d in sorted(MISSIONS_DIR.glob("MISSION-*")):
        if d.is_dir():
            m = d / "mission.md"
            if m.exists():
                files.append(m)
    return files


def stage_progress(stage: str) -> str:
    if stage in STAGES:
        idx = STAGES.index(stage)
        return f"{idx + 1}/{len(STAGES)}"
    return "?/?"


def collect() -> list[dict]:
    rows = []
    for path in find_mission_files():
        text = path.read_text(encoding="utf-8")
        meta = parse_metadata(text)
        rel = path.relative_to(REPO_ROOT)
        rows.append({
            "id": meta.get("id", path.stem),
            "title": meta.get("title", "(no title in metadata)"),
            "status": meta.get("status", "UNKNOWN"),
            "stage": meta.get("stage", "unknown"),
            "progress": stage_progress(meta.get("stage", "")),
            "priority": meta.get("priority", "-"),
            "owner": meta.get("owner", "-"),
            "path": str(rel),
            "has_metadata": bool(meta),
        })
    return rows


def print_table(rows: list[dict]) -> None:
    if not rows:
        print("No missions found under missions/.")
        return
    headers = ["ID", "STATUS", "STAGE", "PROG", "PRI", "TITLE"]
    data = [[r["id"], r["status"], r["stage"], r["progress"],
             r["priority"], r["title"]] for r in rows]
    widths = [max(len(h), *(len(row[i]) for row in data)) for i, h in enumerate(headers)]
    fmt = "  ".join("{:<" + str(w) + "}" for w in widths)
    print(fmt.format(*headers))
    print(fmt.format(*["-" * w for w in widths]))
    for row in data:
        print(fmt.format(*row))
    missing = [r["id"] for r in rows if not r["has_metadata"]]
    if missing:
        print(f"\nNote: no metadata block found for: {', '.join(missing)}")


def main(argv: list[str]) -> int:
    rows = collect()
    if "--json" in argv:
        print(json.dumps(rows, indent=2))
    else:
        print_table(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
