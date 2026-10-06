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
GROUP_ORDER=['⭐ FAVORİLER','HABER','ULUSAL','SPOR','BELGESEL','MÜZİK','DİNİ','ALTERNATİF','İNTERNET','ÇOCUK','SİNEMA-DİZİ','EĞİTİM-KÜLTÜR','KAMU-TEMATİK','YEREL KANALLAR']
FAVORITE_ORDER=[
 ('TRT 1',1440),('TRT 2',1080),('KANAL D',1080),('ATV',1080),('SHOW TV',1080),
 ('NOW',1080),('NOW',720),('TV8',1080),('TV8.5',1080),('TV8.5',1080),('STAR TV',1080),
 ('TV100',1080),('TV100',720),('NTV',1080),('NTV',1080),('CNN TÜRK',1080),('CNN TÜRK',1080),
 ('TRT HABER',1440),('TRT HABER',1440),('TRT HABER',1080),('TRT HABER',1080),
 ('HABERTÜRK',1080),('HABERTÜRK',1080),('HALK TV',1080),('HALK TV',1080),('TGRT HABER',1080),
 ('A HABER',1080),('A HABER',1080),('A HABER',1080),('24 TV',1080),('ULUSAL KANAL',576),('KANAL 7',1080),
 ('BEYAZ TV',1080),('BEYAZ TV',1080),('A2',1080),('A2',1080),('TEVE2',1080),('HABER GLOBAL',720),
 ('A PARA',1080),('A PARA',1080),('HT SPOR',1080),('HT SPOR',1080),
 ('FLASH HABER',720),('FLASH HABER',1080),('TRT SPOR YILDIZ',1080),('TRT SPOR YILDIZ',1080),
 ('A SPOR',1080),('A SPOR',1080),('EKOL SPORTS',1080),('DMAX',1080),('DMAX',1080),
 ('TLC',720),('TLC',720),('CNBC-E',1080),('TV4',1080),('TV4',720),
 ('BLOOMBERG HT',1080),('BLOOMBERG HT',1080),('360',720),('TABİİ TV',1080),('TABİİ TV',1080),
 ('TVNET',720),('ÜLKE TV',720),('ÜLKE TV',1080),('TELE1',1080)
]
CATEGORY={
'TRT 1':'ULUSAL','ATV':'ULUSAL','KANAL D':'ULUSAL','SHOW TV':'ULUSAL','STAR TV':'ULUSAL','NOW':'ULUSAL','TV8':'ULUSAL','KANAL 7':'ULUSAL','BEYAZ TV':'ULUSAL','360':'ULUSAL','A2':'ULUSAL','TEVE2':'ULUSAL','DMAX':'ULUSAL','TLC':'ULUSAL','TV8.5':'ULUSAL','TRT 2':'ULUSAL',
'SÖZCÜ TV':'HABER','TV100':'HABER','NTV':'HABER','CNN TÜRK':'HABER','TRT HABER':'HABER','HABERTÜRK':'HABER','HABER GLOBAL':'HABER','HALK TV':'HABER','TGRT HABER':'HABER','A HABER':'HABER','24 TV':'HABER','EKOL TV':'HABER','TELE1':'HABER','ULUSAL KANAL':'HABER','BLOOMBERG HT':'HABER','A PARA':'HABER','TVNET':'HABER','ÜLKE TV':'HABER','FLASH HABER':'HABER','BENGÜTÜRK':'HABER',
'TRT SPOR':'SPOR','TRT SPOR YILDIZ':'SPOR','A SPOR':'SPOR','HT SPOR':'SPOR','SPORTS TV':'SPOR','TJK TV':'SPOR','TJK TV 2':'SPOR','FB TV':'SPOR','EKOL SPORTS':'SPOR','SIFIR TV':'SPOR','TAY TV':'SPOR','GS TV':'SPOR','BJK TV':'SPOR','SATRANÇ TV':'SPOR',
'TRT ÇOCUK':'ÇOCUK','TRT DİYANET ÇOCUK':'ÇOCUK','MİNİKA GO':'ÇOCUK','MİNİKA ÇOCUK':'ÇOCUK','TRT BELGESEL':'BELGESEL','TGRT BELGESEL':'BELGESEL','TARIM TV':'BELGESEL','ÇİFTÇİ TV':'BELGESEL','TOPRAK TV':'BELGESEL',
'DİYANET TV':'DİNİ','VAV TV':'DİNİ','SEMERKAND TV':'DİNİ','LALEGÜL TV':'DİNİ','DOST TV':'DİNİ','SAT 7 TÜRK':'DİNİ','ON4 TV':'DİNİ','REHBER TV':'DİNİ','TRT MÜZİK':'MÜZİK','DREAM TÜRK':'MÜZİK','KRAL POP TV':'MÜZİK','POWER TÜRK TV':'MÜZİK','NUMBER1 TV':'MÜZİK','NUMBER1 TÜRK':'MÜZİK','POWER TV':'MÜZİK','POWER DANCE':'MÜZİK','POWER LOVE':'MÜZİK','POWER TÜRK AKUSTİK':'MÜZİK','POWERTÜRK SLOW':'MÜZİK','POWERTÜRK TAPTAZE':'MÜZİK','NUMBER1 AŞK':'MÜZİK','NUMBER1 DANCE':'MÜZİK','NUMBER1 DAMAR':'MÜZİK','TATLİSES TV':'MÜZİK',
'BIR TV':'ULUSAL','TİVİ 6':'ULUSAL','ATV AVRUPA':'ULUSAL','CNBC-E':'ULUSAL','EURO D':'ULUSAL','EUROSTAR':'ULUSAL','TABİİ TV':'İNTERNET','TV4':'ULUSAL','KRT TV':'HABER','GZT':'İNTERNET','DHA CANLI':'İNTERNET','TRT EBA':'EĞİTİM-KÜLTÜR','TRT EBA İLKOKUL':'EĞİTİM-KÜLTÜR','TRT EBA ORTAOKUL':'EĞİTİM-KÜLTÜR','TRT EBA LİSE':'EĞİTİM-KÜLTÜR','TÜRK HABER':'HABER','TV1':'ULUSAL','TV264':'ULUSAL','TBMM TV':'KAMU-TEMATİK','TRT AVAZ':'KAMU-TEMATİK','TRT TÜRK':'KAMU-TEMATİK','TRT KURDİ':'KAMU-TEMATİK','TRT WORLD':'KAMU-TEMATİK'}
# Türkiye/Türkçe açık yayın havuzlarında bulunan yerel kanallar.
# Bunlar ana/favori sırasını değiştirmez; çalışanlar kendi grubuna, ek kaynakları ALTERNATİF'e gider.
for _n in [
 'VAN65','İKRA TV','TV3','AYAZ TV','İÇEL TV','KANAL 56','ORDU ALTAŞ TV','TV KAYSERİ','TV 52','EKİN TÜRK TV','KON TV','EGEMAX TV','TV DEN','KANAL 32','KANAL 26','BRTV','CAN TEMPO TV','GRT','MK TV','ANADOLU NET','ANADOLU NET TV','AKSU TV','BALKAN TÜRK','BR TV','BRTV KARABÜK','BRÜKSEL TÜRK',
 'DENİZ POSTASI','DİM TV','DİYAR TV','ER TV MALATYA','ERCİYES TV','ERZURUM WEB TV','ES TV','ETV','ETV KAYSERİ',
 'EZGİ TV','FRT TV','FTV TÜRK','FİNEST TV','GRT GAZİANTEP TV','HABER61 TRABZON','HABER61 TV','HUNAT TV',
 'K+ KAYSERİ','KANAL 12','KANAL 15','KANAL 19 ÇORUM','KANAL 23','KANAL 26','KANAL 3','KANAL 3 AFYONKARAHİSAR',
 'KANAL 32','KANAL 34 İSTANBUL','KANAL 53 RİZE','KANAL 58','KANAL B','KANAL V','KANAL AVRUPA',
 'KAY TV KAYSERİ','KONYA KTV','KONYA OLAY TV','LIFE TV KAYSERİ','LUYS TV','MC EU TV','MERCAN TV','MERCAN TV ADIYAMAN',
 'OLAY TÜRK','ORDU BEL TV','POSTA TV ALANYA','ALANYA POSTA TV','REHBER TV','RİZE TÜRK TV','SUN RTV','SUN RTV MERSİN',
 'SAT 7 TÜRK','TV 41','TV 41 KOCAELİ','TV DEN','TEMPO TV','TİVİ 6','TON TV','URFANATİK TV','VİYANA TV','VUSLAT TV',
 'İZMİR TIME 35 TV','4U TV','ALTAS TV','BURSA AS TV','ÇAY TV','FİNANS TÜRK TV','FORTUNA TV','GONCA TV','GÜNEYDOĞU TV','KANAL 68','KANAL FIRAT','KANAL URFA','KARDELEN TV','KENT TÜRK TV','LINE TV','MAVİ KARADENİZ','MELTEM TV','MTÜRK TV','ON4 TV','ON 6','ÖNCÜ TV','POWER TV','POWER DANCE','POWER LOVE','POWER TÜRK AKUSTİK','NUMBER1 AŞK','NUMBER1 DANCE','NUMBER1 DAMAR','POWERTÜRK SLOW','POWERTÜRK TAPTAZE','TRT ARABİ','KANAL S SAMSUN','SAMSUN HABER TV','AKİT TV','CAN TV','TATLİSES TV','TOPRAK TV','TEK RUMELİ TV','TGRT EU','SIFIR TV','EDESSA TV','ETV MANİSA','LIFE TV','TRABZON BÜYÜKŞEHİR BELEDİYESİ TV'
]:
 CATEGORY.setdefault(_n,'YEREL KANALLAR')

