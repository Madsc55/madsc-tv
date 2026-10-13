import json
import tempfile
import unittest
from pathlib import Path
from scripts.central_management_summary import build, SOURCES

class YonetimOzetiTesti(unittest.TestCase):
    def test_eksik_kanit_basarili_sayilmaz(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / SOURCES["sekiz_gorev"]).write_text('{"kontrol_sayisi":8}')
            result = build(folder)
            self.assertEqual(result["section_count"], len(SOURCES))
            self.assertEqual(result["sections"]["sekiz_gorev"]["status"], "RAPOR_VAR")
            self.assertIn("logo_epg_kimlik", result["missing_evidence"])
            self.assertEqual(result["device_ibo_approval"], "NOT_VERIFIED")
            self.assertFalse(result["playlist_change"])

    def test_bozuk_json_ayri_raporlanir(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / SOURCES["kaynak_mutabakati"]).write_text("{broken")
            result = build(folder)
            self.assertEqual(result["sections"]["kaynak_mutabakati"]["status"], "GECERSIZ_RAPOR")

if __name__ == "__main__":
    unittest.main()
