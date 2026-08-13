import unittest

from leadintel.metrics import compute_metrics


class TestMetrics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = compute_metrics()

    def test_metrics_shape(self):
        for key in ("qualification_precision", "recall", "false_positive_rate",
                    "false_negative_rate", "category_accuracy",
                    "average_data_completeness", "provenance_completeness_rate",
                    "confusion_matrix"):
            self.assertIn(key, self.m)

    def test_no_false_positives_on_synthetic_baseline(self):
        # The category gate must keep non-electrical trades out of QUALIFIED.
        self.assertEqual(self.m["confusion_matrix"]["fp"], 0)
        self.assertEqual(self.m["false_positive_rate"], 0.0)

    def test_precision_is_high(self):
        self.assertGreaterEqual(self.m["qualification_precision"], 0.9)

    def test_category_accuracy_perfect_on_labeled_set(self):
        self.assertEqual(self.m["category_accuracy"], 1.0)

    def test_expected_behavior_accuracy_perfect(self):
        self.assertEqual(self.m["expected_behavior_accuracy"], 1.0)
        self.assertEqual(self.m["mismatches"], [])

    def test_provenance_complete(self):
        self.assertEqual(self.m["provenance_completeness_rate"], 1.0)

    def test_disclaimer_marks_synthetic(self):
        self.assertIn("SYNTHETIC", self.m["_disclaimer"])


if __name__ == "__main__":
    unittest.main()
