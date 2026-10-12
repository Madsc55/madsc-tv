import unittest
from final_validation import assess

class ContinuityEvidenceTests(unittest.TestCase):
    def test_missing_invalid_and_short_evidence_cannot_pass(self):
        for progress in ('', 'frame=9000\nout_time_us=N/A\n',
                         'frame=0\nout_time_us=300000000\n',
                         'frame=9000\nout_time_us=30000000\n'):
            with self.subTest(progress=progress):
                self.assertFalse(assess(0, progress, 300)['passed'])
        self.assertFalse(assess(1, 'frame=9000\nout_time_us=300000000\n', 300)['passed'])
        self.assertTrue(assess(0, 'frame=9000\nout_time_us=300000000\n', 300)['passed'])

if __name__ == '__main__':
    unittest.main()
