#!/usr/bin/env python3
"""Apply the user's spoken selections to CURRENT 11367-backup order, losslessly."""
import csv,json,re
from pathlib import Path
P=Path("CALISANLAR.m3u")
D=Path("madsc_kesif")
A=D/"ibo_3_5281_ayrilanlar.m3u"
C=D/"ibo_3_5281_kararlar.csv"
R=D/"ibo_3_5281_rapor.json"
# Explicitly spoken Turkish positions; 26 and 165 were explicitly withdrawn.
TURK={8,9,11,21,22,23,24,25,155,156,157,158,159,160,161,162,
      2370,2374,3362,3363,3570,3571,3665,5271,5272,5273,5274}
NOT_WORKING={3362,3363,3570,3571,3665}
WORKING={2370,2374}
def entries(lines):
 for i,m in enumerate(lines[:-1]):
  if m.startswith("#EXTINF") and lines[i+1].strip().startswith(("http://","https://")):yield i,m,lines[i+1].strip()
def main():
 if A.exists() or C.exists() or R.exists():raise RuntimeError("Already applied; refusing repeat")
 raw=P.read_text(encoding="utf-8-sig")
 lines=raw.splitlines(keepends=True)
 before=list(entries(lines))
 backups=[e for e in before if 'group-title="📦 YEDEKLER' in e[1]]
 if len(backups)!=11367:raise RuntimeError(f"Expected 11367 backups, found {len(backups)}; no changes")
 if not TURK.issubset(set(range(3,5282))):raise RuntimeError("Invalid selected positions")
 to_remove={n for n in range(3,5282) if n not in TURK}
 archived=[];drop=set()
 for n,(i,m,u) in enumerate(backups,1):
  if n in to_remove:
   archived.append((n,m,u))
   drop.update((i,i+1))
 new_count=len(backups)-len(archived)
 out=[]
 for i,line in enumerate(lines):
  if i in drop:continue
  if 'group-title="📦 YEDEKLER' in line:
   line=re.sub(r'group-title="📦 YEDEKLER \(\d+\)"',f'group-title="📦 YEDEKLER ({new_count})"',line)
  out.append(line)
 after=list(entries(out))
 protected_before=[(m,u) for _,m,u in before if 'group-title="📦 YEDEKLER' not in m]
 protected_after=[(m,u) for _,m,u in after if 'group-title="📦 YEDEKLER' not in m]
 if protected_before!=protected_after:raise RuntimeError("Protected categories changed")
 kept=[(m,u) for _,m,u in after if 'group-title="📦 YEDEKLER' in m]
 expected=[(m,u) for n,(i,m,u) in enumerate(backups,1) if n not in to_remove]
 if len(kept)!=new_count or [u for m,u in kept]!=[u for m,u in expected]:
  raise RuntimeError("Backup positions/URLs mismatch")
 A.write_text("#EXTM3U\n"+"".join(m+u+"\n" for _,m,u in archived),encoding="utf-8")
 with C.open("w",encoding="utf-8",newline="") as f:
  w=csv.writer(f);w.writerow(["original_position_in_11367","name","url","country_user","ibo_status","action"])
  for n,(i,m,u) in enumerate(backups,1):
   if n<3 or n>5281:continue
   status="CALISIYOR" if n in WORKING else "CALISMIYOR" if n in NOT_WORKING else "BELIRTILMEDI"
   w.writerow([n,m.rsplit(",",1)[-1].strip(),u,"TURK" if n in TURK else "YABANCI_KULLANICI_TESPITI",status if n in TURK else "BELIRLENMEDI","YEDEKLERDE_KALDI" if n in TURK else "ARSIVE_ALINDI"])
 report={"position_basis":"11367-current-backup-order","range":"3-5281","kept_turkish_positions":sorted(TURK),
         "turkish_kept_in_range":len(TURK),"foreign_archived":len(archived),
         "previous_backup":len(backups),"remaining_backup":new_count,
         "working_positions":sorted(WORKING),"not_working_positions":sorted(NOT_WORKING),
         "withdrawn_positions":[26,165],"untouched":"1-2 and 5282 onward; all other categories",
         "foreign_playback":"NOT_DETERMINED","archive":str(A)}
 R.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 P.write_text("".join(out),encoding="utf-8")
 print(json.dumps(report,ensure_ascii=False))
if __name__=="__main__":main()
