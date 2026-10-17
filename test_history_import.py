import unittest
import os
from comparison_history import save_comparison, load_history, clear_history, HISTORY_FILE


class TestComparisonHistoryModule(unittest.TestCase):
    def setUp(self):
        clear_history()

    def tearDown(self):
        clear_history()

    def test_imports_exist(self):
        self.assertTrue(callable(save_comparison))
        self.assertTrue(callable(load_history))
        self.assertTrue(callable(clear_history))

    def test_save_and_load_workflow(self):
        # 1. Initial history should be empty
        records = load_history()
        self.assertEqual(len(records), 0)

        # 2. Save comparison
        save_comparison(
            "ref_signature.png",
            "test_signature.png",
            92.456,
            "Very High Similarity"
        )

        # 3. Load history
        records = load_history()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["Reference Signature"], "ref_signature.png")
        self.assertEqual(records[0]["Test Signature"], "test_signature.png")
        self.assertEqual(records[0]["Similarity Percentage"], "92.46")
        self.assertEqual(records[0]["Similarity Level"], "Very High Similarity")

        # 4. Clear history
        clear_history()
        self.assertEqual(len(load_history()), 0)


if __name__ == "__main__":
    unittest.main()
