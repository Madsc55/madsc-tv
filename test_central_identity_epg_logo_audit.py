import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent

class KimlikEpgLogoTesti(unittest.TestCase):
    def test_ibo_onayi_ve_kimlik_otomatik_verilmez(self):
        subprocess.run([sys.executable, str(ROOT / "scripts/central_identity_epg_logo_audit.py")], cwd=ROOT, check=True)
        report = json.loads((ROOT / "madsc_merkezi_denetim/logo_epg_kimlik_gecmis_tek_rapor.json").read_text())
        self.assertEqual(report["user_ibo_approval"], "NOT_VERIFIED")
        self.assertFalse(report["playlist_approved_by_this_audit"])
        self.assertFalse(report["logos"]["visual_identity_verified_by_this_audit"])
        self.assertFalse(report["epg"]["sweden_ibo_verified_by_this_audit"])
        self.assertTrue(report["final_validation"]["identity_and_device_confirmation_required"])

if __name__ == "__main__":
    unittest.main()
