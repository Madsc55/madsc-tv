import ast
import collections
import csv
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from scripts import category_candidate_media as media
from scripts import category_candidate_scoring as scoring

ROOT = Path(__file__).parent
URL = 'https://example.test/a'


def fixture(folder, at=None, state='VIDEO_SES_VAR', priority_at=None):
    folder.mkdir(parents=True, exist_ok=True)
    at = at or dt.datetime.now(dt.timezone.utc).isoformat()
    row = dict(KANAL='Fixture', YAYIN_URL=URL, TEKNIK_MEDYA=state, OLCUM_ZAMANI=at,
               SES_IZI=str(state == 'VIDEO_SES_VAR'), COZUNURLUK='', KAYNAK='fixture')
    for kind, filename in media.FILES.items():
        current = {**row, 'OLCUM_ZAMANI': priority_at or at} if kind == 'priority' else row
        with (folder / filename).open('w', encoding='utf-8-sig', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=list(current)); writer.writeheader(); writer.writerow(current)
    (folder / media.SUMMARIES[0]).write_text(json.dumps({'toplam': 1, 'sonuclar': {state: 1}}))
    (folder / media.SUMMARIES[1]).write_text(json.dumps({'test_edilen': 0, 'yeniden_kullanilan': 1, 'sonuclar': {state: 1}}))
    manifest = {'schema': 1, 'playlist_write': False, 'device_approval': False, 'hashes': {name: hashlib.sha256((folder / name).read_bytes()).hexdigest()
                                     for name in (*media.FILES.values(), *media.SUMMARIES)}}
    (folder / 'kabul.json').write_text(json.dumps(manifest))
    return manifest


