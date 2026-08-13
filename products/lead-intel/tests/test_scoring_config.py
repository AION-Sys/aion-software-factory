import json
import tempfile
import unittest
from pathlib import Path

from leadintel.models import CategoryVerdict, Status
from leadintel.scoring.config import DEFAULT_CONFIG_PATH, load_config
from tests.helpers import make_lead


class TestScoringConfig(unittest.TestCase):
    def test_default_config_loads_and_validates(self):
        config = load_config()
        self.assertTrue(config.version)
        self.assertEqual(config.validate(), [])
        self.assertLess(config.review_threshold, config.qualified_threshold)

    def test_invalid_config_rejected(self):
        bad = json.loads(DEFAULT_CONFIG_PATH.read_text(encoding="utf-8"))
        bad["thresholds"] = {"qualified": 40, "review": 60}  # inverted
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "bad.json"
            p.write_text(json.dumps(bad), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_config(p)

    def test_config_is_configurable_thresholds_change_outcome(self):
        """Raising the qualified threshold should demote a borderline lead."""
        base = json.loads(DEFAULT_CONFIG_PATH.read_text(encoding="utf-8"))
        strict = dict(base)
        strict["thresholds"] = {"qualified": 95, "review": 40}
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "strict.json"
            p.write_text(json.dumps(strict), encoding="utf-8")
            strict_cfg = load_config(p)

        kw = dict(name="Aurora Residential Electricians", website="https://example.com/a",
                  city="Denver", region="CO", categories=["residential electrical", "electrician"],
                  phone="+1-303-555-0007", review_count=60, years_in_business=8)
        default_lead = make_lead(**kw)
        strict_lead = make_lead(qualify_it=False, **kw)
        from leadintel.scoring.engine import qualify
        from tests.helpers import DEFAULT_QUERY
        qualify(strict_lead, DEFAULT_QUERY, strict_cfg)

        self.assertEqual(default_lead.category_verdict, CategoryVerdict.ELECTRICAL)
        self.assertEqual(default_lead.status, Status.QUALIFIED)
        self.assertNotEqual(strict_lead.status, Status.QUALIFIED)  # demoted by stricter config
        self.assertEqual(strict_lead.scoring_config_version, strict_cfg.version)

    def test_config_version_recorded_on_lead(self):
        lead = make_lead(name="Denver Electric", website="https://example.com/e",
                         city="Denver", region="CO", categories=["electrical contractor"],
                         phone="+1-303-555-0008")
        self.assertEqual(lead.scoring_config_version, load_config().version)


if __name__ == "__main__":
    unittest.main()