EPG={'KANAL D':'bbwgmhsmhhoatzg','SHOW TV':'pvr08e5grfsebfw','STAR TV':'75tz02ooforewap','ATV':'2zkzbuscxwyjc4k','TRT 1':'af0zo9et4xguwsk','KANAL 7':'a8t877hb0oandbv','TV8':'w7x32brlcz26ibb','NOW':'m0abaihy7vla6ma','CNN TÜRK':'ah7mr9ol040kp3b','NTV':'nyz5s8p798n9cqg','TRT HABER':'in3p7jng04mr97m','HABERTÜRK':'gil1w2erz9l7imc','24 TV':'9b7ltozvb9c333g','A HABER':'ql8qf4vb46o1h7t','TLC':'9z32hgan37zhgr6','TV100':'5i5mds6ap6h7m7w','EKOL TV':'3kluptlla8k8re0','BEYAZ TV':'edf3lp61qexxxhl','TVNET':'njoweqtgl6xngkj','HABER GLOBAL':'bwmpobxuqn2pz87','360':'cphtdpl9j70cn3a','BLOOMBERG HT':'4nu4fjjhm0y6wqm','TGRT HABER':'qz2fp61itc8xm4g','DMAX':'6sokobdd9dwe0gl','TV8.5':'pd29xh24glvq4qz','ÜLKE TV':'kanaalkyymvqcjf','A PARA':'8yfvm8ak2t1qoe6','TRT BELGESEL':'80spas00o3iq47a','TJK TV':'jgxiih7f6yhagpj','HT SPOR':'spgsorunhgejuu2','A SPOR':'v25znppc6itjprw','FB TV':'jemrsooej8d8jku','TRT SPOR':'v0kvdikxec8nngd','TRT SPOR YILDIZ':'1yyvuttcurbkcnr','ULUSAL KANAL':'rjxdtygyec6mqjz','SÖZCÜ TV':'5zoe73avn97ggnt','TRT 2':'nzdc0yd5xxv43yl','TRT TÜRK':'xe24vekaidpsql3','TRT MÜZİK':'18ws4yk42js588h','DREAM TÜRK':'ttlji9eholru11x','POWER TÜRK TV':'82e4q3ribmz2mt1','TRT ÇOCUK':'ybv52n8pldp0lfq','MİNİKA GO':'phekqx3pyw2wiiq','MİNİKA ÇOCUK':'52hjq0o16nwpdnq','HALK TV':'d1exl1gxity48nl','TELE1':'2m3k6xyjyek7djr','FLASH HABER':'10bd6fhoe76yplp','A2':'fc29p3wbp8wkgo4','TRT WORLD':'j1x67766q1lr7r6','TRT KURDİ':'u552n6w4dkv49wz','TRT AVAZ':'p6sz5lndgfas2r9','TEVE2':'6vs4sg9183gdxth','DİYANET TV':'DiyanetTV.tr@SD','KRAL POP TV':'KralPopTV.tr@SD','NUMBER1 TV':'Number1TV.tr@SD','SEMERKAND TV':'SemerkandTV.tr','TRT DİYANET ÇOCUK':'TRTDiyanetCocuk.tr@SD','DOST TV':'DostTV.tr@SD','LALEGÜL TV':'LalegulTV.tr@SD','TBMM TV':'TBMMTV.tr@SD','TRT EBA':'TRTEBA.tr@SD'}

