#!/usr/bin/env python3
"""Execute existing read-only media checks once, or reuse fresh accepted K3 evidence."""
import collections
import csv
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

try:
    from scripts.discovery_history_restore import find_previous, gh_json
    from scripts.kanal_kararlilik_takip import timestamp
except ModuleNotFoundError:
    from discovery_history_restore import find_previous, gh_json
    from kanal_kararlilik_takip import timestamp

ROOT = Path(__file__).resolve().parents[1]
FILES = {'priority': 'ONCELIKLI_KANAL_TEK_NIK_RAPOR.csv',
         'general': 'GENEL_ADAY_GERCEK_MEDYA_RAPORU.csv'}
SUMMARIES = ('ONCELIKLI_OZET.json', 'GENEL_ADAY_MEDYA_OZET.json')
STATES = {'VIDEO_SES_VAR', 'YALNIZ_VIDEO', 'YALNIZ_SES', 'MEDYA_YOK', 'DOGRULANAMADI', 'GECERSIZ_URL'}
ARTIFACT = 'madsc-kanal-test-tek-kosu-rapor'


def reports(folder, now=None):
    now = now or dt.datetime.now(dt.timezone.utc)
    result = {}
    for kind, filename in FILES.items():
        path = folder / filename
        if path.is_symlink():
            raise ValueError('Medya raporu symlink olamaz')
        with path.open(encoding='utf-8-sig', newline='') as handle:
            reader = csv.DictReader(handle)
            if not {'KANAL', 'YAYIN_URL', 'TEKNIK_MEDYA', 'OLCUM_ZAMANI', 'SES_IZI', 'COZUNURLUK'} <= set(reader.fieldnames or []):
                raise ValueError('Medya raporunda olcum zamani veya medya semasi eksik')
            rows = list(reader)
        seen = set()
        for row in rows:
            if None in row or not row['YAYIN_URL'].startswith(('https://', 'http://')) or row['YAYIN_URL'] in seen:
                raise ValueError('Medya raporunda kaymis/yinelenen/gecersiz URL satiri')
            seen.add(row['YAYIN_URL'])
            if row['TEKNIK_MEDYA'] not in STATES:
                raise ValueError('Bilinmeyen medya durumu')
            timestamp(row['OLCUM_ZAMANI'], now)
            if row['TEKNIK_MEDYA'] == 'VIDEO_SES_VAR' and row['SES_IZI'].lower() != 'true':
                raise ValueError('Ses kaniti celisiyor')
        if not rows or (kind == 'general' and len(rows) > 30):
            raise ValueError('Medya kapsami bos veya parti sinirini asti')
        result[kind] = rows
    return result


def load_cache(folder, now=None):
    now = now or dt.datetime.now(dt.timezone.utc)
    manifest = json.loads((folder / 'kabul.json').read_text(encoding='utf-8'))
    if manifest.get('schema') != 1 or set(manifest.get('hashes', {})) != set(FILES.values()) | set(SUMMARIES):
        raise ValueError('Medya kabul manifesti eksik')
    for name, digest in manifest['hashes'].items():
        path = folder / name
        if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError('Medya kaniti hash uyusmazligi')
    result = reports(folder, now)
    priority = json.loads((folder / SUMMARIES[0]).read_text(encoding='utf-8'))
    general = json.loads((folder / SUMMARIES[1]).read_text(encoding='utf-8'))
    if priority['toplam'] != len(result['priority']) or priority['sonuclar'] != dict(collections.Counter(r['TEKNIK_MEDYA'] for r in result['priority'])):
        raise ValueError('Oncelikli medya kapsam/ozet celiskisi')
    if general['test_edilen'] + general['yeniden_kullanilan'] != len(result['general']):
        raise ValueError('Genel medya olcum/tekrar kapsam celiskisi')
    fresh = all(dt.timedelta(0) <= now - timestamp(row['OLCUM_ZAMANI'], now) < dt.timedelta(hours=6)
                for rows in result.values() for row in rows)
    return result, manifest, fresh


