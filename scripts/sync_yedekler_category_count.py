#!/usr/bin/env python3
import re
from pathlib import Path
p=Path("CALISANLAR.m3u")
lines=p.read_text(encoding="utf-8-sig").splitlines(keepends=True)
pattern=re.compile('group-title="([^"]*YEDEKLER[^"]*)"')
count=sum(bool(pattern.search(line)) for line in lines if line.startswith("#EXTINF"))
if count==0:raise RuntimeError("YEDEKLER not found")
out=[]
for line in lines:
 if line.startswith("#EXTINF"):
  m=pattern.search(line)
  if m:
   old=m.group(1)
   clean=re.sub(r"[(][0-9]+[)]$","",old.strip()).strip()
   line=line[:m.start(1)]+clean+" ("+str(count)+")"+line[m.end(1):]
 out.append(line)
p.write_text("".join(out),encoding="utf-8")
print("YEDEKLER count:",count)
