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


    def test_vod_complete_success_replaces_metadata(self):
        import json
        spec = importlib.util.spec_from_file_location("vod_k1_success", VOD)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as d:
            mod.out = pathlib.Path(d) / "guncel-bolumler.json"
            mod.out.write_text('{"existing":true}', encoding="utf-8")
            mod.collect = lambda today: (15, [{"episode": "verified"}])
            mod.main()
            result = json.loads(mod.out.read_text(encoding="utf-8"))
            self.assertEqual(result["episodes"], [{"episode": "verified"}])
            self.assertFalse(list(pathlib.Path(d).glob(".vod-*.tmp")))


    def test_vod_malformed_day_does_not_count_or_leak_partial_records(self):
        import io
        import json
        import urllib.parse
        spec = importlib.util.spec_from_file_location("vod_k1_malformed", VOD)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        class Response(io.BytesIO):
            def __enter__(self):
                return self
            def __exit__(self, *args):
                self.close()

        def fake_opener(request, timeout):
            day = urllib.parse.parse_qs(urllib.parse.urlparse(request.full_url).query)["date"][0]
            episodes = [{"show": {"name": "Valid"}, "name": "first"}]
            if day == "2026-10-25":
                episodes.append({"show": [], "name": "invalid"})
            return Response(json.dumps(episodes).encode("utf-8"))

        successes, records = mod.collect(datetime.date(2026, 10, 25), opener=fake_opener)
        self.assertEqual(successes, 14)
        self.assertEqual(len(records), 14)
        self.assertTrue(all(row["show"] == "Valid" for row in records))


    def test_vod_replace_failure_preserves_previous_data_and_cleans_temp(self):
        from unittest.mock import patch
        spec = importlib.util.spec_from_file_location("vod_k1_replace", VOD)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as d:
            mod.out = pathlib.Path(d) / "guncel-bolumler.json"
            original = b'{"existing":true}'
            mod.out.write_bytes(original)
            mod.collect = lambda today: (15, [{"episode": "valid"}])
            with patch.object(mod.os, "replace", side_effect=OSError("disk error")):
                with self.assertRaises(OSError):
                    mod.main()
            self.assertEqual(mod.out.read_bytes(), original)
            self.assertFalse(list(pathlib.Path(d).glob(".vod-*.tmp")))


    def test_vod_malformed_api_day_preserves_existing_file_end_to_end(self):
        import io
        import json
        from unittest.mock import patch
        spec = importlib.util.spec_from_file_location("vod_k1_end_to_end", VOD)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as d:
            mod.out = pathlib.Path(d) / "guncel-bolumler.json"
            original = b'{"existing":true}'
            mod.out.write_bytes(original)
            def fake_opener(request, timeout):
                day = request.full_url.rsplit("=", 1)[-1]
                episodes = [] if day != "2026-10-25" else [{"show": [], "name": "bad"}]
                return io.BytesIO(json.dumps(episodes).encode("utf-8"))
            real_collect = mod.collect
            with patch.object(mod, "collect", side_effect=lambda today: real_collect(
                datetime.date(2026, 10, 25), opener=fake_opener)):
                with self.assertRaises(RuntimeError):
                    mod.main()
            self.assertEqual(mod.out.read_bytes(), original)
            self.assertFalse(list(pathlib.Path(d).glob(".vod-*.tmp")))

if __name__ == "__main__":
    unittest.main()
