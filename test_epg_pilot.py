import unittest
from epg_deneme.build import period, stamp


class EpgMidnightTests(unittest.TestCase):
    def test_narrow_midnight_rollover(self):
        start, stop, repaired = period('20261012200000 +0300', '20261012001500 +0300')
        self.assertTrue(repaired)
        self.assertEqual(stop, stamp('20261013001500 +0300'))
        self.assertEqual((stop-start).total_seconds(), 15300)

    def test_ordinary_intervals_unchanged(self):
        _, stop, repaired = period('20261012200000 +0300', '20261013001500 +0300')
        self.assertFalse(repaired)
        self.assertEqual(stop, stamp('20261013001500 +0300'))

    def test_other_backwards_intervals_rejected(self):
        for start, stop in [('20261012130000 +0300','20261012120000 +0300'),
                            ('20261012200000 +0300','20261011001500 +0300')]:
            with self.assertRaises(ValueError):
                period(start, stop)


if __name__ == '__main__':
    unittest.main()
