#!/usr/bin/env python3
import csv, json, re, subprocess, sys, urllib.request, urllib.parse, unicodedata
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict

EPG_URL='https://raw.githubusercontent.com/ahmethascelik/epghost/main/xmltv.xml'
UA='Mozilla/5.0 (MADSC-TV/2.0)'
HTTP_TIMEOUT=10
PROBE_TIMEOUT=30
WORKERS=12
MAX_PER_CHANNEL=9999
BLOCKED=('helga.iptv2022.com',)
GROUP_ORDER=['⭐ FAVORİLER','ULUSAL','HABER','SPOR','ALTERNATİF','ÇOCUK','BELGESEL','DİNİ','MÜZİK','SİNEMA-DİZİ','EĞİTİM-KÜLTÜR','KAMU-TEMATİK','İNTERNET','YOUTUBE']
FAVORITE_ORDER=[
 ('TRT 1',1440),('TRT 2',1080),('ATV',1080),('KANAL D',1080),('SHOW TV',1080),('NOW',1080),('TV8',1080),('STAR TV',1080),
 ('TV100',1080),('NTV',1080),('CNN TÜRK',1080),('TRT HABER',1440),('HABERTÜRK',1080),('HALK TV',1080),('TGRT HABER',1080),
 ('A HABER',1080),('24 TV',1080),('ULUSAL KANAL',576),('KANAL 7',1080),('TV8.5',1080),('BEYAZ TV',1080),('A2',1080),
 ('TRT HABER',1080),('HABER GLOBAL',720),('A PARA',1080),('HT SPOR',1080),('FLASH HABER',720),('ÜLKE TV',720),
 ('NOW',720),('TRT SPOR YILDIZ',1080),('A SPOR',1080),('EKOL SPORTS',1080)
]
CATEGORY={
'TRT 1':'ULUSAL','ATV':'ULUSAL','KANAL D':'ULUSAL','SHOW TV':'ULUSAL','STAR TV':'ULUSAL','NOW':'ULUSAL','TV8':'ULUSAL','KANAL 7':'ULUSAL','BEYAZ TV':'ULUSAL','360':'ULUSAL','A2':'ULUSAL','TEVE2':'ULUSAL','DMAX':'ULUSAL','TLC':'ULUSAL','TV8.5':'ULUSAL','TRT 2':'ULUSAL',
'SÖZCÜ TV':'HABER','TV100':'HABER','NTV':'HABER','CNN TÜRK':'HABER','TRT HABER':'HABER','HABERTÜRK':'HABER','HABER GLOBAL':'HABER','HALK TV':'HABER','TGRT HABER':'HABER','A HABER':'HABER','24 TV':'HABER','EKOL TV':'HABER','TELE1':'HABER','ULUSAL KANAL':'HABER','BLOOMBERG HT':'HABER','A PARA':'HABER','TVNET':'HABER','ÜLKE TV':'HABER','FLASH HABER':'HABER','BENGÜTÜRK':'HABER',
'TRT SPOR':'SPOR','TRT SPOR YILDIZ':'SPOR','A SPOR':'SPOR','HT SPOR':'SPOR','SPORTS TV':'SPOR','TJK TV':'SPOR','TJK TV 2':'SPOR','FB TV':'SPOR','EKOL SPORTS':'SPOR',
'TRT ÇOCUK':'ÇOCUK','TRT DİYANET ÇOCUK':'ÇOCUK','MİNİKA GO':'ÇOCUK','MİNİKA ÇOCUK':'ÇOCUK','TRT BELGESEL':'BELGESEL','TGRT BELGESEL':'BELGESEL','TARIM TV':'BELGESEL','ÇİFTÇİ TV':'BELGESEL',
'DİYANET TV':'DİNİ','VAV TV':'DİNİ','SEMERKAND TV':'DİNİ','LALEGÜL TV':'DİNİ','DOST TV':'DİNİ','TRT MÜZİK':'MÜZİK','DREAM TÜRK':'MÜZİK','KRAL POP TV':'MÜZİK','POWER TÜRK TV':'MÜZİK','NUMBER1 TV':'MÜZİK','NUMBER1 TÜRK':'MÜZİK',
'ATV AVRUPA':'ULUSAL','CNBC-E':'ULUSAL','EURO D':'ULUSAL','EUROSTAR':'ULUSAL','TABİİ TV':'İNTERNET','TV4':'ULUSAL','KRT TV':'HABER','GZT':'İNTERNET','DHA CANLI':'İNTERNET','TRT EBA':'EĞİTİM-KÜLTÜR','TBMM TV':'KAMU-TEMATİK','TRT AVAZ':'KAMU-TEMATİK','TRT TÜRK':'KAMU-TEMATİK','TRT KURDİ':'KAMU-TEMATİK','TRT WORLD':'KAMU-TEMATİK'}
EPG={'KANAL D':'bbwgmhsmhhoatzg','SHOW TV':'pvr08e5grfsebfw','STAR TV':'75tz02ooforewap','ATV':'2zkzbuscxwyjc4k','TRT 1':'af0zo9et4xguwsk','KANAL 7':'a8t877hb0oandbv','TV8':'w7x32brlcz26ibb','NOW':'m0abaihy7vla6ma','CNN TÜRK':'ah7mr9ol040kp3b','NTV':'nyz5s8p798n9cqg','TRT HABER':'in3p7jng04mr97m','HABERTÜRK':'gil1w2erz9l7imc','24 TV':'9b7ltozvb9c333g','A HABER':'ql8qf4vb46o1h7t','TLC':'9z32hgan37zhgr6','TV100':'5i5mds6ap6h7m7w','EKOL TV':'3kluptlla8k8re0','BEYAZ TV':'edf3lp61qexxxhl','TVNET':'njoweqtgl6xngkj','HABER GLOBAL':'bwmpobxuqn2pz87','360':'cphtdpl9j70cn3a','BLOOMBERG HT':'4nu4fjjhm0y6wqm','TGRT HABER':'qz2fp61itc8xm4g','DMAX':'6sokobdd9dwe0gl','TV8.5':'pd29xh24glvq4qz','ÜLKE TV':'kanaalkyymvqcjf','A PARA':'8yfvm8ak2t1qoe6','TRT BELGESEL':'80spas00o3iq47a','TJK TV':'jgxiih7f6yhagpj','HT SPOR':'spgsorunhgejuu2','A SPOR':'v25znppc6itjprw','FB TV':'jemrsooej8d8jku','TRT SPOR':'v0kvdikxec8nngd','TRT SPOR YILDIZ':'1yyvuttcurbkcnr','ULUSAL KANAL':'rjxdtygyec6mqjz','SÖZCÜ TV':'5zoe73avn97ggnt','TRT 2':'nzdc0yd5xxv43yl','TRT TÜRK':'xe24vekaidpsql3','TRT MÜZİK':'18ws4yk42js588h','DREAM TÜRK':'ttlji9eholru11x','POWER TÜRK TV':'82e4q3ribmz2mt1','TRT ÇOCUK':'ybv52n8pldp0lfq','MİNİKA GO':'phekqx3pyw2wiiq','MİNİKA ÇOCUK':'52hjq0o16nwpdnq','HALK TV':'d1exl1gxity48nl','TELE1':'2m3k6xyjyek7djr','FLASH HABER':'10bd6fhoe76yplp','A2':'fc29p3wbp8wkgo4','TRT WORLD':'j1x67766q1lr7r6','TRT KURDİ':'u552n6w4dkv49wz','TRT AVAZ':'p6sz5lndgfas2r9','TEVE2':'6vs4sg9183gdxth','DİYANET TV':'DiyanetTV.tr@SD','KRAL POP TV':'KralPopTV.tr@SD','NUMBER1 TV':'Number1TV.tr@SD','SEMERKAND TV':'SemerkandTV.tr','TRT DİYANET ÇOCUK':'TRTDiyanetCocuk.tr@SD','DOST TV':'DostTV.tr@SD','LALEGÜL TV':'LalegulTV.tr@SD','TBMM TV':'TBMMTV.tr@SD','TRT EBA':'TRTEBA.tr@SD'}

