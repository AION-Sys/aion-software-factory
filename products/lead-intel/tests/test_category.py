"""Category + qualification regression tests, data-driven from the labeled dataset.

Each record in synthetic_leads.json declares its expected category verdict and
whether it should qualify. This guards against regressions per category
(electrical, commercial, residential, subcontractor, solar+electrical, general
contractor, handyman, HVAC, plumber, ambiguous, incomplete-data).
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

from leadintel.enrich import enrich
from leadintel.models import Query, Status
from leadintel.normalize import normalize
from leadintel.providers.base import RawBusiness
from leadintel.scoring.config import load_config
from leadintel.scoring.engine import qualify

DATASET = Path(__file__).resolve().parents[1] / "data" / "fixtures" / "synthetic_leads.json"
QUERY = Query(market="electrical contractors", location="CO")
CONFIG = load_config()


def _records():
    payload = json.loads(DATASET.read_text(encoding="utf-8"))
    return payload["businesses"]


def _lead_from(record: dict):
    raw = RawBusiness(
        name=record["name"], website=record.get("website"),
        city=record.get("city"), region=record.get("region"), country=record.get("country"),
        categories=list(record.get("categories", [])),
        phone=record.get("phone"), email=record.get("email"),
        contact_form_url=record.get("contact_form_url"), socials=list(record.get("socials", [])),
        employees=record.get("employees"), review_count=record.get("review_count"),
        years_in_business=record.get("years_in_business"), rating=record.get("rating"),
        decision_makers=list(record.get("decision_makers", [])),
        source_url=record.get("source_url"), notes=record.get("notes", ""),
    )
    lead = enrich(normalize(raw, "fixture", is_synthetic=True))
    qualify(lead, QUERY, CONFIG)
    return lead


class TestCategoryRegression(unittest.TestCase):
    def test_dataset_present_and_labeled(self):
        recs = _records()
        self.assertGreaterEqual(len(recs), 20)
        for r in recs:
            self.assertIn("ground_truth", r, r["name"])
            gt = r["ground_truth"]
            self.assertIn("expected_category", gt)
            self.assertIn("is_target", gt)
            self.assertIn("expected_qualified", gt)

    def test_expected_category_per_record(self):
        for r in _records():
            lead = _lead_from(r)
            self.assertEqual(
                lead.category_verdict.value, r["ground_truth"]["expected_category"],
                f"{r['name']}: category mismatch",
            )

    def test_expected_qualification_per_record(self):
        for r in _records():
            lead = _lead_from(r)
            expected_qualified = r["ground_truth"]["expected_qualified"]
            got_qualified = lead.status == Status.QUALIFIED
            self.assertEqual(
                got_qualified, expected_qualified,
                f"{r['name']}: expected_qualified={expected_qualified} but status={lead.status.value}",
            )

    def test_no_non_electrical_is_ever_qualified(self):
        for r in _records():
            lead = _lead_from(r)
            if lead.category_verdict.value == "NON_ELECTRICAL":
                self.assertNotEqual(lead.status, Status.QUALIFIED, r["name"])

    def test_all_synthetic_flagged(self):
        for r in _records():
            self.assertTrue(_lead_from(r).is_synthetic, r["name"])


if __name__ == "__main__":
    unittest.main()
