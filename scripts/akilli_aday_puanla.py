#!/usr/bin/env python3
"""Read-only scoring of candidate CSVs; no channel promotion or playlist edits."""
import argparse,csv,json,re,collections
from pathlib import Path

def value(row,*keys):
    return next((str(row.get(k) or "").strip() for k in keys if str(row.get(k) or "").strip()),"")
def score(row):
    technical=value(row,"TEKNIK_MEDYA","MEDYA_TEST","TEKNIK_TEST")
    audio=value(row,"SES_IZI")
    resolution=value(row,"COZUNURLUK")
    logo=value(row,"LOGO_ADAY_URL")
    video=technical in ("VIDEO_SES_VAR","YALNIZ_VIDEO")
    sound=technical=="VIDEO_SES_VAR" or (video and audio.lower()=="true")
    # These are evidence points, not proof of correct channel identity.
    points=(20 if video else 0)+(15 if sound else 0)
    if resolution:
        m=re.search(r"(\d+)x(\d+)",resolution)
        if m: points+=10 if int(m.group(2))>=1080 else 7 if int(m.group(2))>=720 else 3
    if logo.startswith("https://"):points+=5
    # Stability and identity points deliberately withheld until repeated, independent checks.
    return points,"TEKNIK_ADAY" if video and sound else "EK_DOGRULAMA_GEREKLI"
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("inputs",nargs="+")
    parser.add_argument("--output",default="AKILLI_ADAY_PUANLARI.csv")
    args=parser.parse_args()
    candidates={}
    evidence={}
    for path in args.inputs:
        if "ONCELIKLI_KANAL_TEK_NIK_RAPORU" not in path: continue
        with open(path,encoding="utf-8-sig",newline="") as handle:
            for row in csv.DictReader(handle):
                url=value(row,"YAYIN_URL")
                if url: evidence[url]=row
    for path in args.inputs:
        with open(path,encoding="utf-8-sig",newline="") as handle:
            for row in csv.DictReader(handle):
                url=value(row,"YAYIN_URL")
                if not url.startswith(("https://","http://")):continue
                key=url
                if url in evidence:
                    row={**row,**{k:v for k,v in evidence[url].items() if v and k in ("TEKNIK_MEDYA","COZUNURLUK","SES_IZI")}}
                points,status=score(row)
                item={"KANAL":value(row,"KANAL"),"ADAY_TURU":value(row,"ADAY_TURU","GRUP"),"PUAN":points,"DURUM":status,"TEKNIK_KANIT":value(row,"TEKNIK_MEDYA","MEDYA_TEST","TEKNIK_TEST"),"COZUNURLUK":value(row,"COZUNURLUK"),"SES_IZI":value(row,"SES_IZI"),"LOGO_ADAY_URL":value(row,"LOGO_ADAY_URL"),"YAYIN_URL":url,"KAYNAK":value(row,"KAYNAK"),"KIMLIK_DOGRULANDI":"HAYIR","KARARLILIK_DOGRULANDI":"HAYIR","ANA_LISTEYE_EKLENEBILIR":"HAYIR"}
                if key not in candidates or points>candidates[key]["PUAN"]:candidates[key]=item
    rows=sorted(candidates.values(),key=lambda r:(-r["PUAN"],r["KANAL"]))
    fields=["KANAL","ADAY_TURU","PUAN","DURUM","TEKNIK_KANIT","COZUNURLUK","SES_IZI","LOGO_ADAY_URL","YAYIN_URL","KAYNAK","KIMLIK_DOGRULANDI","KARARLILIK_DOGRULANDI","ANA_LISTEYE_EKLENEBILIR"]
    with open(args.output,"w",encoding="utf-8-sig",newline="") as out:
        writer=csv.DictWriter(out,fieldnames=fields);writer.writeheader();writer.writerows(rows)
    counts=collections.Counter(r["DURUM"] for r in rows)
    summary={"aday_sayisi":len(rows),"durumlar":dict(counts),"en_yuksek_puan":max((r["PUAN"] for r in rows),default=0),"eslesen_teknik_kanit":sum(1 for url in candidates if url in evidence),"uyari":"Puan yalnızca eldeki teknik kanıtları gösterir. Kimlik, 24-48 saat kararlılık ve IBO Player oynatma onayı yoktur. Otomatik ekleme yasaktır."}
    Path("AKILLI_ADAY_OZET.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False))
if __name__=="__main__":main()
