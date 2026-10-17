import csv
import datetime as dt
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import contextlib

from scripts import category_candidate_scoring as scoring

ROOT = Path(__file__).resolve().parent


def csv_write(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8-sig', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


class CandidateScoringTests(unittest.TestCase):
    def test_real_scoring_and_combined_scripts_keep_approval_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            csv_write(root / 'madsc_kesif/adaylar.csv', [dict(kanal='Technical', url='https://example.test/a',
                      video='True', ses='True', durum='TEKNIK_ONAY_BEKLIYOR', cozunurluk='1920x1080', kaynak='fixture'),
                      dict(kanal='Deferred', url='https://example.test/b', video='True', ses='True',
                           durum='SONRAKI_TEST_BEKLIYOR', cozunurluk='1920x1080', kaynak='fixture')],
                      ['kanal', 'url', 'video', 'ses', 'durum', 'cozunurluk', 'kaynak'])
            review = root / 'madsc_genis_tarama/candidate_review.json'
            review.parent.mkdir()
            review.write_text(json.dumps({'candidates': {'new': {'name': 'Unverified', 'url': 'https://example.test/c'}}}))
            playlist = root / 'CALISANLAR.m3u'
            playlist.write_bytes(b'#EXTM3U\n')
            with contextlib.redirect_stdout(io.StringIO()):
                result = scoring.build_reports(root, root / 'output')
            self.assertEqual(result['scored_candidates'], 3)
            self.assertEqual(result['explicit_media_rows'], 1)
            self.assertEqual(result['additional_media_probes'], 0)
            with (root / 'output/AKILLI_ADAY_PUANLARI.csv').open(encoding='utf-8-sig') as handle:
                scores = {row['KANAL']: row for row in csv.DictReader(handle)}
            self.assertEqual(scores['Technical']['TEKNIK_KANIT'], 'VIDEO_SES_VAR')
            self.assertEqual(scores['Technical']['PUAN'], '45')
            self.assertEqual(scores['Deferred']['TEKNIK_KANIT'], 'TEST_EDILMEDI')
            self.assertEqual(scores['Unverified']['PUAN'], '0')
            self.assertTrue(all(row['ANA_LISTEYE_EKLENEBILIR'] == 'HAYIR' for row in scores.values()))
            self.assertEqual(playlist.read_bytes(), b'#EXTM3U\n')

    def test_actual_priority_filename_merges_technical_evidence_into_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fields = ['KANAL', 'YAYIN_URL', 'TEKNIK_MEDYA', 'COZUNURLUK', 'LOGO_ADAY_URL']
            csv_write(root / 'discovery.csv', [dict(KANAL='Original', YAYIN_URL='https://example.test/a',
                      TEKNIK_MEDYA='TEST_EDILMEDI', COZUNURLUK='', LOGO_ADAY_URL='https://example.test/logo.png')], fields)
            csv_write(root / 'ONCELIKLI_KANAL_TEK_NIK_RAPOR.csv', [dict(KANAL='Probe label',
                      YAYIN_URL='https://example.test/a', TEKNIK_MEDYA='VIDEO_SES_VAR',
                      COZUNURLUK='1920x1080', LOGO_ADAY_URL='')], fields)
            subprocess.run([sys.executable, str(ROOT / 'scripts/akilli_aday_puanla.py'), 'discovery.csv',
                            'ONCELIKLI_KANAL_TEK_NIK_RAPOR.csv'], cwd=root, check=True, capture_output=True)
            with (root / 'AKILLI_ADAY_PUANLARI.csv').open(encoding='utf-8-sig') as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]['KANAL'], 'Original')
            self.assertEqual(rows[0]['PUAN'], '50')
            self.assertEqual(rows[0]['ANA_LISTEYE_EKLENEBILIR'], 'HAYIR')

    def test_corrupt_stability_history_is_preserved_and_never_reset(self):
        for corrupt in ('{broken', '[]', '{"url":{}}', '{"url":[{"at":"bad","state":"VIDEO_SES_VAR"}]}'):
            with self.subTest(corrupt=corrupt), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                path = root / 'KARARLILIK_GECMISI.json'
                path.write_text(corrupt)
                csv_write(root / 'ONCELIKLI_KANAL_TEK_NIK_RAPOR.csv', [], ['YAYIN_URL', 'TEKNIK_MEDYA'])
                run = subprocess.run([sys.executable, str(ROOT / 'scripts/kanal_kararlilik_takip.py')],
                                     cwd=root, capture_output=True)
                self.assertNotEqual(run.returncode, 0)
                self.assertEqual(path.read_text(), corrupt)

    def test_stability_needs_24_hours_and_no_intervening_failure(self):
        for failed in (False, True):
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                now = dt.datetime.now(dt.timezone.utc)
                observations = [{'at': (now - dt.timedelta(hours=25)).isoformat(), 'state': 'VIDEO_SES_VAR'}]
                if failed:
                    observations.append({'at': (now - dt.timedelta(hours=12)).isoformat(), 'state': 'DOGRULANAMADI'})
                (root / 'KARARLILIK_GECMISI.json').write_text(json.dumps({'https://example.test/a': observations}))
                csv_write(root / 'ONCELIKLI_KANAL_TEK_NIK_RAPOR.csv',
                          [{'YAYIN_URL': 'https://example.test/a', 'TEKNIK_MEDYA': 'VIDEO_SES_VAR'}],
                          ['YAYIN_URL', 'TEKNIK_MEDYA'])
                subprocess.run([sys.executable, str(ROOT / 'scripts/kanal_kararlilik_takip.py')],
                               cwd=root, check=True, capture_output=True)
                with (root / 'KARARLILIK_RAPORU.csv').open(encoding='utf-8-sig') as handle:
                    result = next(csv.DictReader(handle))
                self.assertEqual(result['24_SAAT_KARARLI'], 'HAYIR' if failed else 'EVET')
                self.assertEqual(result['ANA_LISTEYE_EKLENEBILIR'], 'HAYIR')

    def test_failed_current_k2_is_not_used_as_evidence(self):
        metadata = dict(path='.github/workflows/madsc-05-genel-bakim.yml', head_sha='a' * 40,
                        head_branch='branch', head_repository={'full_name': 'o/r'})
        def api(repo, endpoint):
            if '/jobs' in endpoint:
                return {'jobs': [{'name': 'MADSC 02 - Kanal Kesfi Toplu', 'conclusion': 'failure'}]}
            return metadata
        with patch.dict(os.environ, {'GITHUB_REPOSITORY': 'o/r', 'GITHUB_REF_NAME': 'branch', 'GITHUB_RUN_ID': '1'}), \
             patch.object(scoring, 'gh_json', side_effect=api), \
             patch.object(scoring.subprocess, 'check_output', return_value='a' * 40 + '\n'):
            with self.assertRaises(ValueError):
                scoring.source_run(Path('.'))

    def test_current_category_acceptance_and_workflow_gate(self):
        workflow = (ROOT / '.github/workflows/madsc-03-kanal-test.yml').read_text()
        self.assertIn('scripts/category_candidate_scoring.py', workflow)
        self.assertIn('steps.scoring.outcome', workflow)
        self.assertIn('madsc_aday_puanlama/', workflow)
