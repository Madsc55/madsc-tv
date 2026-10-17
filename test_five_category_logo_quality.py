"""Preserve the legacy Test 15 warning contract in category three."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest
from tools.logo_epg_audit import audit

ROOT = Path(__file__).resolve().parent


class LogoQualityTests(unittest.TestCase):
    def test_legacy_warning_contract(self):
        sample = ('#EXTM3U\n'
                  '#EXTINF:-1 tvg-id="same" tvg-logo="https://example.com/a.png",One\n'
                  'https://example.com/stream1\n'
                  '#EXTINF:-1 tvg-id="SAME" tvg-logo="",Two\n'
                  'https://example.com/stream2\n'
                  '#EXTINF:-1 tvg-logo="bad-path",Three\n'
                  'https://example.com/stream3\n')
        result = audit(sample)
        self.assertEqual(result['channels_checked'], 3)
        kinds = [w['type'] for w in result['warnings']]
        self.assertEqual(kinds.count('duplicate_tvg_id'), 1)
        for kind in ('missing_logo', 'missing_tvg_id', 'suspicious_logo_url'):
            self.assertIn(kind, kinds)
        self.assertEqual(audit('#EXTM3U')['channels_checked'], 0)
        with tempfile.TemporaryDirectory() as tmp:
            playlist = Path(tmp) / 'CALISANLAR.m3u'
            playlist.write_text(sample, encoding='utf-8-sig')
            before = playlist.read_bytes()
            run = subprocess.run([sys.executable, str(ROOT / 'tools/logo_epg_audit.py'), str(playlist)],
                                 check=True, capture_output=True, text=True)
            self.assertEqual(json.loads(run.stdout)['channels_checked'], 3)
            self.assertEqual(playlist.read_bytes(), before)

    def test_category_gate_and_artifact_are_connected(self):
        workflow = (ROOT / '.github/workflows/madsc-03-kanal-test.yml').read_text()
        self.assertIn('tools/logo_epg_audit.py CALISANLAR.m3u > madsc_merkezi_denetim/logo_epg_kalite.json', workflow)
        self.assertIn('steps.logo_quality.outcome', workflow)
        self.assertIn('REPORTS LOGO_QUALITY EPG', workflow)
        self.assertIn('report["channels_checked"] == count > 0', workflow)
