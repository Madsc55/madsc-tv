#!/usr/bin/env python3
"""Archive current YEDEKLER positions 355-364 as user-confirmed foreign channels."""
import json,re
from pathlib import Path
p=Path("CALISANLAR.m3u");d=Path("madsc_kesif")
a=d/"ibo_364_355_364_yabanci_arsiv.m3u";r=d/"ibo_364_355_364_rapor.json"
if a.exists() or r.exists():raise RuntimeError("Already applied")
lines=p.read_text(encoding="utf-8-sig").splitlines(keepends=True)
items=[(i,line) for i,line in enumerate(lines) if line.startswith("#EXTINF") and 'group-title="📦 YEDEKLER' in line]
if len(items)!=364:raise RuntimeError(f"Expected 364 backups, found {len(items)}; no changes")
drop=set();archived=[]
for n,(i,m) in enumerate(items,1):
 if 355<=n<=364:
  if i+1>=len(lines) or not lines[i+1].strip().startswith(("http://","https://")):raise RuntimeError("Malformed entry")
  archived.append((n,m,lines[i+1]));drop.update((i,i+1))
if len(archived)!=10:raise RuntimeError("Wrong archive count")
out=[]
for i,line in enumerate(lines):
 if i in drop:continue
 if line.startswith("#EXTINF") and 'group-title="📦 YEDEKLER' in line:
  line=re.sub(r'group-title="📦 YEDEKLER [(][0-9]+[)]"','group-title="📦 YEDEKLER (354)"',line)
 out.append(line)
if sum(line.startswith("#EXTINF") and 'group-title="📦 YEDEKLER' in line for line in out)!=354:raise RuntimeError("Wrong retained count")
a.write_text("#EXTM3U\n"+"".join(m+u for _,m,u in archived),encoding="utf-8")
r.write_text(json.dumps({"before":364,"foreign_positions":"355-364","archived":10,"after":354,"classification":"YABANCI_KULLANICI_TESPITI","playback":"BELIRTILMEDI","archive":str(a)},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
p.write_text("".join(out),encoding="utf-8")
print("Archived 10 foreign channels; 354 remain")
