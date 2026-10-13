#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "scripts/central_run_status.py"

class MerkeziKosuDurumTesti(unittest.TestCase):
    def test_son_100_kanit_siniflari(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "madsc_merkezi_denetim"
            folder.mkdir()
            flows = [{"id": 1, "name": "Saglik", "path": "a.yml", "state": "active"},
                     {"id": 2, "name": "Yedek", "path": "b.yml", "state": "active"},
                     {"id": 3, "name": "EPG", "path": "c.yml", "state": "active"}]
            (folder / "github_workflow_durumlari.jsonl").write_text(
                "\n".join(json.dumps(x) for x in flows), encoding="utf-8")
            runs = [{"workflow_id": 1, "name": "Saglik", "status": "completed",
                     "conclusion": "success", "created_at": "2026-10-13T10:00:00Z"},
                    {"workflow_id": 2, "name": "Yedek", "status": "completed",
                     "conclusion": "failure", "created_at": "2026-10-13T10:00:00Z"}]
            (folder / "son_100_kosu.json").write_text(json.dumps(runs), encoding="utf-8")
            subprocess.run([sys.executable, str(SCRIPT)], cwd=tmp, check=True)
            report = json.loads((folder / "is_akisi_son_durum_siniflandirma.json").read_text())
            self.assertEqual(report["classifications"]["BASARILI"], 1)
            self.assertEqual(report["classifications"]["BASARISIZ"], 1)
            self.assertEqual(report["classifications"]["SON_100_KOSUDA_YOK"], 1)

if __name__ == "__main__":
    unittest.main()
