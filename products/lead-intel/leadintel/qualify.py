"""Backward-compatible entry point for qualification.

The real implementation now lives in the provider-independent, config-driven
`leadintel.scoring` engine (MISSION-003, ADR-0006). This module preserves the
`qualify(lead, query)` call site and exposes the active thresholds.
"""
from __future__ import annotations

from .scoring.config import load_config
from .scoring.engine import qualify  # noqa: F401 (re-exported)

_DEFAULT = load_config()
QUALIFY_THRESHOLD = _DEFAULT.qualified_threshold
REVIEW_THRESHOLD = _DEFAULT.review_threshold

__all__ = ["qualify", "QUALIFY_THRESHOLD", "REVIEW_THRESHOLD"]
