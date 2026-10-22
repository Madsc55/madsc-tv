import unittest
from scripts.central_actions_evidence import fetch, summarize


class ActionsEvidenceTests(unittest.TestCase):
    def test_current_run_excluded_and_branch_failures_not_hidden(self):
        runs = [dict(run_id=1, workflow_id=1, head_branch='main', created_at='2026-10-15',
                     status='completed', conclusion='failure'),
                dict(run_id=2, workflow_id=1, head_branch='feature', created_at='2026-10-16',
                     status='completed', conclusion='success'),
                dict(run_id=3, workflow_id=2, head_branch='feature', created_at='2026-10-16',
                     status='in_progress', conclusion=None),
                dict(run_id=4, workflow_id=3, head_branch='feature', created_at='2026-10-16',
                     status='in_progress', conclusion=None)]
        report = summarize(runs, '4')
        self.assertEqual(report['checked'], 3)
        self.assertEqual(report['successful'], 1)
        self.assertEqual(len(report['failed']), 1)
        self.assertEqual(report['failed'][0]['head_branch'], 'main')
        self.assertEqual(len(report['pending']), 1)
        self.assertFalse(any(row['run_id'] == 4 for row in report['workflows']))

    def test_new_success_supersedes_older_failure_only_on_same_branch(self):
        runs = [dict(run_id=n, workflow_id=1, head_branch='main', created_at=str(n),
                     status='completed', conclusion='success' if n == 2 else 'failure') for n in (1, 2)]
        report = summarize(runs, 3)
        self.assertEqual(report['successful'], 1)
        self.assertEqual(report['failed'], [])
        self.assertEqual(report['sample_size'], 2)

    def test_pagination_failure_details_and_no_blanket_success(self):
        calls = []
        def api(repo, endpoint):
            calls.append(endpoint)
            if 'workflows?' in endpoint:
                return {'workflows': [dict(id=n, name='Fixture', path='x.yml', state='active') for n in range(100)]
                        if endpoint.endswith('&page=1') else [dict(id=101, name='Other', path='y.yml', state='active')]}
            if endpoint == 'actions/runs?per_page=100':
                return {'workflow_runs': [dict(id=10, workflow_id=1, head_branch='main',
                          created_at='2026-10-16', status='completed', conclusion='failure')]}
            return {'jobs': [{'name': 'Failed', 'conclusion': 'failure',
                              'steps': [{'name': 'Step', 'conclusion': 'failure'}]}]}
        workflows, runs, jobs, report = fetch('o/r', '11', api)
        self.assertEqual(len(workflows), 101)
        self.assertEqual(runs[0]['run_id'], 10)
        self.assertEqual(jobs[0]['status'], 'ALINDI')
        self.assertEqual(report['successful'], 0)
        self.assertEqual(len(report['failed']), 1)
        self.assertTrue(any('/10/jobs?' in call for call in calls))

    def test_unavailable_historical_job_evidence_stays_unknown(self):
        def api(repo, endpoint):
            if 'workflows?' in endpoint: return {'workflows': []}
            if endpoint == 'actions/runs?per_page=100':
                return {'workflow_runs': [dict(id=10, workflow_id=1, head_branch='main',
                          created_at='2026-10-16', status='completed', conclusion='failure')]}
            raise OSError('unavailable')
        _, _, jobs, report = fetch('o/r', '11', api)
        self.assertEqual(jobs[0]['status'], 'API_KANITI_ALINAMADI')
        self.assertEqual(len(report['failed']), 1)
