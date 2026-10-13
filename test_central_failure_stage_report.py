import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "scripts/central_failure_stage_report.py"

class HataAsamaTesti(unittest.TestCase):
    def test_hata_asamasi_kok_neden_sayilmaz(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "madsc_merkezi_denetim"
            folder.mkdir()
            (folder / "son_100_kosu.json").write_text(json.dumps([
                {"run_id": 42, "name": "Kontrol", "conclusion": "failure", "html_url": "https://example.org/42"},
                {"run_id": 43, "name": "Saglik", "conclusion": "success"}]))
            (folder / "basarisiz_kosu_isleri.json").write_text(json.dumps([
                {"run_id": 42, "status": "ALINDI", "jobs": [
                    {"name": "Denetim", "conclusion": "failure",
                     "steps": [{"name": "Kaynak kontrolu", "conclusion": "success"},
                               {"name": "Yayin testi", "conclusion": "failure"}]}]}]))
            subprocess.run([sys.executable, str(SCRIPT)], cwd=tmp, check=True)
            report = json.loads((folder / "hata_asama_raporu.json").read_text())
            self.assertEqual(report["failed_runs_in_sample"], 1)
            self.assertEqual(report["runs"][0]["failed_jobs"][0]["failed_steps"][0]["name"], "Yayin testi")
            self.assertEqual(report["runs"][0]["root_cause"], "LOG_INCELEMESI_GEREKLI")

if __name__ == "__main__":
    unittest.main()
