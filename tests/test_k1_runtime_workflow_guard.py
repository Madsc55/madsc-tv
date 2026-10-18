"""Prevent regression of K1 runtime protected-file safeguards."""
from pathlib import Path
import unittest

WORKFLOW = Path(".github/workflows/k1-protected-write-tests.yml")


class K1RuntimeWorkflowGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = WORKFLOW.read_text(encoding="utf-8")

    def test_snapshot_before_test_execution(self):
        text = self.workflow
        self.assertIn("--mode snapshot --manifest", text)
        self.assertLess(text.index("--mode snapshot --manifest"),
                        text.index("Kanal listelerine dokunmadan guvenlik negatif testleri"))

    def test_check_always_runs_after_inventory(self):
        text = self.workflow
        self.assertIn("K1 korunan dosya calisma sonu butunluk kontrolu\n        if: always()", text)
        self.assertIn("--mode check --manifest", text)
        self.assertLess(text.index("Tum workflow risk envanterini olustur"),
                        text.index("K1 korunan dosya calisma sonu butunluk kontrolu"))

    def test_manifest_is_shared_between_snapshot_and_check(self):
        self.assertEqual(self.workflow.count('"${RUNNER_TEMP}/k1-protected-snapshot.json"'), 2)

    def test_branch_drift_still_recorded(self):
        text = self.workflow
        self.assertIn("k1-protected-diff.log", text)
        self.assertIn("name: k1-protected-diff", text)
        self.assertIn('test "${PIPESTATUS[0]}" -eq 1', text)


if __name__ == "__main__":
    unittest.main()
