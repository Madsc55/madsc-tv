#!/usr/bin/env python3
"""Carry K3 media observations from a successful same-branch ancestor artifact."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

try:
    from scripts.discovery_history_restore import find_previous, gh_json
    from scripts.kanal_kararlilik_takip import validate, timestamp, track, FIELDS
except ModuleNotFoundError:
    from discovery_history_restore import find_previous, gh_json
    from kanal_kararlilik_takip import validate, timestamp, track, FIELDS

NAME = 'KARARLILIK_GECMISI.json'
ARTIFACT = 'madsc-kanal-test-tek-kosu-rapor'


def load(path):
    if path.is_symlink():
        raise ValueError('Kararlilik gecmisi symlink olamaz')
    return validate(json.loads(path.read_text(encoding='utf-8')), dt.datetime.now(dt.timezone.utc))


def restore(root):
    # A malformed existing file must never be hidden by artifact restoration.
    local = root / 'madsc_aday_puanlama' / NAME
    if local.exists() or local.is_symlink():
        load(local)
    repo, branch, run_id = (os.environ[k] for k in
                            ('GITHUB_REPOSITORY', 'GITHUB_REF_NAME', 'GITHUB_RUN_ID'))
    source = find_previous(root, repo, branch, run_id,
                           workflows=('madsc-03-kanal-test.yml', 'madsc-05-genel-bakim.yml'))
    report = {'source_run_id': None, 'source_commit': None, 'mode': 'FIRST_BOOTSTRAP',
              'restored_channels': 0, 'restored_observations': 0}
    if not source:
        return (load(local) if local.exists() else {}), report
    artifacts = gh_json(repo, f'actions/runs/{source["id"]}/artifacts?per_page=100')['artifacts']
    matches = [item for item in artifacts if item.get('name') == ARTIFACT]
    if len(matches) != 1 or matches[0].get('expired'):
        raise ValueError('Kararlilik kaynak artifact eksik/gecersiz')
    provenance = matches[0].get('workflow_run') or {}
    if provenance.get('id') != source['id'] or provenance.get('head_sha') != source['head_sha']:
        raise ValueError('Kararlilik artifact kaynak kosu/HEAD uyusmazligi')
    required = bool(subprocess.check_output(['git', 'ls-tree', '--name-only', source['head_sha'],
                    'scripts/category_stability_history.py'], cwd=root, text=True).strip())
    with tempfile.TemporaryDirectory(prefix='madsc-stability-') as tmp:
        subprocess.run(['gh', 'run', 'download', str(source['id']), '--repo', repo,
                        '--name', ARTIFACT, '--dir', tmp], check=True, capture_output=True)
        folder = Path(tmp) / 'madsc_aday_puanlama'
        path = folder / NAME
        if not path.exists() and not path.is_symlink():
            if required:
                raise ValueError('Entegre edilmis kosuda kararlilik gecmisi yok; sifirlanmadi')
            history, mode = {}, 'PRE_INTEGRATION_BOOTSTRAP'
        else:
            history, mode = load(path), 'RESTORED_SUCCESSFUL_ANCESTOR'
            accepted = json.loads((folder / 'kabul.json').read_text(encoding='utf-8'))
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if accepted.get('stability_history_sha256') != digest:
                raise ValueError('Kararlilik gecmisi kabul hash uyusmazligi')
    if local.exists():
        existing = load(local)
        for url, observations in existing.items():
            target = history.setdefault(url, [])
            for observation in observations:
                if observation not in target:
                    target.append(observation)
        validate(history, dt.datetime.now(dt.timezone.utc))
    report.update(source_run_id=source['id'], source_commit=source['head_sha'], mode=mode,
                  restored_channels=len(history), restored_observations=sum(map(len, history.values())))
    return history, report


def measured_rows(artifact, technical):
    path = artifact / 'madsc_kesif/gecmis.json'
    if path.is_symlink():
        raise ValueError('K2 gecmisi symlink olamaz')
    history = json.loads(path.read_text(encoding='utf-8')).get('history')
    if not isinstance(history, dict) or any(not isinstance(x, dict) for x in history.values()):
        raise ValueError('K2 gozlem zamani gecmisi gecersiz')
    by_url = {}
    for item in history.values():
        url = item.get('url')
        if url:
            if url in by_url and item.get('last_test') != by_url[url].get('last_test'):
                raise ValueError('K2 gozlem URL zaman celiskisi')
            by_url[url] = item
    result = []
    now = dt.datetime.now(dt.timezone.utc)
    for row in technical:
        observation = by_url.get(row['YAYIN_URL'], {})
        stamp = timestamp(observation.get('last_test'), now)
        result.append({**row, 'OLCUM_ZAMANI': stamp.isoformat()})
    return result
