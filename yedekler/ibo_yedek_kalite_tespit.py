#!/usr/bin/env python3
"""Probe backup streams, annotate only backup display names, preserve every URL."""
import csv, json, subprocess, concurrent.futures, re
from pathlib import Path
playlist=Path("CALISANLAR.m3u")
lines=playlist.read_text(encoding="utf-8-sig").splitlines()
targets=[]
for i,line in enumerate(lines[:-1]):
    if line.startswith("#EXTINF") and 'group-title="📦 YEDEKLER"' in line and lines[i+1].startswith(("http://","https://")):
        targets.append((i,lines[i+1].strip()))
def check(item):
    i,url=item
    try:
        p=subprocess.run(["ffprobe","-v","error","-show_entries","stream=codec_type,width,height,codec_name","-of","json","-rw_timeout","9000000",url],capture_output=True,text=True,timeout=14)
        streams=json.loads(p.stdout or "{}").get("streams",[])
        videos=[s for s in streams if s.get("codec_type")=="video" and s.get("height")]
        audio=any(s.get("codec_type")=="audio" for s in streams)
        if videos:
            v=max(videos,key=lambda s:s.get("height",0))
            h=int(v["height"]); w=int(v.get("width",0))
            quality=("2160P UHD" if h>=2160 else "1440P QHD" if h>=1440 else "1080P FHD" if h>=1080 else "720P HD" if h>=720 else "576P SD" if h>=576 else "480P SD" if h>=480 else str(h)+"P")
            return i,url,quality,w,h,"VIDEO_SES" if audio else "VIDEO_SES_BELIRSIZ"
        return i,url,"KALİTE BELİRSİZ",0,0,"DOGRULANAMADI"
    except Exception:
        return i,url,"KALİTE BELİRSİZ",0,0,"DOGRULANAMADI"
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
    results=list(pool.map(check,targets))
for i,url,quality,w,h,status in results:
    meta=lines[i]
    # Replace only the displayed name after the final metadata comma; keep metadata, URLs and all non-backup entries intact.
    before,display=meta.split(",",1)
    display=re.sub(r" (?:2160P UHD|1440P QHD|1080P FHD|720P HD|576P SD|480P SD|[0-9]+P|KALİTE BELİRSİZ)$","",display)
    lines[i]=before+","+display+" "+quality
playlist.write_text("\n".join(lines)+"\n",encoding="utf-8")
with Path("yedekler/IBO_YEDEK_KALITE_RAPORU_2026-10-09.csv").open("w",encoding="utf-8-sig",newline="") as f:
    writer=csv.writer(f);writer.writerow(["KANAL","KALITE","GENISLIK","YUKSEKLIK","TEKNIK_DURUM","URL"])
    for i,url,quality,w,h,status in results:
        writer.writerow([lines[i].split(",",1)[1],quality,w,h,status,url])
print("Yedek kanal:",len(results),"kalitesi belirlenen:",sum(x[2]!="KALİTE BELİRSİZ" for x in results))
