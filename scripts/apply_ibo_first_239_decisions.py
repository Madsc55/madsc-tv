#!/usr/bin/env python3
"""Record user IBO decisions by ORIGINAL 1-based YEDEKLER positions and remove from player only."""
import csv,json,re,datetime
from pathlib import Path
P=Path("CALISANLAR.m3u")
ROOT=Path("madsc_kesif")
DEC=ROOT/"ibo_kullanici_kararlari.csv"
REPORT=ROOT/"ibo_ilk_239_ayirma_raporu.json"
TURK=set(range(6,9))|set(range(11,43))|{104}
FOREIGN=set(range(43,240))-{104}
def main():
 lines=P.read_text(encoding="utf-8-sig").splitlines(keepends=True)
 entries=[]
 for i,line in enumerate(lines[:-1]):
  if line.startswith("#EXTINF") and lines[i+1].strip().startswith(("http://","https://")):
   entries.append((i,line,lines[i+1]))
 backups=[e for e in entries if 'group-title="📦 YEDEKLER' in e[1]]
 if len(backups)!=11599:raise RuntimeError(f"Expected 11599 backups before positional action; found {len(backups)}")
 positions={i+1:e for i,e in enumerate(backups)}
 selected={p:positions[p] for p in sorted(TURK|FOREIGN)}
 if len(selected)!=len(TURK)+len(FOREIGN):raise RuntimeError("Selection mismatch")
 if DEC.exists():raise RuntimeError("Decision file already exists; avoid duplicate overwrite")
 with DEC.open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.writer(f);w.writerow(["original_backup_position","channel","url","country_user","ibo_user","source"])
  for p,(i,m,u) in selected.items():
   w.writerow([p,m.rsplit(",",1)[-1].strip(),u.strip(),"TURK" if p in TURK else "YABANCI","CALISMIYOR" if p in TURK else "BELIRLENMEDI","USER_2026-10-13"])
 drop={i for i,m,u in selected.values()}
 drop|={i+1 for i in list(drop)}
 count=len(backups)-len(selected)
 updated=[]
 for i,line in enumerate(lines):
  if i in drop:continue
  if 'group-title="📦 YEDEKLER' in line:
   line=re.sub(r'group-title="📦 YEDEKLER \(\d+\)"',f'group-title="📦 YEDEKLER ({count})"',line)
  updated.append(line)
 before=[(m,u) for i,m,u in entries if 'group-title="📦 YEDEKLER' not in m]
 after=[(m,u) for i,m,u in ((j,m,updated[j+1]) for j,m in enumerate(updated[:-1]) if m.startswith("#EXTINF") and updated[j+1].strip().startswith(("http://","https://"))) if 'group-title="📦 YEDEKLER' not in m]
 if before!=after:raise RuntimeError("Protected channels changed")
 if sum('group-title="📦 YEDEKLER' in m for m,u in [(m,updated[j+1]) for j,m in enumerate(updated[:-1]) if m.startswith("#EXTINF") and updated[j+1].strip().startswith(("http://","https://"))])!=count:raise RuntimeError("Count mismatch")
 P.write_text("".join(updated),encoding="utf-8")
 report={"original_backup":11599,"turkish_not_working_removed":len(TURK),"foreign_unknown_playback_removed":len(FOREIGN),"total_removed":len(selected),"remaining_backup":count,"decision_file":str(DEC),"note":"Positions refer to original 11599 backup order; foreign playback status UNDETERMINED"}
 REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(report,ensure_ascii=False))
if __name__=="__main__":main()
