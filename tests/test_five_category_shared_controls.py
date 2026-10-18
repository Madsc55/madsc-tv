"""Cross-category shared control regression checks."""
import tempfile
import unittest
from pathlib import Path
from scripts.five_category_shared_controls import CATEGORIES, inspect

class SharedControlsTests(unittest.TestCase):
    def test_shared_control_references_across_five_categories(self):
        report = inspect()
        self.assertEqual(set(report["shared_controls"]["protected_integrity"]["consumers"]), set(CATEGORIES))
        self.assertEqual(report["status"], "STATIC_READY", report["missing_consumers"])

    def test_five_integrity_phases(self):
        root = Path(__file__).resolve().parents[1]
        for name in CATEGORIES.values():
            raw = (root / ".github" / "workflows" / name).read_text(encoding="utf-8")
            with self.subTest(name=name):
                self.assertIn("--mode snapshot", raw)
                self.assertIn("--mode check", raw)
                self.assertIn("sha256sum -c", raw)

    def test_comments_do_not_count_as_executed_controls(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / ".github" / "workflows"
            folder.mkdir(parents=True)
            for name in CATEGORIES.values():
                (folder / name).write_text("# scripts/k1_protected_integrity.py\\n", encoding="utf-8")
            report = inspect(root)
            self.assertEqual(report["status"], "BLOCKED")
            self.assertFalse(report["shared_controls"]["protected_integrity"]["all_consumers_present"])

    def test_real_python_invocations_are_recognized(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / ".github" / "workflows"
            folder.mkdir(parents=True)
            for name in CATEGORIES.values():
                lines = ["name: fixture", "run: |", "  python3 scripts/k1_protected_integrity.py --mode snapshot", "  python3 scripts/k1_protected_integrity.py --mode check", "  sha256sum -c checksum.txt"]
                if name == CATEGORIES["K5"]:
                    lines += ["  python3 scripts/category_evidence_collect.py", "  python3 scripts/five_system_cutover_readiness.py"]
                (folder / name).write_text(chr(10).join(lines) + chr(10), encoding="utf-8")
            result = inspect(root)
            self.assertEqual(result["status"], "STATIC_READY", result["missing_consumers"])

    def test_inline_run_commands_are_recognized(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / ".github" / "workflows"
            folder.mkdir(parents=True)
            for name in CATEGORIES.values():
                lines = ["name: fixture", "run: |", "  python3 scripts/k1_protected_integrity.py --mode snapshot", "  python3 scripts/k1_protected_integrity.py --mode check", "  sha256sum -c checksum.txt"]
                if name == CATEGORIES["K5"]:
                    lines += ["- run: python3 scripts/category_evidence_collect.py", "  python3 scripts/five_system_cutover_readiness.py"]
                (folder / name).write_text(chr(10).join(lines) + chr(10), encoding="utf-8")
            result = inspect(root)
            self.assertEqual(result["status"], "STATIC_READY", result["missing_consumers"])

    def test_missing_k5_evidence_blocks_shared_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / ".github" / "workflows"
            folder.mkdir(parents=True)
            for name in CATEGORIES.values():
                commands = ["python3 scripts/k1_protected_integrity.py --mode snapshot", "python3 scripts/k1_protected_integrity.py --mode check", "sha256sum -c checksum.txt"]
                if name == CATEGORIES["K5"]:
                    commands += ["python3 scripts/five_system_cutover_readiness.py"]
                (folder / name).write_text(chr(10).join(commands) + chr(10), encoding="utf-8")
            result = inspect(root)
            self.assertEqual(result["status"], "BLOCKED")
            self.assertEqual(result["missing_consumers"], [{"control": "category_evidence", "category": "K5", "workflow": CATEGORIES["K5"]}])

    def test_missing_checksum_blocks_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / ".github" / "workflows"
            folder.mkdir(parents=True)
            for name in CATEGORIES.values():
                lines = ["python3 scripts/k1_protected_integrity.py --mode snapshot", "python3 scripts/k1_protected_integrity.py --mode check", "sha256sum -c checksum.txt"]
                if name == CATEGORIES["K3"]:
                    lines.pop()
                if name == CATEGORIES["K5"]:
                    lines.extend(["python3 scripts/category_evidence_collect.py", "python3 scripts/five_system_cutover_readiness.py"])
                (folder / name).write_text(chr(10).join(lines), encoding="utf-8")
            report = inspect(Path(tmp))
            self.assertEqual(report["status"], "BLOCKED")
            self.assertFalse(report["shared_controls"]["protected_integrity"]["consumers"]["K3"])

    def test_missing_consumer_blocks_all_category_acceptance(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / ".github" / "workflows"
            folder.mkdir(parents=True)
            for name in CATEGORIES.values():
                (folder / name).write_text("name: placeholder\n", encoding="utf-8")
            report = inspect(root)
            self.assertEqual(report["status"], "BLOCKED")
            self.assertEqual(len(report["shared_controls"]["protected_integrity"]["consumers"]), 5)
            self.assertTrue(report["missing_consumers"])

if __name__ == "__main__":
    unittest.main()
