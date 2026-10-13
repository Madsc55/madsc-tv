#!/usr/bin/env python3
"""Second IBO voice selection; use the exact pre-change 6115 backup positions."""
import csv,json,re
from pathlib import Path
P=Path("CALISANLAR.m3u"); D=Path("madsc_kesif")
A=D/"ibo_6115_ikinci_ayrilanlar.m3u";C=D/"ibo_6115_ikinci_kararlar.csv";R=D/"ibo_6115_ikinci_rapor.json"
T=set(range(3,11))|set(range(14,19))|{782,3504,3505,3920,4310,4311,5935}|set(range(3555,3905))|set(range(4987,4997))
T-={3564}
def entries(lines):
 for i,m in enumerate(lines[:-1]):
  if m.startswith("#EXTINF") and lines[i+1].strip().startswith(("http://","https://")):yield i,m,lines[i+1].strip()
def main():
 if A.exists() or C.exists() or R.exists():raise RuntimeError("Already applied")
 lines=P.read_text(encoding="utf-8-sig").splitlines(keepends=True)
 before=list(entries(lines))
 backups=[x for x in before if 'group-title="📦 YEDEKLER' in x[1]]
 if len(backups)!=6115:raise RuntimeError(f"Expected 6115, found {len(backups)}; no change")
 foreign=set(range(3,5967))-T
 drop=set();removed=[]
 for n,(i,m,u) in enumerate(backups,1):
  if n in foreign:drop.update((i,i+1));removed.append((n,m,u))
 count=len(backups)-len(removed);out=[]
 for i,line in enumerate(lines):
  if i in drop:continue
  if 'group-title="📦 YEDEKLER' in line:line=re.sub(r'group-title="📦 YEDEKLER \\(\\d+\\)"',f'group-title="📦 YEDEKLER ({count})"',line)
  out.append(line)
 after=list(entries(out))
 protected=lambda a:[(m,u) for _,m,u in a if 'group-title="📦 YEDEKLER' not in m]
 if protected(before)!=protected(after):raise RuntimeError("Protected categories changed")
 actual=[u for _,m,u in after if 'group-title="📦 YEDEKLER' in m]
 expected=[u for n,(_,m,u) in enumerate(backups,1) if n not in foreign]
 if actual!=expected:raise RuntimeError("URLs changed")
 A.write_text("#EXTM3U\n"+"".join(m+u+"\n" for _,m,u in removed),encoding="utf-8")
 with C.open("w",newline="",encoding="utf-8") as f:
  w=csv.writer(f);w.writerow(["position_in_6115","name","url","country","action","playback"])
  for n,(_,m,u) in enumerate(backups,1):
   if 3<=n<=5966:w.writerow([n,m.rsplit(",",1)[-1],u,"TURK" if n in T else "YABANCI","KALDI" if n in T else "ARSIV","BELIRTILMEDI"])
 result={"before":6115,"turkish_kept_in_review":len(T),"foreign_archived":len(removed),"after":count,"reviewed":"3-5966","unreviewed":"1-2,5967-6115","note":"3555-3904 user suspected encrypted; 3564 explicitly excluded; 5936-5966 excluded"}
 R.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 P.write_text("".join(out),encoding="utf-8")
 print(result)
if __name__=="__main__":main()
