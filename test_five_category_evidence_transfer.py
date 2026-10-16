import copy
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from scripts import category_evidence_collect as evidence
from scripts.central_management_summary import build

HEAD = 'a' * 40


def provenance():
    run = dict(id=1, head_sha=HEAD, head_branch='branch', head_repository={'full_name': 'o/r'},
               path='.github/workflows/madsc-05-genel-bakim.yml', event='push')
    jobs = [dict(id=n, name=f'MADSC 0{n} - Test', status='completed', conclusion='success') for n in range(1, 5)]
    artifacts = [dict(id=n, name=spec[0], expired=False, workflow_run={'id': 1, 'head_sha': HEAD})
                 for n, spec in enumerate(evidence.SPECS.values(), 1)]
    return run, jobs, artifacts


def make_sources(root):
    folders = {}
    for category, (_, specs) in evidence.SPECS.items():
        folder = root / category
        folders[category] = folder
        for source, target in specs:
            path = folder / source
            path.parent.mkdir(parents=True, exist_ok=True)
            data = {'fixture': category}
            if target == 'ana_liste_saglik_teknik_sonuc.json':
                data = dict(ana_liste_toplam=1039, bu_kosuda_test_edilen=1, sonuclar=[{'teknik_durum': 'DOGRULANAMADI'}],
                            otomatik_kanal_degisikligi=False, ibo_onayi_verildi=False, tum_liste_bu_kosuda_test_edildi=False)
            elif target == 'yedek_ve_korunan_dosyalar_kanit.json':
                data = dict(restore_test='GIT_HEAD_IZOLE_ESLESME_DOGRULANDI', historical_recovery_verified=False,
                            off_github_copy='DOGRULANMADI')
            path.write_text(json.dumps(data))
        (folder / 'YENILER.m3u').write_text('DO NOT COPY')
    run, jobs, artifacts = provenance()
    sources = evidence.validate_provenance(run, jobs, artifacts, 'o/r', 'branch', HEAD, '1')
    return folders, sources


