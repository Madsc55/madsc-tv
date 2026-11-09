"""Offline regression tests for VOD snapshot preservation."""
import datetime
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "vod_guncelle.py"
spec = importlib.util.spec_from_file_location("vod_guncelle_under_test", SCRIPT)
vod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vod)


class Response(io.StringIO):
    def __enter__(self):
        return self
    def __exit__(self, *args):
        self.close()


class VodSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.out = Path(self.tmp.name) / "vod" / "guncel-bolumler.json"
        self.out.parent.mkdir()
        self.previous = b'{"episodes":[{"show":"previous"}]}\n'
        self.out.write_bytes(self.previous)
        self.day = datetime.date(2026, 10, 22)

    def test_total_network_failure_preserves_previous_snapshot(self):
        def fail(request, timeout):
            raise OSError("offline")
        self.assertEqual(vod.update(self.out, self.day, fail), 1)
        self.assertEqual(self.out.read_bytes(), self.previous)

    def test_partial_failure_preserves_previous_snapshot(self):
        calls = 0
        def partial(request, timeout):
            nonlocal calls
            calls += 1
            if calls == 3:
                raise OSError("offline")
            return Response("[]")
        self.assertEqual(vod.update(self.out, self.day, partial), 1)
        self.assertEqual(self.out.read_bytes(), self.previous)

    def test_invalid_response_preserves_previous_snapshot(self):
        def invalid(request, timeout):
            return Response('{"unexpected":true}')
        self.assertEqual(vod.update(self.out, self.day, invalid), 1)
        self.assertEqual(self.out.read_bytes(), self.previous)

    def test_malformed_episode_in_one_day_preserves_snapshot(self):
        calls = 0
        def malformed(request, timeout):
            nonlocal calls
            calls += 1
            if calls == 8:
                return Response('[{"show":{"name":"Valid"}}, {"show":"invalid"}]')
            return Response("[]")
        self.assertEqual(vod.update(self.out, self.day, malformed), 1)
        self.assertEqual(self.out.read_bytes(), self.previous)

    def test_all_successful_but_empty_days_preserve_snapshot(self):
        def empty(request, timeout):
            return Response("[]")
        self.assertEqual(vod.update(self.out, self.day, empty), 1)
        self.assertEqual(self.out.read_bytes(), self.previous)

    def test_atomic_replace_failure_preserves_snapshot_and_cleans_temp(self):
        def valid(request, timeout):
            return Response('[{"show":{"name":"Example"},"name":"Episode"}]')
        with mock.patch.object(vod.os, "replace", side_effect=OSError("disk failure")):
            with self.assertRaises(OSError):
                vod.update(self.out, self.day, valid)
        self.assertEqual(self.out.read_bytes(), self.previous)
        self.assertEqual(list(self.out.parent.glob(".vod-*.tmp")), [])

    def test_unserializable_api_data_preserves_snapshot_and_cleans_temp(self):
        def invalid_json_value(request, timeout):
            return Response('[{"show":{"name":"Example"},"season":1}]')
        original_collect = vod.collect
        def bad_collect(day, opener):
            return ([{"show": object()}], 15)
        with mock.patch.object(vod, "collect", side_effect=bad_collect):
            with self.assertRaises(TypeError):
                vod.update(self.out, self.day, invalid_json_value)
        self.assertEqual(self.out.read_bytes(), self.previous)
        self.assertEqual(list(self.out.parent.glob(".vod-*.tmp")), [])

    def test_complete_success_atomically_updates_snapshot(self):
        def valid(request, timeout):
            return Response(json.dumps([{"show":{"name":"Example"},"name":"Episode 1"}]))
        self.assertEqual(vod.update(self.out, self.day, valid), 0)
        result = json.loads(self.out.read_text(encoding="utf-8"))
        self.assertEqual(len(result["episodes"]), 15)
        self.assertEqual(result["episodes"][0]["show"], "Example")
        self.assertTrue(all(ep["watch_url"] is None for ep in result["episodes"]))
        self.assertEqual(list(self.out.parent.glob(".vod-*.tmp")), [])


if __name__ == "__main__":
    unittest.main()
