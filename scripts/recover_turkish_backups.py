#!/usr/bin/env python3
"""Recover Turkish channels from the lossless backup snapshot using positive country evidence.

Do not classify unknown as foreign. Do not touch protected non-backup groups.
"""
import csv, json, re, urllib.request
from pathlib import Path
from urllib.parse import urlsplit,parse_qsl,urlencode,urlunsplit
ROOT=Path("madsc_kesif")
PLAY=Path("CALISANLAR.m3u")
SNAP=ROOT/"yedeklerden_ayrilanlar_20261013T170042Z.m3u"
REG=ROOT/"bulunan_kanal_arsivi.csv"
FOREIGN=Path("YABANCI_KANALLAR.m3u")
def key(u):
 p=urlsplit(u.strip())
 q=[(k,v) for k,v in parse_qsl(p.query) if k.lower() not in {"token","auth","expires","signature","sig","hash"}]
 return urlunsplit((p.scheme.lower(),p.netloc.lower(),p.path.rstrip("/"),urlencode(sorted(q)),""))
def entries(lines):
 for i,m in enumerate(lines[:-1]):
  if m.startswith("#EXTINF") and lines[i+1].strip().startswith(("https://","http://")):yield i,m,lines[i+1].strip()
def get(url):
 req=urllib.request.Request(url,headers={"User-Agent":"MADSC-Turkish-channel-audit/1.0"})
 with urllib.request.urlopen(req,timeout=35) as r:return r.read().decode("utf-8-sig")
def main():
 original=PLAY.read_text(encoding="utf-8-sig").splitlines(keepends=True)
 archived=SNAP.read_text(encoding="utf-8-sig").splitlines(keepends=True)
 with REG.open(encoding="utf-8-sig",newline="") as f:
  registry={key(r["url"]):r for r in csv.DictReader(f) if r.get("url")}
 foreign={key(u) for _,_,u in entries(FOREIGN.read_text(encoding="utf-8-sig").splitlines(keepends=True))}
 # IPTV-org publishes country-filtered source metadata, not guesses based on labels.
 tr=get("https://iptv-org.github.io/iptv/countries/tr.m3u").splitlines(keepends=True)
 tr_urls={key(u) for _,_,u in entries(tr)}
 tr_ids=set()
 for _,m,_ in entries(tr):
  match=re.search(r'tvg-id="([^"]+)"',m)
  if match and match.group(1):tr_ids.add(match.group(1).casefold())
 if not tr_urls:raise RuntimeError("Turkey country playlist unavailable; abort without edits")
 existing={key(u) for _,_,u in entries(original)}
 backups=[(i,m,u) for i,m,u in entries(original) if 'group-title="📦 YEDEKLER' in m]
 if not backups:raise RuntimeError("No existing backups")
 restored=[];remaining=[];foreign_count=0
 for _,m,u in entries(archived):
  k=key(u)
  if k in existing:continue
  r=registry.get(k,{})
  source=r.get("kaynaklar","").lower()
  id_match=re.search(r'tvg-id="([^"]+)"',m)
  channel_id=id_match.group(1).casefold() if id_match else ""
  positive=(k in tr_urls or (channel_id and channel_id in tr_ids)
      or bool(re.search(r'(^|[^a-z])(iptv-org-tr|iptv-org-turkiye|dearbulut-tr|turkiye|türkiye)([^a-z]|$)',source)))
  if k in foreign:
   foreign_count+=1;remaining.append((m,u,"FOREIGN_ARCHIVE"))
  elif positive:
   restored.append((m,u));existing.add(k)
  else:remaining.append((m,u,"COUNTRY_NOT_VERIFIED"))
 count=len(backups)+len(restored)
 updated=[]
 for line in original:
  if 'group-title="📦 YEDEKLER' in line:
   line=re.sub(r'group-title="📦 YEDEKLER \(\d+\)"','group-title="📦 YEDEKLER ('+str(count)+')"',line)
  updated.append(line)
 for m,u in restored:
  meta=re.sub(r'group-title="[^"]*"','group-title="📦 YEDEKLER ('+str(count)+')"',m)
  if 'group-title=' not in meta:meta=meta.rstrip("\n").replace(",",' group-title="📦 YEDEKLER ('+str(count)+')",',1)+"\n"
  updated.extend([meta,u+"\n"])
 before=[(m,u) for _,m,u in entries(original) if 'group-title="📦 YEDEKLER' not in m]
 after=[(m,u) for _,m,u in entries(updated) if 'group-title="📦 YEDEKLER' not in m]
 if before!=after:raise RuntimeError("Protected categories changed")
 if sum('group-title="📦 YEDEKLER' in m for _,m,_ in entries(updated))!=count:raise RuntimeError("Count mismatch")
 report={"previous_backup":len(backups),"turkish_restored":len(restored),"backup_after":count,
         "remaining_unverified":sum(s=="COUNTRY_NOT_VERIFIED" for _,_,s in remaining),
         "foreign_archive_matches":foreign_count,"country_source":"iptv-org countries/tr.m3u",
         "note":"Not a definitive count of all Turkish channels; unknown entries remain archived and may contain Turkish channels."}
 # Keep a structured per-URL review record without mislabeling unknown as foreign.
 with (ROOT/"yedek_ulke_inceleme.csv").open("w",encoding="utf-8",newline="") as f:
  w=csv.writer(f);w.writerow(["channel","url","status"])
  for m,u,s in remaining:w.writerow([m.rsplit(",",1)[-1].strip(),u,s])
 PLAY.write_text("".join(updated),encoding="utf-8")
 (ROOT/"yedek_turk_yeniden_inceleme_raporu.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(report,ensure_ascii=False))
if __name__=="__main__":main()
