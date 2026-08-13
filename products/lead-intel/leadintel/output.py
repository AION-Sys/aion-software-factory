"""OUTPUT / ORGANIZE — persist leads as JSONL, JSON, and CSV.

CSV flattens nested structures into operator-friendly columns. Missing values are
rendered as empty (CSV) / null (JSON), never invented.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

from .models import Lead

# Column order for the operator-facing CSV (mirrors the mission's required fields).
CSV_COLUMNS = [
    "id",
    "company",
    "website",
    "location",
    "service_type",
    "estimated_opportunity",
    "estimated_opportunity_basis",
    "decision_makers",
    "phone",
    "email",
    "contact_form_url",
    "socials",
    "qualification_score",
    "score_breakdown",
    "status",
    "research_notes",
    "source_provider",
    "source_url",
    "retrieved_at",
]


def write_jsonl(leads: list[Lead], path: Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        for lead in leads:
            fh.write(json.dumps(lead.to_dict(), ensure_ascii=False) + "\n")
    return path


def write_json(leads: list[Lead], path: Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump([lead.to_dict() for lead in leads], fh, ensure_ascii=False, indent=2)
    return path


def write_csv(leads: list[Lead], path: Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for lead in leads:
            writer.writerow(_row(lead))
    return path


def _row(lead: Lead) -> dict:
    dms = "; ".join(
        " ".join(p for p in (dm.name, f"({dm.title})" if dm.title else "") if p)
        for dm in lead.decision_makers
    )
    breakdown = ", ".join(f"{k}={v}" for k, v in lead.score_breakdown.items())
    return {
        "id": lead.id,
        "company": lead.company,
        "website": lead.website or "",
        "location": lead.location.as_text(),
        "service_type": "; ".join(lead.service_type),
        "estimated_opportunity": lead.estimated_opportunity.value,
        "estimated_opportunity_basis": lead.estimated_opportunity_basis,
        "decision_makers": dms,
        "phone": lead.contact_channels.phone or "",
        "email": lead.contact_channels.email or "",
        "contact_form_url": lead.contact_channels.contact_form_url or "",
        "socials": "; ".join(lead.contact_channels.socials),
        "qualification_score": lead.qualification_score,
        "score_breakdown": breakdown,
        "status": lead.status.value,
        "research_notes": lead.research_notes,
        "source_provider": lead.source.provider if lead.source else "",
        "source_url": (lead.source.url if lead.source else "") or "",
        "retrieved_at": (lead.source.retrieved_at if lead.source else "") or "",
    }
