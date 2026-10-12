#!/usr/bin/env python3
"""Join existing discovery, artwork and XMLTV evidence; never approve or edit playlists."""
import json
import re
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DISCOVERY=ROOT/"madsc_kesif"
def load(path,default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default
def main():
    logos=load(DISCOVERY/"candidate_logos.json",{}).get("results",[])
    by_hash={r.get("stream_sha256"):r for r in logos if r.get("stream_sha256")}
    candidates=load(DISCOVERY/"logo_candidates.json",[])
    epg=ROOT/"epg/ibo-test-epg.xml"
    if not epg.exists(): raise RuntimeError("EPG pilot missing")
    root=ET.parse(epg).getroot()
    if root.tag!="tv": raise RuntimeError("Invalid XMLTV")
    guide={x.get("id") for x in root.findall("channel")}
    programmes=Counter(x.get("channel") for x in root.findall("programme"))
    out=[]
    for c in candidates:
        cid=c.get("channel_id","").strip()
        h=c.get("stream_sha256","")
        logo=by_hash.get(h,{})
        epg_status=("PILOT_MATCH_WITH_PROGRAMMES" if cid in guide and programmes[cid]>0
                    else "PILOT_ID_NO_PROGRAMMES" if cid in guide
                    else "NOT_IN_FIVE_CHANNEL_PILOT")
        logo_status=logo.get("status","NOT_PREPARED")
        out.append({"channel":c.get("channel",""),"stream_sha256":h,"channel_id":cid,
                    "epg_pilot_status":epg_status,"logo_status":logo_status,
                    "logo_visual_match":logo.get("visual_match","NOT_VERIFIED"),
                    "broadcast_status":"SEE_EXISTING_DISCOVERY_AND_CONTINUITY_REPORTS",
                    "sweden_ibo_status":"NOT_DEVICE_VERIFIED",
                    "playlist_approved":False,
                    "ready_for_playlist":False})
    report={"checked_utc":datetime.now(timezone.utc).isoformat(),
            "source_candidates":len(candidates),"candidate_results":out,
            "pilot_epg_channels":len(guide),
            "notes":["Five-channel XMLTV pilot is not full production EPG coverage.",
                     "Logo PNG preparation does not prove on-air identity.",
                     "Broadcast evidence remains in existing test reports; no implicit pass.",
                     "Never changes playlists, logos, EPG or approval decisions."]}
    target=DISCOVERY/"candidate_epg_logo_join.json"
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"candidates":len(out),"report":str(target),"approved":0}))
if __name__=="__main__":main()
