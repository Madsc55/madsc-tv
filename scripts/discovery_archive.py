#!/usr/bin/env python3
"""Persist discovered URLs and prevent repeat candidate probes without editing playlists."""
import csv
import datetime as dt
import json
from pathlib import Path
from urllib.parse import urlsplit, parse_qsl, urlencode, urlunsplit

ROOT=Path("madsc_kesif")
ROOT.mkdir(exist_ok=True)
HISTORY=ROOT/"gecmis.json"
REGISTRY=ROOT/"bulunan_kanal_arsivi.csv"
FIELDS=["kanal","url","kaynaklar","sinif","teknik_durum","ibo_durum","ilk_gorulme","son_gorulme"]
def key(url):
 p=urlsplit(url)
 q=[(k,v) for k,v in parse_qsl(p.query) if k.lower() not in ("token","auth","expires","signature","sig","hash")]
 return urlunsplit((p.scheme.lower(),p.netloc.lower(),p.path.rstrip("/"),urlencode(sorted(q)),""))
def rows(path):
 if not path.exists():return []
 with path.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def m3u(path):
 if not path.exists():return []
 lines=path.read_text(encoding="utf-8-sig").splitlines()
 return [{"kanal":line.rsplit(",",1)[-1].strip(),"url":lines[i+1].strip(),"kaynak":"YABANCI_ARSIV"} for i,line in enumerate(lines[:-1]) if line.startswith("#EXTINF") and lines[i+1].strip().startswith(("http://","https://"))]
def load_history():
 if not HISTORY.exists():raise RuntimeError("Missing history; refusing to erase previous test evidence")
 doc=json.loads(HISTORY.read_text(encoding="utf-8"))
 if not isinstance(doc.get("history"),dict):raise RuntimeError("Invalid history")
 return doc
def main():
 import sys
 mode=sys.argv[1]
 doc=load_history()
 history=doc["history"]
 previous={key(r["url"]):r for r in rows(REGISTRY) if r.get("url")}
 now=dt.datetime.now(dt.timezone.utc).isoformat()
 foreign=m3u(Path("YABANCI_KANALLAR.m3u"))
 main_urls={key(x["url"]) for x in m3u(Path("CALISANLAR.m3u"))}
 def keep(x,classification,technical="BILINMIYOR"):
  u=x.get("url","")
  if not u or key(u) in main_urls:return
  k=key(u)
  r=previous.get(k)
  if r is None:
   r=dict(kanal=x.get("kanal",""),url=u,kaynaklar=x.get("kaynak",""),sinif=classification,teknik_durum=technical,ibo_durum="TEKIL_ONAY_YOK",ilk_gorulme=now,son_gorulme=now)
   previous[k]=r
  else:
   r["son_gorulme"]=now
   if classification=="YABANCI_ARSIV":r["sinif"]=classification
   if technical!="BILINMIYOR":r["teknik_durum"]=technical
   sources=set(filter(None,r.get("kaynaklar","").split(" | ")))
   if x.get("kaynak"):sources.add(x["kaynak"])
   r["kaynaklar"]=" | ".join(sorted(sources))
 for x in foreign:keep(x,"YABANCI_ARSIV")
 if mode=="after":
  for x in rows(ROOT/"adaylar.csv"):
   keep({"kanal":x.get("kanal"),"url":x.get("url"),"kaynak":x.get("kaynak")},"SINIFLANDIRMA_BEKLIYOR",x.get("durum","BILINMIYOR"))
  for x in rows(ROOT/"alternatifler.csv"):
   keep({"kanal":x.get("kanal"),"url":x.get("url"),"kaynak":x.get("kaynak")},"SINIFLANDIRMA_BEKLIYOR")
  for k,v in history.items():
   if v.get("url"):keep({"kanal":v.get("channel"),"url":v["url"],"kaynak":v.get("source_id","GECMIS")},"SINIFLANDIRMA_BEKLIYOR",v.get("last_result","BILINMIYOR"))
 # Mark archived URLs as previously seen so discovery does not repeat technical tests.
 # No fake success is recorded. Historical evidence is never overwritten.
 if mode=="before":
  for k,r in previous.items():
   if k not in history:
    history[k]={"url":r["url"],"channel":r["kanal"],"runs":1,"successful_runs":0,
                "last_result":"ARSIVDE_TEKRAR_TEST_YOK","source_id":"KALICI_ARSIV"}
  HISTORY.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 elif mode!="after":raise SystemExit("usage: python scripts/discovery_archive.py before|after")
 with REGISTRY.open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(sorted(previous.values(),key=lambda r:(r["kanal"] or "",r["url"])))
 print(json.dumps({"mode":mode,"archive_urls":len(previous),"foreign_archive":len(foreign),"new_probes_blocked_by_history":len(history)},ensure_ascii=False))
if __name__=="__main__":main()
