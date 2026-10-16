"""Exercise the migrated archive lifecycle with isolated, synthetic data."""
import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent


class DiscoveryBehaviorTests(unittest.TestCase):
    def test_archive_lifecycle_preserves_evidence_and_playlists(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            out = root / 'madsc_kesif'
            out.mkdir()
            old = {'url': 'https://example.test/old', 'channel': 'Old',
                   'runs': 4, 'successful_runs': 2, 'last_result': 'EXISTING'}
            (out / 'gecmis.json').write_text(json.dumps({'history': {old['url']: old}}))
            playlists = {'CALISANLAR.m3u': '#EXTM3U\n#EXTINF:-1,Main\nhttps://example.test/main\n',
                         'YABANCI_KANALLAR.m3u': '#EXTM3U\n#EXTINF:-1,Foreign\nhttps://example.test/foreign\n',
                         'YENILER.m3u': '#EXTM3U\n', 'FAVORILER.m3u': '#EXTM3U\n'}
            for name, content in playlists.items():
                (root / name).write_text(content)
            def run(mode):
                subprocess.run([sys.executable, str(ROOT / 'scripts/discovery_archive.py'), mode],
                               cwd=root, check=True, capture_output=True)
            run('before')
            history = json.loads((out / 'gecmis.json').read_text())['history']
            self.assertEqual(history[old['url']], old)
            archived = history['https://example.test/foreign']
            self.assertEqual(archived['successful_runs'], 0)
            self.assertEqual(archived['last_result'], 'ARSIVDE_TEKRAR_TEST_YOK')
            with (out / 'adaylar.csv').open('w', newline='') as handle:
                writer = csv.DictWriter(handle, fieldnames=['kanal', 'url', 'kaynak', 'durum'])
                writer.writeheader()
                for name in ['new', 'main']:
                    writer.writerow(dict(kanal=name, url='https://example.test/' + name,
                                         kaynak='fixture', durum='TEST_ONLY'))
            run('after')
            run('after')
            with (out / 'bulunan_kanal_arsivi.csv').open(encoding='utf-8-sig') as handle:
                rows = list(csv.DictReader(handle))
            urls = [row['url'] for row in rows]
            self.assertEqual(len(urls), len(set(urls)))
            self.assertIn('https://example.test/new', urls)
            self.assertNotIn('https://example.test/main', urls)
            self.assertEqual(json.loads((out / 'gecmis.json').read_text())['history'], history)
            for name, content in playlists.items():
                self.assertEqual((root / name).read_text(), content)

    def test_category_runs_lifecycle_in_legacy_order(self):
        text = (ROOT / '.github/workflows/madsc-02-kesif.yml').read_text()
        commands = ['python3 scripts/discovery_archive.py before',
                    'python3 madsc_akilli_kesif.py',
                    'python3 scripts/discovery_archive.py after',
                    'python3 scripts/four_stage_discovery_report.py']
        positions = [text.index(command) for command in commands]
        self.assertEqual(positions, sorted(positions))
        self.assertIn('set -euo pipefail\n          ' + commands[0], text)
        self.assertIn('contents: read', text)
        self.assertNotIn('git push', text)
