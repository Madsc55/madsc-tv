import unittest
from scripts.central_ibo_review_queue import prepare

class IboIncelemeKuyruguTesti(unittest.TestCase):
    def test_adaylar_onaysiz_ve_tekrarsizdir(self):
        raw={"candidate_results":[
            {"channel":"TRT","stream_sha256":"abc","epg_pilot_status":"PILOT_MATCH_WITH_PROGRAMMES","logo_status":"PNG_READY_REVIEW_PENDING","playlist_approved":True,"ready_for_playlist":True},
            {"channel":"TRT","stream_sha256":"abc","ready_for_playlist":True},
            {"channel":"TRT","stream_sha256":"def"}]}
        rows,status=prepare(raw)
        self.assertEqual(len(rows),2)
        self.assertEqual(status,"ADAY_LISTESI_OKUNDU")
        self.assertTrue(all(x["ready_for_playlist"]=="HAYIR" for x in rows))
        self.assertTrue(all(x["user_decision"]=="ONAY_BEKLIYOR" for x in rows))
        self.assertTrue(all(x["sweden_ibo_status"]=="NOT_DEVICE_VERIFIED" for x in rows))
    def test_eksik_kanit_uydurulmaz(self):
        self.assertEqual(prepare(None),([],"KAYNAK_KANITI_YOK"))

if __name__=="__main__":
    unittest.main()
