#!/usr/bin/env python3
"""User-requested, one-time archive-to-backup staging. Does not test playback."""
import csv
import re
from pathlib import Path
from urllib.parse import urlsplit,parse_qsl,urlencode,urlunsplit

playlist=Path("CALISANLAR.m3u")
registry=Path("madsc_kesif/bulunan_kanal_arsivi.csv")
foreign=Path("YABANCI_KANALLAR.m3u")
def key(u):
 p=urlsplit(u.strip())
 q=[(k,v) for k,v in parse_qsl(p.query) if k.lower() not in {"token","auth","expires","signature","sig","hash"}]
 return urlunsplit((p.scheme.lower(),p.netloc.lower(),p.path.rstrip("/"),urlencode(sorted(q)),""))
def entries(s):
 ls=s.splitlines()
 for i,line in enumerate(ls):
  if line.startswith("#EXTINF") and i+1<len(ls) and ls[i+1].strip().startswith(("http://","https://")):
   yield line,ls[i+1].strip()
def safe(s):
 return re.sub(r'[\r\n",]',' ',s or "").strip()[:140]
def main():
 original=playlist.read_text(encoding="utf-8-sig")
 known={key(url) for _,url in entries(original)}
 additions=[]
 def stage(label,url):
  if not url.startswith(("http://","https://")) or key(url) in known:return
  known.add(key(url))
  label=safe(label) or "Isimsiz aday"
  additions.append((label,url))
 with registry.open(encoding="utf-8-sig",newline="") as f:
  for r in csv.DictReader(f):stage(r.get("kanal",""),r.get("url",""))
 for meta,url in entries(foreign.read_text(encoding="utf-8-sig")):
  stage(meta.rsplit(",",1)[-1],url)
 if not additions:
  print("No new backup candidates")
  return
 # Existing backup group counts are metadata only; never alter other categories.
 old=list(entries(original))
 backup=sum('group-title="📦 YEDEKLER' in meta for meta,_ in old)
 count=backup+len(additions)
 updated=re.sub(r'group-title="📦 YEDEKLER \(\d+\)"',
                'group-title="📦 YEDEKLER ('+str(count)+')"',original)
 suffix="".join('#EXTINF:-1 tvg-name="'+label+'" group-title="📦 YEDEKLER ('+str(count)+')",'+label+'\n'+url+'\n' for label,url in additions)
 playlist.write_text(updated.rstrip("\n")+"\n"+suffix,encoding="utf-8")
 print("Existing backup:",backup,"new:",len(additions),"total backup:",count)
if __name__=="__main__":main()
