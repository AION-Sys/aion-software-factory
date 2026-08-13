"""Qualification engine — provider-independent, config-driven, explainable.

Pipeline position: (enriched) Lead + ScoringConfig -> category verdict + score +
opportunity + status, with a per-signal explanation of WHY.

Two-part model (see ADR-0006):
  1. Category validation (the gate): classify the business as ELECTRICAL,
     ADJACENT, NON_ELECTRICAL, or AMBIGUOUS from its categories + name.
  2. Weighted, explainable scoring: positive signals add, negative signals
     subtract. The category verdict caps the achievable status so non-electrical
     businesses (e.g., handymen) cannot qualify regardless of other strengths.
"""
from __future__ import annotations

from typing import Optional

from ..models import (
    CategoryVerdict,
    Lead,
    Opportunity,
    Query,
    ScoreContribution,
    Status,
)
from .config import ScoringConfig, load_config


def _text_of(lead: Lead) -> str:
    return " ".join([*(c.lower() for c in lead.service_type), lead.company.lower()])


def _any_kw(text: str, keywords: list[str]) -> list[str]:
    return [kw for kw in keywords if kw in text]


def classify_category(lead: Lead, config: ScoringConfig) -> tuple[CategoryVerdict, str]:
    """Classify the business. Returns (verdict, human-readable reason)."""
    text = _text_of(lead)
    core = _any_kw(text, config.keywords("core_electrical"))
    adjacent = _any_kw(text, config.keywords("adjacent"))
    exclusion = _any_kw(text, config.keywords("exclusion_trades"))

    if core:
        reason = f"Electrical specialization found: {', '.join(sorted(set(core)))}."
        if exclusion:
            reason += f" (Also lists non-electrical trades: {', '.join(sorted(set(exclusion)))}.)"
        return CategoryVerdict.ELECTRICAL, reason
    if exclusion:
        return (
            CategoryVerdict.NON_ELECTRICAL,
            f"Non-electrical trade with no electrical specialization: "
            f"{', '.join(sorted(set(exclusion)))}.",
        )
    if adjacent:
        return (
            CategoryVerdict.ADJACENT,
            f"Adjacent services only (no core electrical category): "
            f"{', '.join(sorted(set(adjacent)))}.",
        )
    return (
        CategoryVerdict.AMBIGUOUS,
        "No electrical, adjacent, or exclusion signals found; category unclear.",
    )


def _opportunity(lead: Lead, config: ScoringConfig) -> tuple[int, Opportunity, str]:
    """(maturity_points, opportunity_tier, basis) from available size signals."""
    s = lead.size_signals
    scale = config.maturity_scale
    parts: list[str] = []
    strength = 0.0
    count = 0

    def rate(value, key):
        nonlocal strength, count
        if value is None:
            return
        count += 1
        hi = scale[key]["high"]
        mid = scale[key]["medium"]
        if value >= hi:
            strength += 1.0
        elif value >= mid:
            strength += 0.6
        else:
            strength += 0.2

    rate(s.employees, "employees")
    if s.employees is not None:
        parts.append(f"{s.employees} employees")
    rate(s.review_count, "review_count")
    if s.review_count is not None:
        parts.append(f"{s.review_count} reviews")
    rate(s.years_in_business, "years_in_business")
    if s.years_in_business is not None:
        parts.append(f"{s.years_in_business}y in business")

    max_points, _ = config.pos("business_maturity")
    if count == 0:
        return 0, Opportunity.UNKNOWN, "No size signals available."
    normalized = strength / count
    points = round(max_points * normalized)
    if normalized >= 0.75:
        tier = Opportunity.HIGH
    elif normalized >= 0.45:
        tier = Opportunity.MEDIUM
    else:
        tier = Opportunity.LOW
    return points, tier, f"{tier.value} from " + ", ".join(parts)


