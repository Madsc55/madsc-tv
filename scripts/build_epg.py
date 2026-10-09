#!/usr/bin/env python3
"""Build an independent XMLTV guide from public XMLTV feeds. Never edits CALISANLAR.m3u."""
import gzip, json, re, urllib.request, xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "epg"
OUT.mkdir(exist_ok=True)
PLAYLIST = ROOT / "CALISANLAR.m3u"
SOURCES = [
    "https://raw.githubusercontent.com/trology85/iptv-epg-turkey/main/epg/turksat_epg.xml.gz",
    "https://raw.githubusercontent.com/ahmethascelik/epghost/main/xmltv.xml",
]
def normalize(s):
    return re.sub(r"[^a-z0-9]+", "", s.casefold().replace("ı","i").replace("İ","i").replace("ş","s").replace("ğ","g").replace("ü","u").replace("ö","o").replace("ç","c"))
def attr(line, name):
    m = re.search(r'\b' + re.escape(name) + r'="([^"]*)"', line)
    return m.group(1) if m else ""
def playlist_channels():
    result = []
    for line in PLAYLIST.read_text(encoding="utf-8-sig").splitlines():
        if line.startswith("#EXTINF"):
            result.append({"id": attr(line,"tvg-id"), "name": attr(line,"tvg-name") or line.rsplit(",",1)[-1], "display":line.rsplit(",",1)[-1]})
    return result
def download(url):
    req = urllib.request.Request(url,headers={"User-Agent":"madsc-tv-epg/1.0"})
    with urllib.request.urlopen(req,timeout=90) as response:
        data=response.read(120_000_000)
    return gzip.decompress(data) if data[:2]==b"\x1f\x8b" else data
def main():
    channels=playlist_channels()
    all_channels={}
    all_programmes=[]
    source_results=[]
    for url in SOURCES:
        try:
            root=ET.fromstring(download(url))
            if root.tag!="tv": raise ValueError("Not an XMLTV tv document")
            count=0
            for ch in root.findall("channel"):
                cid=ch.get("id")
                if cid and cid not in all_channels: all_channels[cid]=ch
            for prog in root.findall("programme"):
                if prog.get("channel"): all_programmes.append(prog); count+=1
            source_results.append({"url":url,"status":"ok","programmes":count})
        except Exception as exc:
            source_results.append({"url":url,"status":"error","reason":str(exc)[:250]})
    by_name=defaultdict(set)
    for cid,ch in all_channels.items():
        by_name[normalize(cid)].add(cid)
        for label in ch.findall("display-name"):
            if label.text: by_name[normalize(label.text)].add(cid)
    matched={}
    unmatched=[]
    ambiguous=[]
    for channel in channels:
        key=channel["id"] or channel["name"]
        choices=set()
        if channel["id"] in all_channels: choices={channel["id"]}
        if not choices:
            for name in (channel["name"],channel["display"]):
                choices |= by_name.get(normalize(name),set())
        if len(choices)==1: matched[key]=next(iter(choices))
        elif len(choices)>1: ambiguous.append(channel)
        else: unmatched.append(channel)
    result=ET.Element("tv",{"generator-info-name":"madsc-tv EPG builder"})
    for cid in set(matched.values()):
        result.append(all_channels[cid])
    count=0
    valid=set(matched.values())
    for prog in all_programmes:
        if prog.get("channel") in valid:
            result.append(prog);count+=1
    ET.ElementTree(result).write(OUT/"madsc-epg.xml",encoding="utf-8",xml_declaration=True)
    report={"generated_utc":datetime.now(timezone.utc).isoformat(),"playlist_entries":len(channels),"matched_entries":len(matched),"unmatched_entries":len(unmatched),"ambiguous_entries":len(ambiguous),"programmes":count,"sources":source_results,"unmatched":unmatched,"ambiguous":ambiguous}
    (OUT/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k not in ("unmatched","ambiguous")},ensure_ascii=False,indent=2))
if __name__=="__main__": main()
