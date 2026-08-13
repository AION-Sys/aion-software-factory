"""Canonical data models for the lead-intelligence pipeline.

Design rules:
- Absence is represented explicitly (None / empty). Nothing here fabricates data.
- Synthetic data is labeled end-to-end (`is_synthetic`) and never treated as
  real-world evidence (MISSION-003).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional


class Status(str, Enum):
    """Lifecycle/qualification status of a lead."""
    NEW = "NEW"                    # pre-scoring
    QUALIFIED = "QUALIFIED"        # electrical + score >= qualified threshold
    NEEDS_REVIEW = "NEEDS_REVIEW"  # review threshold <= score < qualified, or capped
    DISQUALIFIED = "DISQUALIFIED"  # below review threshold, or category-gated out


class Opportunity(str, Enum):
    """Estimated opportunity tier derived from available size signals."""
    UNKNOWN = "UNKNOWN"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class CategoryVerdict(str, Enum):
    """Result of category validation — the qualification gate (MISSION-003)."""
    ELECTRICAL = "ELECTRICAL"          # confirmed electrical specialization
    ADJACENT = "ADJACENT"              # related (solar/lighting) but no core electrical
    NON_ELECTRICAL = "NON_ELECTRICAL"  # a different trade (handyman/plumber/HVAC/GC)
    AMBIGUOUS = "AMBIGUOUS"            # insufficient evidence to classify


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
    is_synthetic: bool = False  # True when produced from a fixture/synthetic provider


@dataclass
class SizeSignals:
    """Optional size indicators used to estimate opportunity. All optional."""
    employees: Optional[int] = None
    review_count: Optional[int] = None
    years_in_business: Optional[int] = None
    rating: Optional[float] = None

    def any_present(self) -> bool:
        return any(v is not None for v in (self.employees, self.review_count,
                                           self.years_in_business, self.rating))


@dataclass
class ScoreContribution:
    """One explainable line item in a lead's score (positive or negative)."""
    signal: str
    points: int
    kind: str          # "positive" | "negative"
    reason: str

    def to_dict(self) -> dict:
        return {"signal": self.signal, "points": self.points,
                "kind": self.kind, "reason": self.reason}


@dataclass
class NormalizedBusiness:
    """Output of the Normalizer stage: cleaned, standardized, still unscored.

    This is the provider-independent representation the enrichment and
    qualification stages consume — no provider-specific shapes leak past here.
    """
    company: str
    location: Location = field(default_factory=Location)
    website: Optional[str] = None
    categories: list[str] = field(default_factory=list)          # cleaned, lowercased
    contact_channels: ContactChannels = field(default_factory=ContactChannels)
    decision_makers: list[DecisionMaker] = field(default_factory=list)
    size_signals: SizeSignals = field(default_factory=SizeSignals)
    source: Optional[Source] = None
    provider_notes: str = ""


@dataclass
class Lead:
    """The output contract (the Lead Record)."""
    company: str
    location: Location = field(default_factory=Location)
    website: Optional[str] = None
    service_type: list[str] = field(default_factory=list)
    contact_channels: ContactChannels = field(default_factory=ContactChannels)
    decision_makers: list[DecisionMaker] = field(default_factory=list)
    size_signals: SizeSignals = field(default_factory=SizeSignals)
    source: Optional[Source] = None
    research_notes: str = ""

    # Enrichment-derived:
    data_completeness: float = 0.0     # 0..1 fraction of key fields present
    provenance_complete: bool = False  # source provider+url+retrieved_at present

    # Qualification-engine-derived:
    category_verdict: CategoryVerdict = CategoryVerdict.AMBIGUOUS
    category_reason: str = ""
    qualification_score: int = 0
    score_breakdown: dict = field(default_factory=dict)          # {signal: points}
    score_contributions: list = field(default_factory=list)      # [ScoreContribution]
    estimated_opportunity: Opportunity = Opportunity.UNKNOWN
    estimated_opportunity_basis: str = ""
    status: Status = Status.NEW
    scoring_config_version: str = ""

    @property
    def id(self) -> str:
        return slugify(f"{self.company}-{self.location.city or ''}")

    @property
    def is_synthetic(self) -> bool:
        return bool(self.source and self.source.is_synthetic)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["status"] = self.status.value
        d["estimated_opportunity"] = self.estimated_opportunity.value
        d["category_verdict"] = self.category_verdict.value
        d["score_contributions"] = [
            c.to_dict() if isinstance(c, ScoreContribution) else c
            for c in self.score_contributions
        ]
        d["id"] = self.id
        d["is_synthetic"] = self.is_synthetic
        return d


@dataclass
class Query:
    """Operator input to the pipeline."""
    market: str          # e.g. "electrical contractors"
    location: str        # e.g. "Austin, TX"
    limit: Optional[int] = None


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "lead"
