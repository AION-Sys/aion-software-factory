"""ENRICH — map a RawBusiness into the canonical Lead schema.

Rule (AC-2, AC-6): never fabricate. Missing fields become None / empty. We only
normalize and carry forward what the provider supplied. Decision-makers are only
included when the source legitimately provided them.
"""
from __future__ import annotations

from datetime import datetime, timezone

from .models import (
    ContactChannels,
    DecisionMaker,
    Lead,
    Location,
    Query,
    SizeSignals,
    Source,
)
from .providers.base import RawBusiness


def enrich(raw: RawBusiness, query: Query, retrieved_at: str | None = None) -> Lead:
    location = Location(
        city=_clean(raw.city),
        region=_clean(raw.region),
        country=_clean(raw.country),
    )
    contacts = ContactChannels(
        phone=_clean(raw.phone),
        email=_clean(raw.email),
        contact_form_url=_clean(raw.contact_form_url),
        socials=[s for s in (raw.socials or []) if s],
    )
    decision_makers = [
        DecisionMaker(
            name=dm.get("name", "").strip(),
            title=_clean(dm.get("title")),
            source=_clean(dm.get("source")),
            contact=_clean(dm.get("contact")),
        )
        for dm in (raw.decision_makers or [])
        if dm.get("name")
    ]
    size = SizeSignals(
        employees=raw.employees,
        review_count=raw.review_count,
        years_in_business=raw.years_in_business,
        rating=raw.rating,
    )
    notes = raw.notes.strip() if raw.notes else ""
    if not decision_makers and "decision-maker" not in notes.lower():
        notes = _append(notes, "No decision-maker legitimately available at research time.")
    if not raw.website and "website" not in notes.lower():
        notes = _append(notes, "No website found.")

    return Lead(
        company=raw.name.strip(),
        location=location,
        website=_clean(raw.website),
        service_type=[c.strip() for c in (raw.categories or []) if c.strip()],
        contact_channels=contacts,
        decision_makers=decision_makers,
        size_signals=size,
        source=Source(
            provider=_provider_of(raw),
            url=_clean(raw.source_url),
            retrieved_at=retrieved_at or datetime.now(timezone.utc).isoformat(timespec="seconds"),
        ),
        research_notes=notes,
    )


def _clean(value):
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _append(notes: str, extra: str) -> str:
    return f"{notes} {extra}".strip() if notes else extra


def _provider_of(raw: RawBusiness) -> str:
    # Provenance hint; the pipeline overwrites with the actual provider name.
    return "unknown"
