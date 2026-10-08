import csv, re, urllib.request, concurrent.futures, json, subprocess
from urllib.parse import urlsplit
def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
    return urllib.request.urlopen(req,timeout=20).read().decode('utf-8-sig','replace')
def parse(txt):
    out=[]; meta=''
    for line in txt.splitlines():
        line=line.strip()
        if line.startswith('#EXTINF:'): meta=line
        elif line.startswith(('http://','https://')) and meta:
            out.append((meta.split(',',1)[-1],line,re.search(r'tvg-id="([^"]*)"',meta).group(1) if 'tvg-id="' in meta else ''))
            meta=''
    return out
def norm(s):
    s=s.casefold().translate(str.maketrans('ıİşğüöç','iisguoc'))
    s=re.sub(r'\[[^]]*\]|\([^)]*\)','',s)
    s=re.sub(r'\b(1440p|1080p|900p|720p|576p|480p|360p|hd|fhd|uhd|qhd|aday|alternatif)\b','',s)
    return re.sub(r'[^a-z0-9]','',s)
old=parse(open('CALISANLAR.m3u',encoding='utf-8-sig').read())
oldurls={u for _,u,_ in old}; oldnames={norm(n) for n,_,_ in old}
source=parse(get('https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr.m3u'))
seen=set(); candidates=[]
for n,u,cid in source:
    if u in oldurls or u in seen: continue
    seen.add(u)
    if not u.startswith(('https://','http://')):continue
    candidates.append((n,u,cid,'ALTERNATIF' if norm(n) in oldnames else 'YENI'))
try:
    logos=json.loads(get('https://iptv-org.github.io/api/logos.json'))
    logo_by_id={}
    for item in logos:
        if item.get('channel') and item.get('url') and item.get('in_use'):
            logo_by_id.setdefault(item['channel'],item['url'])
except Exception: logo_by_id={}
def check(item):
    n,u,cid,kind=item
    try:
        p=subprocess.run(['ffprobe','-v','error','-rw_timeout','9000000','-analyzeduration','1000000','-probesize','1000000','-show_entries','stream=codec_type','-of','csv=p=0',u],capture_output=True,text=True,timeout=14)
        status='ERISIM_VAR' if p.returncode==0 and ('video' in p.stdout or 'audio' in p.stdout) else 'DOGRULANAMADI'
    except Exception:status='DOGRULANAMADI'
    return (n,kind,status,u,cid,logo_by_id.get(cid,''),'LOGO_ADAY' if logo_by_id.get(cid) else 'LOGO_YOK')
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
    results=list(pool.map(check,candidates))
with open('YENI_ADAY_ON_TEST.csv','w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['KANAL','TUR','ON_TEST','URL','TVG_ID','LOGO_URL','LOGO_DURUM']);w.writerows(results)
print('ANA_LISTE',len(old),'KAYNAK',len(source),'ADAY',len(candidates),'ON_TEST_ERISIM',sum(r[2]=='ERISIM_VAR' for r in results),'LOGO_ADAY',sum(bool(r[5]) for r in results))
