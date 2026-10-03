import sys,subprocess,csv
from pathlib import Path
src=Path(sys.argv[1]); lines=src.read_text(encoding="utf-8-sig",errors="ignore").splitlines()
items=[]; info=None
for line in lines:
 s=line.strip()
 if s.startswith("#EXTINF:"): info=s
 elif info and s and not s.startswith("#"): items.append((info,info.split(",",1)[-1].strip(),s)); info=None
ok=["#EXTM3U"]; bad=[]; rows=[]
for i,(inf,name,url) in enumerate(items,1):
 print(f"[{i}/{len(items)}] {name}",flush=True)
 try:
  p=subprocess.run(["ffprobe","-v","error","-rw_timeout","12000000","-analyzeduration","5000000","-probesize","5000000","-select_streams","v:0","-show_entries","stream=codec_name,width,height","-of","csv=p=0",url],capture_output=True,text=True,timeout=20)
  good=p.returncode==0 and bool(p.stdout.strip()); detail=(p.stdout or p.stderr).strip().replace("\n"," ")[:500]
 except Exception as e: good=False; detail=str(e)
 if good: ok += [inf,url]
 else: bad += [name,url,""]
 rows.append([name,"CALISIYOR" if good else "CALISMIYOR",detail,url])
Path("CALISANLAR.m3u").write_text("\n".join(ok)+"\n",encoding="utf-8")
Path("CALISMAYANLAR.txt").write_text("\n".join(bad),encoding="utf-8")
with open("TEST_RAPORU.csv","w",newline="",encoding="utf-8-sig") as f:
 w=csv.writer(f); w.writerow(["Kanal","Durum","Detay","URL"]); w.writerows(rows)