ALIASES={
 'TRT ÇOCUK DİYANET':'TRT DİYANET ÇOCUK',
 'POWER TÜRK':'POWER TÜRK TV','POWERTÜRK TV':'POWER TÜRK TV',
 'NUMBER 1 TV':'NUMBER1 TV','NUMBER 1 TÜRK':'NUMBER1 TÜRK'
}

def canonical_name(name):
 return ALIASES.get(name.strip(),name.strip())

def parse(text):
 out=[]; info=None
 for raw in text.splitlines():
  s=raw.strip()
  if s.startswith('#EXTINF:'): info=s
  elif info and s.startswith(('http://','https://')):
   name=canonical_name(info.split(',',1)[-1].strip()); logo=''; m=re.search(r'tvg-logo="([^"]*)"',info)
   if m: logo=m.group(1).strip()
   out.append((name,s,logo)); info=None
 return out

def get(url, limit=None):
 req=urllib.request.Request(url,headers={'User-Agent':UA,'Accept':'*/*'})
 with urllib.request.urlopen(req,timeout=HTTP_TIMEOUT) as r:
  return r.read(limit or 1024*1024)

def hls_check(url):
 try:
  data=get(url).decode('utf-8-sig','ignore')
  if '#EXTM3U' not in data: return False,url,'not-hls'
  lines=[x.strip() for x in data.splitlines() if x.strip()]
  variants=[]
  for i,l in enumerate(lines):
   if l.startswith('#EXT-X-STREAM-INF') and i+1<len(lines) and not lines[i+1].startswith('#'):
    m=re.search(r'RESOLUTION=(\d+)x(\d+)',l); pix=int(m.group(1))*int(m.group(2)) if m else 0
    variants.append((pix,urllib.parse.urljoin(url,lines[i+1])))
  media=max(variants)[1] if variants else url
  if variants: data=get(media).decode('utf-8-sig','ignore'); lines=[x.strip() for x in data.splitlines() if x.strip()]
  seg=next((x for x in lines if not x.startswith('#')),None)
  if not seg: return False,media,'no-segment'
  segurl=urllib.parse.urljoin(media,seg)
  if len(get(segurl,65536))<512: return False,media,'empty-segment'
  return True,media,'hls+segment'
 except Exception as e: return False,url,str(e)[:160]