ALIASES={
 'TRT ÇOCUK DİYANET':'TRT DİYANET ÇOCUK','SAT7 TÜRK':'SAT 7 TÜRK','GS TV HD':'GS TV',
 'POWER TÜRK':'POWER TÜRK TV','POWERTÜRK TV':'POWER TÜRK TV',
 'NUMBER 1 TV':'NUMBER1 TV','NUMBER 1 TÜRK':'NUMBER1 TÜRK'
}

def canonical_name(name):
 raw=name.strip()
 raw=re.sub(r'\s*\((?:\d{3,4}p|\d{3,4}i)\)\s*',' ',raw,flags=re.I)
 raw=re.sub(r'\s*\[Not 24/7\]\s*',' ',raw,flags=re.I).strip()
 aliased=ALIASES.get(raw.upper(),raw)
 upper=aliased.upper()
 return upper if upper in CATEGORY else aliased

def parse(text):
 out=[]; info=None
 for raw in text.splitlines():
  s=raw.strip()
  if s.startswith('#EXTINF:'): info=s
  elif info and s.startswith(('http://','https://','rtmp://')):
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

def protocol(url):
 u=url.lower().split('?',1)[0]
 if is_youtube(url): return 'YOUTUBE'
 if u.startswith('rtmp://'): return 'RTMP'
 if u.endswith('.mpd'): return 'DASH'
 if u.endswith(('.ts','.m2ts')): return 'TS'
 if u.endswith('.mp4'): return 'MP4'
 if u.endswith('.webm'): return 'WEBM'
 return 'HLS'

