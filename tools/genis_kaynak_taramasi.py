#!/usr/bin/env python3
"""Weekly targeted and monthly 155-feed metadata discovery. No playback or playlist writes."""
import ast
import concurrent.futures
import csv
import hashlib
import io
import json
import os
import re
from urllib.parse import urlsplit, urlunsplit
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
        candidates=[]
        for index,line in enumerate(lines[:-1]):
            if not line.lstrip().startswith("#EXTINF"):
                continue
            title=line.rsplit(",",1)[-1].strip()
            link=lines[index+1].strip()
            if link.startswith(("http://","https://")) and title:
                candidates.append((title,link))
        return name,{"status":"OK","url":url,"digest":hashlib.sha256(data).hexdigest(),"entries":len(candidates),"candidates":candidates}
    except Exception as exc:
        return name,{"status":"ERROR","url":url,"error":str(exc)[:160]}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    current=dict(pool.map(fetch,selected.items()))
changed=[]
# Build a separate review queue; never mutate three-stage verification state.
known=set()
def norm(url):
    try:
        p=urlsplit(url.strip())
        return urlunsplit((p.scheme.lower(),p.netloc.lower(),p.path,p.query,""))
    except ValueError:
        return url.strip()
for playlist in ("CALISANLAR.m3u","YENILER.m3u","MADSC_TV_47_LISTE_ADAY.m3u"):
    p=Path(playlist)
    if p.exists():
        known.update(norm(line) for line in p.read_text(encoding="utf-8-sig",errors="replace").splitlines() if line.strip().startswith(("http://","https://")))
history_file=Path("madsc_kesif/gecmis.json")
if history_file.exists():
    try:
        history=json.loads(history_file.read_text(encoding="utf-8"))
        if not isinstance(history.get("history"),dict):
            raise ValueError("Missing history map")
        known.update(norm(link) for link in history["history"])
    except (ValueError,OSError) as exc:
        raise SystemExit("Cannot read prior test history: "+str(exc))
review_file=ROOT/"candidate_review.json"
try:
    previous=json.loads(review_file.read_text(encoding="utf-8")) if review_file.exists() else {"candidates":{}}
    if not isinstance(previous.get("candidates"),dict):
        raise ValueError("Invalid candidate history")
except (ValueError,OSError) as exc:
    raise SystemExit("Cannot read candidate history: "+str(exc))
review=previous["candidates"]
new_review=0
for name,info in current.items():
    if info["status"]=="OK" and info.get("digest")!=old.get(name,{}).get("digest"):
        changed.append(name)
        # Only explicitly Turkish feeds can supply automatic review candidates.
        eligible=("TURK" in name or name.endswith("-TR") or "KIBRIS" in name)
        if eligible:
            for title,link in info.get("candidates",[]):
                identity=norm(link)
                if identity in known or identity in review:
                    continue
                review[identity]={"name":title,"url":link,"source":name,"status":"IDENTITY_REVIEW_REQUIRED_NOT_TESTED"}
                new_review+=1
        old[name]={k:v for k,v in info.items() if k!="candidates"}
    elif info["status"]=="OK":
        old[name]={k:v for k,v in info.items() if k!="candidates"}
# Failed sources do not erase last known good hashes.
review_file.write_text(json.dumps({"candidates":review},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
state_file.write_text(json.dumps(old,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
summary={"generated_utc":datetime.now(timezone.utc).isoformat(),"mode":mode,"configured":len(sources),"checked":len(selected),"accessible":sum(v["status"]=="OK" for v in current.values()),"changed":len(changed),"changed_sources":sorted(changed),"new_identity_review_candidates":new_review,"total_identity_review_candidates":len(review),"errors":{k:v.get("error",v["status"]) for k,v in current.items() if v["status"]!="OK"},"note":"Changed-source URL candidates are queued for identity review, NOT inserted into three-stage tests or playlists."}
(ROOT/("summary_"+mode+".json")).write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
with (ROOT/("sources_"+mode+".csv")).open("w",newline="",encoding="utf-8") as file:
    w=csv.writer(file);w.writerow(["source","status","entries","changed","url"])
    for name,info in sorted(current.items()):
        w.writerow([name,info["status"],info.get("entries",""),name in changed,info["url"]])
print(json.dumps(summary,ensure_ascii=False))
