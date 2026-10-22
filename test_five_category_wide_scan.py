import contextlib
import copy
import io
import json
import os
from pathlib import Path
import runpy
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from scripts import wide_source_scan as wide

ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / 'tools/genis_kaynak_taramasi.py'


class WideScanTests(unittest.TestCase):
    def test_real_scanner_modes_keep_queue_and_last_good_hashes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'madsc_akilli_kesif.py').write_text("SOURCES={'fixture-KIBRIS':'https://example.test/tr','fixture-ISVEC':'https://example.test/se','fixture-TR':'https://example.test/daily'}")
            playlist = root / 'CALISANLAR.m3u'
            playlist.write_text('#EXTM3U\n#EXTINF:-1,Keep\nhttps://example.test/keep\n')
            before = playlist.read_bytes()
            def fetch(request, **kwargs):
                return io.BytesIO(b'#EXTM3U\n#EXTINF:-1,New\nhttps://example.test/new\n')
            def invoke(mode, failure=False):
                with contextlib.chdir(root), patch.dict(os.environ, {'MADSC_SCAN_MODE': mode}), \
                     patch('urllib.request.urlopen', side_effect=OSError('fixture') if failure else fetch), \
                     contextlib.redirect_stdout(io.StringIO()):
                    runpy.run_path(str(SCRIPT), run_name='__main__')
                return json.loads((root / 'madsc_genis_tarama' / ('summary_' + mode + '.json')).read_text())
            weekly = invoke('weekly')
            self.assertEqual(weekly['checked'], 2)
            self.assertEqual(weekly['new_identity_review_candidates'], 1)
            monthly = invoke('monthly')
            self.assertEqual(monthly['checked'], 3)
            self.assertEqual(monthly['new_identity_review_candidates'], 0)
            state = wide.read_documents(root / 'madsc_genis_tarama')
            self.assertEqual(len(state['state.json']), 3)
            invoke('monthly', failure=True)
            self.assertEqual(wide.read_documents(root / 'madsc_genis_tarama'), state)
            self.assertEqual(playlist.read_bytes(), before)

    def test_three_way_merge_never_silently_overwrites_changes(self):
        ancestor = wide.empty_documents()
        ancestor['state.json']['a'] = {'digest': 'old'}
        checkout = copy.deepcopy(ancestor)
        incoming = copy.deepcopy(ancestor)
        incoming['state.json']['a'] = {'digest': 'new'}
        incoming['candidate_review.json']['candidates']['new'] = {'status': 'REVIEW'}
        merged = wide.merge_documents(checkout, incoming, ancestor)
        self.assertEqual(merged, incoming)
        self.assertEqual(wide.merge_documents(merged, incoming, ancestor), merged)
        checkout['state.json']['a'] = {'digest': 'repository update'}
        with self.assertRaises(ValueError):
            wide.merge_documents(checkout, incoming, ancestor)
        self.assertEqual(wide.merge_documents(checkout, ancestor, ancestor), checkout)
        checkout['state.json']['repository-only'] = {'digest': 'keep'}
        incoming['state.json'].pop('a')
        result = wide.merge_documents(checkout, incoming, ancestor)
        self.assertEqual(result['state.json'], checkout['state.json'])

    def test_incomplete_or_invalid_state_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertIsNone(wide.read_documents(root))
            (root / 'state.json').write_text('{}')
            with self.assertRaises(ValueError):
                wide.read_documents(root)
            (root / 'candidate_review.json').write_text('{"candidates":[]}')
            with self.assertRaises(ValueError):
                wide.read_documents(root)

    def test_wrapper_runs_both_modes_in_order_and_rejects_zero_access(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / 'madsc_genis_tarama'
            folder.mkdir()
            seen = []
            def scanner(args, **kwargs):
                mode = kwargs['env']['MADSC_SCAN_MODE']
                seen.append(mode)
                summary = dict(mode=mode, configured=3, checked=2, accessible=1, changed=1,
                               new_identity_review_candidates=1)
                (folder / ('summary_' + mode + '.json')).write_text(json.dumps(summary))
            with patch.object(wide, 'restore_state', return_value=12), \
                 patch.object(wide.subprocess, 'run', side_effect=scanner), \
                 contextlib.redirect_stdout(io.StringIO()):
                result = wide.run('both', root)
                self.assertEqual(seen, ['weekly', 'monthly'])
                self.assertFalse(result['playlist_write'])
                self.assertFalse(result['main_dispatch'])
                wide.run('none', root)
                self.assertEqual(len(seen), 2)
            with patch.object(wide, 'restore_state', return_value=12), \
                 patch.object(wide.subprocess, 'run'):
                (folder / 'summary_weekly.json').write_text(json.dumps(dict(mode='weekly', configured=3,
                                                                            checked=2, accessible=0)))
                with self.assertRaises(ValueError):
                    wide.run('weekly', root)

    def test_workflow_wires_modes_failure_gate_and_artifact(self):
        category = (ROOT / '.github/workflows/madsc-02-kesif.yml').read_text()
        parent = (ROOT / '.github/workflows/madsc-05-genel-bakim.yml').read_text()
        self.assertIn('reports discovery wide regressions;', category)
        self.assertIn('madsc_genis_tarama/', category)
        self.assertIn('steps.wide.outcome', category)
        self.assertIn("github.event_name == 'push' && 'both'", parent)
        self.assertIn("inputs.wide_scan_mode || 'none'", parent)
        self.assertNotIn('git push', category)

    def test_artifact_state_survives_two_restores_and_incomplete_pair_is_not_written(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / 'madsc_genis_tarama'
            folder.mkdir()
            for name, doc in wide.empty_documents().items():
                (folder / name).write_text(json.dumps(doc))
            incoming = wide.empty_documents()
            incoming['state.json']['source'] = {'digest': 'retained'}
            incoming['candidate_review.json']['candidates']['candidate'] = {'status': 'REVIEW'}
            source = {'id': 12, 'head_sha': 'a' * 40}
            invalid = False
            def command(args, **kwargs):
                if args[:3] == ['gh', 'run', 'download']:
                    downloaded = Path(args[-1]) / 'madsc_genis_tarama'
                    downloaded.mkdir()
                    for name, doc in incoming.items():
                        if not (invalid and name == 'candidate_review.json'):
                            (downloaded / name).write_text(json.dumps(doc))
                return subprocess.CompletedProcess(args, 0, stdout='')
            with patch.dict(os.environ, {'GITHUB_REPOSITORY': 'o/r', 'GITHUB_REF_NAME': 'b', 'GITHUB_RUN_ID': '13'}), \
                 patch.object(wide, 'find_previous', return_value=source), \
                 patch.object(wide.subprocess, 'run', side_effect=command):
                self.assertEqual(wide.restore_state(root), 12)
                self.assertEqual(wide.restore_state(root), 12)
                self.assertEqual(wide.read_documents(folder), incoming)
                before = {name: (folder / name).read_bytes() for name in wide.FILES}
                invalid = True
                with self.assertRaises(ValueError):
                    wide.restore_state(root)
                for name, data in before.items():
                    self.assertEqual((folder / name).read_bytes(), data)
