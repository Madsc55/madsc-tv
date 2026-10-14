import tempfile
import unittest
from pathlib import Path
from scripts.central_single_screen_report import build, markdown, FILES

class TekEkranTopluTest(unittest.TestCase):
    def test_bes_asama_ve_eksikler_tek_raporda(self):
        with tempfile.TemporaryDirectory() as temp:
            report = build(Path(temp))
        self.assertEqual(len(report["bes_asama"]), 5)
        self.assertEqual(report["eksik_rapor"], sum(len(v) for v in FILES.values()))
        self.assertEqual(report["genel_kabul"], "HENUZ_ONAYLANMADI")
        self.assertIn("TEK EKRANDA", markdown(report))
    def test_korunan_dosyalara_yazilmaz(self):
        source = Path("scripts/central_single_screen_report.py").read_text()
        self.assertNotIn("CALISANLAR.m3u", source)
        self.assertNotIn("git push", source)
