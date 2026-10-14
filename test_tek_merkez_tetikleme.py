import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent

class TekMerkezKuralTesti(unittest.TestCase):
    def test_belge_push_ayri_kosmaz(self):
        doc = (ROOT / ".github/workflows/madsc-documentation-check.yml").read_text()
        self.assertNotIn("\n  push:", doc)
        self.assertIn("workflow_dispatch:", doc)

    def test_logo_kanal_degisiminde_ayri_push_acmaz(self):
        logo = (ROOT / ".github/workflows/automatic-png-logos.yml").read_text()
        self.assertIn("  workflow_dispatch:", logo)
        self.assertIn("    - cron: '23 5 * * *'", logo)
        self.assertNotIn("      - 'CALISANLAR.m3u'", logo)
        self.assertIn("      - 'scripts/automatic_png_logos.py'", logo)
        self.assertIn("  contents: read", logo)
        self.assertIn("Korunan kanal listesi degisikliklerini engelle", logo)

    def test_merkez_dokuman_ve_kanal_kontrolu(self):
        central = (ROOT / ".github/workflows/madsc-aylik-merkezi-denetim.yml").read_text()
        for name in ("AGENTS.md", "DEVAM_NOTU.md", "CALISANLAR.m3u", "GUVENLIK_KURALLARI.md"):
            self.assertIn("'"+name+"'", central)
        self.assertIn("Proje kayitlari ve dokumantasyonu merkezi kontrolde dogrula", central)
        self.assertIn("  contents: read", central)

if __name__ == "__main__":
    unittest.main()
