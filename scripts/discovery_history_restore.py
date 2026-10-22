#!/usr/bin/env python3
"""Carry validated discovery observations across read-only Actions runs."""
import datetime as dt
import json
import os
from pathlib import Path
import subprocess
import tempfile
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
FILES = {'gecmis.json': 'history', 'ana_liste_test_gecmisi.json': 'channels'}
WORKFLOWS = ('madsc-02-kesif.yml', 'madsc-05-genel-bakim.yml')
OBSERVATIONS = {'runs', 'successful_runs', 'last_test', 'last_success', 'last_result', 'resolution'}


def stamp(value):
    if value is None:
        return dt.datetime.min.replace(tzinfo=dt.timezone.utc)
    parsed = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('Observation timestamp has no timezone')
    return parsed


def load_pair(folder):
    result = {}
    for filename, key in FILES.items():
        path = folder / filename
        if path.is_symlink():
            raise ValueError('History must be a regular file')
        document = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(document, dict) or not isinstance(document.get(key), dict):
            raise ValueError('Invalid history document: ' + filename)
        for entry in document[key].values():
            if not isinstance(entry, dict):
                raise ValueError('Invalid history record')
            for field in ('runs', 'successful_runs'):
                if field in entry and (type(entry[field]) is not int or entry[field] < 0):
                    raise ValueError('Invalid history counter')
            for field in ('last_test', 'last_success', 'first_seen'):
                if entry.get(field) is not None:
                    stamp(entry[field])
            if 'source_history' in entry and (not isinstance(entry['source_history'], list)
                    or any(not isinstance(x, str) for x in entry['source_history'])):
                raise ValueError('Invalid source history')
        result[filename] = document
    return result


def merge_pair(base, incoming):
    merged = json.loads(json.dumps(base))
    changes = {}
    for filename, key in FILES.items():
        records = merged[filename][key]
        added = updated = 0
        for identity, observation in incoming[filename][key].items():
            if identity not in records:
                records[identity] = observation.copy()
                added += 1
                continue
            old = records[identity]
            old_time, new_time = stamp(old.get('last_test')), stamp(observation.get('last_test'))
            if new_time > old_time:
                if observation.get('runs', old.get('runs', 0)) < old.get('runs', 0):
                    raise ValueError('Newer observation has a regressed run count')
                # Keep repository metadata and decisions; replace only machine observations.
                for field in OBSERVATIONS:
                    if field in observation:
                        old[field] = observation[field]
                updated += 1
            elif new_time == old_time and old_time != stamp(None):
                if any(old.get(f) != observation.get(f) for f in OBSERVATIONS):
                    raise ValueError('Conflicting observations at the same timestamp')
            if 'source_history' in observation:
                old['source_history'] = sorted(set(old.get('source_history', []))
                                               | set(observation['source_history']))
        changes[filename] = {'added': added, 'updated': updated, 'total': len(records)}
    return merged, changes


def gh_json(repo, endpoint):
    result = subprocess.run(['gh', 'api', f'repos/{repo}/{endpoint}'], check=True,
                            capture_output=True, text=True)
    return json.loads(result.stdout)


def find_previous(root, repo, branch, current_run, workflows=WORKFLOWS):
    page = 1
    while True:
        data = gh_json(repo, f'actions/runs?branch={quote(branch, safe="")}'
                            f'&status=success&per_page=100&page={page}')
        runs = data['workflow_runs']
        eligible = []
        for run in runs:
            if (str(run['id']) == str(current_run) or run.get('head_branch') != branch
                    or run.get('conclusion') != 'success'
                    or run.get('status') != 'completed'
                    or (run.get('head_repository') or {}).get('full_name') != repo
                    or run.get('path') not in {'.github/workflows/' + w for w in workflows}
                    or run.get('event') not in ('push', 'schedule', 'workflow_dispatch')):
                continue
            sha = run['head_sha']
            if len(sha) != 40 or any(c not in '0123456789abcdef' for c in sha):
                raise ValueError('Invalid source commit')
            ancestry = subprocess.run(['git', 'merge-base', '--is-ancestor', sha, 'HEAD'], cwd=root,
                                     capture_output=True)
            if ancestry.returncode == 0:
                eligible.append(run)
            elif ancestry.returncode != 1:
                raise ValueError('Cannot verify source commit ancestry')
        if eligible:
            return max(eligible, key=lambda r: (r['created_at'], r['id']))
        if len(runs) < 100:
            return None
        page += 1


def restore(root=ROOT):
    folder = root / 'madsc_kesif'
    base = load_pair(folder)  # Never replace a corrupt checkout with an artifact.
    repo, branch = os.environ['GITHUB_REPOSITORY'], os.environ['GITHUB_REF_NAME']
    source = find_previous(root, repo, branch, os.environ['GITHUB_RUN_ID'])
    report = {'source_run_id': None, 'source_commit': None, 'mode': 'CHECKOUT_BOOTSTRAP'}
    if source:
        with tempfile.TemporaryDirectory(prefix='madsc-history-') as tmp:
            subprocess.run(['gh', 'run', 'download', str(source['id']), '--repo', repo,
                            '--name', 'madsc-kesif-tek-kosu-rapor', '--dir', tmp],
                           check=True, capture_output=True)
            artifact = Path(tmp) / 'madsc_kesif'
            if not artifact.is_dir():
                artifact = Path(tmp)
            incoming = load_pair(artifact)
            merged, changes = merge_pair(base, incoming)
            # Validate and stage BOTH documents before replacing either working copy.
            staged = []
            try:
                for name in FILES:
                    with tempfile.NamedTemporaryFile(mode='w', dir=folder, encoding='utf-8',
                                                     delete=False) as handle:
                        json.dump(merged[name], handle, ensure_ascii=False, indent=2)
                        handle.write('\n')
                        staged.append((Path(handle.name), folder / name))
                for temporary, target in staged:
                    temporary.replace(target)
            finally:
                for temporary, _ in staged:
                    temporary.unlink(missing_ok=True)
            report.update(source_run_id=source['id'], source_commit=source['head_sha'],
                          mode='MERGED_SUCCESSFUL_ANCESTOR', files=changes)
    out = root / 'madsc_merkezi_denetim'
    out.mkdir(exist_ok=True)
    (out / 'kesif_gecmis_devamliligi.json').write_text(
        json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report))  # Counts/provenance only; no raw stream URLs.
    return report


if __name__ == '__main__':
    try:
        restore()
    except Exception as exc:
        detail = str(exc) if isinstance(exc, ValueError) else type(exc).__name__
        raise SystemExit('Kesif gecmisi geri yuklenemedi; tarama durduruldu: ' + detail)
