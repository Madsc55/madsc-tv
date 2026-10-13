#!/usr/bin/env python3
"""Second voice review; use fixed 6115 backup order; lossless archival."""
import csv,json,re
from pathlib import Path
p=Path("CALISANLAR.m3u");d=Path("madsc_kesif")
a=d/"ibo_6115_second_foreign.m3u";c=d/"ibo_6115_second_decisions.csv";r=d/"ibo_6115_second_report.json"
# Spoken selections. Last correction: 3555-3904 Turkish except 3564.
turk=set(range(3,11))|set(range(14,19))|{782,3504,3505,3920,4310,4311,5935}|set(range(3555,3905))|set(range(4987,4997))
turk.discard(3564)
def entries(lines):
 for i,m in enumerate(lines[:-1]):
  if m.startswith("#EXTINF") and lines[i+1].strip().startswith(("http://","https://")):yield i,m,lines[i+1].strip()
def main():
 if any(x.exists() for x in (a,c,r)):raise RuntimeError("Already applied")
 lines=p.read_text(encoding="utf-8-sig").splitlines(keepends=True)
 before=list(entries(lines));backup=[x for x in before if 'group-title="📦 YEDEKLER' in x[1]]
 if len(backup)!=6115:raise RuntimeError("Expected 6115 backup channels; no changes")
 foreign=set(range(3,5967))-turk
 drop=set();removed=[]
 for n,(i,m,u) in enumerate(backup,1):
  if n in foreign:drop.update((i,i+1));removed.append((n,m,u))
 count=len(backup)-len(removed)
 out=[]
 for i,line in enumerate(lines):
  if i in drop:continue
  if 'group-title="📦 YEDEKLER' in line:line=re.sub(r'group-title="📦 YEDEKLER \\(\\d+\\)"',f'group-title="📦 YEDEKLER ({count})"',line)
  out.append(line)
 after=list(entries(out))
 protected=lambda es:[(m,u) for _,m,u in es if 'group-title="📦 YEDEKLER' not in m]
 if protected(before)!=protected(after):raise RuntimeError("Protected groups changed")
 actual=[u for _,m,u in after if 'group-title="📦 YEDEKLER' in m]
 expected=[u for n,(_,m,u) in enumerate(backup,1) if n not in foreign]
 if actual!=expected:raise RuntimeError("Retained URLs changed")
 a.write_text("#EXTM3U\n"+"".join(m+u+"\n" for _,m,u in removed),encoding="utf-8")
 with c.open("w",newline="",encoding="utf-8") as f:
  w=csv.writer(f);w.writerow(["original_6115_position","name","url","country","action","playback"])
  for n,(_,m,u) in enumerate(backup,1):
   if 3<=n<=5966:w.writerow([n,m.rsplit(",",1)[-1],u,"TURK" if n in turk else "YABANCI","KALDI" if n in turk else "ARSIV","BELIRLENMEDI"])
 result={"baseline":6115,"reviewed":"3-5966","turkish_kept":len(turk),"foreign_archived":len(removed),"remaining_backup":count,"untouched":"1-2 and 5967-6115","possible_encrypted":"3555-3904; not tested","retracted":"3511,3512,3564 and 5936-5966"}
 r.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 p.write_text("".join(out),encoding="utf-8")
 print(result)
if __name__=="__main__":main()
