import unittest
import json
import csv
import tempfile
from pathlib import Path
from unittest.mock import patch
from datetime import datetime, timezone
from akilli_tekrar_test_takvimi import plan

class SchedulerTest(unittest.TestCase):
    def test_real_retry_only_due_candidates(self):
        import altinci_aday_tekrar_test as retry
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            state = root / "gecmis.json"
            output = root / "report.csv"
            state.write_text(json.dumps({
                "https://example.org/due.m3u8": {
                    "name": "Due", "last_seen": "2020-01-01T00:00:00+00:00",
                    "successful_runs": [], "technical": "HATA", "media": "YOK"},
                "https://example.org/notdue.m3u8": {
                    "name": "Not due", "last_seen": "2099-01-01T00:00:00+00:00",
                    "successful_runs": [], "technical": "HATA", "media": "YOK"}
            }), encoding="utf-8")
            with patch.object(retry, "STATE", state), patch.object(retry, "OUT", output), \\
                 patch.object(retry, "check", return_value=["Due", "https://example.org/due.m3u8", "", "", "", "", "", ""]) as probe:
                retry.main()
                self.assertEqual(probe.call_count, 1)
                self.assertEqual(probe.call_args.args[0], "https://example.org/due.m3u8")
            with output.open(encoding="utf-8-sig", newline="") as file:
                self.assertEqual(len(list(csv.DictReader(file))), 1)

    def test_priority_and_no_mutation(self):
        now = datetime(2026, 10, 10, 12, tzinfo=timezone.utc)
        records = {
            "broken": {"name":"B", "last_seen":"2026-10-10T09:00:00+00:00", "technical":"HATA", "media":"YOK", "runs":["1"]},
            "stable": {"name":"S", "last_seen":"2026-10-10T09:00:00+00:00", "technical":"TEKNIK_AKIS_VAR", "media":"VIDEO_SES_VAR", "successful_runs":["1","2","3"]},
        }
        result = {r["YAYIN_URL"]: r for r in plan(records, now)}
        self.assertEqual(result["broken"]["TEST_ARALIGI_SAAT"], 2)
        self.assertEqual(result["broken"]["TEST_ZAMANI_GELDI"], "EVET")
        self.assertEqual(result["stable"]["TEST_ARALIGI_SAAT"], 24)
        self.assertEqual(result["stable"]["TEST_ZAMANI_GELDI"], "HAYIR")
        self.assertEqual(records["broken"]["technical"], "HATA")

if __name__ == "__main__":
    unittest.main()
