#!/usr/bin/env python3
"""Weekly targeted and monthly 155-feed metadata discovery. No playback or playlist writes."""
import ast
import concurrent.futures
import csv
import hashlib
import io
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT=Path("madsc_genis_tarama")
ROOT.mkdir(exist_ok=True)
tree=ast.parse(Path("madsc_akilli_kesif.py").read_text(encoding="utf-8"))
sources={}
for node in tree.body:
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="SOURCES" for t in node.targets):
        sources=ast.literal_eval(node.value)
        break
mode=os.environ.get("MADSC_SCAN_MODE","weekly")
if mode not in ("weekly","monthly"):
    raise SystemExit("Unknown mode")
daily={"iptv-turk-tr-EK-KAYNAK","iptv-org-TR","iptv-org-TURKIYE","iptv-org-TURKCE","omerdenizhan-TR","ilyswch-TR","itasli-TR","gkhncksn-TR","Lunedor-TR","dearbulut-TR","dearbulut-TURKCE"}
priority=("AZER","KURT","KIBRIS","TURKMEN","ALMANYA","ISVEC","HOLLANDA","BELCIKA","AVUSTURYA","HABER","SPOR","BELGESEL","COCUK","MUZIK","KULTUR","BILIM","EGITIM","country-de","country-se","country-nl","country-be")
selected=sources if mode=="monthly" else {k:v for k,v in sources.items() if k not in daily and any(t in k for t in priority)}
state_file=ROOT/"state.json"
try:
    old=json.loads(state_file.read_text(encoding="utf-8")) if state_file.exists() else {}
except (ValueError,OSError):
    raise SystemExit("Invalid previous state: stopping to protect history")
if not isinstance(old,dict):
    raise SystemExit("Invalid state object")
def fetch(item):
    name,url=item
    try:
        with urlopen(Request(url,headers={"User-Agent":"MADSC-TV-source-audit/1.0"}),timeout=16) as resp:
            data=resp.read(3000000)
        decoded=data.decode("utf-8-sig",errors="replace")
        if not decoded.lstrip().startswith("#EXTM3U"):
            return name,{"status":"INVALID_M3U","url":url}
        lines=decoded.splitlines()
        return name,{"status":"OK","url":url,"digest":hashlib.sha256(data).hexdigest(),"entries":sum(x.lstrip().startswith("#EXTINF") for x in lines)}
    except Exception as exc:
        return name,{"status":"ERROR","url":url,"error":str(exc)[:160]}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    current=dict(pool.map(fetch,selected.items()))
changed=[]
for name,info in current.items():
    if info["status"]=="OK" and info.get("digest")!=old.get(name,{}).get("digest"):
        changed.append(name)
        old[name]=info
    elif info["status"]=="OK":
        old[name]=info
# Failed sources do not erase last known good hashes.
state_file.write_text(json.dumps(old,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
summary={"generated_utc":datetime.now(timezone.utc).isoformat(),"mode":mode,"configured":len(sources),"checked":len(selected),"accessible":sum(v["status"]=="OK" for v in current.values()),"changed":len(changed),"changed_sources":sorted(changed),"errors":{k:v.get("error",v["status"]) for k,v in current.items() if v["status"]!="OK"},"note":"Metadata-only source change discovery. Not unique channel counts, identity checks, or stream playback."}
(ROOT/("summary_"+mode+".json")).write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
with (ROOT/("sources_"+mode+".csv")).open("w",newline="",encoding="utf-8") as file:
    w=csv.writer(file);w.writerow(["source","status","entries","changed","url"])
    for name,info in sorted(current.items()):
        w.writerow([name,info["status"],info.get("entries",""),name in changed,info["url"]])
print(json.dumps(summary,ensure_ascii=False))
