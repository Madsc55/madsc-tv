"""Behavioral regression for central cron extraction; never edits project files."""
import tempfile
import unittest
from pathlib import Path

from scripts.five_category_92_workflow_audit import inspect


class CentralCronRegressionTests(unittest.TestCase):
    def test_exact_schedule_match_and_unmatched_schedule(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            (workflows / "legacy-matched.yml").write_text(
                "name: Matched\non:\n  schedule:\n    - cron: '15 4 * * *'\njobs: {}\n",
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
            # A matching cron in another central category must count as covered.
            (workflows / "madsc-02-kesif.yml").write_text(
                "name: Discovery\\non:\\n  schedule:\\n    - cron: '15 4 * * *'\\njobs: {}\\n".replace("\\n", "\n"),
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
            self.assertEqual(items["legacy-matched.yml"]["unmatched_cron_expressions"], [])
            self.assertEqual(
                items["legacy-unmatched.yml"]["unmatched_cron_expressions"],
                ["30 7 * * 1"],
            )
            self.assertFalse(items["legacy-matched.yml"]["behavioral_parity_verified"])
            self.assertFalse(items["legacy-unmatched.yml"]["behavioral_parity_verified"])


if __name__ == "__main__":
    unittest.main()
