import csv
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import category_stability_history as continuity
from scripts import category_candidate_scoring as scoring
from scripts.kanal_kararlilik_takip import track

NOW = dt.datetime(2026, 10, 16, 12, tzinfo=dt.timezone.utc)
URL = 'https://example.test/stream'


def row(hours=0, state='VIDEO_SES_VAR'):
    return dict(KANAL='Fixture', YAYIN_URL=URL, TEKNIK_MEDYA=state,
                OLCUM_ZAMANI=(NOW - dt.timedelta(hours=hours)).isoformat())


class StabilityHistoryTests(unittest.TestCase):
    def test_real_25_hour_evidence_is_used_once_and_never_auto_approves(self):
        history, _, _ = track([row(25)], {}, NOW, True)
        history, report, counts = track([row()], history, NOW, True)
        self.assertEqual(report[0]['24_SAAT_KARARLI'], 'EVET')
        self.assertEqual(report[0]['IBO_ONAYI'], 'YOK')
        self.assertEqual(report[0]['ANA_LISTEYE_EKLENEBILIR'], 'HAYIR')
        again, report2, counts = track([row()], history, NOW + dt.timedelta(hours=2), True)
        self.assertEqual(again, history)
        self.assertEqual(counts['new_observations'], 0)
        self.assertEqual(counts['reused_measurements_not_added'], 1)
        self.assertEqual(report2[0]['BASARILI_ARALIK_SAAT'], 25)

    def test_single_measurement_cannot_age_into_two_observations(self):
        history, _, _ = track([row()], {}, NOW, True)
        _, report, counts = track([row()], history, NOW + dt.timedelta(hours=25), True)
        self.assertEqual(counts['new_observations'], 0)
        self.assertEqual(report[0]['24_SAAT_KARARLI'], 'HAYIR')
        self.assertEqual(report[0]['GOZLEM_SAYISI'], 1)

    def test_intervening_failure_or_stale_latest_evidence_blocks_stability(self):
        history, _, _ = track([row(25), row(12, 'DOGRULANAMADI')], {}, NOW, True)
        _, report, _ = track([row()], history, NOW, True)
        self.assertEqual(report[-1]['24_SAAT_KARARLI'], 'HAYIR')
        history, _, _ = track([row(50), row(25)], {}, NOW, True)
        _, report, _ = track([row(25)], history, NOW, True)
        self.assertEqual(report[0]['24_SAAT_KARARLI'], 'HAYIR')

    def test_missing_future_naive_and_conflicting_times_preserve_input(self):
        history, _, _ = track([row()], {}, NOW, True)
        before = json.dumps(history)
        for value in ('', '2026-10-16T12:00:00', '2026-10-17T12:00:00+00:00'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                track([{**row(), 'OLCUM_ZAMANI': value}], history, NOW, True)
        with self.assertRaises(ValueError):
            track([row(0, 'DOGRULANAMADI')], history, NOW, True)
        self.assertEqual(json.dumps(history), before)

    def test_old_audit_history_is_retained_without_counting_it_in_window(self):
        old = {'at': (NOW - dt.timedelta(days=31)).isoformat(), 'state': 'DOGRULANAMADI'}
        history, report, _ = track([row()], {URL: [old]}, NOW, True)
        self.assertEqual(history[URL][0], old)
        self.assertEqual(report[0]['GOZLEM_SAYISI'], 1)

    def test_untested_rows_do_not_create_measurements(self):
        with self.assertRaises(ValueError):
            track([row(0, 'TEST_EDILMEDI')], {}, NOW, True)
        history, rows, counts = track([], {URL: []}, NOW, True)
        self.assertEqual(counts['new_observations'], 0)
        self.assertEqual(rows, [])
        self.assertEqual(history, {URL: []})

    def test_k2_explicit_measurement_time_is_required_not_success_counter(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'madsc_kesif').mkdir()
            path = root / 'madsc_kesif/gecmis.json'
            path.write_text(json.dumps({'history': {'key': {'url': URL, 'successful_runs': 99}}}))
            with self.assertRaises(ValueError):
                continuity.measured_rows(root, [row()])
            path.write_text(json.dumps({'history': {'key': {'url': URL, 'last_test': NOW.isoformat()}}}))
            self.assertEqual(continuity.measured_rows(root, [row()])[0]['OLCUM_ZAMANI'], NOW.isoformat())

    def test_scoring_uses_real_history_and_combined_report_keeps_approval_closed(self):
        now = dt.datetime.now(dt.timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / 'madsc_kesif'; folder.mkdir()
            with (folder / 'adaylar.csv').open('w', newline='') as handle:
                writer = csv.DictWriter(handle, fieldnames=['kanal', 'url', 'video', 'ses', 'durum'])
                writer.writeheader(); writer.writerow(dict(kanal='Fixture', url=URL, video=True, ses=True, durum='TEKNIK'))
            (folder / 'gecmis.json').write_text(json.dumps({'history': {'key': {'url': URL, 'last_test': now.isoformat()}}}))
            before = {URL: [{'at': (now - dt.timedelta(hours=25)).isoformat(), 'state': 'VIDEO_SES_VAR'}]}
            result = scoring.build_reports(root, root / 'out', history=before)
            self.assertEqual(result['stable_24h_current_candidates'], 1)
            self.assertEqual(result['new_observations'], 1)
            self.assertEqual(result['additional_media_probes'], 0)
            with (root / 'out/BIRLESIK_ADAY_ONAY_RAPORU.csv').open(encoding='utf-8-sig') as handle:
                actual = next(csv.DictReader(handle))
            self.assertEqual(actual['24_SAAT_KARARLI'], 'EVET')
            self.assertEqual(actual['ANA_LISTEYE_EKLE'], 'HAYIR')
            self.assertEqual(actual['KULLANICI_ONAYI'], 'YOK')
            again = scoring.build_reports(root, root / 'out', history=continuity.load(root / 'out' / continuity.NAME))
            self.assertEqual(again['new_observations'], 0)
            self.assertEqual(again['reused_measurements_not_added'], 1)

    def restore_fixture(self, root, required=True, missing=False, corrupt=False, bad_hash=False):
        source = dict(id=123, head_sha='a' * 40)
        artifact = dict(name=continuity.ARTIFACT, expired=False,
                        workflow_run=dict(id=123, head_sha='a' * 40))
        def download(args, **kwargs):
            folder = Path(args[-1]) / 'madsc_aday_puanlama'; folder.mkdir()
            if not missing:
                path = folder / continuity.NAME
                path.write_text('{broken' if corrupt else json.dumps({URL: []}))
                (folder / 'kabul.json').write_text(json.dumps({'stability_history_sha256':
                    'bad' if bad_hash else hashlib.sha256(path.read_bytes()).hexdigest()}))
        with patch.dict(os.environ, dict(GITHUB_REPOSITORY='o/r', GITHUB_REF_NAME='branch', GITHUB_RUN_ID='456')), \
             patch.object(continuity, 'find_previous', return_value=source), \
             patch.object(continuity, 'gh_json', return_value={'artifacts': [artifact]}), \
             patch.object(continuity.subprocess, 'check_output', return_value='marker' if required else ''), \
             patch.object(continuity.subprocess, 'run', side_effect=download):
            return continuity.restore(root)

    def test_successful_ancestor_restores_and_preintegration_can_bootstrap(self):
        with tempfile.TemporaryDirectory() as tmp:
            history, report = self.restore_fixture(Path(tmp))
            self.assertEqual(history, {URL: []})
            self.assertEqual(report['source_run_id'], 123)
            self.assertEqual(report['mode'], 'RESTORED_SUCCESSFUL_ANCESTOR')
            history, report = self.restore_fixture(Path(tmp), required=False, missing=True)
            self.assertEqual(history, {})
            self.assertEqual(report['mode'], 'PRE_INTEGRATION_BOOTSTRAP')

    def test_missing_corrupt_or_changed_accepted_history_fails_closed(self):
        for kwargs in ({'missing': True}, {'corrupt': True}, {'bad_hash': True}):
            with self.subTest(kwargs=kwargs), tempfile.TemporaryDirectory() as tmp, self.assertRaises(ValueError):
                self.restore_fixture(Path(tmp), **kwargs)

    def test_yaml_and_artifact_wiring(self):
        root = Path(__file__).parent
        workflow = (root / '.github/workflows/madsc-03-kanal-test.yml').read_text()
        self.assertIn('test_five_category_stability_history', workflow)
        self.assertIn('madsc_aday_puanlama/', workflow)
        self.assertIn('scripts/category_stability_history.py', (root / '.github/workflows/madsc-05-genel-bakim.yml').read_text())
