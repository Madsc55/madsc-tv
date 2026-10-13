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

class EvidenceSeparationTests(unittest.TestCase):
    def test_final_review_defaults_never_certify_identity_or_rights(self):
        from unittest.mock import patch
        import subprocess
        from final_validation import audit
        candidate = {'url': 'https://example.org/live', 'label': 'Test', 'reason': 'test'}
        with patch('final_validation.subprocess.run',
                   side_effect=subprocess.TimeoutExpired(['ffprobe'], 35)):
            result = audit(candidate, 300)
        self.assertEqual(result['license_status'], 'NOT_VERIFIED')
        self.assertEqual(result['source_rights_review'], 'REQUIRED')
        self.assertEqual(result['station_identity_evidence'], 'NOT_VERIFIED')
        self.assertEqual(result['logo_identity_evidence'], 'NOT_VERIFIED')
        self.assertEqual(result['epg_device_evidence'], 'NOT_VERIFIED')
        self.assertEqual(result['ibo_sweden'], 'NOT_VERIFIED')

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

class TurkishPriorityTests(unittest.TestCase):
    def test_explicit_turkish_source_before_ambiguous_name(self):
        rows = [
            dict(url='https://example.org/one', label='ATV', reason='ambiguous'),
            dict(url='https://example.org/two', label='Kanal X', source_id='iptv-org-TR', reason='Turkish source'),
            dict(url='https://example.org/three', label='Station Y', source_language_hint='tur', reason='Turkish language source'),
            dict(url='https://example.org/four', label='Channel Z', country='az', reason='Azerbaijan'),
        ]
        selected = pending_candidates({'candidates': rows}, {}, [])
        self.assertEqual([x['url'] for x in selected[:2]],
                         ['https://example.org/two', 'https://example.org/three'])
        self.assertEqual(selected[2]['country'], 'az')

    def test_source_provenance_survives_state_to_final_review(self):
        record = dict(channel='Turkce Kanal', url='https://example.org/live',
                      checks=[{'passed': True}]*3, source_id='dearbulut-TURKCE',
                      source_language_hint='tur')
        selected = pending_candidates({'candidates': []}, {'key': record}, [])
        self.assertEqual(selected[0]['source_id'], 'dearbulut-TURKCE')
        self.assertEqual(selected[0]['source_language_hint'], 'tur')

    def test_multiple_source_origins_survive_final_queue(self):
        record = dict(channel='Kanal', url='https://example.org/multi',
                      checks=[{'passed': True}]*3,
                      source_id='iptv-org-TR',
                      source_language_hint='tur',
                      source_history=['iptv-org-TR', 'dearbulut-TR'])
        selected = pending_candidates({'candidates': []}, {'one': record}, [])
        self.assertEqual(selected[0]['source_history'],
                         ['iptv-org-TR', 'dearbulut-TR'])
        self.assertEqual(selected[0]['source_id'], 'iptv-org-TR')

    def test_turkish_candidates_first_and_completed_not_repeated(self):
        rows = [
            dict(url='https://example.org/foreign', label='BBC Earth', reason='wide'),
            dict(url='https://example.org/az', label='Az TV', country='az', reason='wide'),
            dict(url='https://example.org/tr', label='TRT 1', country='tr', reason='wide'),
            dict(url='https://example.org/ambiguous', label='ATV', reason='name only'),
            dict(url='https://example.org/turk', label='SAT 7 TÜRK', reason='wide'),
        ]
        old = [{'candidate_id': hashlib.sha256(rows[4]['url'].encode()).hexdigest()[:20]}]
        selected = pending_candidates({'candidates': rows}, {}, old)
        self.assertEqual([r['label'] for r in selected],
                         ['TRT 1', 'Az TV', 'BBC Earth', 'ATV'])
        self.assertEqual(len(selected), 4)

if __name__ == '__main__':
    unittest.main()
