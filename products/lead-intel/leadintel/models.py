"""Canonical data models for the lead-intelligence pipeline.

Design rule (AC-2, AC-6): absence is represented explicitly (None / empty list).
Nothing here fabricates data — enrichment only maps what a provider supplies.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional


class Status(str, Enum):
    """Lifecycle/qualification status of a lead."""
    NEW = "NEW"                    # pre-scoring
    QUALIFIED = "QUALIFIED"        # score >= QUALIFY_THRESHOLD
    NEEDS_REVIEW = "NEEDS_REVIEW"  # REVIEW_THRESHOLD <= score < QUALIFY_THRESHOLD
    DISQUALIFIED = "DISQUALIFIED"  # score < REVIEW_THRESHOLD


class Opportunity(str, Enum):
    """Estimated opportunity tier derived from available size signals."""
    UNKNOWN = "UNKNOWN"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


@dataclass
class Location:
    city: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None

    def as_text(self) -> str:
        parts = [p for p in (self.city, self.region, self.country) if p]
        return ", ".join(parts)


@dataclass
class ContactChannels:
    phone: Optional[str] = None
    email: Optional[str] = None
    contact_form_url: Optional[str] = None
    socials: list[str] = field(default_factory=list)

    def has_any(self) -> bool:
        return bool(self.phone or self.email or self.contact_form_url or self.socials)


@dataclass
class DecisionMaker:
    """Populated ONLY when legitimately available from a source. Never inferred."""
    name: str
    title: Optional[str] = None
    source: Optional[str] = None
    contact: Optional[str] = None


@dataclass
class Source:
    provider: str
    url: Optional[str] = None
    retrieved_at: Optional[str] = None


@dataclass
class SizeSignals:
    """Optional size indicators used to estimate opportunity. All optional."""
    employees: Optional[int] = None
    review_count: Optional[int] = None
    years_in_business: Optional[int] = None
    rating: Optional[float] = None


@dataclass
class Lead:
    """The output contract. See architecture.md § Data model."""
    company: str
    location: Location = field(default_factory=Location)
    website: Optional[str] = None
    service_type: list[str] = field(default_factory=list)
    contact_channels: ContactChannels = field(default_factory=ContactChannels)
    decision_makers: list[DecisionMaker] = field(default_factory=list)
    size_signals: SizeSignals = field(default_factory=SizeSignals)
    source: Optional[Source] = None
    research_notes: str = ""

    # Populated by qualify():
    qualification_score: int = 0
    score_breakdown: dict = field(default_factory=dict)
    estimated_opportunity: Opportunity = Opportunity.UNKNOWN
    estimated_opportunity_basis: str = ""
    status: Status = Status.NEW

    @property
    def id(self) -> str:
        return slugify(f"{self.company}-{self.location.city or ''}")

    def to_dict(self) -> dict:
        d = asdict(self)
        # Enums -> their string values for stable serialization.
        d["status"] = self.status.value
        d["estimated_opportunity"] = self.estimated_opportunity.value
        d["id"] = self.id
        return d


@dataclass
class Query:
    """Operator input to the pipeline."""
    market: str          # e.g. "electrical contractors"
    location: str        # e.g. "Austin, TX"
    limit: Optional[int] = None

    # Keywords that indicate the target service intent (used by scoring).
    service_keywords: tuple[str, ...] = (
        "electric", "electrical", "electrician", "wiring", "panel",
        "lighting", "solar", "generator", "ev charger",
    )


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "lead"
