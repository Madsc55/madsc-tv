import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent

class YedekKanitiTesti(unittest.TestCase):
    def test_korunan_dosyalar_ve_dogrulama_siniri(self):
        subprocess.run([sys.executable, str(ROOT / "scripts/central_backup_evidence.py")], cwd=ROOT, check=True)
        report = json.loads((ROOT / "madsc_merkezi_denetim/yedek_ve_korunan_dosyalar_kanit.json").read_text())
        self.assertFalse(report["protected_missing"])
        self.assertEqual(report["restore_test"], "BU_KOSUDA_YAPILMADI")
        self.assertEqual(report["off_github_copy"], "DOGRULANMADI")
        self.assertTrue(all(len(x["sha256"]) == 64 for x in report["protected_files"]))

if __name__ == "__main__":
    unittest.main()
