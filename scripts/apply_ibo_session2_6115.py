#!/usr/bin/env python3
import json,re
from pathlib import Path
p=Path("CALISANLAR.m3u")
a=Path("madsc_kesif/ibo_session2_foreign_20261013.m3u")
r=Path("madsc_kesif/ibo_session2_report_20261013.json")
if a.exists() or r.exists(): raise SystemExit("Already applied")
lines=p.read_text(encoding="utf-8-sig").splitlines(keepends=True)
items=[(i,lines[i],lines[i+1]) for i in range(len(lines)-1) if lines[i].startswith("#EXTINF") and lines[i+1].strip().startswith(("http://","https://"))]
backups=[x for x in items if 'group-title="📦 YEDEKLER' in x[1]]
if len(backups)!=6115: raise SystemExit("Unexpected backup count: "+str(len(backups)))
ranges=[(3,10),(14,18),(782,782),(3504,3505),(3594,3605),(3607,3614),(3656,3662),(3666,3666),(3668,3904),(3920,3920),(4310,4311),(4987,4996),(5935,5935)]
keep={n for start,end in ranges for n in range(start,end+1)}
assert not keep.intersection({3511,3512,3564,3606,3663,3664,3665,3667})
removed={n for n in range(3,5967) if n not in keep}
indices=set()
archived=[]
for n,(i,meta,url) in enumerate(backups,1):
 if n in removed:
  indices.update([i,i+1])
  archived.extend([meta,url])
output=[line for i,line in enumerate(lines) if i not in indices]
old_protected=[(m,u) for _,m,u in items if 'group-title="📦 YEDEKLER' not in m]
new_items=[(output[i],output[i+1]) for i in range(len(output)-1) if output[i].startswith("#EXTINF") and output[i+1].strip().startswith(("http://","https://"))]
new_protected=[(m,u) for m,u in new_items if 'group-title="📦 YEDEKLER' not in m]
assert old_protected==new_protected
actual=[u for m,u in new_items if 'group-title="📦 YEDEKLER' in m]
expected=[u for n,(_,m,u) in enumerate(backups,1) if n not in removed]
assert actual==expected
a.write_text("#EXTM3U\n"+"".join(archived),encoding="utf-8")
r.write_text(json.dumps({"before":6115,"archived":len(removed),"after":len(actual),"kept_turkish":len(keep),"other_groups_unchanged":True},ensure_ascii=False,indent=2)+"\n")
p.write_text("".join(output),encoding="utf-8")
