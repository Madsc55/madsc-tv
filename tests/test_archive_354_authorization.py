"""Regression tests: historical archive migration must deny implicit execution."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "archive_backups_354_classified.py"


class HistoricalArchiveAuthorizationTests(unittest.TestCase):
    def test_unauthorized_invocations_preserve_playlist(self):
        cases = [
            ([], None),
            (["--apply-authorized"], None),
            ([], "YES"),
            (["--apply-authorized"], "NO"),
            (["--apply-authorized", "--extra"], "YES"),
        ]
        for args, authorization in cases:
            with self.subTest(args=args, authorization=authorization):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    playlist = root / "CALISANLAR.m3u"
                    original = b"#EXTM3U\n#EXTINF:-1,Protected\nhttps://example.invalid/live.m3u8\n"
                    playlist.write_bytes(original)
                    env = os.environ.copy()
                    env.pop("MADSC_ARCHIVE_354_AUTHORIZED", None)
                    if authorization is not None:
                        env["MADSC_ARCHIVE_354_AUTHORIZED"] = authorization
                    result = subprocess.run(
                        [sys.executable, str(SCRIPT), *args],
                        cwd=root, env=env, capture_output=True, text=True, timeout=10,
                    )
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("DENY:", result.stderr + result.stdout)
                    self.assertEqual(playlist.read_bytes(), original)
                    self.assertFalse((root / "madsc_kesif").exists())


if __name__ == "__main__":
    unittest.main()
