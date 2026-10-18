"""Regression tests for the read-only five-system cutover gate."""
import tempfile
import unittest
from pathlib import Path
from scripts.five_system_cutover_readiness import CATEGORIES, REQUIRED, inspect

class CutoverReadinessTests(unittest.TestCase):
    def test_repository_never_auto_approves_migration(self):
        result = inspect()
        self.assertFalse(result["cutover_allowed"])
        self.assertFalse(result["migration_approved"])
        self.assertFalse(result["legacy_workflows_retirement_allowed"])
        self.assertEqual(result["mode"], "READ_ONLY_SHADOW")
        self.assertTrue(set(REQUIRED).issubset(result["blockers"]))

    def test_missing_category_fails_static_check_without_approval(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            result = inspect(root)
            self.assertFalse(result["static_checks"]["FIVE_WORKFLOW_FILES_PRESENT"])
            self.assertIn("FIVE_WORKFLOW_FILES_PRESENT", result["blockers"])
            self.assertFalse(result["cutover_allowed"])

    def test_all_five_category_workflows_exist(self):
        result = inspect()
        self.assertEqual(set(result["category_files"]), set(CATEGORIES))
        self.assertTrue(all(result["category_files"].values()))

if __name__ == "__main__":
    unittest.main()