def score_lead(
    lead: Lead, query: Query, config: ScoringConfig, verdict: CategoryVerdict
) -> list[ScoreContribution]:
    """Compute explainable contributions. Does not set status (see determine_status)."""
    text = _text_of(lead)
    contribs: list[ScoreContribution] = []

    def add_pos(name: str, condition: bool, override_reason: Optional[str] = None):
        if condition:
            pts, reason = config.pos(name)
            contribs.append(ScoreContribution(name, pts, "positive", override_reason or reason))

    def add_neg(name: str, condition: bool, override_reason: Optional[str] = None):
        if condition:
            pts, reason = config.neg(name)
            contribs.append(ScoreContribution(name, pts, "negative", override_reason or reason))

    # --- Positive signals ---
    add_pos("core_electrical_category", verdict == CategoryVerdict.ELECTRICAL)
    add_pos("commercial_electrical",
            any(k in text for k in ("commercial electrical", "industrial electrical")))
    add_pos("established_website", bool(lead.website))
    # Location match (full vs partial):
    loc_points = _location_points(lead, query)
    if loc_points == "full":
        add_pos("service_area_match_full", True)
    elif loc_points == "partial":
        add_pos("service_area_match_partial", True)
    add_pos("contactable", lead.contact_channels.has_any())
    # Business maturity (variable points):
    maturity_pts, _tier, _basis = _opportunity(lead, config)
    if maturity_pts > 0:
        _, reason = config.pos("business_maturity")
        contribs.append(ScoreContribution("business_maturity", maturity_pts, "positive", reason))
    add_pos("decision_maker_identified", bool(lead.decision_makers))
    add_pos("relevant_indicators",
            bool(_any_kw(text, config.keywords("supporting_indicators")))
            or bool(_any_kw(text, config.keywords("adjacent"))))

    # --- Negative signals ---
    add_neg("non_electrical_trade", verdict == CategoryVerdict.NON_ELECTRICAL)
    add_neg("adjacent_only", verdict == CategoryVerdict.ADJACENT)
    no_evidence = (not lead.website and not lead.contact_channels.has_any()
                   and not lead.size_signals.any_present())
    add_neg("insufficient_evidence", no_evidence)
    add_neg("ambiguous_no_evidence", verdict == CategoryVerdict.AMBIGUOUS)

    return contribs


def _location_points(lead: Lead, query: Query) -> str:
    tokens = [t for t in query.location.lower().replace(",", " ").split() if len(t) > 1]
    hay = " ".join(
        v for v in (lead.location.city, lead.location.region, lead.location.country) if v
    ).lower()
    if not tokens or not hay:
        return "none"
    matched = [t for t in tokens if t in hay]
    if not matched:
        return "none"
    return "full" if len(matched) == len(tokens) else "partial"


def determine_status(score: int, verdict: CategoryVerdict, config: ScoringConfig) -> Status:
    """Category verdict gates the achievable status; score decides within the gate."""
    if verdict == CategoryVerdict.NON_ELECTRICAL:
        return Status.DISQUALIFIED  # hard gate: never qualify a non-electrical trade
    if verdict == CategoryVerdict.AMBIGUOUS:
        return Status.NEEDS_REVIEW if score >= config.review_threshold else Status.DISQUALIFIED
    if verdict == CategoryVerdict.ADJACENT:
        # Related but unconfirmed: cannot fully qualify without a core electrical category.
        return Status.NEEDS_REVIEW if score >= config.review_threshold else Status.DISQUALIFIED
    # ELECTRICAL:
    if score >= config.qualified_threshold:
        return Status.QUALIFIED
    if score >= config.review_threshold:
        return Status.NEEDS_REVIEW
    return Status.DISQUALIFIED


def qualify(lead: Lead, query: Query, config: Optional[ScoringConfig] = None) -> Lead:
    """Run category validation + scoring + status onto the lead, in place."""
    config = config or load_config()

    verdict, reason = classify_category(lead, config)
    contribs = score_lead(lead, query, config, verdict)
    score = max(0, min(100, sum(c.points for c in contribs)))
    _, tier, basis = _opportunity(lead, config)

    lead.category_verdict = verdict
    lead.category_reason = reason
    lead.score_contributions = contribs
    lead.score_breakdown = {c.signal: c.points for c in contribs}
    lead.qualification_score = score
    lead.estimated_opportunity = tier
    lead.estimated_opportunity_basis = basis
    lead.status = determine_status(score, verdict, config)
    lead.scoring_config_version = config.version
    return lead
