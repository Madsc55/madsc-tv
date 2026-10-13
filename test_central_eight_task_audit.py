import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "madsc_merkezi_denetim/sekiz_gorev_tek_merkezi_rapor.json"

class SekizGorevMerkeziTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(ROOT / "scripts/central_eight_task_audit.py")],
                       cwd=ROOT, check=True)
        cls.report = json.loads(REPORT.read_text(encoding="utf-8"))

    def test_sekiz_benzersiz_baslik(self):
        self.assertEqual(self.report["total"], 8)
        self.assertEqual([x["no"] for x in self.report["tasks"]], list(range(1, 9)))

    def test_eksik_kanit_basarili_gosterilmez(self):
        self.assertEqual(self.report["summary"]["needs_followup"], 8)
        self.assertTrue(all(x["durum"] == "TAKIP_GEREKIYOR" for x in self.report["tasks"]))
        self.assertEqual(self.report["summary"]["fully_completed"], 0)

    def test_korunan_dosyalara_yazma_yok(self):
        self.assertEqual(self.report["safety"], {
            "playlists_modified": False, "backups_modified": False,
            "cron_modified": False, "device_test_claimed": False})
        self.assertTrue(self.report["tasks"][3]["kanit"]["protected_files"]["CALISANLAR.m3u"])

if __name__ == "__main__":
    unittest.main()
