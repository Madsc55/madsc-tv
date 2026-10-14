#!/usr/bin/env python3
"""Merkezi denetimin salt okunur rapor sozlesmesi."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "madsc_merkezi_denetim"

class MerkeziDenetimTesti(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(ROOT / "scripts/central_workflow_inventory.py")],
                       cwd=ROOT, check=True)

    def test_raporlar_ve_kapsam(self):
        paths = ["otomasyon_haritasi.json", "otomasyon_cakisma_on_analizi.json",
                 "otomasyon_es_zamanlilik_raporu.json", "merkezi_oncelik_ve_koruma_raporu.json"]
        for name in paths:
            self.assertTrue((OUT / name).is_file(), name)
        inv = json.loads((OUT / paths[0]).read_text(encoding="utf-8"))
        risk = json.loads((OUT / paths[3]).read_text(encoding="utf-8"))
        self.assertEqual(inv["workflow_count"], len(risk["all_workflows"]))
        self.assertEqual(risk["workflows_checked"], inv["workflow_count"])
        self.assertGreater(inv["workflow_count"], 0)
        self.assertEqual(len({x["file"] for x in risk["all_workflows"]}), inv["workflow_count"])

    def test_bes_asama_tam_kapsam_ve_takvim(self):
        report = json.loads((OUT / "bes_asama_tum_workflow_eslestirmesi.json").read_text(encoding="utf-8"))
        inv = json.loads((OUT / "otomasyon_haritasi.json").read_text(encoding="utf-8"))
        self.assertEqual(len(report["stages"]), 5)
        mapped = [name for stage in report["stages"] for name in stage["workflows"]]
        self.assertEqual(len(mapped), report["workflow_count"])
        self.assertEqual(len(set(mapped)), len(mapped))
        self.assertEqual(set(mapped), {item["file"] for item in inv["workflows"]})
        self.assertFalse(report["complete_historical_coverage_verified"])
        central = next(item for item in inv["workflows"]
                       if item["file"] == "madsc-aylik-merkezi-denetim.yml")
        self.assertEqual(central["schedule_utc"], ["0 7 1,15 * *"])

    def test_koruma_ve_rapor_sozlesmesi(self):
        report = json.loads((OUT / "merkezi_oncelik_ve_koruma_raporu.json").read_text(encoding="utf-8"))
        self.assertEqual(report["safety"], {
            "protected_playlists_modified": False, "schedules_modified": False,
            "workflows_triggered": False})
        self.assertTrue(any(x["category"] == "YEDEK_VE_KURTARMA" for x in report["all_workflows"]))
        self.assertTrue(any(x["category"] == "EPG" for x in report["all_workflows"]))
        self.assertTrue(any(x["category"] == "KESIF" for x in report["all_workflows"]))
        self.assertTrue(all(x["review_only"] for x in report["all_workflows"]))

if __name__ == "__main__":
    unittest.main()
