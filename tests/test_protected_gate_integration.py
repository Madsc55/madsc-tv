"""Real subprocess integration checks for the protected write gate; isolated temp Git repo."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

GATE = Path(__file__).resolve().parents[1] / "tools" / "protected_write_gate.py"


class ProtectedGateIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.git("init", "-q")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "user.name", "MADSC Test")
        (self.repo / "baseline.txt").write_text("baseline\n", encoding="utf-8")
        self.git("add", "baseline.txt")
        self.git("commit", "-qm", "baseline")
        self.base = self.git("rev-parse", "HEAD").stdout.strip()

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.repo, text=True,
                              capture_output=True, check=True)

    def gate(self, base=None):
        return subprocess.run([sys.executable, str(GATE), "--base", base or self.base],
                              cwd=self.repo, text=True, capture_output=True)

    def test_real_git_denies_modified_protected_playlist(self):
        (self.repo / "CALISANLAR.m3u").write_text("#EXTM3U\n", encoding="utf-8")
        result = self.gate()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("CALISANLAR.m3u", result.stderr)

    def test_real_git_denies_ignored_protected_epg(self):
        (self.repo / ".gitignore").write_text("EPG/\n", encoding="utf-8")
        folder = self.repo / "EPG"
        folder.mkdir()
        (folder / "hidden.xml").write_text("<tv/>\n", encoding="utf-8")
        result = self.gate()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("EPG/hidden.xml", result.stderr)

    def test_real_git_allows_only_unprotected_report(self):
        folder = self.repo / "madsc_kesif"
        folder.mkdir()
        (folder / "report.json").write_text("{}\n", encoding="utf-8")
        result = self.gate()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_invalid_baseline_denied(self):
        result = self.gate("nonexistent-ref")
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("DENY", result.stderr)


if __name__ == "__main__":
    unittest.main()
