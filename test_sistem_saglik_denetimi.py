import tempfile
import unittest
from pathlib import Path
from tools.sistem_saglik_denetimi import inspect


class SistemSaglikTesti(unittest.TestCase):
    def test_salt_okunur_ve_eksik_dosya(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".github/workflows").mkdir(parents=True)
            (root / ".github/workflows/check.yml").write_text("name: test\non: push\n", encoding="utf-8")
            report = inspect(root)
            self.assertEqual(report["mode"], "READ_ONLY")
            self.assertTrue(any(f["code"] == "MISSING_FILE" for f in report["findings"]))
            self.assertFalse((root / "madsc_bakim").exists())

    def test_tehlikeli_izin_ve_kod_hatasi(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".github/workflows").mkdir(parents=True)
            (root / "tools").mkdir()
            (root / ".github/workflows/a.yml").write_text("permissions: write-all\n", encoding="utf-8")
            (root / "tools/broken.py").write_text("def (\n", encoding="utf-8")
            codes = {f["code"] for f in inspect(root)["findings"]}
            self.assertIn("BROAD_PERMISSIONS", codes)
            self.assertIn("PYTHON_SYNTAX", codes)

    def test_tekrar_eden_aday_ve_bos_epg_raporu(self):
        import json
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".github/workflows").mkdir(parents=True)
            (root / ".github/workflows/check.yml").write_text("name: kontrol\\n", encoding="utf-8")
            (root / "madsc_son_kontrol").mkdir()
            (root / "madsc_kesif").mkdir()
            (root / "madsc_son_kontrol/summary.json").write_text(json.dumps({"completed": 2, "remaining": 0}))
            (root / "madsc_son_kontrol/results.json").write_text(json.dumps([{"candidate_id": "x"}, {"candidate_id": "x"}]))
            (root / "madsc_kesif/candidate_epg_logo_join.json").write_text(json.dumps({"source_candidates": 0}))
            codes = {f["code"] for f in inspect(root)["findings"]}
            self.assertIn("DUPLICATE_CANDIDATE_IDS", codes)
            self.assertIn("EMPTY_CANDIDATE_JOIN", codes)

if __name__ == "__main__":
    unittest.main()
