import unittest
from scripts.central_archive_consistency import backup_metadata_consistent

class BackupArchiveCounterTests(unittest.TestCase):
    def test_actual_backup_count_not_historical_constant(self):
        entries = [{"meta": '#EXTINF:-1 group-title="📦 YEDEKLER (11599)",Kanal'}] * 11599
        result = backup_metadata_consistent(entries)
        self.assertTrue(result["ok"])
        self.assertEqual(result["actual_count"], 11599)
    def test_stale_category_count_is_detected(self):
        entries = [{"meta": '#EXTINF:-1 group-title="📦 YEDEKLER (2)",Kanal'}] * 3
        self.assertFalse(backup_metadata_consistent(entries)["ok"])
    def test_missing_group_metadata_is_detected(self):
        self.assertFalse(backup_metadata_consistent([{"meta": "#EXTINF:-1,Kanal"}])["ok"])

if __name__ == "__main__":
    unittest.main()
