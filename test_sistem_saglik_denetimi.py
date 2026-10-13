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

if __name__ == "__main__":
    unittest.main()
