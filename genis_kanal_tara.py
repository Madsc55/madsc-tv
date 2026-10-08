import csv,re,urllib.request,concurrent.futures,subprocess,unicodedata
SOURCES={
'iptv-org':'https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr.m3u',
'omerdenizhan':'https://raw.githubusercontent.com/omerdenizhan/IPTV-M3U/main/m3u/turkiye.m3u',
'ilyswch':'https://raw.githubusercontent.com/ilyswch/turk-iptv/main/index.m3u',
'itasli':'https://itasli.github.io/TURKTV/index.m3u',
'Yusiff0':'https://raw.githubusercontent.com/Yusiff0/IPTV-Azerbaycan-ve-Turkiye-kanallari/main/az_tr.m3u',
'gkhncksn':'https://raw.githubusercontent.com/gkhncksn/m3u8_lists/main/TURK_KANALLARI.m3u',
'Lunedor':'https://raw.githubusercontent.com/Lunedor/iptvTR/main/iptv_tum_kanallar.m3u',
'maotuon':'https://raw.githubusercontent.com/maotuon/iptv-listesi/main/iptv.m3u',
'oldstuffs':'https://raw.githubusercontent.com/oldstuffs/iptv_tr/master/playlist.m3u'}
def fetch(item):
 name,url=item
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  return name,urllib.request.urlopen(req,timeout=22).read().decode('utf-8-sig','replace'),'OK'
 except Exception as e:return name,'',str(e)[:100]
def parse(text):
 rows=[];meta=None
 for l in text.splitlines():
  l=l.strip()
  if l.startswith('#EXTINF:'):meta=l
  elif l.startswith(('http://','https://')) and meta:
   rows.append((meta.split(',',1)[-1],l,meta));meta=None
 return rows
def norm(s):
 s=re.sub(r'\[[^]]*\]|\([^)]*\)','',s).casefold()
 s=''.join(c for c in unicodedata.normalize('NFKD',s.replace('ı','i')) if not unicodedata.combining(c))
 s=re.sub(r'\b(4k|uhd|fhd|hd|sd|hq|1440p|1080p|720p|576p|480p|360p|270p|aday|alternatif|tr)\b','',s)
 return re.sub(r'[^a-z0-9]','',s)
old=parse(open('CALISANLAR.m3u',encoding='utf-8-sig').read())
knownurls={u for n,u,m in old}
knownnames={norm(n) for n,u,m in old}
knownids={x.group(1) for n,u,m in old if (x:=re.search(r'tvg-id="([^"]+)"',m))}
with concurrent.futures.ThreadPoolExecutor(max_workers=9) as ex: sources=list(ex.map(fetch,SOURCES.items()))
rows=[];seen=set()
for source,txt,status in sources:
 print('SOURCE',source,status,'entries',len(parse(txt)))
 for n,u,m in parse(txt):
  if u in knownurls or u in seen:continue
  seen.add(u)
  tvgid=(re.search(r'tvg-id="([^"]*)"',m) or [None,''])[1]
  logo=(re.search(r'tvg-logo="([^"]*)"',m) or [None,''])[1]
  kind='ALTERNATIF' if norm(n) in knownnames or tvgid and tvgid in knownids else 'YENI_ADAY'
  rows.append((n,u,source,kind,tvgid,logo))
def probe(row):
 n,u,source,kind,tvgid,logo=row
 try:
  p=subprocess.run(['ffprobe','-v','error','-rw_timeout','6500000','-analyzeduration','800000','-probesize','800000','-show_entries','stream=codec_type','-of','csv=p=0',u],capture_output=True,text=True,timeout=11)
  ok=p.returncode==0 and ('video' in p.stdout or 'audio' in p.stdout)
 except Exception:ok=False
 return (n,source,kind,'ERISIM_VAR' if ok else 'DOGRULANAMADI',u,tvgid,logo)
with concurrent.futures.ThreadPoolExecutor(max_workers=28) as ex:result=list(ex.map(probe,rows))
with open('GENIS_KANAL_TARAMA_RAPORU.csv','w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['KANAL','KAYNAK','TUR','ON_TEST','URL','TVG_ID','LOGO_ADAY']);w.writerows(result)
print('TOTAL',len(rows),'PASS',sum(x[3]=='ERISIM_VAR' for x in result),'TGRT',[(x[0],x[3],x[1]) for x in result if 'tgrt' in x[0].lower()])