def probe(url):
 try:
  p=subprocess.run(['ffprobe','-v','error','-rw_timeout','20000000','-user_agent',UA,'-select_streams','v:0','-show_entries','stream=width,height,codec_name','-of','json',url],capture_output=True,text=True,timeout=PROBE_TIMEOUT)
  j=json.loads(p.stdout or '{}'); st=(j.get('streams') or [{}])[0]; w=int(st.get('width') or 0); h=int(st.get('height') or 0)
  return p.returncode==0 and w>0 and h>0,w,h,st.get('codec_name','')
 except Exception as e: return False,0,0,str(e)[:120]

def test(url):
 if any(x in url.lower() for x in BLOCKED): return {'ok':False,'detail':'blocked','url':url,'w':0,'h':0}
 hls,media,detail=hls_check(url)
 ok,w,h,codec=probe(media if hls else url)
 return {'ok':bool(hls and ok),'detail':detail,'url':url,'media':media,'w':w,'h':h,'codec':codec}

def q(w,h):
 if w>=3840 or h>=2160:return '2160P 4K UHD'
 if h>=1440:return '1440P QHD'
 if h>=1080:return '1080P FHD'
 if h>=720:return '720P HD'
 if h>=576:return '576P SD'
 return f'{h}P SD'

def host(u): return urllib.parse.urlparse(u).netloc.lower()

def is_youtube(url):
 return 'youtube.com/' in url.lower() or 'youtu.be/' in url.lower()

