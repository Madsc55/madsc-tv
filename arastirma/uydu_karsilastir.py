#!/usr/bin/env python3
"""Read-only satellite catalogue / playlist name comparison; no stream probing."""
import argparse, hashlib, json, re
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

class Rows(HTMLParser):
    def __init__(self):
        super().__init__(); self.rows=[]; self.row=None; self.cell=None
    def handle_starttag(self, tag, attrs):
        if tag=='tr': self.row=[]
        if tag in ('td','th') and self.row is not None: self.cell=[]
    def handle_data(self, text):
        if self.cell is not None: self.cell.append(text)
    def handle_endtag(self, tag):
        if tag in ('td','th') and self.cell is not None:
            self.row.append(' '.join(''.join(self.cell).split())); self.cell=None
        if tag=='tr' and self.row is not None: self.rows.append(self.row); self.row=None

def key(name, playlist=False):
    name=re.sub(r'\([^)]*\)|\[[^]]*\]', '', name).strip()
    name=re.sub(r'\b(?:HD|FHD|UHD|SD)\b', '', name, flags=re.I).strip().rstrip('.')
    name=re.sub(r'\s+(?:ADAY|ALTERNATİF)$', '', name, flags=re.I).strip()
    if playlist and not re.fullmatch(r'(?:TRT|BRT|TV|Tele|Kanal|Tivi)\s+\d+', name, flags=re.I) and name!='Imam Hussein TV 5':
        name=re.sub(r'\s+\d+$', '', name)
    name=name.casefold().translate(str.maketrans('ıİşçğüö','iiscguo'))
    return re.sub(r'[^a-z0-9]', '', name)

ALIASES={'24':'24tv','show':'showtv','lalegul':'lalegultv','semerkandtv':'semerkandtv','powerturk':'powerturktv','thturkhaber':'turkhaber','van65':'van65tv','trtkurd':'trtkurdi','ordualtastv':'altastv'}
REVIEW={'alzahratv':'Al-Zahra TV Turkic','cantempotv':'TEMPO TV','kkardelentv':'KARDELEN TV','kontv':'KONYA KTV','ulusal1tv':'ULUSAL KANAL','cartonnetwork':'Cartoon Network','flashtv':'FLASH HABER','as':'Bursa AS TV'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--html',type=Path,required=True);p.add_argument('--playlist',type=Path,required=True);a=p.parse_args()
    original=a.playlist.read_bytes();text=original.decode('utf-8-sig'); names={}
    for line in text.splitlines():
        if not line.startswith('#EXTINF'): continue
        m=re.search(r'tvg-name="([^"]*)"',line);name=m.group(1) if m and m.group(1) else line.rsplit(',',1)[-1]
        names.setdefault(key(name,True),set()).add(name)
    parser=Rows();parser.feed(a.html.read_text());rows=[r for r in parser.rows if len(r)==8 and r[1].isdigit()]
    catalogue={}
    for row in rows:
        k=key(row[0]);c=catalogue.setdefault(k,{'name':row[0],'listed_names':[],'frequencies':[]})
        if row[0] not in c['listed_names']: c['listed_names'].append(row[0])
        c['frequencies'].append(dict(zip(['frequency','polarization','coverage','symbol_rate','fec','satellite','package'],row[1:])))
    for k,c in catalogue.items():
        target=k if k in names else ALIASES.get(k)
        c['playlist_names']=sorted(names.get(target,set()))
        c['status']='NAME_MATCH' if k in names else 'ALIAS_MATCH' if target in names else 'REVIEW_ALIAS' if k in REVIEW else 'NOT_FOUND_BY_NAME'
        if k in REVIEW: c['review_note']=REVIEW[k]
    counts={s:sum(c['status']==s for c in catalogue.values()) for s in ['NAME_MATCH','ALIAS_MATCH','REVIEW_ALIAS','NOT_FOUND_BY_NAME']}
    blob=hashlib.sha1(b'blob '+str(len(original)).encode()+b'\0'+original).hexdigest()
    report={'checked_utc':datetime.now(timezone.utc).isoformat(),'source':'https://www.uydufrekans.com.tr/turksat-sifresiz-kanallar.html','playlist_blob':blob,'satellite_rows':len(rows),'normalized_channel_names':len(catalogue),'counts':counts,'channels':list(catalogue.values()),'limits':['Satellite frequency is not an IPTV URL or proof of current playback.','Name and alias matches do not prove stream identity.','Catalogue contains international services and promotional channels; not all are Turkish TV search priorities.'],'playlist_changes':0,'existing_tests_changed':False}
    assert a.playlist.read_bytes()==original
    out=Path(__file__).resolve().parent
    (out/'uydu_karsilastirma.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='channels'},ensure_ascii=False)); print(json.dumps([c['name'] for c in catalogue.values() if c['status']=='NOT_FOUND_BY_NAME'],ensure_ascii=False))

if __name__=='__main__':main()
