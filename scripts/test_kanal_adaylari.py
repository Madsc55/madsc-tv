#!/usr/bin/env python3
import concurrent.futures, datetime, json, re, urllib.request, urllib.error
from pathlib import Path
SOURCE=Path("tarama/iptv-org-tr-adaylar-2026-10-10.m3u")
OUT=Path("yedekler/TARAMA-TEST-SONUCLARI.m3u")
REPORT=Path("tarama/son-test-raporu.json")
def entries(text):
    lines=text.splitlines()
    for i,line in enumerate(lines):
        if line.startswith("#EXTINF"):
            for url in lines[i+1:]:
                if url.strip() and not url.startswith("#"):
                    yield line,url.strip()
                    break
def test(item):
    line,url=item
    name=line.split(",",1)[-1]
    if not url.startswith(("http://","https://")):
        return dict(name=name,url=url,status="unsupported",detail="not http(s)",line=line)
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 IPTV-Check/1.0","Range":"bytes=0-8191","Accept":"*/*"})
        with urllib.request.urlopen(req,timeout=12) as r:
            status=r.status; ctype=r.headers.get("Content-Type","").lower(); body=r.read(8192)
        is_hls=b"#EXTM3U" in body or "mpegurl" in ctype
        is_ts=body[:1]==b"\\x47" or "video/mp2t" in ctype
        ok=status in (200,206) and (is_hls or is_ts)
        return dict(name=name,url=url,status="candidate_pass" if ok else "unverified",http=status,content_type=ctype,detail="HLS/TS response" if ok else "No HLS/TS signature",line=line)
    except Exception as e:
        return dict(name=name,url=url,status="failed",detail=str(e)[:180],line=line)
items=list(entries(SOURCE.read_text(encoding="utf-8-sig")))
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
    results=list(pool.map(test,items))
passed=[r for r in results if r["status"]=="candidate_pass"]
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text("#EXTM3U\n# YALNIZCA ILK HTTP/HLS TESTINI GECEN ADAYLAR. Oynaticida dogrulanmadi.\n"+"".join(r["line"]+"\n"+r["url"]+"\n" for r in passed),encoding="utf-8")
REPORT.write_text(json.dumps({"tested_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"total":len(results),"http_hls_pass":len(passed),"not_verified_in_player":True,"results":[{k:v for k,v in r.items() if k!="line"} for r in results]},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(f"Checked {len(results)}; HTTP/HLS candidates {len(passed)}; failed {sum(r['status']=='failed' for r in results)}")
