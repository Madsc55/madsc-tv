import datetime as dt
import importlib.util
from pathlib import Path
import unittest

MODULE = Path(__file__).resolve().parents[1] / "scripts" / "k3_alti_saat_kanit.py"
spec = importlib.util.spec_from_file_location("k3_kanit", MODULE)
k3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(k3)

def evidence(channels=75, hours=6, gap=300):
    start = dt.datetime(2026, 10, 25, tzinfo=dt.timezone.utc)
    return [dict(channel_id=f"opaque-{i}", timestamp=(start + dt.timedelta(seconds=t)).isoformat(),
                 video_ok=True, audio_ok=True)
            for i in range(channels) for t in range(0, hours * 3600 + 1, gap)]

class K3EvidenceTests(unittest.TestCase):
    def test_75_six_hours_periodic_only(self):
        result = k3.validate(evidence())
        self.assertEqual(result["periyodik_probe_kabulu"], "EVET")
        self.assertEqual(result["kesintisiz_oynatma_kaniti"], "YOK")

    def test_74_channels_not_enough(self):
        self.assertEqual(k3.validate(evidence(channels=74))["periyodik_probe_kabulu"], "BEKLIYOR")

    def test_missing_gap_rejects(self):
        rows = evidence(channels=1)
        rows = [r for r in rows if not r["timestamp"].endswith("00:05:00+00:00")]
        self.assertEqual(k3.validate(rows, target=1)["kanitli_tekil_kanal"], 0)

    def test_failure_rejects(self):
        rows = evidence(channels=1)
        rows[4]["audio_ok"] = False
        self.assertEqual(k3.validate(rows, target=1)["kanitli_tekil_kanal"], 0)

    def test_short_span_rejects(self):
        self.assertEqual(k3.validate(evidence(channels=1, hours=5), target=1)["kanitli_tekil_kanal"], 0)

    def test_naive_timestamp_rejects(self):
        rows = evidence(channels=1)
        rows[0]["timestamp"] = "2026-10-25T00:00:00"
        with self.assertRaises(ValueError):
            k3.validate(rows)

    def test_string_boolean_rejects(self):
        rows = evidence(channels=1)
        rows[0]["video_ok"] = "true"
        with self.assertRaises(ValueError):
            k3.validate(rows)

    def test_duplicate_timestamp_rejects(self):
        rows = evidence(channels=1)
        rows.append(dict(rows[0]))
        self.assertEqual(k3.validate(rows, target=1)["kanitli_tekil_kanal"], 0)

if __name__ == "__main__":
    unittest.main()
