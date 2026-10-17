#!/usr/bin/env python3
"""Import only named JSON reports from accepted jobs in this exact Actions run."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

try:
    from scripts.discovery_history_restore import gh_json
except ModuleNotFoundError:
    from discovery_history_restore import gh_json

ROOT = Path(__file__).resolve().parents[1]
CENTRAL = 'madsc_merkezi_denetim/'
SPECS = {
    'K1': ('madsc-guvenlik-tek-kosu-rapor', [
        ('protected-write-gate-report.json', 'protected-write-gate-report.json')]),
    'K2': ('madsc-kesif-tek-kosu-rapor', [(CENTRAL + name, name) for name in (
        'kaynak_hedef_mutabakati.json', 'tekrar_test_analizi.json', 'ibo_aday_inceleme_ozeti.json',
        'kesif_gecmis_devamliligi.json', 'genis_kaynak_kabul.json')] + [
        ('madsc_kesif/candidate_logo_missing_report.json', 'candidate_logo_missing_report.json')]),
    'K3': ('madsc-kanal-test-tek-kosu-rapor', [
        (CENTRAL + 'logo_epg_kimlik_gecmis_tek_rapor.json', 'logo_epg_kimlik_gecmis_tek_rapor.json'),
        (CENTRAL + 'ana_liste_saglik_kosu_kaniti.json', 'ana_liste_saglik_eski_kapsam_kaniti.json'),
        (CENTRAL + 'logo_epg_kalite.json', 'logo_epg_kalite.json'),
        ('madsc_ana_liste_saglik/ana_liste_saglik.json', 'ana_liste_saglik_teknik_sonuc.json'),
        ('madsc_aday_puanlama/kabul.json', 'aday_puanlama_kabul.json'),
        ('madsc_aday_puanlama/AKILLI_ADAY_OZET.json', 'aday_puanlama_ozeti.json'),
        ('madsc_aday_puanlama/BIRLESIK_ADAY_OZET.json', 'birlesik_aday_ozeti.json')]),
    'K4': ('madsc-arsiv-yedek-tek-kosu-rapor', [
        (CENTRAL + 'izole_git_geri_yukleme_kaniti.json', 'izole_git_geri_yukleme_kaniti.json'),
        (CENTRAL + 'yedek_ve_korunan_dosyalar_kanit.json', 'yedek_ve_korunan_dosyalar_kanit.json'),
        ('DISASTER-RECOVERY-REPORT.json', 'felaket_kurtarma_tatbikati.json')]),
}
# Imported owner reports must not be regenerated from K5's stale checkout.
OWNERS = {
    'scripts/central_source_reconciliation.py': 'kaynak_hedef_mutabakati.json',
    'scripts/central_duplicate_test_audit.py': 'tekrar_test_analizi.json',
    'scripts/central_backup_evidence.py': 'yedek_ve_korunan_dosyalar_kanit.json',
    'scripts/central_identity_epg_logo_audit.py': 'logo_epg_kimlik_gecmis_tek_rapor.json',
    'scripts/central_ibo_review_queue.py': 'ibo_aday_inceleme_ozeti.json',
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def validate_provenance(run, jobs, artifacts, repo, branch, head, run_id):
    if (str(run.get('id')) != str(run_id) or run.get('head_sha') != head
            or run.get('head_branch') != branch
            or (run.get('head_repository') or {}).get('full_name') != repo
            or run.get('path') != '.github/workflows/madsc-05-genel-bakim.yml'
            or run.get('event') not in ('push', 'workflow_dispatch', 'schedule')):
        raise ValueError('Unexpected current run provenance')
    sources = {}
    for category, (artifact_name, _) in SPECS.items():
        number = category[-1]
        matches = [job for job in jobs if 'MADSC 0' + number + ' - ' in job.get('name', '')]
        if len(matches) != 1 or matches[0].get('status') != 'completed' or matches[0].get('conclusion') != 'success':
            raise ValueError('Source category did not complete successfully: ' + category)
        selected = [a for a in artifacts if a.get('name') == artifact_name]
        if len(selected) != 1 or selected[0].get('expired') is not False:
            raise ValueError('Missing, duplicate or expired category artifact: ' + category)
        origin = selected[0].get('workflow_run') or {}
        if str(origin.get('id')) != str(run_id) or origin.get('head_sha') != head:
            raise ValueError('Artifact is from another run or commit')
        sources[category] = {'job_id': matches[0]['id'], 'job_status': 'completed',
                             'job_conclusion': 'success', 'artifact_id': selected[0]['id'],
                             'artifact_name': artifact_name, 'source_commit': head,
                             'artifact_digest': selected[0].get('digest')}
    return sources


def health_evidence(data, source, run_id):
    total, checked = data.get('ana_liste_toplam'), data.get('bu_kosuda_test_edilen')
    if (type(total) is not int or type(checked) is not int or not 0 < checked <= total
            or not isinstance(data.get('sonuclar'), list) or len(data['sonuclar']) != checked
            or data.get('otomatik_kanal_degisikligi') is not False
            or data.get('ibo_onayi_verildi') is not False
            or data.get('tum_liste_bu_kosuda_test_edildi') != (checked == total)):
        raise ValueError('Invalid accepted channel health coverage')
    return {'asama': 3, 'durum': 'IS_AKISI_BASARILI_KANAL_SONUCU_INCELENMELI',
            'son_kosu': {'run_id': run_id, 'job_id': source['job_id'], 'scope': 'CATEGORY_JOB',
                         'status': 'completed', 'conclusion': 'success'},
            'parent_run_complete': False, 'kanal_sonuclari_dogrulandi': False,
            'butun_ana_liste_test_edildi': checked == total, 'otomatik_degisiklik': False,
            'tested_count': checked, 'playlist_count': total,
            'technical_report': 'ana_liste_saglik_teknik_sonuc.json',
            'aciklama': 'Ayni kosunun kabul edilmis K3 isi ve teknik raporu; K5 genel sonucu, tum kanallarin sagligi veya IBO onayi degildir.'}


def collect_reports(folders, sources, output, run_id, head):
    planned = {}
    manifest = {'run_id': run_id, 'source_commit': head, 'categories': sources,
                'verified_category_count': 4, 'overall_run_verified': False,
                'migration_approved': False, 'ibo_approved': False, 'files': []}
    health = None
    for category, (_, specs) in SPECS.items():
        folder = folders[category]
        for relative, target in specs:
            source = folder / relative
            if (source.is_symlink() or any(parent.is_symlink() for parent in source.parents)
                    or not source.resolve().is_relative_to(folder.resolve())):
                raise ValueError('Unsafe report path')
            content = source.read_bytes()
            data = json.loads(content.decode('utf-8'))
            if not isinstance(data, dict):
                raise ValueError('Category report must be a JSON object: ' + target)
            if target == 'ana_liste_saglik_teknik_sonuc.json':
                health = health_evidence(data, sources['K3'], run_id)
            for destination in (target, 'kategori_kanitlari/' + category + '/' + target):
                if destination in planned and planned[destination] != content:
                    raise ValueError('Category report collision')
                planned[destination] = content
                manifest['files'].append({'path': destination, 'sha256': digest(content),
                                          'category': category, 'source_path': relative})
    planned['ana_liste_saglik_kosu_kaniti.json'] = (json.dumps(health, indent=2) + '\n').encode()
    manifest['files'].append({'path': 'ana_liste_saglik_kosu_kaniti.json',
                              'sha256': digest(planned['ana_liste_saglik_kosu_kaniti.json']),
                              'category': 'K3', 'derived_from': 'ana_liste_saglik_teknik_sonuc.json'})
    # Validate ALL source files and destination collisions before the first write.
    for name, content in planned.items():
        destination = output / name
        if destination.is_symlink() or any(parent.is_symlink() for parent in destination.parents):
            raise ValueError('Unsafe report destination')
        if destination.exists() and destination.read_bytes() != content:
            raise ValueError('Existing report differs; refusing overwrite: ' + name)
    output.mkdir(parents=True, exist_ok=True)
    for name, content in planned.items():
        destination = output / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)
    (output / 'kategori_kanit_aktarimi.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({'verified_categories': 4, 'report_count': len(SPECS['K1'][1]) + len(SPECS['K2'][1]) + len(SPECS['K3'][1]) + len(SPECS['K4'][1]),
                      'copied_and_derived_files': len(planned), 'source_run_id': run_id,
                      'overall_run_verified': False}))
    return manifest


def verify(output):
    manifest = json.loads((output / 'kategori_kanit_aktarimi.json').read_text())
    if set(manifest.get('categories', {})) != set(SPECS) or manifest.get('verified_category_count') != 4:
        raise ValueError('Category provenance manifest is incomplete')
    expected = {name for _, specs in SPECS.values() for _, name in specs}
    expected |= {'kategori_kanitlari/' + category + '/' + target
                 for category, (_, specs) in SPECS.items() for _, target in specs}
    expected.add('ana_liste_saglik_kosu_kaniti.json')
    files = manifest.get('files', [])
    if {item['path'] for item in files} != expected or len(files) != len(expected):
        raise ValueError('Imported report coverage changed')
    for item in files:
        path = output / item['path']
        if path.is_symlink() or digest(path.read_bytes()) != item['sha256']:
            raise ValueError('Imported evidence changed: ' + item['path'])
    return manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--run-report')
    args = parser.parse_args()
    output = ROOT / 'madsc_merkezi_denetim'
    if args.verify or args.run_report:
        verify(output)
        if args.run_report:
            if args.run_report in OWNERS:
                print('Ayni kosunun kategori kaniti korundu: ' + OWNERS[args.run_report])
            else:
                script = Path(args.run_report)
                if script.parent != Path('scripts') or script.suffix != '.py':
                    raise ValueError('Unexpected central report script')
                subprocess.run([sys.executable, str(ROOT / script)], cwd=ROOT, check=True)
                verify(output)
        return
    repo, branch, run_id = (os.environ[key] for key in
                            ('GITHUB_REPOSITORY', 'GITHUB_REF_NAME', 'GITHUB_RUN_ID'))
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    run = gh_json(repo, 'actions/runs/' + run_id)
    jobs = gh_json(repo, 'actions/runs/' + run_id + '/jobs?per_page=100&filter=latest')['jobs']
    artifacts = gh_json(repo, 'actions/runs/' + run_id + '/artifacts?per_page=100')['artifacts']
    sources = validate_provenance(run, jobs, artifacts, repo, branch, head, run_id)
    with tempfile.TemporaryDirectory(prefix='madsc-category-evidence-') as tmp:
        folders = {}
        for category, (artifact_name, _) in SPECS.items():
            folder = Path(tmp) / category
            subprocess.run(['gh', 'run', 'download', run_id, '--repo', repo,
                            '--name', artifact_name, '--dir', str(folder)], check=True, capture_output=True)
            folders[category] = folder
        collect_reports(folders, sources, output, run_id, head)
    verify(output)


if __name__ == '__main__':
    main()
