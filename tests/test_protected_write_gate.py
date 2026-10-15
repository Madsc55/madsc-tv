"""Negative tests: never modify a protected playlist."""
import unittest
from unittest.mock import patch
import subprocess

from tools.protected_write_gate import blocked_paths, main


class ProtectedWriteGateTests(unittest.TestCase):
    def test_protected_playlists_are_denied(self):
        self.assertEqual(
            blocked_paths(["CALISANLAR.m3u", "YENILER.m3u", "YABANCI_KANALLAR.m3u"]),
            ["CALISANLAR.m3u", "YENILER.m3u", "YABANCI_KANALLAR.m3u"],
        )

    def test_backups_and_nested_m3u_are_denied(self):
        self.assertEqual(blocked_paths(["yedekler/old.txt", "test/backup.m3u"]),
                         ["yedekler/old.txt", "test/backup.m3u"])

    def test_reports_are_allowed(self):
        self.assertEqual(blocked_paths(["madsc_kesif/report.json", "DEVAM_NOTU.md"]), [])

    @patch("tools.protected_write_gate.git_changed_paths")
    def test_denied_before_push(self, changed):
        changed.return_value = ["CALISANLAR.m3u"]
        self.assertEqual(main(["--base", "deadbeef"]), 1)

    @patch("tools.protected_write_gate.git_changed_paths")
    def test_git_failure_is_denied(self, changed):
        changed.side_effect = subprocess.CalledProcessError(128, ["git", "diff"])
        self.assertEqual(main(["--base", "deadbeef"]), 2)

    @patch("tools.protected_write_gate.git_changed_paths")
    def test_safe_report_only_is_allowed(self, changed):
        changed.return_value = ["madsc_kesif/report.json"]
        self.assertEqual(main(["--base", "deadbeef"]), 0)


if __name__ == "__main__":
    unittest.main()
