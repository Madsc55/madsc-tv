#!/usr/bin/env python3
"""Separate staged verification; never writes playlists or discovery history."""
import concurrent.futures, datetime as dt, json, pathlib, subprocess
from madsc_akilli_kesif import probe
ROOT=pathlib.Path("madsc_kesif")
UTC=dt.timezone.utc
def due(item, now):
    if item["count"]>=3 or item.get("failed"): return False
    return (now-dt.datetime.fromisoformat(item["last_success"])).total_seconds()>=21600
def check(item):
    video,audio,resolution=probe(item["url"])
    if not (video and audio): return False,resolution
    try:
        p=subprocess.run(["ffmpeg","-nostdin","-v","error","-rw_timeout","9000000","-i",item["url"],"-t","30","-map","0:v:0","-map","0:a:0","-f","null","-"],capture_output=True,timeout=65)
        return p.returncode==0 and not p.stderr.strip(),resolution
    except subprocess.TimeoutExpired: return False,resolution
def main():
    now=dt.datetime.now(UTC)
    source=json.loads((ROOT/"gecmis.json").read_text())["history"]
    path=ROOT/"uc_asama_gecmis.json"
    state=json.loads(path.read_text()) if path.exists() else {}
    for key,item in source.items():
        if key not in state and item.get("successful_runs",0)>0:
            state[key]={"channel":item["channel"],"url":item["url"],"count":min(3,item["successful_runs"]),"last_success":item["last_success"],"checks":[],"identity":"ONAY_BEKLIYOR","sweden":"DOGRULANMADI"}
    selected=sorted((k for k,v in state.items() if due(v,now)),key=lambda k:(state[k]["count"],state[k]["last_success"],k))[:240]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results=list(pool.map(check,[state[k] for k in selected]))
    for key,(ok,resolution) in zip(selected,results):
        timestamp=dt.datetime.now(UTC).isoformat()
        item=state[key]
        item["checks"].append({"time":timestamp,"passed":ok,"resolution":resolution,"decode_seconds":30})
        if ok: item["count"]+=1; item["last_success"]=timestamp
        else: item["failed"]=True
    path.write_text(json.dumps(state,ensure_ascii=False,indent=2))
    summary={"time":dt.datetime.now(UTC).isoformat(),"candidates":len(state),"tested_this_run":len(selected),"due_remaining":sum(due(v,dt.datetime.now(UTC)) for v in state.values()),"technical_three_checks_passed":sum(v["count"]>=3 and not v.get("failed") for v in state.values()),"failed":sum(bool(v.get("failed")) for v in state.values()),"waiting":sum(v["count"]<3 and not v.get("failed") for v in state.values()),"note":"Teknik test kanal kimligini veya Isvec IBO uyumlulugunu kanitlamaz. Liste aktarimi yapilmadi."}
    (ROOT/"uc_asama_ozet.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    print(json.dumps(summary,ensure_ascii=False))
if __name__=="__main__": main()
