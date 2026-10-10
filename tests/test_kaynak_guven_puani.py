import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "kaynak_guven_puani.py"

class KaynakPuaniTest(unittest.TestCase):
    def test_rapor_ve_guven_duzeyi(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            state = root / "aday_bekletme"
            state.mkdir()
            data = {}
            for i in range(12):
                data[f"https://ornek.test/kanal{i}.m3u8"] = {
                    "source": "ornek",
                    "runs": ["1", "2"],
                    "successful_runs": ["1", "2"],
                }
            (state / "gecmis.json").write_text(json.dumps(data), encoding="utf-8")
            subprocess.run([sys.executable, str(SCRIPT)], cwd=root, check=True, capture_output=True)
            with (state / "KAYNAK_GUVEN_PUANLARI.csv").open(encoding="utf-8-sig", newline="") as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["GUVEN_DUZEYI"], "YUKSEK")
            self.assertEqual(rows[0]["ADAY_SAYISI"], "12")

    def test_bos_gecmis(self):
        with tempfile.TemporaryDirectory() as d:
            subprocess.run([sys.executable, str(SCRIPT)], cwd=d, check=True, capture_output=True)
            with (Path(d) / "aday_bekletme/KAYNAK_GUVEN_PUANLARI.csv").open(encoding="utf-8-sig", newline="") as f:
                self.assertEqual(len(list(csv.DictReader(f))), 0)

if __name__ == "__main__":
    unittest.main()
