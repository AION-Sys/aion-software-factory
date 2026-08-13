"""Configurable, explainable qualification scoring engine.

The qualification engine is INDEPENDENT of any data provider: it consumes an
enriched `Lead` and a `ScoringConfig`, and produces a category verdict, an
explainable 0-100 score, an opportunity tier, and a status.
"""
from .config import ScoringConfig, load_config, DEFAULT_CONFIG_PATH
from .engine import qualify, classify_category, score_lead

__all__ = [
    "ScoringConfig", "load_config", "DEFAULT_CONFIG_PATH",
    "qualify", "classify_category", "score_lead",
]
