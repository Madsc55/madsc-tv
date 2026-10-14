import tempfile
import unittest
from pathlib import Path
from scripts.central_single_screen_report import build, markdown, FILES

class TekEkranTopluTest(unittest.TestCase):
    def test_bes_asama_ve_eksikler_tek_raporda(self):
        with tempfile.TemporaryDirectory() as temp:
            report = build(Path(temp), Path(temp) / "olmayan_kesif")
        self.assertEqual(len(report["bes_asama"]), 5)
        self.assertEqual(report["eksik_rapor"], sum(len(v) for v in FILES.values()) + 1)
        self.assertEqual(report["genel_kabul"], "HENUZ_ONAYLANMADI")
        self.assertIn("TEK EKRANDA", markdown(report))
    def test_kesif_logo_raporunu_gercek_yerinden_okur(self):
        import json
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            discovery = root / "madsc_kesif"
            discovery.mkdir()
            (discovery / "candidate_logo_missing_report.json").write_text(json.dumps({
                "total_candidates": 3, "category_counts": {"LOGO_KAYNAGI_YOK": 2}}))
            report = build(root, discovery)
        self.assertEqual(report["aday_logo_sayisi"], 3)
        self.assertEqual(report["eksik_rapor"], sum(len(v) for v in FILES.values()))
        self.assertTrue(any(x["tur"] == "ADAY_LOGO_INCELEME" for x in report["acik_isler"]))

    def test_yedek_kaniti_eksikse_basarili_gosterme(self):
        import json
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / "yedek_ve_korunan_dosyalar_kanit.json").write_text(json.dumps({
                "restore_test": "GIT_HEAD_IZOLE_ESLESME_DOGRULANDI",
                "historical_recovery_verified": False, "off_github_copy": "DOGRULANMADI"}))
            report = build(folder, folder / "olmayan_kesif")
        self.assertEqual(report["yedek_kaniti"]["durum"], "EKSIK_KANIT")
        self.assertTrue(any(x["tur"] == "TARIHSEL_YEDEK" for x in report["acik_isler"]))
        self.assertTrue(any(x["tur"] == "HARICI_KOPYA" for x in report["acik_isler"]))

    def test_korunan_dosyalara_yazilmaz(self):
        source = Path("scripts/central_single_screen_report.py").read_text()
        self.assertNotIn("CALISANLAR.m3u", source)
        self.assertNotIn("git push", source)
