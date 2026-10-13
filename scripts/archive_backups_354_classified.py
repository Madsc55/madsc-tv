#!/usr/bin/env python3
"""Archive user-classified backup positions 3-334 and 335-354, retaining 1-2."""
from pathlib import Path
import json,re
p=Path("CALISANLAR.m3u"); d=Path("madsc_kesif")
tr=d/"ibo_354_3_334_turk_calismaz_arsiv.m3u"
foreign=d/"ibo_354_335_354_yabanci_arsiv.m3u"
report=d/"ibo_354_iki_kategori_rapor.json"
if any(x.exists() for x in (tr,foreign,report)): raise RuntimeError("Already processed")
lines=p.read_text(encoding="utf-8-sig").splitlines(keepends=True)
items=[i for i,line in enumerate(lines) if line.startswith("#EXTINF") and 'group-title="📦 YEDEKLER' in line]
if len(items)!=354:raise RuntimeError(f"Expected 354, found {len(items)}")
tr_items=[]; foreign_items=[];remove=set()
for pos,i in enumerate(items,1):
 if pos<=2:continue
 if i+1>=len(lines) or not lines[i+1].strip().startswith(("http://","https://")):raise RuntimeError(f"Malformed {pos}")
 entry=lines[i]+lines[i+1]
 (tr_items if pos<=334 else foreign_items).append(entry)
 remove.update([i,i+1])
if len(tr_items)!=332 or len(foreign_items)!=20:raise RuntimeError("Unexpected partition")
out=[]
for i,line in enumerate(lines):
 if i in remove:continue
 if line.startswith("#EXTINF") and 'group-title="📦 YEDEKLER' in line:
  line=re.sub(r'group-title="📦 YEDEKLER \(\d+\)"','group-title="📦 YEDEKLER (2)"',line)
 out.append(line)
if sum(x.startswith("#EXTINF") and 'group-title="📦 YEDEKLER' in x for x in out)!=2:raise RuntimeError("Wrong count")
d.mkdir(exist_ok=True)
tr.write_text("#EXTM3U\n"+"".join(tr_items),encoding="utf-8")
foreign.write_text("#EXTM3U\n"+"".join(foreign_items),encoding="utf-8")
report.write_text(json.dumps({"before":354,"kept_positions":"1-2","turkish_user_reported_not_working":{"positions":"3-334","count":332,"archive":str(tr),"status":"KULLANICI_BILDIRIMI_TEST_EDILMEDI"},"foreign_user_identified":{"positions":"335-354","count":20,"archive":str(foreign)},"after":2},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
p.write_text("".join(out),encoding="utf-8")
print("Retained 2; archived 332 user-reported nonworking Turkish, 20 foreign")
