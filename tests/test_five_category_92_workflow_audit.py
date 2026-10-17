"""Behavioral regression for central cron extraction; never edits project files."""
import tempfile
import unittest
from pathlib import Path

from scripts.five_category_92_workflow_audit import inspect


class CentralCronRegressionTests(unittest.TestCase):
    def test_write_side_effects_without_explicit_permissions_are_reviewed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            (workflows / "legacy-api-push.yml").write_text(
                "name: API push\non:\n  push:\njobs:\n  write:\n    steps:\n"
                "      - run: |\n          git push origin HEAD:main\n"
                "          gh api repos/owner/repo/actions/workflows/test.yml/dispatches -X POST\n",
                encoding="utf-8",
            )
            for number in range(91):
                (workflows / f"legacy-filler-{number:02d}.yml").write_text(
                    f"name: Filler {number}\non:\n  workflow_dispatch:\njobs: {{}}\n",
                    encoding="utf-8",
                )
            report = inspect(root)
            item = next(x for x in report["items"] if x["file"] == "legacy-api-push.yml")
            self.assertTrue(item["write_permission_parity_unverified"])
            self.assertEqual(item["review_priority"], "HIGH")
            self.assertIn("WRITE_SIDE_EFFECTS_UNVERIFIED", item["migration_gap_reasons"])
            self.assertIn("VERIFY_API_DISPATCH_TARGET_AND_IDEMPOTENCY", item["required_acceptance_checks"])

    def test_exact_schedule_match_and_unmatched_schedule(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            (workflows / "legacy-matched.yml").write_text(
                "name: Matched\non:\n  schedule:\n    - cron: '15 4 * * *'\njobs:\n  check:\n    steps:\n      - run: python3 scripts/cron_shared.py\n",
                encoding="utf-8",
            )
            (workflows / "legacy-unmatched.yml").write_text(
                'name: Unmatched\non:\n  schedule:\n    - cron: "30 7 * * 1"\njobs: {}\n',
                encoding="utf-8",
            )
            (workflows / "madsc-05-genel-bakim.yml").write_text(
                "name: Central\non:\n  schedule:\n    - cron: '15 4 * * *'\njobs: {}\n",
                encoding="utf-8",
            )
            # Cron coverage requires a shared script linking legacy and central jobs.
            (workflows / "madsc-02-kesif.yml").write_text(
                "name: Discovery\non:\n  schedule:\n    - cron: '15 4 * * *'\njobs:\n  check:\n    steps:\n      - run: python3 scripts/cron_shared.py\n",
                encoding="utf-8",
            )
            # The inventory enforces 92 legacy workflows, including in fixtures.
            for number in range(90):
                (workflows / f"legacy-filler-{number:02d}.yml").write_text(
                    f"name: Filler {number}\non:\n  workflow_dispatch:\njobs: {{}}\n",
                    encoding="utf-8",
                )
            report = inspect(root)
            items = {row["file"]: row for row in report["items"]}
            self.assertEqual(report["total"], 92)
            self.assertIn("madsc-02-kesif.yml", items["legacy-matched.yml"]["possible_replacement_workflows"])
            self.assertEqual(items["legacy-matched.yml"]["unmatched_cron_expressions"], [])
            self.assertEqual(
                items["legacy-unmatched.yml"]["unmatched_cron_expressions"],
                ["30 7 * * 1"],
            )
            self.assertFalse(items["legacy-matched.yml"]["behavioral_parity_verified"])
            self.assertFalse(items["legacy-unmatched.yml"]["behavioral_parity_verified"])


if __name__ == "__main__":
    unittest.main()