class CandidateMediaTests(unittest.TestCase):
    def test_timestamp_cache_boundary_and_hash_corruption_fail_closed(self):
        now = dt.datetime.now(dt.timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            fixture(folder, now.isoformat())
            self.assertTrue(media.load_cache(folder, now)[2])
            self.assertFalse(media.load_cache(folder, now + dt.timedelta(hours=6))[2])
            (folder / media.FILES['priority']).write_text('changed')
            with self.assertRaises(ValueError): media.load_cache(folder, now)

    def test_schema_unknown_future_or_missing_timestamp_is_not_media_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            for value, state in (('', 'VIDEO_SES_VAR'), ('2099-01-01T00:00:00+00:00', 'VIDEO_SES_VAR'),
                                  ('2026-10-16T12:00:00+00:00', 'TEST_EDILMEDI')):
                fixture(folder, at=value or 'bad', state=state)
                with self.assertRaises(ValueError): media.load_cache(folder)

    def test_existing_scripts_first_run_then_real_timestamp_reuse_without_probe(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'scripts').mkdir()
            for name in ('scripts/oncelikli_kanal_dogrula.py', 'scripts/genel_aday_medya_test.py', 'yeni_kanal_tara.py'):
                (root / name).write_text('# fixture generator')
            (root / 'CALISANLAR.m3u').write_bytes(b'#EXTM3U\n')
            def execute(r, folder): fixture(folder)
            with patch.dict(os.environ, dict(GITHUB_REPOSITORY='o/r', GITHUB_REF_NAME='branch', GITHUB_RUN_ID='1')), \
                 patch.object(media, 'previous', return_value=None), \
                 patch.object(media, 'execute', side_effect=execute), \
                 patch.object(media.subprocess, 'check_output', return_value='a' * 40):
                first = media.prepare(root)
            self.assertEqual(first['network_media_probes'], 1)
            saved = root / 'saved'; shutil.copytree(root / 'madsc_aday_medya', saved)
            original = (saved / media.FILES['priority']).read_bytes()
            shutil.rmtree(root / 'madsc_aday_medya')
            def previous(r, dest):
                shutil.copytree(saved, dest / 'madsc_aday_medya'); return {'id': 1}
            with patch.dict(os.environ, dict(GITHUB_RUN_ID='2')), \
                 patch.object(media, 'previous', side_effect=previous), \
                 patch.object(media, 'execute') as probes, \
                 patch.object(media.subprocess, 'check_output', return_value='b' * 40):
                second = media.prepare(root)
            probes.assert_not_called()
            self.assertEqual(second['network_media_probes'], 0)
            self.assertEqual(second['origin_run_id'], '1')
            self.assertEqual(second['run_id'], '2')
            self.assertEqual((root / 'madsc_aday_medya' / media.FILES['priority']).read_bytes(), original)
            self.assertEqual((root / 'CALISANLAR.m3u').read_bytes(), b'#EXTM3U\n')

    def test_general_probe_reuses_priority_without_ffprobe_or_retiming(self):
        source = ROOT / 'scripts/genel_aday_medya_test.py'
        node = next(n for n in ast.parse(source.read_text()).body if isinstance(n, ast.FunctionDef) and n.name == 'probe')
        stamp = dt.datetime.now(dt.timezone.utc).isoformat()
        previous = dict(TEKNIK_MEDYA='DOGRULANAMADI', COZUNURLUK='', SES_IZI='False', HATA='fixture', OLCUM_ZAMANI=stamp)
        subprocess = SimpleNamespace(run=Mock())
        ns = dict(reuse={URL: previous}, subprocess=subprocess, datetime=dt, json=json)
        exec(compile(ast.Module(body=[node], type_ignores=[]), str(source), 'exec'), ns)
        result = ns['probe']({'YAYIN_URL': URL})
        subprocess.run.assert_not_called()
        self.assertEqual(result['OLCUM_ZAMANI'], stamp)
        self.assertEqual(result['TEKNIK_MEDYA'], 'DOGRULANAMADI')
        ns['reuse'] = {}
        subprocess.run.return_value = SimpleNamespace(returncode=1, stderr='failed')
        actual = ns['probe']({'YAYIN_URL': URL})
        self.assertIsNotNone(dt.datetime.fromisoformat(actual['OLCUM_ZAMANI']).tzinfo)
        self.assertEqual(actual['TEKNIK_MEDYA'], 'DOGRULANAMADI')

    def test_new_failure_replaces_old_positive_and_history_still_keeps_both(self):
        now = dt.datetime.now(dt.timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); k2 = root / 'madsc_kesif'; k2.mkdir()
            with (k2 / 'adaylar.csv').open('w', newline='') as handle:
                writer = csv.DictWriter(handle, fieldnames=['kanal', 'url', 'video', 'ses', 'durum', 'cozunurluk'])
                writer.writeheader(); writer.writerow(dict(kanal='Old positive', url=URL, video=True, ses=True,
                                                            durum='TEKNIK', cozunurluk='1920x1080'))
            (k2 / 'gecmis.json').write_text(json.dumps({'history': {'key': {'url': URL,
                                  'last_test': (now - dt.timedelta(hours=1)).isoformat()}}}))
            folder = root / 'media'; fixture(folder, now.isoformat(), 'DOGRULANAMADI')
            result = scoring.build_reports(root, root / 'out', history={}, media_folder=folder)
            self.assertEqual(result['new_observations'], 2)
            self.assertEqual(result['reused_measurements_not_added'], 1)
            with (root / 'out/AKILLI_ADAY_PUANLARI.csv').open(encoding='utf-8-sig') as handle:
                scores = list(csv.DictReader(handle))
            self.assertEqual(len(scores), 1)
            self.assertEqual(scores[0]['TEKNIK_KANIT'], 'DOGRULANAMADI')
            self.assertEqual(scores[0]['PUAN'], '0')
            self.assertEqual(scores[0]['ANA_LISTEYE_EKLENEBILIR'], 'HAYIR')
            history = json.loads((root / 'out/KARARLILIK_GECMISI.json').read_text())
            self.assertEqual(len(history[URL]), 2)

    def test_execute_uses_existing_discovery_only_mode_and_isolated_read_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); folder = root / 'work'; folder.mkdir()
            (root / 'CALISANLAR.m3u').write_bytes(b'#EXTM3U\n')
            calls = []
            def run(args, **kwargs):
                calls.append((args, kwargs))
                if len(calls) == 1: fixture(folder)
            with patch.object(media.subprocess, 'run', side_effect=run): media.execute(root, folder)
            self.assertEqual(len(calls), 3)
            self.assertEqual(calls[1][1]['env']['SCAN_BATCH'], '-1')
            self.assertEqual(calls[2][1]['env']['ADAY_TEST_GRUBU'], '0')
            self.assertEqual(calls[2][1]['env']['MADSC_MEDYA_SKIP_CSV'], str(folder / media.FILES['priority']))
            self.assertTrue(all(call[1]['cwd'] == folder for call in calls))
            self.assertEqual((root / 'CALISANLAR.m3u').read_bytes(), b'#EXTM3U\n')

    def test_previous_artifact_wrong_head_or_missing_integrated_reports_is_rejected(self):
        source = dict(id=123, head_sha='a' * 40)
        good = dict(name=media.ARTIFACT, expired=False, workflow_run=dict(id=123, head_sha='a' * 40))
        cases = [('wrong_head', {**good, 'workflow_run': dict(id=123, head_sha='b' * 40)}),
                 ('expired', {**good, 'expired': True}), ('missing_reports', good)]
        for name, artifact in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                with patch.dict(os.environ, dict(GITHUB_REPOSITORY='o/r', GITHUB_REF_NAME='branch', GITHUB_RUN_ID='456')), \
                     patch.object(media, 'find_previous', return_value=source), \
                     patch.object(media, 'gh_json', return_value={'artifacts': [artifact]}), \
                     patch.object(media.subprocess, 'check_output', return_value='marker'), \
                     patch.object(media.subprocess, 'run') as download:
                    with self.assertRaises(ValueError): media.previous(root, root)
                    if name != 'missing_reports': download.assert_not_called()

    def test_missing_timestamp_schema_never_falls_back_to_now(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp); fixture(folder)
            path = folder / media.FILES['priority']
            content = path.read_text(encoding='utf-8-sig').replace('OLCUM_ZAMANI', 'ESKI_BASLIK')
            path.write_text(content, encoding='utf-8-sig')
            with self.assertRaises(ValueError): media.reports(folder)
            self.assertNotIn('OLCUM_ZAMANI', path.read_text())

    def test_valid_hash_does_not_hide_bad_summary_or_forbidden_approval(self):
        for case in ('summary', 'approval'):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as tmp:
                folder = Path(tmp); manifest = fixture(folder)
                if case == 'summary':
                    path = folder / media.SUMMARIES[1]
                    summary = json.loads(path.read_text()); summary['sonuclar'] = {'DOGRULANAMADI': 1}
                    path.write_text(json.dumps(summary))
                    manifest['hashes'][path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
                else:
                    manifest['device_approval'] = True
                (folder / 'kabul.json').write_text(json.dumps(manifest))
                with self.assertRaises(ValueError): media.load_cache(folder)

    def test_workflow_gates_media_before_scoring_and_publishes_isolated_files(self):
        workflow = (ROOT / '.github/workflows/madsc-03-kanal-test.yml').read_text()
        self.assertLess(workflow.index('id: media'), workflow.index('id: scoring'))
        self.assertIn('steps.media.outcome', workflow)
        self.assertIn('COVERAGE MEDIA SCORING REGRESSIONS', workflow)
        self.assertIn('madsc_aday_medya/', workflow)