class EvidenceTransferTests(unittest.TestCase):
    def test_same_run_commit_branch_repo_and_success_are_required(self):
        for kind in ('run', 'head', 'branch', 'repo', 'failed_job', 'expired', 'artifact_run', 'artifact_head'):
            with self.subTest(kind=kind):
                run, jobs, artifacts = provenance()
                if kind == 'run': run['id'] = 2
                elif kind == 'head': run['head_sha'] = 'b' * 40
                elif kind == 'branch': run['head_branch'] = 'other'
                elif kind == 'repo': run['head_repository']['full_name'] = 'fork/r'
                elif kind == 'failed_job': jobs[0]['conclusion'] = 'failure'
                elif kind == 'expired': artifacts[0]['expired'] = True
                elif kind == 'artifact_run': artifacts[0]['workflow_run']['id'] = 2
                elif kind == 'artifact_head': artifacts[0]['workflow_run']['head_sha'] = 'b' * 40
                with self.assertRaises(ValueError):
                    evidence.validate_provenance(run, jobs, artifacts, 'o/r', 'branch', HEAD, '1')

    def test_reports_only_are_copied_health_scope_and_open_acceptance_remain(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folders, sources = make_sources(root)
            output = root / 'out'
            with contextlib.redirect_stdout(io.StringIO()):
                manifest = evidence.collect_reports(folders, sources, output, '1', HEAD)
                evidence.collect_reports(folders, sources, output, '1', HEAD)
            self.assertEqual(evidence.verify(output), manifest)
            self.assertFalse(list(output.rglob('*.m3u')))
            self.assertTrue(all(p.suffix == '.json' for p in output.rglob('*') if p.is_file()))
            health = json.loads((output / 'ana_liste_saglik_kosu_kaniti.json').read_text())
            self.assertEqual(health['son_kosu']['job_id'], 3)
            self.assertEqual(health['tested_count'], 1)
            self.assertFalse(health['butun_ana_liste_test_edildi'])
            self.assertFalse(health['parent_run_complete'])
            result = build(output)
            self.assertEqual(result['sections']['izole_geri_yukleme']['status'], 'RAPOR_VAR')
            self.assertEqual(result['key_indicators']['main_playlist_health_run'],
                             'IS_AKISI_BASARILI_KANAL_SONUCU_INCELENMELI')
            self.assertFalse(result['key_indicators']['actions_current_run_verified'])
            self.assertEqual(result['device_ibo_approval'], 'NOT_VERIFIED')
            self.assertFalse(result['sections']['korunan_dosyalar_yedek']['data']['historical_recovery_verified'])
            self.assertFalse(manifest['migration_approved'])
            self.assertEqual((folders['K2'] / 'YENILER.m3u').read_text(), 'DO NOT COPY')

    def test_missing_or_corrupt_final_report_aborts_before_any_copy(self):
        for corrupt in (False, True):
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                folders, sources = make_sources(root)
                path = folders['K4'] / 'DISASTER-RECOVERY-REPORT.json'
                if corrupt: path.write_text('{bad')
                else: path.unlink()
                output = root / 'out'
                with self.assertRaises((ValueError, FileNotFoundError)):
                    evidence.collect_reports(folders, sources, output, '1', HEAD)
                self.assertFalse(output.exists())

    def test_existing_report_collision_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folders, sources = make_sources(root)
            output = root / 'out'
            output.mkdir()
            protected = output / 'genis_kaynak_kabul.json'
            protected.write_text('{"existing":true}')
            before = protected.read_bytes()
            with self.assertRaises(ValueError):
                evidence.collect_reports(folders, sources, output, '1', HEAD)
            self.assertEqual(protected.read_bytes(), before)
            self.assertEqual(len(list(output.iterdir())), 1)

    def test_imported_evidence_mutation_fails_verification(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folders, sources = make_sources(root)
            output = root / 'out'
            with contextlib.redirect_stdout(io.StringIO()):
                evidence.collect_reports(folders, sources, output, '1', HEAD)
            (output / 'izole_git_geri_yukleme_kaniti.json').write_text('{}')
            with self.assertRaises(ValueError):
                evidence.verify(output)

    def test_invalid_health_count_cannot_claim_acceptance(self):
        with self.assertRaises(ValueError):
            evidence.health_evidence(dict(ana_liste_toplam=100, bu_kosuda_test_edilen=50,
                                         sonuclar=[], otomatik_kanal_degisikligi=False,
                                         ibo_onayi_verildi=False, tum_liste_bu_kosuda_test_edildi=False), {}, '1')

    def test_symlink_is_rejected_before_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folders, sources = make_sources(root)
            source = folders['K1'] / 'protected-write-gate-report.json'
            source.unlink()
            (root / 'external.json').write_text('{}')
            source.symlink_to(root / 'external.json')
            with self.assertRaises(ValueError):
                evidence.collect_reports(folders, sources, root / 'out', '1', HEAD)

    def test_workflow_gates_transfer_and_builds_summary_after_dependencies(self):
        workflow = (Path(__file__).resolve().parent / '.github/workflows/madsc-05-genel-bakim.yml').read_text()
        self.assertIn('steps.category_evidence.outcome', workflow)
        self.assertIn('"category_evidence", "audit_1"', workflow)
        loop = workflow.split('for script in ', 1)[1].split('; do', 1)[0]
        self.assertLess(loop.index('central_eighteen_task_audit.py'), loop.index('central_management_summary.py'))
        self.assertLess(loop.index('central_all_remaining_tasks.py'), loop.index('central_management_summary.py'))
        self.assertIn('--run-report "${script}"', workflow)
        self.assertIn('category_evidence_collect.py --verify', workflow)

    def test_owner_report_is_not_recomputed_and_other_reports_cannot_replace_it(self):
        from unittest.mock import patch
        import sys
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folders, sources = make_sources(root)
            output = root / 'madsc_merkezi_denetim'
            with contextlib.redirect_stdout(io.StringIO()):
                evidence.collect_reports(folders, sources, output, '1', HEAD)
            with patch.object(evidence, 'ROOT', root), \
                 patch.object(sys, 'argv', ['collector', '--run-report', 'scripts/central_backup_evidence.py']), \
                 patch.object(evidence.subprocess, 'run') as process, \
                 contextlib.redirect_stdout(io.StringIO()):
                evidence.main()
                process.assert_not_called()
            (root / 'scripts').mkdir()
            (root / 'scripts/bad_report.py').write_text(
                'from pathlib import Path\nPath("madsc_merkezi_denetim/yedek_ve_korunan_dosyalar_kanit.json").write_text("{}")\n')
            with patch.object(evidence, 'ROOT', root), \
                 patch.object(sys, 'argv', ['collector', '--run-report', 'scripts/bad_report.py']):
                with self.assertRaises(ValueError):
                    evidence.main()
