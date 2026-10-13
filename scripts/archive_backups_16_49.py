#!/usr/bin/env python3
"""Archive user-classified foreign channels in current YEDEKLER positions 16-49."""
import json,re
from pathlib import Path
p=Path("CALISANLAR.m3u");d=Path("madsc_kesif")
a=d/"ibo_398_16_49_yabanci_arsiv.m3u";r=d/"ibo_398_16_49_rapor.json"
if a.exists() or r.exists():raise RuntimeError("Already applied")
lines=p.read_text(encoding="utf-8-sig").splitlines(keepends=True)
items=[(i,line) for i,line in enumerate(lines) if line.startswith("#EXTINF") and 'group-title="📦 YEDEKLER' in line]
if len(items)!=398:raise RuntimeError(f"Expected 398 backups, found {len(items)}; no changes")
drop=set();archived=[]
for n,(i,m) in enumerate(items,1):
 if 16<=n<=49:
  if i+1>=len(lines) or not lines[i+1].strip().startswith(("http://","https://")):raise RuntimeError("Malformed entry")
  archived.append((n,m,lines[i+1]));drop.update((i,i+1))
if len(archived)!=34:raise RuntimeError("Wrong archive count")
out=[]
for i,line in enumerate(lines):
 if i in drop:continue
 if line.startswith("#EXTINF") and 'group-title="📦 YEDEKLER' in line:
  line=re.sub(r'group-title="📦 YEDEKLER [(][0-9]+[)]"','group-title="📦 YEDEKLER (364)"',line)
 out.append(line)
if sum(line.startswith("#EXTINF") and 'group-title="📦 YEDEKLER' in line for line in out)!=364:raise RuntimeError("Wrong retained count")
a.write_text("#EXTM3U\n"+"".join(m+u for _,m,u in archived),encoding="utf-8")
r.write_text(json.dumps({"before":398,"foreign_positions":"16-49","archived":34,"after":364,"classification":"YABANCI_KULLANICI_TESPITI","playback":"BELIRTILMEDI","archive":str(a)},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
p.write_text("".join(out),encoding="utf-8")
print("Archived 34 foreign channels; 364 remain")
