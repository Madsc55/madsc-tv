#!/usr/bin/env python3
"""Stage only confidently Turkish discovered backup channels for IBO review.

Preserves every removed line verbatim in a separate M3U snapshot. Never touches
non-backup groups or user-verified status; ambiguous sources are NOT called foreign.
"""
import csv
import datetime as dt
import json
import re
from pathlib import Path
from urllib.parse import urlsplit,parse_qsl,urlencode,urlunsplit

PLAYLIST=Path("CALISANLAR.m3u")
REGISTRY=Path("madsc_kesif/bulunan_kanal_arsivi.csv")
FOREIGN=Path("YABANCI_KANALLAR.m3u")
OUT=Path("madsc_kesif")
GROUP=re.compile(r'group-title="📦 YEDEKLER \(\d+\)"')
TURKISH_SOURCE=re.compile(r'(?:^|[^a-z])(iptv.org.tr|iptv-org-tr|turkiye|türkiye|turkce|türkçe|dearbulut-tr)(?:$|[^a-z])',re.I)
TURKISH_NAME=re.compile(r'(?:\bTRT\s*(?:1|2|3|4|HABER|SPOR|BELGESEL|ÇOCUK|KURDÎ|TÜRK|AVAZ)\b|\b(?:SHOW TV|STAR TV|KANAL D|ATV TÜRKİYE|TV8 TÜRKİYE|HALK TV|SÖZCÜ TV|HABERTÜRK|NTV TÜRKİYE|TELE1|TV5 TÜRKİYE)\b)',re.I)
def key(u):
 p=urlsplit(u.strip())
 q=[(k,v) for k,v in parse_qsl(p.query) if k.lower() not in {"token","auth","expires","signature","sig","hash"}]
 return urlunsplit((p.scheme.lower(),p.netloc.lower(),p.path.rstrip("/"),urlencode(sorted(q)),""))
def entries(lines):
 for i,line in enumerate(lines[:-1]):
  if line.startswith("#EXTINF") and lines[i+1].strip().startswith(("http://","https://")):
   yield i,line,lines[i+1].strip()
def main():
 lines=PLAYLIST.read_text(encoding="utf-8-sig").splitlines(keepends=True)
 with REGISTRY.open(encoding="utf-8-sig",newline="") as f:
  registry={key(r["url"]):r for r in csv.DictReader(f) if r.get("url")}
 foreign={key(url) for _,_,url in entries(FOREIGN.read_text(encoding="utf-8-sig").splitlines(keepends=True))}
 backup=[(i,m,u) for i,m,u in entries(lines) if GROUP.search(m)]
 if not backup:raise RuntimeError("No backup entries found; refusing to change playlist")
 # Original YEDEKLER entries predate bulk import; preserve these two.
 preserve_original=2
 kept=[];removed=[];ambiguous=[];foreign_removed=[]
 for position,(i,meta,url) in enumerate(backup):
  r=registry.get(key(url),{})
  sources=r.get("kaynaklar","")
  name=meta.rsplit(",",1)[-1]
  is_foreign=key(url) in foreign or r.get("sinif")=="YABANCI_ARSIV"
  confident_tr=(bool(TURKISH_SOURCE.search(sources)) or bool(TURKISH_NAME.search(name)))
  if position<preserve_original or (confident_tr and not is_foreign):
   kept.append((i,meta,url))
  else:
   removed.append((i,meta,url))
   (foreign_removed if is_foreign else ambiguous).append((i,meta,url))
 if not removed:raise RuntimeError("No candidates selected; refusing no-op")
 stamp=dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
 snapshot=OUT/("yedeklerden_ayrilanlar_"+stamp+".m3u")
 snapshot.write_text("#EXTM3U\n"+"".join(meta+url+"\n" for _,meta,url in removed),encoding="utf-8")
 count=len(kept)
 drop={i for i,_,_ in removed}
 drop.update(i+1 for i in drop)
 updated=[]
 for i,line in enumerate(lines):
  if i in drop:continue
  if any(i==j for j,_,_ in kept):
   line=GROUP.sub('group-title="📦 YEDEKLER ('+str(count)+')"',line)
  updated.append(line)
 # Fail-closed structural verification: non-backup entries unchanged and in order.
 before=[(m,u) for _,m,u in entries(lines) if not GROUP.search(m)]
 after=[(m,u) for _,m,u in entries(updated) if not GROUP.search(m)]
 if before!=after:raise RuntimeError("Protected categories changed")
 if len([1 for _,m,_ in entries(updated) if GROUP.search(m)])!=count:raise RuntimeError("Backup count mismatch")
 PLAYLIST.write_text("".join(updated),encoding="utf-8")
 report={"time_utc":stamp,"original_backup":len(backup),"kept_backup":count,
         "removed_from_player":len(removed),"foreign_archived":len(foreign_removed),
         "identity_pending_archived":len(ambiguous),"archive_snapshot":str(snapshot),
         "classification_note":"Ambiguous channels are archived as pending, not claimed foreign. IBO status not inferred."}
 (OUT/"yedek_turk_ayirma_raporu.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(report,ensure_ascii=False))
if __name__=="__main__":main()
