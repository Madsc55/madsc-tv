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
    "https://epgshare01.online/epgshare01/epg_ripper_TR1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_TR3.xml.gz",
    "https://www.open-epg.com/files/turkey1.xml.gz",
    "https://www.open-epg.com/files/turkey2.xml.gz",
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
    # Prefer programme-bearing sources and normalized display names over opaque provider IDs.
    programme_counts=defaultdict(int)
    for prog in all_programmes:
        programme_counts[prog.get("channel")]+=1
    by_name=defaultdict(set)
    def clean_name(value):
        value=normalize(value)
        return re.sub(r"(?:1080p|720p|2160p|4k|uhd|fhd|hd|sd|hevc|h265|h264|backup|alternatif|alternative|yedek|canli|live|turkiye|tr|[0-9]+)$","",value)
    for cid,ch in all_channels.items():
        if not programme_counts[cid]:
            continue
        for label in [cid]+[x.text or "" for x in ch.findall("display-name")]:
            for key in (normalize(label),clean_name(label)):
                if key: by_name[key].add(cid)
    matched={}
    unmatched=[]
    ambiguous=[]
    for index, channel in enumerate(channels):
        choices=set()
        if channel["id"] in programme_counts:
            choices={channel["id"]}
        if not choices:
            for name in (channel["name"],channel["display"]):
                for key in (normalize(name),clean_name(name)):
                    choices |= by_name.get(key,set())
        if choices:
            # If several EPG providers use the same name, use the most complete schedule.
            matched[index]=max(choices,key=lambda cid:(programme_counts[cid],cid))
        else:
            unmatched.append(channel)
    result=ET.Element("tv",{"generator-info-name":"madsc-tv EPG builder"})
    output_ids={}
    written=set()
    for index, source_id in matched.items():
        ch=channels[index]
        target_id=ch["id"] or "madsc-"+str(index)
        output_ids.setdefault(source_id,set()).add(target_id)
        if target_id not in written:
            new_channel=ET.SubElement(result,"channel",{"id":target_id})
            ET.SubElement(new_channel,"display-name").text=ch["name"]
            written.add(target_id)
    count=0
    for prog in all_programmes:
        for target_id in output_ids.get(prog.get("channel"),()):
            new_prog=ET.fromstring(ET.tostring(prog))
            new_prog.set("channel",target_id)
            result.append(new_prog)
            count+=1
    if count == 0:
        raise RuntimeError("No matching EPG programmes found; refusing to replace existing EPG")
    ET.ElementTree(result).write(OUT/"madsc-epg.xml",encoding="utf-8",xml_declaration=True)
    report={"generated_utc":datetime.now(timezone.utc).isoformat(),"playlist_entries":len(channels),"matched_entries":len(matched),"unmatched_entries":len(unmatched),"ambiguous_entries":len(ambiguous),"programmes":count,"sources":source_results,"unmatched":unmatched,"ambiguous":ambiguous}
    (OUT/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k not in ("unmatched","ambiguous")},ensure_ascii=False,indent=2))
if __name__=="__main__": main()
