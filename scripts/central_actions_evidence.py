#!/usr/bin/env python3
"""Fetch read-only Actions samples for the existing status/failure reporters."""
import json
import os
from pathlib import Path

try:
    from scripts.discovery_history_restore import gh_json
    from scripts.category_evidence_collect import verify
except ModuleNotFoundError:
    from discovery_history_restore import gh_json
    from category_evidence_collect import verify

ROOT = Path(__file__).resolve().parents[1]
FAILURES = {'failure', 'timed_out', 'startup_failure', 'action_required'}


def summarize(runs, current_run):
    latest = {}
    for run in sorted(runs, key=lambda item: item.get('created_at') or '', reverse=True):
        if str(run.get('run_id')) == str(current_run) or run.get('workflow_id') is None:
            continue
        # A green feature branch must not hide a red main branch.
        key = (run['workflow_id'], run.get('head_branch'))
        latest.setdefault(key, run)
    checked = [{key: run.get(key) for key in
                ('workflow_id', 'name', 'run_id', 'head_branch', 'head_sha', 'status', 'conclusion', 'html_url')}
               | {'verified_success': run.get('status') == 'completed' and run.get('conclusion') == 'success'}
               for run in latest.values()]
    return {'checked': len(checked), 'sample_size': len(runs),
            'scope': 'LATEST_PER_WORKFLOW_AND_BRANCH_IN_LAST_100',
            'current_run': {'id': current_run, 'status': 'IN_PROGRESS_NOT_VERIFIED'},
            'current_run_excluded': True,
            'current_run_found_in_sample': any(str(r.get('run_id')) == str(current_run) for r in runs),
            'successful': sum(item['verified_success'] for item in checked),
            'failed': [item for item in checked if item['status'] == 'completed' and item['conclusion'] in FAILURES],
            'pending': [item for item in checked if item['status'] != 'completed'],
            'unknown': 'Last 100 runs only; workflows or branches absent from the sample are not verified.',
            'workflows': checked}


def fetch(repo, current_run, api=gh_json):
    workflows, page = [], 1
    while True:
        entries = api(repo, f'actions/workflows?per_page=100&page={page}')['workflows']
        workflows.extend({key: item.get(key) for key in ('id', 'name', 'path', 'state')} for item in entries)
        if len(entries) < 100:
            break
        page += 1
    raw = api(repo, 'actions/runs?per_page=100')['workflow_runs']
    runs = [{key: item.get(key) for key in ('workflow_id', 'name', 'status', 'conclusion',
                                         'created_at', 'html_url', 'head_branch', 'head_sha', 'path')}
            | {'run_id': item['id']} for item in raw]
    failed = [run for run in runs if run.get('conclusion') in FAILURES
              and str(run['run_id']) != str(current_run)]
    job_evidence = []
    for run in failed[:20]:
        try:
            data = api(repo, f'actions/runs/{run["run_id"]}/jobs?per_page=100')
            jobs = [{key: job.get(key) for key in ('name', 'conclusion', 'steps')} for job in data['jobs']]
            job_evidence.append({'run_id': run['run_id'], 'status': 'ALINDI', 'jobs': jobs})
        except (ValueError, KeyError, OSError):
            job_evidence.append({'run_id': run['run_id'], 'status': 'API_KANITI_ALINAMADI', 'jobs': []})
    summary = summarize(runs, current_run)
    summary['failure_job_evidence_limit'] = 20
    summary['failed_runs_with_job_evidence_attempted'] = len(job_evidence)
    summary['older_failed_runs_without_job_evidence'] = max(0, len(failed) - 20)
    return workflows, runs, job_evidence, summary


def main():
    output = ROOT / 'madsc_merkezi_denetim'
    verify(output)
    workflows, runs, jobs, summary = fetch(os.environ['GITHUB_REPOSITORY'], os.environ['GITHUB_RUN_ID'])
    files = {'son_100_kosu.json': runs, 'basarisiz_kosu_isleri.json': jobs,
             'actions_otomatik_sonuc_dogrulama.json': summary}
    for name, data in files.items():
        (output / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    (output / 'github_workflow_durumlari.jsonl').write_text(
        ''.join(json.dumps(item, ensure_ascii=False) + '\n' for item in workflows))
    verify(output)
    print(json.dumps({'workflows_fetched': len(workflows), 'sample_size': len(runs),
                      'latest_workflow_branch_pairs': summary['checked'],
                      'successful': summary['successful'], 'failed': len(summary['failed']),
                      'pending': len(summary['pending']), 'current_run_excluded': True}))


if __name__ == '__main__':
    main()
