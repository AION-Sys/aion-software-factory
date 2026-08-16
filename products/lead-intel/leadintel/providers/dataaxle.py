"""DataAxleProvider — DISABLED-by-default adapter for the MISSION-005 pilot.

Implements the existing `ResearchProvider` seam for Data Axle. It is **disabled by
default** and cannot acquire data until it is explicitly enabled with verified
parameters after all MISSION-005 pre-execution gates pass.

It technically enforces the CEO-ratified caps (gates 9 & 10):
  - **volume cap** (`max_records`, ratified 500) — clamps requests and responses;
  - **hard spend cap** (`spend_cap_usd`, ratified $100) — armed only when a
    **verified `cost_per_record_usd`** is supplied (gate 1: written quote);
  - **approved-market guard** — refuses any location outside Denver–Aurora–Lakewood,
    CO (no expansion beyond the approved market).

Credentials are read from a secret manager / environment variable **only** — never
hardcoded or committed (gate 8). **No live network call is possible** during pilot
preparation: `enabled` defaults to `False`, and the real transport is intentionally
unimplemented. Tests inject a mock transport, so nothing in this repository ever
calls the Data Axle API.

Field mapping is based on Data Axle's **documented** API fields (Mission 004
research) and MUST be validated against a real API response before execution — see
`missions/MISSION-005/PRE-EXECUTION-VERIFICATION.md`.
"""
from __future__ import annotations

import os
import re
from typing import Callable, Optional

from ..models import Query
from .base import RawBusiness, ResearchProvider

# NAICS for electrical contractors — the only approved vertical filter.
ELECTRICAL_CONTRACTOR_NAICS = "238210"

# Ratified pilot caps (MISSION-005). Constructor args default to these.
RATIFIED_MAX_RECORDS = 500
RATIFIED_SPEND_CAP_USD = 100.0
# Approved market: Denver–Aurora–Lakewood, CO. Matched as WHOLE TOKENS, and a
# location must contain an approved city AND the approved state — so substrings
# like "Aurora, IL", "Colorado Springs, CO", or "Concord, CA" are correctly rejected.
APPROVED_MARKET_CITIES = ("denver", "aurora", "lakewood")
APPROVED_MARKET_STATES = ("co", "colorado")


class DataAxleGateError(RuntimeError):
    """Raised when a pre-execution gate or a ratified cap would be violated."""


