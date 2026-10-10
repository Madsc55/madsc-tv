import unittest
from datetime import datetime, timezone
from akilli_tekrar_test_takvimi import plan

class SchedulerTest(unittest.TestCase):
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
