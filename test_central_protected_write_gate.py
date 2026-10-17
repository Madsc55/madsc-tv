import unittest
from pathlib import Path
from scripts.central_protected_write_gate import inspect

class KorunanYazmaKapisiTesti(unittest.TestCase):
    def test_gercek_workflow_dosyalari(self):
        report = inspect(Path(__file__).resolve().parent)
        self.assertGreater(report["workflows_scanned"], 0)
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["central_write_violations"], [])
        self.assertTrue(all(x["status"] == "MANUAL_REVIEW_REQUIRED"
                            for x in report["review_required"]))

    def test_job_duzeyi_yazma_yetkisi_yakalanir(self):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / ".github" / "workflows"
            folder.mkdir(parents=True)
            (folder / "madsc-01-guvenlik.yaml").write_text(
                "name: Test\non: workflow_dispatch\npermissions:\n  contents: read\njobs:\n  check:\n    runs-on: ubuntu-latest\n    permissions:\n      contents: write\n    steps:\n      - run: echo ok\n",
                encoding="utf-8",
            )
            report = inspect(root)
            self.assertEqual(report["workflows_scanned"], 1)
            self.assertEqual(len(report["central_write_violations"]), 1)
            self.assertEqual(report["errors"], [])

    def test_legacy_yazma_raporlanir_ama_otomatik_kapatilmaz(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / ".github" / "workflows"
            folder.mkdir(parents=True)
            (folder / "eski-kanal-guncelleme.yml").write_text(
                "name: Eski\non: workflow_dispatch\npermissions:\n  contents: write\njobs:\n  job:\n    runs-on: ubuntu-latest\n    steps:\n      - run: echo test\n",
                encoding="utf-8",
            )
            report = inspect(root)
            self.assertEqual(report["errors"], [])
            self.assertEqual(report["central_write_violations"], [])
            self.assertEqual(report["review_count"], 1)

    def test_legacy_belirsiz_izin_ve_riskli_komut_raporlanir(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / ".github" / "workflows"
            folder.mkdir(parents=True)
            (folder / "legacy.yml").write_text(
                "name: Legacy\non: workflow_dispatch\njobs:\n  check:\n"
                "    runs-on: ubuntu-latest\n    steps:\n"
                "      - run: git reset --hard HEAD\n",
                encoding="utf-8",
            )
            report = inspect(root)
            self.assertEqual(report["errors"], [])
            self.assertEqual(report["central_write_violations"], [])
            self.assertEqual(report["review_count"], 1)
            row = report["review_required"][0]
            self.assertTrue(row["inherited_permissions"])
            self.assertFalse(row["write_capability"])
            self.assertIn("git reset", row["risky_commands"][0])

    def test_yazma_hedefi_raporu_salt_okunur(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / ".github" / "workflows"
            folder.mkdir(parents=True)
            (folder / "eski.yml").write_text(
                "name: Eski\non: workflow_dispatch\npermissions:\n  contents: write\n"
                "jobs:\n  job:\n    runs-on: ubuntu-latest\n    steps:\n"
                "      - run: |\n          cp rapor.csv YENILER.m3u\n"
                "          echo veri >> CALISANLAR.m3u\n", encoding="utf-8")
            report = inspect(root)
            self.assertEqual(report["errors"], [])
            hints = report["review_required"][0]["write_target_hints"]
            self.assertIn({"kind": "COPY_MOVE", "target": "YENILER.m3u"}, hints)
            self.assertIn({"kind": "SHELL_REDIRECT", "target": "CALISANLAR.m3u"}, hints)

    def test_salt_okunur_izinle_yazma_hedefi_incelemeye_alinir(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / ".github" / "workflows"
            folder.mkdir(parents=True)
            (folder / "eski.yml").write_text(
                "name: Eski\non: workflow_dispatch\npermissions:\n  contents: read\n"
                "jobs:\n  job:\n    runs-on: ubuntu-latest\n    steps:\n"
                "      - run: cp rapor.csv YENILER.m3u\n", encoding="utf-8")
            report = inspect(root)
            self.assertEqual(report["errors"], [])
            self.assertEqual(report["review_count"], 1)
            self.assertFalse(report["review_required"][0]["write_capability"])
            self.assertIn({"kind": "COPY_MOVE", "target": "YENILER.m3u"},
                          report["review_required"][0]["write_target_hints"])

    def test_environment_isaretleyicisi_gercek_yamlda_algilanir(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / ".github" / "workflows"
            folder.mkdir(parents=True)
            (folder / "legacy.yml").write_text(
                "name: Legacy\non: workflow_dispatch\npermissions:\n  contents: write\n"
                "jobs:\n  publish:\n    runs-on: ubuntu-latest\n"
                "    environment: production\n    steps:\n      - run: echo ok\n",
                encoding="utf-8")
            report = inspect(root)
            self.assertEqual(report["errors"], [])
            self.assertEqual(report["review_count"], 1)
            self.assertTrue(report["review_required"][0]["environment_gate_marker"])

    def test_merkezi_rapor_kanal_listesini_degistirmez(self):
        source = Path("scripts/central_protected_write_gate.py").read_text()
        self.assertNotIn("write_text(content", source)
        self.assertNotIn("git push", source)

if __name__ == "__main__":
    unittest.main()