class DataAxleProvider(ResearchProvider):
    name = "dataaxle"
    is_synthetic = False  # real provider — output must never be labeled synthetic

    def __init__(
        self,
        *,
        enabled: bool = False,
        api_key_env: str = "DATA_AXLE_API_KEY",
        max_records: int = RATIFIED_MAX_RECORDS,
        spend_cap_usd: float = RATIFIED_SPEND_CAP_USD,
        cost_per_record_usd: Optional[float] = None,
        allowed_cities: tuple[str, ...] = APPROVED_MARKET_CITIES,
        allowed_states: tuple[str, ...] = APPROVED_MARKET_STATES,
        naics: str = ELECTRICAL_CONTRACTOR_NAICS,
        transport: Optional[Callable[[dict], list[dict]]] = None,
    ):
        self.enabled = enabled
        self.api_key_env = api_key_env
        self.max_records = max_records
        self.spend_cap_usd = spend_cap_usd
        self.cost_per_record_usd = cost_per_record_usd
        self.allowed_cities = tuple(c.lower() for c in allowed_cities)
        self.allowed_states = tuple(s.lower() for s in allowed_states)
        self.naics = naics
        self._transport = transport  # injectable; real transport is unimplemented

    @property
    def api_key(self) -> Optional[str]:
        return os.environ.get(self.api_key_env)

    @staticmethod
    def _location_tokens(location: str) -> set[str]:
        """Whole word tokens of a location string (letters only, lowercased)."""
        return {t for t in re.split(r"[^a-z]+", (location or "").lower()) if t}

    def _market_allowed(self, location: str) -> bool:
        """Require an approved city AND the approved state, matched as whole tokens.

        This rejects substring false positives such as 'Aurora, IL' (wrong state),
        'Colorado Springs, CO' (not an approved city), and 'Concord, CA' ('co' is
        only a substring of 'concord', not a token).
        """
        tokens = self._location_tokens(location)
        return bool(tokens & set(self.allowed_cities)) and bool(tokens & set(self.allowed_states))

    # ---- gate / cap enforcement -------------------------------------------
    def _preflight(self, query: Query, requested: int) -> int:
        """Enforce every gate/cap. Returns the permitted record count."""
        if not self.enabled:
            raise DataAxleGateError(
                "DataAxleProvider is disabled. Execution requires ALL MISSION-005 "
                "pre-execution gates satisfied and explicit enablement "
                "(see missions/MISSION-005/GATE-STATUS.md)."
            )
        if not self.api_key:
            raise DataAxleGateError(
                f"No credential found in ${self.api_key_env} (gate 8: secret manager "
                "only; never commit credentials)."
            )
        # Approved-market guard (no expansion beyond Denver–Aurora–Lakewood, CO).
        if not self._market_allowed(query.location):
            raise DataAxleGateError(
                f"Market '{query.location}' is outside the approved pilot market "
                "(Denver, Aurora, or Lakewood, CO). Refusing — scope guard."
            )
        # Volume cap (gate 10).
        n = requested if (requested and requested > 0) else self.max_records
        n = min(n, self.max_records)
        # Spend cap (gate 9) — requires a verified cost/record (gate 1).
        if self.cost_per_record_usd is None:
            raise DataAxleGateError(
                "No verified cost_per_record_usd (gate 1: written provider quote). "
                "Cannot arm the spend cap; refusing to acquire."
            )
        if self.cost_per_record_usd < 0:
            raise DataAxleGateError("cost_per_record_usd must be non-negative.")
        est_cost = n * self.cost_per_record_usd
        if est_cost > self.spend_cap_usd:
            affordable = int(self.spend_cap_usd // self.cost_per_record_usd)
            if affordable <= 0:
                raise DataAxleGateError(
                    "Spend cap too low for even one record at the quoted price."
                )
            n = min(n, affordable)
        return n

    def search(self, query: Query) -> list[RawBusiness]:
        n = self._preflight(query, query.limit or self.max_records)
        transport = self._transport or self._live_transport
        rows = transport(self._build_request(query, n))
        rows = rows[:n]  # hard clamp on the response as well
        return [self.parse_record(r) for r in rows]

    def _build_request(self, query: Query, n: int) -> dict:
        return {
            "naics": self.naics,
            "location": query.location,
            "limit": n,
            "api_key_env": self.api_key_env,  # name only; never the value
        }

    def _live_transport(self, request: dict) -> list[dict]:
        """Real HTTP call — intentionally NOT implemented during pilot preparation.

        It is added and security-reviewed only when every gate passes, per
        missions/MISSION-005/EXECUTION-RUNBOOK.md. No network call originates from
        this repository during the planning phase.
        """
        raise NotImplementedError(
            "Live Data Axle transport is not implemented during pilot preparation. "
            "Add it under the execution runbook after all gates pass."
        )

    @staticmethod
    def parse_record(r: dict) -> RawBusiness:
        """Map a Data Axle record to RawBusiness.

        Field names follow Data Axle's DOCUMENTED API attributes (Mission 004).
        VALIDATE against a real response before execution — do not assume.
        """
        first = (r.get("primary_contact_first_name") or "").strip()
        last = (r.get("primary_contact_last_name") or "").strip()
        title = r.get("primary_contact_job_title") or r.get("primary_contact_job_titles")
        decision_makers = []
        full_name = f"{first} {last}".strip()
        if full_name:
            decision_makers.append({
                "name": full_name,
                "title": title,
                "source": "Data Axle primary contact",
            })

        categories: list[str] = []
        naics = str(r.get("naics") or "")
        if naics.startswith(ELECTRICAL_CONTRACTOR_NAICS):
            categories.append("electrical contractor")
        for key in ("naics_description", "sic_description", "primary_sic_description"):
            desc = r.get(key)
            if desc:
                categories.append(str(desc).strip().lower())

        return RawBusiness(
            name=(r.get("name") or r.get("company_name") or "").strip(),
            website=r.get("website") or r.get("url"),
            city=r.get("city"),
            region=r.get("state") or r.get("region"),
            country=r.get("country") or "USA",
            categories=categories,
            phone=r.get("phone"),
            email=r.get("email"),
            contact_form_url=None,
            socials=[],
            employees=r.get("employees") or r.get("employee_count"),
            review_count=None,
            years_in_business=r.get("years_in_business"),
            rating=None,
            decision_makers=decision_makers,
            source_url=r.get("source_url") or r.get("record_url"),
            notes="",
        )
