import tempfile
import unittest
from pathlib import Path
from scripts.p0_dort_guvenlik_kabul import inspect


class P0DortGuvenlikKabulTesti(unittest.TestCase):
    def test_gercek_92_eski_workflow_tek_raporda(self):
        report = inspect()
        self.assertEqual(report["legacy_count"], 92)
        self.assertEqual(len({r["workflow"] for r in report["rows"]}), 92)
        self.assertEqual(report["acceptance"], "BLOCKED_NEEDS_ENFORCEMENT_AND_RUNTIME_EVIDENCE")

    def test_izinsiz_yazma_ve_devre_kesici_eksigi_gizlenmez(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / ".github" / "workflows"
            folder.mkdir(parents=True)
            raw = ("name: Test\non:\n  schedule:\n    - cron: '0 1 * * *'\n"
                   "permissions:\n  contents: write\njobs:\n  test:\n"
                   "    runs-on: ubuntu-latest\n    steps:\n      - run: git push origin HEAD:main\n")
            for i in range(92):
                (folder / f"old-{i:02d}.yml").write_text(raw if i == 0 else
                    "name: Safe\non:\n  workflow_dispatch:\njobs:\n  test:\n    runs-on: ubuntu-latest\n")
            report = inspect(Path(tmp))
            first = next(r for r in report["rows"] if r["workflow"] == "old-00.yml")
            self.assertIn("WRITE_WITHOUT_CONCURRENCY", first["risk_reasons"])
            self.assertIn("WRITE_WITHOUT_DIRECT_RULE24_GATE", first["risk_reasons"])
            self.assertEqual(report["write_review_count"], 1)


if __name__ == "__main__":
    unittest.main()
