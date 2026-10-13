#!/usr/bin/env python3
"""Synchronize YEDEKLER display label with actual number of channel entries."""
import re
from pathlib import Path
p=Path("CALISANLAR.m3u")
lines=p.read_text(encoding="utf-8-sig").splitlines(keepends=True)
pattern=re.compile(r'group-title="([^"]*YEDEKLER[^"]*)"')
backup=[]
for line in lines:
 if line.startswith("#EXTINF"):
  m=pattern.search(line)
  if m: backup.append(line)
if not backup:raise RuntimeError("No backup group detected; no changes")
count=len(backup)
out=[]
for line in lines:
 if line.startswith("#EXTINF") and pattern.search(line):
  line=pattern.sub(lambda m:'group-title="'+re.sub(r'\\s*\\(\\d+\\)\\s*$','',m.group(1)).rstrip()+f' ({count})"',line,count=1)
 out.append(line)
if sum(bool(pattern.search(x)) for x in out if x.startswith("#EXTINF"))!=count:raise RuntimeError("Count mismatch")
p.write_text("".join(out),encoding="utf-8")
print(f"YEDEKLER actual channels: {count}; display label updated")
