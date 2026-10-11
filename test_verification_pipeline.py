import datetime as dt
import unittest
from unittest.mock import patch
import subprocess
import verification_pipeline as pipeline

class VerificationTests(unittest.TestCase):
    def test_spacing_and_terminal_results(self):
        now = dt.datetime.now(dt.timezone.utc)
        self.assertTrue(pipeline.eligible({'checks': []}, now))
        check = {'passed': True, 'time': now.isoformat()}
        self.assertFalse(pipeline.eligible({'checks': [check]}, now))
        self.assertTrue(pipeline.eligible({'checks': [check]}, now + dt.timedelta(hours=6)))
        self.assertFalse(pipeline.eligible({'checks': [check]*3}, now + dt.timedelta(days=1)))
        failed = {'passed': False, 'time': now.isoformat()}
        self.assertFalse(pipeline.eligible({'checks': [failed]}, now))
        self.assertTrue(pipeline.eligible({'checks': [failed]}, now + dt.timedelta(hours=6)))
        self.assertFalse(pipeline.eligible({'checks': [failed]*3}, now + dt.timedelta(days=1)))

    @patch('verification_pipeline.subprocess.run')
    def test_decode_requires_duration_and_frames(self, run):
        run.return_value = subprocess.CompletedProcess([], 0, 'frame=800\nout_time_us=30000000\n', '')
        self.assertTrue(pipeline.decode('https://example.org/live')['passed'])
        run.return_value = subprocess.CompletedProcess([], 0, 'frame=0\nout_time_us=30000000\n', '')
        self.assertFalse(pipeline.decode('https://example.org/live')['passed'])
        self.assertIn('0:a:0', run.call_args.args[0])

if __name__ == '__main__':
    unittest.main()
