"""Network-free regression tests for VOD snapshot preservation."""
import datetime
import json
import tempfile
import unittest
from pathlib import Path
from scripts.vod_guncelle import update


class Response:
    def __init__(self, value):
        self.value = value
    def __enter__(self):
        return self
    def __exit__(self, *args):
        return False
    def read(self, *args):
        return json.dumps(self.value).encode("utf-8")


class VodSnapshotTests(unittest.TestCase):
    def test_total_failure_preserves_existing_file(self):
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder) / "episodes.json"
            out.write_text('{"previous":true}\n')
            def fail(*args, **kwargs):
                raise OSError("offline")
            self.assertEqual(update(out, datetime.date(2026, 10, 26), fail), 1)
            self.assertEqual(out.read_text(), '{"previous":true}\n')

    def test_partial_failure_preserves_existing_file(self):
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder) / "episodes.json"
            out.write_text("old")
            calls = 0
            def partial(*args, **kwargs):
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("offline")
                return Response([])
            self.assertEqual(update(out, datetime.date(2026, 10, 26), partial), 1)
            self.assertEqual(out.read_text(), "old")

    def test_all_success_allows_valid_empty_schedule(self):
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder) / "episodes.json"
            self.assertEqual(update(out, datetime.date(2026, 10, 26),
                                    lambda *args, **kwargs: Response([])), 0)
            self.assertEqual(json.loads(out.read_text())["episodes"], [])


if __name__ == "__main__":
    unittest.main()
