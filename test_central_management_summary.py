import json
import tempfile
import unittest
from pathlib import Path
from scripts.central_management_summary import build, SOURCES

class YonetimOzetiTesti(unittest.TestCase):
    def test_eksik_kanit_basarili_sayilmaz(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / SOURCES["sekiz_gorev"]).write_text('{"kontrol_sayisi":8}')
            result = build(folder)
            self.assertEqual(result["section_count"], len(SOURCES))
            self.assertEqual(result["sections"]["sekiz_gorev"]["status"], "RAPOR_VAR")
            self.assertIn("logo_epg_kimlik", result["missing_evidence"])
            self.assertEqual(result["device_ibo_approval"], "NOT_VERIFIED")
            self.assertFalse(result["playlist_change"])

    def test_bes_asama_tek_raporda_kanit_ve_hata_ayrimi(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            stages = {
                "workflow_count": 5, "mapped_count": 5,
                "manual_scope_review_required": ["belirsiz.yml"],
                "complete_historical_coverage_verified": False,
                "stages": [
                    {"number": n, "name": f"Asama {n}", "workflows": [f"{n}.yml"]}
                    for n in range(1, 6)
                ],
            }
            (folder / SOURCES["bes_asama"]).write_text(json.dumps(stages))
            (folder / SOURCES["actions_dogrulama"]).write_text(
                json.dumps({"successful": 4, "failed": [{"run_id": 123, "conclusion": "failure"}]}))
            result = build(folder)
            self.assertEqual(len(result["five_stage_results"]), 5)
            self.assertEqual(result["key_indicators"]["five_stage_workflows_mapped"], 5)
            self.assertFalse(result["key_indicators"]["historical_coverage_verified"])
            self.assertEqual(result["key_indicators"]["actions_failed_latest_seen"], 1)
            self.assertFalse(result["key_indicators"]["actions_current_run_verified"])
            self.assertEqual(result["five_stage_results"][0]["status"], "KANIT_EKSIK")
            blockers = {entry["code"] for entry in result["open_blockers"]}
            self.assertIn("UNREVIEWED_WORKFLOW_OWNERSHIP", blockers)
            self.assertIn("FIVE_STAGE_MISSING_EVIDENCE", blockers)
            self.assertIn("LATEST_ACTIONS_FAILURES", blockers)

    def test_on_sekiz_gorev_raporu_ozete_girer(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / SOURCES["on_sekiz_gorev"]).write_text(
                json.dumps({"toplam": 18, "kod_kaniti_eksik": 2}))
            report = build(folder)
            self.assertEqual(report["key_indicators"]["eighteen_tasks_mapped"], 18)
            self.assertEqual(report["key_indicators"]["eighteen_tasks_code_evidence_missing"], 2)

    def test_bozuk_json_ayri_raporlanir(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / SOURCES["kaynak_mutabakati"]).write_text("{broken")
            result = build(folder)
            self.assertEqual(result["sections"]["kaynak_mutabakati"]["status"], "GECERSIZ_RAPOR")

if __name__ == "__main__":
    unittest.main()
