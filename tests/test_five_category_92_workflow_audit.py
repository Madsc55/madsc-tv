"""Regression checks for central schedule extraction (no repository writes)."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "scripts" / "five_category_92_workflow_audit.py"


class CentralCronRegexTests(unittest.TestCase):
    def test_central_cron_pattern_matches_real_yaml(self):
        source = AUDIT.read_text(encoding="utf-8")
        # Match the exact regex literal used in the central schedule extractor.
        line = next(line.strip() for line in source.splitlines()
                    if "for cron in re.findall(" in line and "replacement" not in line)
        self.assertIn(r'^\s+-\s*cron:', line)
        self.assertNotIn(r'^\\s+-\\s*cron:', line)
        pattern = re.compile(r"^\s+-\s*cron:\s*['\"]?([^'\"\n#]+)", re.M)
        yaml = "on:\n  schedule:\n    - cron: '15 4 * * *'\n    - cron: \"30 7 * * 1\"\n"
        self.assertEqual([x.strip() for x in pattern.findall(yaml)],
                         ["15 4 * * *", "30 7 * * 1"])


if __name__ == "__main__":
    unittest.main()
