import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / 'scripts/k1_protected_integrity.py'


class RuntimeIntegrityTests(unittest.TestCase):
    def test_changes_deletions_and_index_removal_are_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            def git(*args):
                subprocess.run(['git', *args], cwd=root, check=True, capture_output=True)
            git('init', '-q')
            originals = {'YENILER.m3u': b'#EXTM3U\n', 'yedekler/state.json': b'{}',
                         'FAVORILER.json': b'[]', 'AGENTS.md': b'policy'}
            for name, value in originals.items():
                path = root / name
                path.parent.mkdir(exist_ok=True)
                path.write_bytes(value)
            git('add', '.')
            git('-c', 'user.name=Test', '-c', 'user.email=test@example.test', 'commit', '-qm', 'fixture')
            manifest = root / 'baseline.json'
            def run(mode):
                return subprocess.run([sys.executable, str(SCRIPT), '--mode', mode,
                                       '--manifest', str(manifest)], cwd=root, capture_output=True)
            self.assertEqual(run('snapshot').returncode, 0)
            self.assertEqual(run('check').returncode, 0)
            for name, value in originals.items():
                path = root / name
                path.write_bytes(b'changed')
                self.assertNotEqual(run('check').returncode, 0, name)
                self.assertEqual(path.read_bytes(), b'changed')
                path.write_bytes(value)
                path.unlink()
                self.assertNotEqual(run('check').returncode, 0, name)
                path.write_bytes(value)
            git('rm', '--cached', 'YENILER.m3u')
            (root / 'YENILER.m3u').unlink()
            self.assertNotEqual(run('check').returncode, 0)
            (root / 'YENILER.m3u').write_bytes(originals['YENILER.m3u'])
            self.assertEqual(run('check').returncode, 0)
            manifest.unlink()
            self.assertNotEqual(run('check').returncode, 0)
            manifest.write_text('{}')
            self.assertNotEqual(run('check').returncode, 0)


    def test_untracked_protected_file_creation_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            def git(*args):
                subprocess.run(['git', *args], cwd=root, check=True, capture_output=True)
            git('init', '-q')
            (root / 'YENILER.m3u').write_bytes(b'#EXTM3U\n')
            git('add', 'YENILER.m3u')
            git('-c', 'user.name=Test', '-c', 'user.email=test@example.test', 'commit', '-qm', 'fixture')
            manifest = root / 'baseline.json'
            def run(mode):
                return subprocess.run([sys.executable, str(SCRIPT), '--mode', mode,
                                       '--manifest', str(manifest)], cwd=root, capture_output=True, text=True)
            self.assertEqual(run('snapshot').returncode, 0)
            candidate = root / 'madsc_kesif' / 'candidate.m3u'
            candidate.parent.mkdir()
            candidate.write_bytes(b'#EXTM3U\n')
            self.assertEqual(run('check').returncode, 0)
            backup = root / 'YEDEKLER' / 'new.m3u'
            backup.parent.mkdir()
            backup.write_bytes(b'#EXTM3U\n')
            result = run('check')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('YEDEKLER/new.m3u', json.loads(result.stdout)['changed_paths'])
            self.assertEqual(backup.read_bytes(), b'#EXTM3U\n')
            backup.unlink()
            self.assertEqual(run('check').returncode, 0)
            root_playlist = root / 'FAVORILER.m3u'
            root_playlist.write_bytes(b'#EXTM3U\n')
            result = run('check')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('FAVORILER.m3u', json.loads(result.stdout)['changed_paths'])

    def test_nested_protected_paths_and_m3u8_are_classified(self):
        from scripts.k1_protected_integrity import protected
        for name in ("tmp/HEPSI/order.json", "archive/FAVORILER/list.txt",
                     "cache/yedekler/old.txt", "streams/list.m3u8"):
            with self.subTest(path=name):
                self.assertTrue(protected(name))
        self.assertFalse(protected("madsc_kesif/report.json"))

    def test_untracked_nested_protected_file_detected_in_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            def git(*args):
                subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)
            git("init", "-q")
            (root / "AGENTS.md").write_text("policy")
            git("add", "AGENTS.md")
            git("-c", "user.name=Test", "-c", "user.email=test@example.test", "commit", "-qm", "fixture")
            manifest = root / "baseline.json"
            def run(mode):
                return subprocess.run([sys.executable, str(SCRIPT), "--mode", mode,
                                       "--manifest", str(manifest)], cwd=root, capture_output=True, text=True)
            self.assertEqual(run("snapshot").returncode, 0)
            nested = root / "tmp" / "HEPSI" / "state.json"
            nested.parent.mkdir(parents=True)
            nested.write_text("new")
            result = run("check")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("tmp/HEPSI/state.json", json.loads(result.stdout)["changed_paths"])

    def test_general_maintenance_baseline_precedes_regression(self):
        workflow = (ROOT / '.github/workflows/madsc-05-genel-bakim.yml').read_text(encoding='utf-8')
        job = workflow.split('  genel-bakim:', 1)[1]
        self.assertLess(job.index('- name: Korunan dosyalarin baslangic ozeti'),
                        job.index('- name: Cron denetimi regresyon testi'))
        self.assertIn('sha256sum -c "${RUNNER_TEMP}/madsc-protected.sha256"', job)
        self.assertIn('scripts/k1_protected_integrity.py --mode check', job)

    def test_all_categories_have_before_and_always_after_checks(self):
        for path in (ROOT / '.github/workflows').glob('madsc-0*.yml'):
            text = path.read_text()
            self.assertIn('--mode snapshot --manifest', text, path.name)
            self.assertIn('if: always()\n        run: |\n          set -euo pipefail\n          sha256sum -c', text, path.name)
            self.assertIn('--mode check --manifest', text, path.name)
