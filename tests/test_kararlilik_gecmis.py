import datetime
import unittest

from scripts.kararlilik_gecmis import normalize_history


class NormalizeHistoryTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime.datetime(2026, 10, 23, 12, tzinfo=datetime.timezone.utc)

    def row(self, at, state="VIDEO_SES_VAR"):
        return {"at": at, "state": state}

    def test_future_and_naive_observations_are_excluded(self):
        rows = [
            self.row("2026-10-24T12:00:00+00:00"),
            self.row("2026-10-23T11:00:00"),
            self.row("2026-10-23T10:00:00+00:00"),
        ]
        result = normalize_history(rows, self.now)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["at"], "2026-10-23T10:00:00+00:00")

    def test_timezone_offsets_normalize_to_utc(self):
        result = normalize_history(
            [self.row("2026-10-23T14:00:00+02:00")], self.now)
        self.assertEqual(result[0]["at"], "2026-10-23T12:00:00+00:00")

    def test_old_malformed_and_non_mapping_rows_are_excluded(self):
        rows = [
            self.row("2026-10-15T11:00:00+00:00"),
            self.row("not-a-time"),
            None,
            {"at": "2026-10-23T10:00:00+00:00"},
        ]
        self.assertEqual(normalize_history(rows, self.now), [])

    def test_exact_seven_day_boundary_is_retained(self):
        result = normalize_history(
            [self.row("2026-10-16T12:00:00+00:00")], self.now)
        self.assertEqual(len(result), 1)

    def test_naive_now_is_rejected(self):
        with self.assertRaises(ValueError):
            normalize_history([], datetime.datetime(2026, 10, 23, 12))


if __name__ == "__main__":
    unittest.main()
