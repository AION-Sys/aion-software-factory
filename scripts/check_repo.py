#!/usr/bin/env python3
"""Repo structure checks for aion-software-factory (no tests exist yet).

1. Every .yml/.yaml file parses.
2. Every relative Markdown link resolves to an existing file.
3. Required factory docs and templates exist.
4. Every mission listed in missions/README.md exists and has a Status line.
"""
import pathlib, re, subprocess, sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
REQUIRED = [
    "README.md", "AGENTS.md", "AION_ENGINEERING.md", "missions/README.md",
    ".github/PULL_REQUEST_TEMPLATE.md", "docs/workflows/END_TO_END.md",
    "docs/templates/MISSION.template.md", "docs/templates/TASK.template.md",
    "docs/templates/QA_REPORT.template.md",
]
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
errors = []

files = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()

for f in files:
    if f.endswith((".yml", ".yaml")):
        try:
            yaml.safe_load((ROOT / f).read_text())
        except yaml.YAMLError as e:
            errors.append(f"{f}: invalid YAML: {e}")

for f in files:
    if not f.endswith(".md"):
        continue
    text = (ROOT / f).read_text()
    text = re.sub(r"```.*?```", "", text, flags=re.S)  # ignore code blocks
    for target in LINK.findall(text):
        if re.match(r"^(https?:|mailto:|#)", target):
            continue
        path = target.split("#")[0]
        if not path:
            continue
        if not ((ROOT / f).parent / path).resolve().exists():
            errors.append(f"{f}: broken link -> {target}")

for r in REQUIRED:
    if not (ROOT / r).exists():
        errors.append(f"missing required file: {r}")

readme = (ROOT / "missions/README.md").read_text()
for m in sorted(set(re.findall(r"\((MISSION-\d{3}\.md)\)", readme))):
    p = ROOT / "missions" / m
    if not p.exists():
        errors.append(f"missions/README.md lists {m} but file is missing")
    elif not re.search(r"status", p.read_text(), re.I):
        errors.append(f"missions/{m}: no Status field")

for e in errors:
    print(f"ERROR {e}")
print(f"checked {len(files)} files: {len(errors)} error(s)")
sys.exit(1 if errors else 0)