def http_media_check(url, kind):
 try:
  data=get(url,65536)
  if len(data)<512: return False,url,'empty-data'
  if kind=='DASH':
   text=data.decode('utf-8-sig','ignore')
   if '<MPD' not in text and '<mpd' not in text: return False,url,'not-mpd'
   return True,url,'dash+manifest'
  if kind=='TS':
   sync=sum(1 for off in range(0,min(len(data),188*20),188) if data[off:off+1]==b'\\x47')
   if sync<2: return False,url,'not-ts'
   return True,url,'ts+data'
  return True,url,kind.lower()+'+data'
 except Exception as e: return False,url,str(e)[:160]

def test(url):
 if any(x in url.lower() for x in BLOCKED): return {'ok':False,'detail':'blocked','url':url,'w':0,'h':0,'protocol':protocol(url)}
 kind=protocol(url)
 if kind=='HLS':
  valid,media,detail=hls_check(url)
 elif kind in ('DASH','TS','MP4','WEBM'):
  valid,media,detail=http_media_check(url,kind)
 elif kind=='RTMP':
  valid,media,detail=True,url,'rtmp+probe'
 else:
  return {'ok':False,'detail':'unsupported','url':url,'w':0,'h':0,'protocol':kind}
 ok,w,h,codec=probe(media if valid else url)
 return {'ok':bool(valid and ok),'detail':detail,'url':url,'media':media,'w':w,'h':h,'codec':codec,'protocol':kind}

