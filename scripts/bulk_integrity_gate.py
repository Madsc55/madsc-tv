#!/usr/bin/env python3
"""Read-only integrated IPTV integrity gate; never edits protected playlists."""
import csv,json,re
from pathlib import Path
from urllib.parse import urlsplit,parse_qsl,urlencode,urlunsplit

def key(url):
 p=urlsplit(url)
 q=[(k,v) for k,v in parse_qsl(p.query) if k.lower() not in {"token","auth","expires","signature","sig","hash"}]
 return urlunsplit((p.scheme.lower(),p.netloc.lower(),p.path.rstrip("/"),urlencode(sorted(q)),""))
def main():
 lines=Path("CALISANLAR.m3u").read_text(encoding="utf-8-sig").splitlines()
 assert lines and lines[0].startswith("#EXTM3U")
 entries=[]
 for i,line in enumerate(lines):
  if line.startswith("#EXTINF"):
   assert i+1<len(lines) and lines[i+1].startswith(("http://","https://")),f"Missing stream after line {i+1}"
   entries.append((line,lines[i+1]))
 urls=[key(url) for _,url in entries]
 groups={}
 for meta,_ in entries:
  group=re.search(r'group-title="([^"]+)"',meta)
  group=group.group(1) if group else "BILINMIYOR"
  groups[group]=groups.get(group,0)+1
 backup=[(meta,url) for meta,url in entries if "YEDEKLER" in meta]
 assert backup,"YEDEKLER is empty"
 # Same stream may intentionally occur in HEPSI and FAVORILER; never delete it.
 # Only duplicates within the newly staged YEDEKLER are a blocking error.
 backup_urls=[key(url) for meta,url in entries if "YEDEKLER" in meta]
 backup_duplicate_count=len(backup_urls)-len(set(backup_urls))
 assert backup_duplicate_count==0,"Duplicate normalized stream URLs inside YEDEKLER"
 assert sum(groups.values())==len(entries)
 with Path("madsc_kesif/bulunan_kanal_arsivi.csv").open(encoding="utf-8-sig",newline="") as f:
  archived=list(csv.DictReader(f))
 archived_keys={key(r["url"]) for r in archived if r.get("url")}
 backup_keys={key(url) for _,url in backup}
 foreign=Path("YABANCI_KANALLAR.m3u").read_text(encoding="utf-8-sig")
 foreign_urls=[key(s.strip()) for s in foreign.splitlines() if s.startswith(("http://","https://"))]
 report={"playlist_channels":len(entries),"backup_channels":len(backup),
         "cross_category_url_repeats_allowed":len(urls)-len(set(urls)),
         "backup_duplicate_urls":backup_duplicate_count,
         "other_channels":len(entries)-len(backup),"archive_unique_urls":len(archived_keys),
         "archive_urls_in_backups":len(archived_keys & backup_keys),
         "foreign_archive_urls":len(foreign_urls),
         "foreign_archive_urls_in_backups":len(set(foreign_urls)&backup_keys),
         "groups":groups,"status":"STRUCTURE_PASS_NOT_PLAYBACK_PROOF",
         "ibo_test":"USER_ONLY","technical_failure_does_not_prove_ibo_failure":True}
 Path("madsc_kesif/toplu_butunluk_kontrol.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(report,ensure_ascii=False))
if __name__=="__main__":main()
