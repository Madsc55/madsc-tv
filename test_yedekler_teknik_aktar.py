import hashlib
import unittest
from tools.son_kontrol_yedekler_aktar import prepare
from tools.yedekler_guvenli_ekle import update

class YedeklerTest(unittest.TestCase):
    def test_technical_only(self):
        url = "https://example.com/test"
        token = hashlib.sha256(url.encode()).hexdigest()[:20]
        state = {"channels": {"x": {"url": url, "channel": "Kanal", "checks": [{"passed": True}] * 3}}}
        row = {"candidate_id": token, "label": "Kanal", "status": "TECHNICAL_PASS_IDENTITY_PENDING", "continuity": {"passed": True}, "review_events": {}}
        candidates = prepare([row], state)
        self.assertEqual(len(candidates), 1)
        self.assertFalse(candidates[0]["identity_verified"])
        self.assertEqual(prepare([dict(row, status="TIMEOUT")], state), [])
        playlist = '#EXTM3U\n#EXTINF:-1 group-title="📦 YEDEKLER (1)",Eski\nhttps://example.com/old\n'
        updated, count = update(playlist, candidates)
        self.assertEqual(count, 1)
        self.assertIn("Kanal [TEST]", updated)
        self.assertEqual(update(updated, candidates)[1], 0)
