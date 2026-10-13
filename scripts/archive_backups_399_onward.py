#!/usr/bin/env python3
"""Archive backups 399 onward from the current 530-order, preserving 1..398."""
import json,re
from pathlib import Path
p=Path("CALISANLAR.m3u");d=Path("madsc_kesif")
a=d/"ibo_530_399_sonrasi_yabanci_arsiv.m3u";r=d/"ibo_530_399_sonrasi_rapor.json"
if a.exists() or r.exists():raise RuntimeError("Already applied")
lines=p.read_text(encoding="utf-8-sig").splitlines(keepends=True)
items=[(i,line) for i,line in enumerate(lines) if line.startswith("#EXTINF") and 'group-title="📦 YEDEKLER' in line]
if len(items)!=530:raise RuntimeError(f"Expected 530 backup entries, got {len(items)}; no changes")
drop=set();archived=[]
for n,(i,m) in enumerate(items,1):
 if n>=399:
  if i+1>=len(lines) or not lines[i+1].strip().startswith(("http://","https://")):raise RuntimeError("Malformed entry")
  archived.append((n,m,lines[i+1]))
  drop.update((i,i+1))
out=[]
for i,line in enumerate(lines):
 if i in drop:continue
 if line.startswith("#EXTINF") and 'group-title="📦 YEDEKLER' in line:
  line=re.sub(r'group-title="📦 YEDEKLER [(][0-9]+[)]"', 'group-title="📦 YEDEKLER (398)"',line)
 out.append(line)
if len(archived)!=132:raise RuntimeError("Wrong archive size")
kept=[line for line in out if line.startswith("#EXTINF") and 'group-title="📦 YEDEKLER' in line]
if len(kept)!=398:raise RuntimeError("Wrong retained count")
a.write_text("#EXTM3U\n"+"".join(m+u for _,m,u in archived),encoding="utf-8")
r.write_text(json.dumps({"before":530,"kept_positions":"1-398","archived_positions":"399-530","archived":132,"after":398,"archive":str(a)},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
p.write_text("".join(out),encoding="utf-8")
print("Archived 132 foreign backups, kept 398")
if __name__=="__main__":pass
