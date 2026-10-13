#!/usr/bin/env python3
"""Restore the exact pre-filter backup population from the lossless snapshot.

Only changes backup group count and appends archived backup entries.
Other groups and archived evidence are preserved.
"""
import json,re
from pathlib import Path
from urllib.parse import urlsplit,parse_qsl,urlencode,urlunsplit
P=Path("CALISANLAR.m3u")
SNAP=Path("madsc_kesif/yedeklerden_ayrilanlar_20261013T170042Z.m3u")
REPORT=Path("madsc_kesif/yedek_11599_geri_yukleme_raporu.json")
def key(u):
 p=urlsplit(u.strip())
 q=[(k,v) for k,v in parse_qsl(p.query) if k.lower() not in {"token","auth","expires","signature","sig","hash"}]
 return urlunsplit((p.scheme.lower(),p.netloc.lower(),p.path.rstrip("/"),urlencode(sorted(q)),""))
def entries(lines):
 for i,m in enumerate(lines[:-1]):
  if m.startswith("#EXTINF") and lines[i+1].strip().startswith(("http://","https://")):yield m,lines[i+1]
def main():
 original=P.read_text(encoding="utf-8-sig")
 archive=SNAP.read_text(encoding="utf-8-sig")
 old=list(entries(original.splitlines()))
 existing={key(u) for _,u in old}
 backups=[(m,u) for m,u in old if 'group-title="📦 YEDEKLER' in m]
 to_restore=[]
 for m,u in entries(archive.splitlines()):
  if key(u) in existing:continue
  existing.add(key(u))
  to_restore.append((m,u))
 target=len(backups)+len(to_restore)
 if target!=11599:
  raise RuntimeError(f"Expected original 11599 backups, found {target}; refusing destructive edit")
 updated=re.sub(r'group-title="📦 YEDEKLER \(\d+\)"',
                'group-title="📦 YEDEKLER (11599)"',original)
 suffix="".join(re.sub(r'group-title="📦 YEDEKLER \(\d+\)"',
                       'group-title="📦 YEDEKLER (11599)"',m)+"\n"+u+"\n"
                for m,u in to_restore)
 updated=updated.rstrip("\n")+"\n"+suffix
 after=list(entries(updated.splitlines()))
 before_protected=[(m,u) for m,u in old if 'group-title="📦 YEDEKLER' not in m]
 after_protected=[(m,u) for m,u in after if 'group-title="📦 YEDEKLER' not in m]
 if before_protected!=after_protected:raise RuntimeError("Protected groups changed")
 if sum('group-title="📦 YEDEKLER' in m for m,u in after)!=11599:
  raise RuntimeError("Backup group count mismatch")
 P.write_text(updated,encoding="utf-8")
 REPORT.write_text(json.dumps({"before_backup":len(backups),"restored":len(to_restore),
   "after_backup":11599,"protected_categories":"UNCHANGED",
   "source_archive":str(SNAP),"foreign_and_uncertain":"RESTORED_FOR_USER_IBO_REVIEW",
   "ibo_playback":"NOT_TESTED"},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(REPORT.read_text())
if __name__=="__main__":main()
