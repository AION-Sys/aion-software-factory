"""NORMALIZER — RawBusiness -> NormalizedBusiness.

Cleans and standardizes provider output into the provider-independent
representation. No scoring, no fabrication: absent fields stay absent. This is the
boundary past which no provider-specific shape is allowed to leak.
"""
from __future__ import annotations

from datetime import datetime, timezone

from .models import (
    ContactChannels,
    DecisionMaker,
    Location,
    NormalizedBusiness,
    SizeSignals,
    Source,
)
from .providers.base import RawBusiness


def normalize(
    raw: RawBusiness,
    provider_name: str,
    retrieved_at: str | None = None,
    is_synthetic: bool = False,
) -> NormalizedBusiness:
    retrieved_at = retrieved_at or datetime.now(timezone.utc).isoformat(timespec="seconds")
    return NormalizedBusiness(
        company=_clean(raw.name) or "",
        location=Location(
            city=_clean(raw.city),
            region=_clean(raw.region),
            country=_clean(raw.country),
        ),
        website=_clean(raw.website),
        categories=_clean_categories(raw.categories),
        contact_channels=ContactChannels(
            phone=_clean(raw.phone),
            email=_clean(raw.email),
            contact_form_url=_clean(raw.contact_form_url),
            socials=[s.strip() for s in (raw.socials or []) if s and s.strip()],
        ),
        decision_makers=[
            DecisionMaker(
                name=dm.get("name", "").strip(),
                title=_clean(dm.get("title")),
                source=_clean(dm.get("source")),
                contact=_clean(dm.get("contact")),
            )
            for dm in (raw.decision_makers or [])
            if dm.get("name")  # no name -> not a usable decision maker
        ],
        size_signals=SizeSignals(
            employees=raw.employees,
            review_count=raw.review_count,
            years_in_business=raw.years_in_business,
            rating=raw.rating,
        ),
        source=Source(
            provider=provider_name,
            url=_clean(raw.source_url),
            retrieved_at=retrieved_at,
            is_synthetic=is_synthetic,
        ),
        provider_notes=(raw.notes or "").strip(),
    )


def _clean(value):
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _clean_categories(categories) -> list[str]:
    seen: list[str] = []
    for c in categories or []:
        cc = str(c).strip().lower()
        if cc and cc not in seen:
            seen.append(cc)
    return seen