def previous(root, destination):
    repo, branch, current = (os.environ[k] for k in ('GITHUB_REPOSITORY', 'GITHUB_REF_NAME', 'GITHUB_RUN_ID'))
    run = find_previous(root, repo, branch, current,
                        workflows=('madsc-03-kanal-test.yml', 'madsc-05-genel-bakim.yml'))
    if run is None:
        return None
    artifacts = gh_json(repo, f'actions/runs/{run["id"]}/artifacts?per_page=100')['artifacts']
    matches = [a for a in artifacts if a.get('name') == ARTIFACT]
    if len(matches) != 1 or matches[0].get('expired'):
        raise ValueError('Onceki K3 medya artifact eksik/gecersiz')
    source = matches[0].get('workflow_run') or {}
    if source.get('id') != run['id'] or source.get('head_sha') != run['head_sha']:
        raise ValueError('Onceki K3 medya artifact kaynak uyusmazligi')
    required = bool(subprocess.check_output(['git', 'ls-tree', '--name-only', run['head_sha'],
                    'scripts/category_candidate_media.py'], cwd=root, text=True).strip())
    subprocess.run(['gh', 'run', 'download', str(run['id']), '--repo', repo, '--name', ARTIFACT,
                    '--dir', str(destination)], check=True, capture_output=True)
    folder = destination / 'madsc_aday_medya'
    if not folder.exists():
        if required:
            raise ValueError('Entegre kosuda medya kaniti eksik; sessiz sifirlama yok')
        return None
    _, manifest, _ = load_cache(folder)
    if str(manifest.get('run_id')) != str(run['id']) or manifest.get('head_sha') != run['head_sha']:
        raise ValueError('Onceki medya kabul run/HEAD uyusmazligi')
    return run


def execute(root, folder):
    # All script outputs stay isolated. The protected list is only a temporary read input.
    shutil.copyfile(root / 'CALISANLAR.m3u', folder / 'CALISANLAR.m3u')
    suggested = root / 'YENI_KAYNAK_ONERILERI.csv'
    if suggested.exists():
        shutil.copyfile(suggested, folder / suggested.name)
    env = dict(os.environ)
    subprocess.run([sys.executable, str(root / 'scripts/oncelikli_kanal_dogrula.py')], cwd=folder, env=env, check=True)
    # Validate priority CSV before it can be reused by the general probe.
    with (folder / FILES['priority']).open(encoding='utf-8-sig', newline='') as handle:
        priority = list(csv.DictReader(handle))
    if any(not row.get('OLCUM_ZAMANI') for row in priority):
        raise ValueError('Oncelikli olcum zamani yok')
    # Existing discovery-only mode: no HLS segment or ffprobe sampling in this step.
    env.update(SCAN_BATCH='-1')
    subprocess.run([sys.executable, str(root / 'yeni_kanal_tara.py')], cwd=folder, env=env, check=True)
    env.update(ADAY_TEST_GRUBU='0', MADSC_MEDYA_SKIP_CSV=str(folder / FILES['priority']))
    subprocess.run([sys.executable, str(root / 'scripts/genel_aday_medya_test.py')], cwd=folder, env=env, check=True)


def prepare(root=ROOT):
    output = root / 'madsc_aday_medya'
    if output.exists() and any(output.iterdir()):
        raise ValueError('Medya cikti klasoru bos olmali; kanitin ustune yazilmadi')
    now = dt.datetime.now(dt.timezone.utc)
    with tempfile.TemporaryDirectory(prefix='madsc-media-cache-') as old, tempfile.TemporaryDirectory(prefix='madsc-media-work-') as work:
        old, work = Path(old), Path(work)
        source = previous(root, old)
        versions = {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in
                    ('scripts/oncelikli_kanal_dogrula.py', 'scripts/genel_aday_medya_test.py', 'yeni_kanal_tara.py')}
        reusable = False
        if source:
            _, old_manifest, reusable = load_cache(old / 'madsc_aday_medya', now)
            reusable = reusable and old_manifest.get('generator_versions') == versions
        if reusable:
            folder = old / 'madsc_aday_medya'
            manifest = {**old_manifest, 'mode': 'REUSED_FRESH_ACCEPTED_ANCESTOR',
                        'network_media_probes': 0, 'candidate_discovery_ran': False}
        else:
            execute(root, work)
            result = reports(work)
            general = json.loads((work / SUMMARIES[1]).read_text(encoding='utf-8'))
            manifest = {'schema': 1, 'mode': 'EXECUTED_EXISTING_SCRIPTS',
                        'origin_run_id': os.environ['GITHUB_RUN_ID'],
                        'origin_head_sha': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip(),
                        'network_media_probes': len(result['priority']) + general['test_edilen'],
                        'general_reused_priority': general['yeniden_kullanilan'],
                        'candidate_discovery_ran': True,
                        'priority_rows': len(result['priority']), 'general_rows': len(result['general']),
                        'hashes': {name: hashlib.sha256((work / name).read_bytes()).hexdigest()
                                   for name in (*FILES.values(), *SUMMARIES)}}
            folder = work
        manifest.update(run_id=os.environ['GITHUB_RUN_ID'],
                        head_sha=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip(),
                        previous_run_id=source['id'] if source else None,
                        generator_versions=versions, cache_max_age_hours=6, playlist_write=False, device_approval=False)
        # Validate every output before publishing any working artifact files.
        (folder / 'kabul.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
        load_cache(folder)
        output.mkdir(exist_ok=True)
        for name in (*FILES.values(), *SUMMARIES, 'kabul.json'):
            shutil.copyfile(folder / name, output / name)
    print(json.dumps(manifest))
    return manifest


if __name__ == '__main__':
    prepare()
