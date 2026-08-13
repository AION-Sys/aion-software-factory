"""ScoringConfig — explicit, configurable scoring rules loaded from JSON.

Keeping the model in data (not code) makes it configurable and auditable: an
operator can adjust weights, thresholds, and keyword lists without touching the
engine. The engine reads only this config.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent / "default_config.json"


@dataclass
class ScoringConfig:
    version: str
    thresholds: dict            # {"qualified": int, "review": int}
    category_keywords: dict     # {"core_electrical": [...], "adjacent": [...], ...}
    positive_signals: dict      # {name: {"points": int, "reason": str}}
    negative_signals: dict      # {name: {"points": int, "reason": str}}
    maturity_scale: dict        # size-signal thresholds
    description: str = ""

    # ---- convenience accessors -------------------------------------------------
    def pos(self, name: str) -> tuple[int, str]:
        s = self.positive_signals[name]
        return int(s["points"]), s.get("reason", name)

    def neg(self, name: str) -> tuple[int, str]:
        s = self.negative_signals[name]
        return int(s["points"]), s.get("reason", name)

    def keywords(self, group: str) -> list[str]:
        return [k.lower() for k in self.category_keywords.get(group, [])]

    @property
    def qualified_threshold(self) -> int:
        return int(self.thresholds["qualified"])

    @property
    def review_threshold(self) -> int:
        return int(self.thresholds["review"])

    def validate(self) -> list[str]:
        """Return a list of config problems (empty = valid)."""
        problems: list[str] = []
        if self.review_threshold >= self.qualified_threshold:
            problems.append("review threshold must be < qualified threshold")
        max_positive = sum(
            s["points"] for k, s in self.positive_signals.items()
            if k != "service_area_match_partial"  # partial is an alternative to full
        )
        if max_positive < self.qualified_threshold:
            problems.append(
                f"max positive score ({max_positive}) < qualified threshold "
                f"({self.qualified_threshold}); nothing could ever qualify"
            )
        for group in ("core_electrical", "adjacent", "exclusion_trades"):
            if not self.category_keywords.get(group):
                problems.append(f"category_keywords.{group} is empty")
        return problems


def load_config(path: Optional[Path | str] = None) -> ScoringConfig:
    path = Path(path) if path else DEFAULT_CONFIG_PATH
    with open(path, "r", encoding="utf-8") as fh:
        raw = json.load(fh)
    config = ScoringConfig(
        version=raw["version"],
        thresholds=raw["thresholds"],
        category_keywords=raw["category_keywords"],
        positive_signals=raw["positive_signals"],
        negative_signals=raw["negative_signals"],
        maturity_scale=raw["maturity_scale"],
        description=raw.get("description", ""),
    )
    problems = config.validate()
    if problems:
        raise ValueError(f"Invalid scoring config at {path}: {problems}")
    return config
