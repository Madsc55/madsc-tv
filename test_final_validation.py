import unittest
from final_validation import assess, pending_candidates
import hashlib

class ContinuityEvidenceTests(unittest.TestCase):
    def test_missing_invalid_and_short_evidence_cannot_pass(self):
        for progress in ('', 'frame=9000\nout_time_us=N/A\n',
                         'frame=0\nout_time_us=300000000\n',
                         'frame=9000\nout_time_us=30000000\n'):
            with self.subTest(progress=progress):
                self.assertFalse(assess(0, progress, 300)['passed'])
        self.assertFalse(assess(1, 'frame=9000\nout_time_us=300000000\n', 300)['passed'])
        self.assertTrue(assess(0, 'frame=9000\nout_time_us=300000000\n', 300)['passed'])

class ResumeTests(unittest.TestCase):
    def test_terminal_outcomes_are_not_retested(self):
        rows=[dict(url='https://example.org/'+str(i),label=str(i),reason='priority') for i in range(4)]
        old=[dict(candidate_id=hashlib.sha256(r['url'].encode()).hexdigest()[:20],status=status) for r,status in zip(rows,['TIMEOUT','CONTINUITY_FAILED','TECHNICAL_PASS_CONTENT_REVIEW','TECHNICAL_PASS_IDENTITY_PENDING'])]
        self.assertEqual(pending_candidates({'candidates':rows},{},old),[])
    def test_only_three_passes_enter_new_batch(self):
        def item(n):return dict(channel='A',url='https://example.org/'+str(n),checks=[{'passed':True}]*n)
        state={'a':item(2),'b':item(3),'c':dict(item(3),url='https://example.org/failed',checks=[{'passed':False}]*3)}
        selected=pending_candidates({'candidates':[]},state,[])
        self.assertEqual(len(selected),1)
        self.assertEqual(selected[0]['url'],'https://example.org/3')

if __name__ == '__main__':
    unittest.main()
