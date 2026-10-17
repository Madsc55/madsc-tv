"""Run the existing disaster drill against an isolated Git repository."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent


class DisasterBehaviorTests(unittest.TestCase):
    def test_real_drill_restores_copies_and_rejects_dirty_original(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            def git(*args):
                subprocess.run(['git', *args], cwd=root, check=True, capture_output=True)
            git('init', '-q')
            original = b'#EXTM3U\n#EXTINF:-1,Fixture\nhttps://example.test/live\n'
            for name in ['CALISANLAR.m3u', 'YENILER.m3u']:
                (root / name).write_bytes(original)
            git('add', '.')
            git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.test',
                'commit', '-qm', 'fixture')
            command = [sys.executable, str(ROOT / 'scripts/disaster_recovery_dry_run.py')]
            subprocess.run(command, cwd=root, check=True, capture_output=True)
            report = json.loads((root / 'DISASTER-RECOVERY-REPORT.json').read_text())
            self.assertEqual(report['status'], 'PASS')
            self.assertEqual(len(report['files']), 2)
            for item in report['files']:
                self.assertEqual(item['simulated_damage'], 'detected')
                self.assertEqual(item['restore'], 'PASS')
                self.assertTrue(item['original_untouched'])
                self.assertEqual((root / item['file']).read_bytes(), original)
            dirty = original + b'# user change\n'
            (root / 'YENILER.m3u').write_bytes(dirty)
            result = subprocess.run(command, cwd=root, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual((root / 'YENILER.m3u').read_bytes(), dirty)

    def test_category_retains_drill_artifact_and_acceptance(self):
        workflow = (ROOT / '.github/workflows/madsc-04-arsiv-yedek.yml').read_text()
        self.assertIn('scripts/disaster_recovery_dry_run.py; do', workflow)
        self.assertIn('DISASTER-RECOVERY-REPORT.json', workflow)
        self.assertIn('recovery["status"] == "PASS"', workflow)
        self.assertIn('contents: read', workflow)
