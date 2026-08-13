"""LiveProvider — DISABLED seam for real data acquisition.

Enabling real/paid data acquisition is a YELLOW gate (see
docs/operations/approval-policy.md and ADR-0005). This class defines the
interface only. It reads its API key from an environment variable — never a
hardcoded secret — and refuses to run until explicitly enabled by a human.

To implement in a future, approved mission:
  1. Obtain human (CEO) approval for the paid provider + budget.
  2. Provide credentials via the env var named by ``api_key_env`` (never commit them).
  3. Implement ``search`` against the approved provider, respecting its Terms of
     Service and robots directives, capturing only legitimately-available
     business information (no PII fabrication).
  4. Pass an AION-SECURITY review before enablement.
"""
from __future__ import annotations

import os
from typing import Optional

from ..models import Query
from .base import RawBusiness, ResearchProvider


class LiveProviderNotEnabled(RuntimeError):
    """Raised when the live provider is used without explicit approval/credentials."""


class LiveProvider(ResearchProvider):
    name = "live"

    def __init__(self, api_key_env: str = "LEAD_INTEL_PROVIDER_API_KEY", enabled: bool = False):
        self.api_key_env = api_key_env
        self.enabled = enabled

    @property
    def api_key(self) -> Optional[str]:
        return os.environ.get(self.api_key_env)

    def search(self, query: Query) -> list[RawBusiness]:
        if not self.enabled:
            raise LiveProviderNotEnabled(
                "LiveProvider is disabled. Enabling real data acquisition is a "
                "YELLOW gate requiring human approval and a security review "
                "(see docs/operations/approval-policy.md, ADR-0005)."
            )
        if not self.api_key:
            raise LiveProviderNotEnabled(
                f"No API key found in ${self.api_key_env}. Provide credentials via "
                "environment only; never hardcode or commit secrets."
            )
        # Intentionally unimplemented in V1 — real acquisition is a future mission.
        raise NotImplementedError(
            "Live acquisition is not implemented in MISSION-002 V1. Implement in an "
            "approved future mission against the chosen provider."
        )
