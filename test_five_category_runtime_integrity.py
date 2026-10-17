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

    def test_all_categories_have_before_and_always_after_checks(self):
        for path in (ROOT / '.github/workflows').glob('madsc-0*.yml'):
            text = path.read_text()
            self.assertIn('--mode snapshot --manifest', text, path.name)
            self.assertIn('if: always()\n        run: |\n          set -euo pipefail\n          sha256sum -c', text, path.name)
            self.assertIn('--mode check --manifest', text, path.name)
