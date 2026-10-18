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

    def test_security_policy_files_are_denied(self):
        self.assertEqual(
            blocked_paths(["AGENTS.md", "GUVENLIK_KURALLARI.md", "agents.MD"]),
            ["AGENTS.md", "GUVENLIK_KURALLARI.md", "agents.MD"],
        )

    def test_backups_and_nested_m3u_are_denied(self):
        self.assertEqual(blocked_paths(["yedekler/old.txt", "test/backup.m3u"]),
                         ["yedekler/old.txt", "test/backup.m3u"])

    def test_case_variants_and_ambiguous_paths_are_denied(self):
        suspicious = [
            "calisanlar.m3u", "favoriler/selection.txt",
            "Yedekler/old.txt", "HEPSI/../report.txt",
            "../CALISMAYANLAR.txt", "./YENILER.m3u",
            "madsc_kesif//report.json",
        ]
        self.assertEqual(blocked_paths(suspicious), suspicious)

    def test_nested_protected_folders_and_m3u8_are_denied(self):
        paths = ["archive/FAVORILER/list.txt", "tmp/HEPSI/order.json",
                 "cache/yedekler/old.txt", "streams/list.m3u8"]
        self.assertEqual(blocked_paths(paths), paths)

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

    @patch("tools.protected_write_gate.subprocess.run")
    def test_unstaged_and_untracked_paths_are_included(self, run):
        from tools.protected_write_gate import git_changed_paths
        import subprocess
        values = [b"", b"", b"YENILER.m3u\x00", b"yedekler/new.txt\x00", b"cache/HEPSI/ignored.txt\x00"]
        run.side_effect = [subprocess.CompletedProcess([], 0, stdout=value) for value in values]
        paths = git_changed_paths("trusted")
        self.assertEqual(paths, ["YENILER.m3u", "yedekler/new.txt", "cache/HEPSI/ignored.txt"])
        self.assertEqual(len(run.call_args_list), 5)


from tests.test_k1_legacy_writer_guards import LegacyWriterGuards  # included in CI discovery; checks explicit permissions


if __name__ == "__main__":
    unittest.main()
