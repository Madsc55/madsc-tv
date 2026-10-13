#!/usr/bin/env python3
"""Apply user IBO decisions by original 1-based YEDEKLER positions, losslessly."""
import csv,json,re
from pathlib import Path
P=Path("CALISANLAR.m3u")
D=Path("madsc_kesif")
REPORT=D/"ibo_kullanici_kararlari_20261013_grup1.json"
CSV=D/"ibo_kullanici_kararlari_20261013_grup1.csv"
ARCH=D/"ibo_yedeklerden_ayrilanlar_20261013_grup1.m3u"
BAD=set(range(6,9))|set(range(11,43))|{104}
FOREIGN=set(range(43,240))-{104}
REMOVE=BAD|FOREIGN
def entries(lines):
 for i,m in enumerate(lines[:-1]):
  if m.startswith("#EXTINF") and lines[i+1].strip().startswith(("http://","https://")):
   yield i,m,lines[i+1].strip()
def main():
 raw=P.read_text(encoding="utf-8-sig")
 lines=raw.splitlines(keepends=True)
 all_entries=list(entries(lines))
 backup=[(i,m,u) for i,m,u in all_entries if 'group-title="📦 YEDEKLER' in m]
 if (D/"ibo_ilk_239_ayirma_raporu.json").exists():
  print("Corrected group 1 already applied by successful workflow; no duplicate changes")
  return
 if len(backup)!=11599:raise RuntimeError(f"Expected 11599 original backups; found {len(backup)}. Refuse to alter positions.")
 if len(REMOVE)!=232 or len(BAD)!=36 or len(FOREIGN)!=196 or BAD&FOREIGN:raise RuntimeError("Invalid decision ranges")
 removed=[];drop=set()
 for n,(i,m,u) in enumerate(backup,1):
  if n in REMOVE:
   removed.append((n,m,u,"TURK_CALISMIYOR" if n in BAD else "YABANCI_KULLANICI_TESPITI"))
   drop.update((i,i+1))
 if len(removed)!=232:raise RuntimeError("Missing expected entries")
 kept=len(backup)-len(removed)
 out=[]
 for i,line in enumerate(lines):
  if i in drop:continue
  if 'group-title="📦 YEDEKLER' in line:
   line=re.sub(r'group-title="📦 YEDEKLER \(\d+\)"',f'group-title="📦 YEDEKLER ({kept})"',line)
  out.append(line)
 before=[(m,u) for _,m,u in all_entries if 'group-title="📦 YEDEKLER' not in m]
 after=[(m,u) for _,m,u in entries(out) if 'group-title="📦 YEDEKLER' not in m]
 if before!=after:raise RuntimeError("Protected categories changed")
 if sum('group-title="📦 YEDEKLER' in m for _,m,_ in entries(out))!=kept:raise RuntimeError("Remaining backup mismatch")
 ARCH.write_text("#EXTM3U\n"+"".join(m+u+"\n" for _,m,u,_ in removed),encoding="utf-8")
 with CSV.open("w",encoding="utf-8",newline="") as f:
  w=csv.writer(f);w.writerow(["original_backup_position","channel","url","user_decision"])
  for n,m,u,status in removed:w.writerow([n,m.rsplit(",",1)[-1].strip(),u,status])
 report={"original_backup_count":len(backup),"removed_turkish_not_working":len(BAD),
         "removed_foreign_user_identified":len(FOREIGN),"removed_total":len(removed),
         "remaining_backup_count":kept,"turkish_not_working_positions":"6-8, 11-42, 104",
         "foreign_positions":"43-239","archive":str(ARCH),"decisions_csv":str(CSV),
         "protected_other_categories":"UNCHANGED","position_basis":"YEDEKLER original 11599 order before this change"}
 REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 P.write_text("".join(out),encoding="utf-8")
 print(json.dumps(report,ensure_ascii=False))
if __name__=="__main__":main()
