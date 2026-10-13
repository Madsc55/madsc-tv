import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent

class KaynakMutabakatTesti(unittest.TestCase):
    def test_gercek_kaynak_tanimlari(self):
        subprocess.run([sys.executable, str(ROOT / "scripts/central_source_reconciliation.py")],
                       cwd=ROOT, check=True)
        r = json.loads((ROOT / "madsc_merkezi_denetim/kaynak_hedef_mutabakati.json").read_text())
        self.assertEqual(r["defined"] - r["target"], r["difference"])
        self.assertEqual(len(r["all_sources"]), r["defined"])
        self.assertEqual(r["unique_endpoint_count"] + sum(len(x["names"])-1 for x in r["duplicate_endpoints"]), r["defined"])
        self.assertEqual(r["invalid_endpoint_definitions"], [])
        self.assertGreaterEqual(r["raw_source_entry_count"], r["defined"])
        self.assertEqual(bool(r["raw_source_entry_count"] > r["defined"]), bool(r["duplicate_source_names"]))

if __name__ == "__main__":
    unittest.main()
