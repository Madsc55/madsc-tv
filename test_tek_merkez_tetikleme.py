import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent

class TekMerkezKuralTesti(unittest.TestCase):
    def test_belge_push_ayri_kosmaz(self):
        doc = (ROOT / ".github/workflows/madsc-documentation-check.yml").read_text()
        self.assertNotIn("\n  push:", doc)
        self.assertIn("workflow_dispatch:", doc)

    def test_merkez_dokuman_ve_kanal_kontrolu(self):
        central = (ROOT / ".github/workflows/madsc-aylik-merkezi-denetim.yml").read_text()
        for name in ("AGENTS.md", "DEVAM_NOTU.md", "CALISANLAR.m3u", "GUVENLIK_KURALLARI.md"):
            self.assertIn("'"+name+"'", central)
        self.assertIn("Proje kayitlari ve dokumantasyonu merkezi kontrolde dogrula", central)
        self.assertIn("  contents: read", central)

if __name__ == "__main__":
    unittest.main()
