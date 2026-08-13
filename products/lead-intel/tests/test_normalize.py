import unittest

from leadintel.normalize import normalize
from leadintel.providers.base import RawBusiness


class TestNormalize(unittest.TestCase):
    def test_trims_and_lowercases_categories(self):
        nb = normalize(RawBusiness(name="  Ace Electric ", categories=["  Electrical Contractor "]),
                       "fixture", is_synthetic=True)
        self.assertEqual(nb.company, "Ace Electric")
        self.assertEqual(nb.categories, ["electrical contractor"])

    def test_blank_strings_become_none(self):
        nb = normalize(RawBusiness(name="X", website="   ", phone=""), "fixture")
        self.assertIsNone(nb.website)
        self.assertIsNone(nb.contact_channels.phone)

    def test_source_records_provider_and_synthetic_flag(self):
        nb = normalize(RawBusiness(name="X", source_url="https://example.com/x"),
                       "fixture", is_synthetic=True)
        self.assertEqual(nb.source.provider, "fixture")
        self.assertTrue(nb.source.is_synthetic)
        self.assertEqual(nb.source.url, "https://example.com/x")

    def test_real_provider_not_flagged_synthetic(self):
        nb = normalize(RawBusiness(name="X"), "live", is_synthetic=False)
        self.assertFalse(nb.source.is_synthetic)


if __name__ == "__main__":
    unittest.main()
