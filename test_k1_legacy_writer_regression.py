"""Offline K1 regression tests; no network or protected playlist mutation."""
import datetime
import importlib.util
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent
ARCHIVE = ROOT / "scripts" / "archive_backups_354_classified.py"
VOD = ROOT / "scripts" / "vod_guncelle.py"

class K1Regression(unittest.TestCase):
    def test_historical_archive_refuses_to_run(self):
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            playlist = root / "CALISANLAR.m3u"
            playlist.write_bytes(b"#EXTM3U\nprotected\n")
            result = subprocess.run([sys.executable, str(ARCHIVE)], cwd=root,
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(playlist.read_bytes(), b"#EXTM3U\nprotected\n")
            self.assertFalse((root / "madsc_kesif").exists())

    def test_vod_total_failure_keeps_previous_data(self):
        spec = importlib.util.spec_from_file_location("vod_k1", VOD)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        def offline(*args, **kwargs):
            raise OSError("offline")
        successes, records = mod.collect(datetime.date(2026, 10, 25), opener=offline)
        self.assertEqual((successes, records), (0, []))
        with tempfile.TemporaryDirectory() as d:
            old_out = mod.out
            try:
                mod.out = pathlib.Path(d) / "guncel-bolumler.json"
                mod.out.write_bytes(b'{"existing":true}\n')
                old_collect = mod.collect
                mod.collect = lambda today: (0, [])
                try:
                    with self.assertRaises(RuntimeError):
                        mod.main()
                    self.assertEqual(mod.out.read_bytes(), b'{"existing":true}\n')
                finally:
                    mod.collect = old_collect
            finally:
                mod.out = old_out


    def test_vod_partial_failure_keeps_previous_data(self):
        spec = importlib.util.spec_from_file_location("vod_k1_partial", VOD)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as d:
            mod.out = pathlib.Path(d) / "guncel-bolumler.json"
            mod.out.write_bytes(b'{"existing":true}\n')
            mod.collect = lambda today: (14, [{"episode": "partial"}])
            with self.assertRaises(RuntimeError):
                mod.main()
            self.assertEqual(mod.out.read_bytes(), b'{"existing":true}\n')

if __name__ == "__main__":
    unittest.main()
