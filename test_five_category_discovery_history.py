import copy
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from scripts import discovery_history_restore as history

T1 = '2026-10-15T08:00:00+00:00'
T2 = '2026-10-16T08:00:00+00:00'


def pair():
    return {'gecmis.json': {'history': {'old': {'runs': 2, 'successful_runs': 2,
                'last_test': T1, 'last_success': T1, 'channel': 'Keep name',
                'user_decision': 'KEEP', 'source_history': ['original']}}},
            'ana_liste_test_gecmisi.json': {'channels': {'1|old': {
                'last_test': T1, 'last_success': T1, 'successful_runs': 2}}}}


def write_pair(folder, data):
    folder.mkdir(parents=True, exist_ok=True)
    for name, doc in data.items():
        (folder / name).write_text(json.dumps(doc))


class DiscoveryHistoryTests(unittest.TestCase):
    def test_merge_preserves_records_metadata_and_newer_failure(self):
        base = pair()
        incoming = pair()
        incoming['gecmis.json']['history']['old'].update(
            runs=3, successful_runs=0, last_test=T2, last_success=None,
            channel='Do not replace metadata', user_decision='CHANGED', source_history=['artifact'])
        incoming['gecmis.json']['history']['new'] = {'runs': 1, 'successful_runs': 0, 'last_test': T2}
        incoming['ana_liste_test_gecmisi.json']['channels']['1|old'].update(
            last_test=T2, last_success=None, successful_runs=0)
        original = copy.deepcopy(base)
        merged, stats = history.merge_pair(base, incoming)
        self.assertEqual(base, original)
        old = merged['gecmis.json']['history']['old']
        self.assertEqual((old['channel'], old['user_decision']), ('Keep name', 'KEEP'))
        self.assertEqual(old['runs'], 3)
        self.assertEqual(old['successful_runs'], 0)
        self.assertEqual(old['source_history'], ['artifact', 'original'])
        self.assertEqual(stats['gecmis.json']['added'], 1)
        self.assertEqual(merged['ana_liste_test_gecmisi.json']['channels']['1|old']['last_test'], T2)
        twice, _ = history.merge_pair(merged, incoming)
        self.assertEqual(twice, merged)
        older, _ = history.merge_pair(merged, original)
        self.assertEqual(older, merged)

    def test_counter_regression_and_equal_timestamp_conflict_fail(self):
        for updates in ({'runs': 1, 'last_test': T2}, {'successful_runs': 0}):
            incoming = pair()
            incoming['gecmis.json']['history']['old'].update(updates)
            with self.assertRaises(ValueError):
                history.merge_pair(pair(), incoming)

    def test_restore_downloads_both_histories_without_touching_playlist(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_pair(root / 'madsc_kesif', pair())
            playlist = root / 'CALISANLAR.m3u'
            playlist.write_bytes(b'#EXTM3U\n')
            incoming = pair()
            incoming['gecmis.json']['history']['new'] = {'runs': 1, 'last_test': T2}
            source = {'id': 123, 'head_sha': 'a' * 40}
            def download(args, **kwargs):
                write_pair(Path(args[-1]) / 'madsc_kesif', incoming)
                return subprocess.CompletedProcess(args, 0)
            with patch.dict(os.environ, {'GITHUB_REPOSITORY': 'o/r', 'GITHUB_REF_NAME': 'branch',
                                         'GITHUB_RUN_ID': '456'}), \
                 patch.object(history, 'find_previous', return_value=source), \
                 patch.object(history.subprocess, 'run', side_effect=download):
                result = history.restore(root)
                self.assertEqual(result['source_run_id'], 123)
                history.restore(root)
            restored = history.load_pair(root / 'madsc_kesif')
            self.assertEqual(restored['gecmis.json']['history']['new']['runs'], 1)
            self.assertEqual(playlist.read_bytes(), b'#EXTM3U\n')
            self.assertNotIn('https://', (root / 'madsc_merkezi_denetim/kesif_gecmis_devamliligi.json').read_text())

    def test_invalid_second_artifact_preserves_both_checkout_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_pair(root / 'madsc_kesif', pair())
            before = {name: (root / 'madsc_kesif' / name).read_bytes() for name in history.FILES}
            def download(args, **kwargs):
                folder = Path(args[-1])
                write_pair(folder, pair())
                (folder / 'ana_liste_test_gecmisi.json').write_text('{}')
            with patch.dict(os.environ, {'GITHUB_REPOSITORY': 'o/r', 'GITHUB_REF_NAME': 'branch',
                                         'GITHUB_RUN_ID': '456'}), \
                 patch.object(history, 'find_previous', return_value={'id': 1, 'head_sha': 'a' * 40}), \
                 patch.object(history.subprocess, 'run', side_effect=download):
                with self.assertRaises(ValueError):
                    history.restore(root)
            for name, content in before.items():
                self.assertEqual((root / 'madsc_kesif' / name).read_bytes(), content)

    def test_selects_successful_ancestor_including_parent_workflow(self):
        def run(number, **updates):
            result = dict(id=number, head_branch='branch', conclusion='success', status='completed',
                          head_repository={'full_name': 'o/r'}, event='push', head_sha='a' * 40,
                          path='.github/workflows/madsc-05-genel-bakim.yml',
                          created_at=f'2026-10-16T08:{number:02}:00Z')
            result.update(updates)
            return result
        def api(repo, endpoint):
            return {'workflow_runs': [run(1, path='.github/workflows/madsc-02-kesif.yml'),
                run(2), run(3, head_branch='other'),
                run(4, head_repository={'full_name': 'fork/r'}), run(5, event='pull_request'),
                run(6, conclusion='failure'), run(7, head_sha='b' * 40), run(8),
                run(9, path='.github/workflows/k1-protected-write-tests.yml')]}
        def ancestry(args, **kwargs):
            return subprocess.CompletedProcess(args, int(args[-2] == 'b' * 40))
        with patch.object(history, 'gh_json', side_effect=api), \
             patch.object(history.subprocess, 'run', side_effect=ancestry):
            self.assertEqual(history.find_previous(Path('.'), 'o/r', 'branch', '8')['id'], 2)

    def test_missing_or_invalid_checkout_never_downloads(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with patch.object(history, 'find_previous') as find:
                with self.assertRaises(FileNotFoundError):
                    history.restore(root)
                find.assert_not_called()

    def test_download_failure_never_resets_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_pair(root / 'madsc_kesif', pair())
            before = {n: (root / 'madsc_kesif' / n).read_bytes() for n in history.FILES}
            with patch.dict(os.environ, {'GITHUB_REPOSITORY': 'o/r', 'GITHUB_REF_NAME': 'branch',
                                         'GITHUB_RUN_ID': '456'}), \
                 patch.object(history, 'find_previous', return_value={'id': 1, 'head_sha': 'a' * 40}), \
                 patch.object(history.subprocess, 'run', side_effect=subprocess.CalledProcessError(1, ['gh'])):
                with self.assertRaises(subprocess.CalledProcessError):
                    history.restore(root)
            for name, content in before.items():
                self.assertEqual((root / 'madsc_kesif' / name).read_bytes(), content)

    def test_bootstrap_retains_checkout_without_empty_initialization(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_pair(root / 'madsc_kesif', pair())
            with patch.dict(os.environ, {'GITHUB_REPOSITORY': 'o/r', 'GITHUB_REF_NAME': 'branch',
                                         'GITHUB_RUN_ID': '456'}), \
                 patch.object(history, 'find_previous', return_value=None):
                self.assertEqual(history.restore(root)['mode'], 'CHECKOUT_BOOTSTRAP')
            self.assertEqual(history.load_pair(root / 'madsc_kesif'), pair())
