#!/usr/bin/env python3
"""Run existing weekly/monthly scans with persistent, isolated report state."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

try:
    from scripts.discovery_history_restore import find_previous
except ModuleNotFoundError:
    from discovery_history_restore import find_previous

ROOT = Path(__file__).resolve().parents[1]
FILES = {'state.json': None, 'candidate_review.json': 'candidates'}


def read_documents(folder):
    present = [bool((folder / name).exists()) for name in FILES]
    if not any(present):
        return None
    if not all(present):
        raise ValueError('Incomplete wide source history pair')
    result = {}
    for name, key in FILES.items():
        path = folder / name
        if path.is_symlink():
            raise ValueError('Source history is not a regular file')
        doc = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(doc, dict) or (key and not isinstance(doc.get(key), dict)):
            raise ValueError('Invalid wide source history')
        records = doc[key] if key else doc
        if any(not isinstance(v, dict) for v in records.values()):
            raise ValueError('Invalid source history record')
        result[name] = doc
    return result


def empty_documents():
    return {'state.json': {}, 'candidate_review.json': {'candidates': {}}}


def merge_documents(checkout, incoming, ancestor):
    merged = json.loads(json.dumps(checkout))
    for name, key in FILES.items():
        current = merged[name][key] if key else merged[name]
        old = ancestor[name][key] if key else ancestor[name]
        proposed = incoming[name][key] if key else incoming[name]
        for identity, value in proposed.items():
            if identity not in current:
                current[identity] = value
            elif current[identity] == value or old.get(identity) == value:
                continue
            elif old.get(identity) == current[identity]:
                current[identity] = value
            else:
                raise ValueError('Conflicting repository and artifact source history')
    return merged


def ancestor_documents(root, sha):
    documents = {}
    for name, key in FILES.items():
        path = 'madsc_genis_tarama/' + name
        listed = subprocess.run(['git', 'ls-tree', '--name-only', sha, '--', path],
                                cwd=root, capture_output=True, text=True, check=True)
        if not listed.stdout.strip():
            documents[name] = {} if key is None else {key: {}}
        else:
            data = subprocess.run(['git', 'show', sha + ':' + path], cwd=root,
                                  capture_output=True, text=True, check=True)
            documents[name] = json.loads(data.stdout)
    return documents


def restore_state(root):
    folder = root / 'madsc_genis_tarama'
    checkout = read_documents(folder) or empty_documents()
    source = find_previous(root, os.environ['GITHUB_REPOSITORY'],
                           os.environ['GITHUB_REF_NAME'], os.environ['GITHUB_RUN_ID'])
    merged = checkout
    source_id = None
    if source:
        with tempfile.TemporaryDirectory(prefix='madsc-wide-state-') as tmp:
            subprocess.run(['gh', 'run', 'download', str(source['id']), '--repo',
                            os.environ['GITHUB_REPOSITORY'], '--name',
                            'madsc-kesif-tek-kosu-rapor', '--dir', tmp],
                           check=True, capture_output=True)
            incoming = read_documents(Path(tmp) / 'madsc_genis_tarama')
            if incoming is None:
                # Only pre-integration artifacts may lack wide-scan state.
                feature = subprocess.run(['git', 'ls-tree', '--name-only', source['head_sha'],
                                          '--', 'scripts/wide_source_scan.py'], cwd=root,
                                         check=True, capture_output=True, text=True)
                if feature.stdout.strip():
                    raise ValueError('Successful integrated run is missing source history')
            else:
                merged = merge_documents(checkout, incoming,
                                         ancestor_documents(root, source['head_sha']))
                source_id = source['id']
    folder.mkdir(exist_ok=True)
    # Merge/validate both histories before writing either one.
    for name, document in merged.items():
        (folder / name).write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n',
                                  encoding='utf-8')
    return source_id


def run(mode, root=ROOT):
    if mode not in ('none', 'weekly', 'monthly', 'both'):
        raise ValueError('Unknown wide scan mode')
    source_id = restore_state(root)
    modes = ['weekly', 'monthly'] if mode == 'both' else ([] if mode == 'none' else [mode])
    summaries = {}
    for selected in modes:
        subprocess.run([sys.executable, 'tools/genis_kaynak_taramasi.py'], cwd=root,
                       env={**os.environ, 'MADSC_SCAN_MODE': selected}, check=True)
        summary = json.loads((root / 'madsc_genis_tarama' / ('summary_' + selected + '.json')).read_text())
        if summary.get('mode') != selected or not (0 < summary['accessible'] <= summary['checked'] <= summary['configured']):
            raise ValueError('Wide scan has no accessible source or invalid coverage')
        summaries[selected] = {key: summary[key] for key in
                               ('configured', 'checked', 'accessible', 'changed', 'new_identity_review_candidates')}
    report = {'requested_mode': mode, 'source_run_id': source_id, 'modes': summaries,
              'playlist_write': False, 'main_dispatch': False, 'device_approval': False}
    out = root / 'madsc_merkezi_denetim'
    out.mkdir(exist_ok=True)
    (out / 'genis_kaynak_kabul.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=('none', 'weekly', 'monthly', 'both'), default='none')
    args = parser.parse_args()
    run(args.mode)