def q(w,h):
 if w>=3840 or h>=2160:return '2160P 4K UHD'
 if h>=1440:return '1440P QHD'
 if h>=1080:return '1080P FHD'
 if h>=720:return '720P HD'
 if h>=576:return '576P SD'
 return f'{h}P SD'

def host(u): return urllib.parse.urlparse(u).netloc.lower()

def ibo_compat(kind):
 return {'HLS':'YUKSEK','TS':'YUKSEK','RTMP':'YUKSEK','DASH':'CIHAZA BAGLI','MP4':'CIHAZA BAGLI','WEBM':'CIHAZA BAGLI','YOUTUBE':'AYRI'}.get(kind,'BILINMIYOR')

def is_youtube(url):
 return 'youtube.com/' in url.lower() or 'youtu.be/' in url.lower()

def main():
 src=Path(sys.argv[1] if len(sys.argv)>1 else 'MADSC_TV_47_LISTE_ADAY.m3u')
 if not src.exists(): raise SystemExit(f'Yok: {src}')
 entries=parse(src.read_text('utf-8-sig',errors='ignore'))
 youtube_entries=[(name,url,logo) for name,url,logo in entries if is_youtube(url) and name.upper().endswith(' YOUTUBE')]
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
   elif info and s.startswith(('http://','https://','rtmp://')):
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
   report.append([name,'CALISIYOR' if r['ok'] else 'CALISMIYOR',r.get('protocol',protocol(u)),ibo_compat(r.get('protocol',protocol(u))),r.get('w',0),r.get('h',0),q(r.get('w',0),r.get('h',0)) if r['ok'] else '',r.get('codec',''),r.get('detail',''),u])
   if r['ok']: good.append(r)
  if not good: failed.append(name); continue
  good.sort(key=lambda r:(r['w']*r['h'], r['url'].startswith('https://')),reverse=True)
  # Mevcut HLS ana yayını önceliklidir; yeni protokoller mevcut kanalı değiştirmez.
  hls_good=[r for r in good if r.get('protocol',protocol(r['url']))=='HLS']
  best=(hls_good[0] if hls_good else good[0]); mainrows.append((name,best))
  # Kullanıcının isteği: 1./2./3./4. taraf ayrımı yapma; çalışan kaliteli kaynakların hepsini koru.
  # Aynı kanalın farklı çözünürlükte ve farklı hostlarda birden fazla kaydı ALTERNATİF altında bulunabilir.
  seen_alt=set()
  for r in good:
   if r['url']==best['url']: continue
   k=(r['url'],r['w'],r['h'])
   if k not in seen_alt:
    seen_alt.add(k); altrows.append((name,r))
 goodmap=defaultdict(list)
 for name in CATEGORY:
  for u in by.get(name,[]):
   r=results.get(u)
   if r and r.get('ok'): goodmap[name].append(r)
  goodmap[name].sort(key=lambda r:(r.get('protocol',protocol(r['url']))=='HLS',r['w']*r['h'],r['url'].startswith('https://')),reverse=True)
 lines=[f'#EXTM3U url-tvg="{EPG_URL}" x-tvg-url="{EPG_URL}"']
 alt_seq=defaultdict(int)
 def add(name,r,group):
  epg=EPG.get(name,''); logo=logos.get(name,''); visible=f'{name} {q(r["w"],r["h"])}'
  if group=='ALTERNATİF':
   alt_seq[name]+=1; n=alt_seq[name]
   identity=f'{name} {n}'; epg_out=epg; visible=f'{name} {n} {q(r["w"],r["h"])}'
  else:
   identity=name; epg_out=epg
  lines.append(f'#EXTINF:-1 tvg-id="{epg_out}" tvg-name="{identity}" tvg-logo="{logo}" group-title="{group}",{visible}')
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
 favorite_occ=defaultdict(int)
 favorite_used=defaultdict(set)
 favorite_identity=defaultdict(int)
 def add_favorite(name,r):
  favorite_identity[name]+=1
  n=favorite_identity[name]
  epg=EPG.get(name,''); logo=logos.get(name,'')
  identity=name if n==1 else f'{name} {n}'
  epg_out=epg
  visible=f'{identity} {q(r["w"],r["h"])}'
  lines.append(f'#EXTINF:-1 tvg-id="{epg_out}" tvg-name="{identity}" tvg-logo="{logo}" group-title="⭐ FAVORİLER",{visible}')
  lines.append(r['url'])
 for name,target_h in FAVORITE_ORDER:
  favorite_occ[(name,target_h)]+=1
  occ=favorite_occ[(name,target_h)]-1
  choices=goodmap.get(name,[])
  if name=='TRT 1':
   preferred='https://tv-trt1.medya.trt.com.tr/master.m3u8'
   choices=sorted(choices,key=lambda r:r['url']!=preferred)
  if name=='TRT 2':
   preferred='https://tv-trt2.medya.trt.com.tr/master.m3u8'
   choices=sorted(choices,key=lambda r:r['url']!=preferred)
  exact=[r for r in choices if r.get('h')==target_h and r['url'] not in favorite_used[name]]
  higher=[r for r in choices if (r.get('h') or 0)>target_h and r['url'] not in favorite_used[name]]
  any_unused=[r for r in choices if r['url'] not in favorite_used[name]]
  pick=(exact[0] if exact else (min(higher,key=lambda r:r.get('h') or 0) if higher else (any_unused[0] if any_unused else (choices[occ % len(choices)] if choices else None))))
  if pick:
   add_favorite(name,pick); favorite_used[name].add(pick['url']); written_favorites.add((name,pick['url'])); continue
  old_same=[x for x in previous_favorite_entries if x[0]==name]
  if old_same:
   info,url=old_same[occ % len(old_same)][2],old_same[occ % len(old_same)][3]
   fallback={'url':url,'w':0,'h':target_h,'logo':logos.get(name,'')}
   add_favorite(name,fallback); written_favorites.add((name,url)); continue
  candidate_same=[e for e in entries if e[0]==name]
  if candidate_same:
   src=candidate_same[occ % len(candidate_same)]
   fallback={'url':src[1],'w':0,'h':target_h,'logo':src[2]}
   add_favorite(name,fallback); written_favorites.add((name,src[1])); continue
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
  if group=='ALTERNATİF':
   for name,r in altrows:add(name,r,'ALTERNATİF')
  else:
   for name,r in mainrows:
    if CATEGORY[name]==group:add(name,r,group)
 # Önceki ALTERNATİF kayıtları da yedek olarak koru; ana kayıtların sırasını bozma.
 alt_urls={r['url'] for _,r in altrows}
 for info,url in preserved_previous:
  if info and 'group-title="ALTERNATİF"' in info and 'ATV 3 1080P FHD' not in info and 'test_atv_hungary' not in url and url not in alt_urls:
   lines.append(info); lines.append(url); alt_urls.add(url)
 output_urls={x for x in lines if x.startswith(('http://','https://','rtmp://'))}
 for info,url in preserved_previous:
  if url not in output_urls and info and 'group-title="⭐ FAVORİLER"' not in info and 'group-title="YOUTUBE"' not in info and 'ATV 3 1080P FHD' not in info and 'test_atv_hungary' not in url:
   lines.append(info); lines.append(url); output_urls.add(url)
 Path('CALISANLAR.m3u').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 Path('CALISMAYANLAR.txt').write_text('\n'.join(failed)+'\n',encoding='utf-8')
 with open('TEST_RAPORU.csv','w',newline='',encoding='utf-8-sig') as f:
  w=csv.writer(f); w.writerow(['Kanal','Durum','Tur','IBO_Uyumlulugu','Genislik','Yukseklik','Kalite','Codec','Kontrol','URL']); w.writerows(report)
 print(f'Bitti. Ana çalışan={len(mainrows)} alternatif={len(altrows)} çalışmayan kanal={len(failed)}',flush=True)

if __name__=='__main__': main()