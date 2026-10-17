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

    def test_actions_api_get_reports_are_read_only(self):
        for command in (
            'gh api "repos/${GITHUB_REPOSITORY}/actions/runs?per_page=100" --jq ".workflow_runs"',
            'gh api --paginate "repos/${GITHUB_REPOSITORY}/actions/workflows?per_page=100" --jq ".workflows"',
        ):
            with self.subTest(command=command):
                record = self.inspect_text(
                    "permissions:\n  contents: read\nsteps:\n  - run: " + command + "\n"
                    + "  - run: cat CALISANLAR.m3u\n"
                )
                self.assertFalse(record["write_command_signal"])
                self.assertEqual(record["tier"], "LOW_STATIC_SIGNAL")

    def test_actions_api_mutations_remain_write_signals(self):
        commands = (
            'gh api -X POST "repos/${GITHUB_REPOSITORY}/actions/runs"',
            'gh api --method PATCH "repos/${GITHUB_REPOSITORY}/actions/runs"',
            'gh api -f value=1 "repos/${GITHUB_REPOSITORY}/actions/runs"',
            'gh api --input payload.json "repos/${GITHUB_REPOSITORY}/actions/runs"',
            'gh api graphql -f query=mutation',
            'gh api repos/${GITHUB_REPOSITORY}/dispatches',
        )
        for command in commands:
            with self.subTest(command=command):
                record = self.inspect_text(
                    "permissions:\n  contents: read\nsteps:\n  - run: " + command + "\n"
                    + "  - run: cat CALISANLAR.m3u\n"
                )
                self.assertTrue(record["write_command_signal"])
                self.assertEqual(record["tier"], "HIGH_WRITE_OR_TRIGGER")

    def test_read_only_workflow_not_flagged(self):
        record = self.inspect_text("permissions:\n  contents: read\nsteps:\n  - run: echo safe\n")
        self.assertEqual(record["git_push_count"], 0)
        self.assertEqual(record["force_push_count"], 0)
        self.assertFalse(record["multiple_push_signal"])

if __name__ == "__main__":
    unittest.main()