def main():
 src=Path(sys.argv[1] if len(sys.argv)>1 else 'MADSC_TV_47_LISTE_ADAY.m3u')
 if not src.exists(): raise SystemExit(f'Yok: {src}')
 entries=parse(src.read_text('utf-8-sig',errors='ignore'))
 youtube_entries=[(name,url,logo) for name,url,logo in entries if is_youtube(url)]
 by=defaultdict(list); logos={}
 for name,url,logo in entries:
  if name not in CATEGORY: continue
  if is_youtube(url): continue
  if url not in [x for x in by[name]]: by[name].append(url)
  if logo and name not in logos: logos[name]=logo
 prev=Path('CALISANLAR.m3u')
 preserved_favorites=[]
 preserved_previous=[]
 if prev.exists():
  prev_text=prev.read_text('utf-8-sig',errors='ignore')
  info=None
  for raw in prev_text.splitlines():
   s=raw.strip()
   if s.startswith('#EXTINF:'): info=s
   elif info and s.startswith(('http://','https://')):
    if 'group-title="⭐ FAVORİLER"' in info:
     visible=info.split(',',1)[-1].strip()
     base=re.sub(r'\s+(2160P 4K UHD|1440P QHD|1080P FHD|720P HD|576P SD|\d+P SD)$','',visible).strip()
     if base in CATEGORY: preserved_favorites.append((base,s))
    preserved_previous.append((info,s))
    info=None
  for name,url,logo in parse(prev_text):
   base=re.sub(r'\s+(2160P 4K UHD|1440P QHD|1080P FHD|720P HD|576P SD|\d+P SD)$','',name).strip()
   if base in CATEGORY and url not in by[base]: by[base].insert(0,url)
   if logo and base not in logos: logos[base]=logo
 urls=[]
 for name in CATEGORY:
  for u in by[name]:
   if u not in urls: urls.append(u)
 print(f'Kanal={len(by)} benzersiz_test={len(urls)} isci={WORKERS} timeout={PROBE_TIMEOUT}s',flush=True)
 results={}
 with ThreadPoolExecutor(max_workers=WORKERS) as ex:
  fut={ex.submit(test,u):u for u in urls}
  for i,f in enumerate(as_completed(fut),1):
   u=fut[f]
   try: results[u]=f.result()
   except Exception as e: results[u]={'ok':False,'detail':str(e),'url':u,'w':0,'h':0}
   if i%20==0: print(f'Test {i}/{len(urls)}',flush=True)
 mainrows=[]; altrows=[]; report=[]; failed=[]
 for name in CATEGORY:
  good=[]
  for u in by.get(name,[]):
   r=results.get(u,{'ok':False,'detail':'not-tested','w':0,'h':0,'url':u})
   report.append([name,'CALISIYOR' if r['ok'] else 'CALISMIYOR',r.get('w',0),r.get('h',0),q(r.get('w',0),r.get('h',0)) if r['ok'] else '',r.get('codec',''),r.get('detail',''),u])
   if r['ok']: good.append(r)
  if not good: failed.append(name); continue
  good.sort(key=lambda r:(r['w']*r['h'], r['url'].startswith('https://')),reverse=True)
  best=good[0]; mainrows.append((name,best))
  # Kullanıcının isteği: 1./2./3./4. taraf ayrımı yapma; çalışan kaliteli kaynakların hepsini koru.
  # Aynı kanalın farklı çözünürlükte ve farklı hostlarda birden fazla kaydı ALTERNATİF altında bulunabilir.
  seen_alt=set()
  for r in good[1:]:
   k=(r['url'],r['w'],r['h'])
   if k not in seen_alt:
    seen_alt.add(k); altrows.append((name,r))
 goodmap=defaultdict(list)
 for name in CATEGORY:
  for u in by.get(name,[]):
   r=results.get(u)
   if r and r.get('ok'): goodmap[name].append(r)
  goodmap[name].sort(key=lambda r:(r['w']*r['h'],r['url'].startswith('https://')),reverse=True)
 lines=[f'#EXTM3U url-tvg="{EPG_URL}" x-tvg-url="{EPG_URL}"']
 def add(name,r,group):
  epg=EPG.get(name,''); logo=logos.get(name,''); visible=f'{name} {q(r["w"],r["h"])}'
  lines.append(f'#EXTINF:-1 tvg-id="{epg}" tvg-name="{name}" tvg-logo="{logo}" group-title="{group}",{visible}')
  lines.append(r['url'])
 # Fotoğraflardaki 1-32 sırası sabittir; hedef çözünürlük bulunamazsa eski doğru favori korunur.
 previous_favorite_entries=[]
 for info,url in preserved_previous:
  if info and 'group-title="⭐ FAVORİLER"' in info:
   visible=info.split(',',1)[-1].strip()
   base=re.sub(r'\\s+(2160P 4K UHD|1440P QHD|1080P FHD|720P HD|576P SD|\\d+P SD)$','',visible).strip()
   m=re.search(r'\\s(\\d+)P(?:\\s|$)',visible)
   previous_favorite_entries.append((base,int(m.group(1)) if m else 0,info,url))
 written_favorites=set()
 for name,target_h in FAVORITE_ORDER:
  choices=goodmap.get(name,[])
  exact=[r for r in choices if r.get('h')==target_h]
  higher=[r for r in choices if (r.get('h') or 0)>target_h]
  if exact:
   pick=exact[0]; add(name,pick,'⭐ FAVORİLER'); written_favorites.add((name,pick['url'])); continue
  old_exact=[x for x in previous_favorite_entries if x[0]==name and x[1]==target_h]
  if old_exact:
   info,url=old_exact[0][2],old_exact[0][3]; lines.extend([info,url]); written_favorites.add((name,url)); continue
  if higher:
   pick=min(higher,key=lambda r:r.get('h') or 0); add(name,pick,'⭐ FAVORİLER'); written_favorites.add((name,pick['url'])); continue
  old_same=[x for x in previous_favorite_entries if x[0]==name]
  if old_same:
   info,url=old_same[0][2],old_same[0][3]; lines.extend([info,url]); written_favorites.add((name,url)); continue
  if choices:
   pick=max(choices,key=lambda r:r.get('h') or 0); add(name,pick,'⭐ FAVORİLER'); written_favorites.add((name,pick['url']))
 fixed_names={name for name,_ in FAVORITE_ORDER}
 for name,url in preserved_favorites:
  if name in fixed_names or (name,url) in written_favorites: continue
  old=[x for x in previous_favorite_entries if x[0]==name and x[3]==url]
  r=results.get(url)
  if r and r.get('ok'): add(name,r,'⭐ FAVORİLER')
  elif old: lines.extend([old[0][2],url])
  else: continue
  written_favorites.add((name,url))
 for group in GROUP_ORDER[1:]:
  if group=='YOUTUBE':
   seen_youtube=set()
   for yname,yurl,ylogo in youtube_entries:
    if yurl in seen_youtube: continue
    seen_youtube.add(yurl)
    lines.append(f'#EXTINF:-1 tvg-id="" tvg-name="{yname}" tvg-logo="{ylogo}" group-title="YOUTUBE",{yname}')
    lines.append(yurl)
  elif group=='ALTERNATİF':
   for name,r in altrows:add(name,r,'ALTERNATİF')
  else:
   for name,r in mainrows:
    if CATEGORY[name]==group:add(name,r,group)
 # Önceki ALTERNATİF kayıtları da yedek olarak koru; ana kayıtların sırasını bozma.
 alt_urls={r['url'] for _,r in altrows}
 for info,url in preserved_previous:
  if info and 'group-title="ALTERNATİF"' in info and url not in alt_urls:
   lines.append(info); lines.append(url); alt_urls.add(url)
 output_urls={x for x in lines if x.startswith(('http://','https://'))}
 for info,url in preserved_previous:
  if url not in output_urls and info and 'group-title="⭐ FAVORİLER"' not in info:
   lines.append(info); lines.append(url); output_urls.add(url)
 Path('CALISANLAR.m3u').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 Path('CALISMAYANLAR.txt').write_text('\n'.join(failed)+'\n',encoding='utf-8')
 with open('TEST_RAPORU.csv','w',newline='',encoding='utf-8-sig') as f:
  w=csv.writer(f); w.writerow(['Kanal','Durum','Genislik','Yukseklik','Kalite','Codec','Kontrol','URL']); w.writerows(report)
 print(f'Bitti. Ana çalışan={len(mainrows)} alternatif={len(altrows)} çalışmayan kanal={len(failed)}',flush=True)

if __name__=='__main__': main()