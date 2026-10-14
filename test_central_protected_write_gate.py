import unittest
from pathlib import Path
from scripts.central_protected_write_gate import inspect

class KorunanYazmaKapisiTesti(unittest.TestCase):
    def test_gercek_workflow_dosyalari(self):
        report = inspect(Path(__file__).resolve().parent)
        self.assertGreater(report["workflows_scanned"], 0)
        self.assertEqual(report["errors"], [])
        self.assertTrue(all(x["status"] == "MANUAL_REVIEW_REQUIRED"
                            for x in report["review_required"]))

    def test_merkezi_rapor_kanal_listesini_degistirmez(self):
        source = Path("scripts/central_protected_write_gate.py").read_text()
        self.assertNotIn("write_text(content", source)
        self.assertNotIn("git push", source)

if __name__ == "__main__":
    unittest.main()
