"""Regression tests for read-only workflow push risk inventory."""
import tempfile
import unittest
from pathlib import Path
from scripts.k1_workflow_risk_inventory import inspect

class WorkflowRiskInventoryTests(unittest.TestCase):
    def inspect_text(self, content):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(dir=root / ".github" / "workflows") as tmp:
            p = Path(tmp) / "fixture.yml"
            p.write_text(content, encoding="utf-8")
            return inspect(p)

    def test_force_push_with_git_config_is_detected(self):
        record = self.inspect_text("steps:\n  - run: git -c user.name=bot push --force origin HEAD\n")
        self.assertEqual(record["git_push_count"], 1)
        self.assertEqual(record["force_push_count"], 1)
        self.assertEqual(record["tier"], "CRITICAL_UNGATED_PUSH")

    def test_two_push_commands_flagged(self):
        record = self.inspect_text("steps:\n  - run: git push origin HEAD\n  - run: git push origin HEAD\n")
        self.assertEqual(record["git_push_count"], 2)
        self.assertTrue(record["multiple_push_signal"])

    def test_read_only_workflow_not_flagged(self):
        record = self.inspect_text("permissions:\n  contents: read\nsteps:\n  - run: echo safe\n")
        self.assertEqual(record["git_push_count"], 0)
        self.assertEqual(record["force_push_count"], 0)
        self.assertFalse(record["multiple_push_signal"])

if __name__ == "__main__":
    unittest.main()
