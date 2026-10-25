#!/usr/bin/env python3
"""Create a small IBO Player XMLTV diagnostic feed from the existing EPG."""
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "epg/madsc-epg.xml"
DEST = ROOT / "epg/ibo-test-epg.xml"
TARGETS = {
    "af0zo9et4xguwsk": "TRT 1",
    "nzdc0yd5xxv43yl": "TRT 2",
    "pvr08e5grfsebfw": "SHOW TV",
    "2zkzbuscxwyjc4k": "ATV",
    "bbwgmhsmhhoatzg": "KANAL D",
}
source = ET.parse(SOURCE).getroot()
result = ET.Element("tv", {"generator-info-name": "MADSC IBO five-channel diagnostic"})
channel_ids = set()
for channel in source.findall("channel"):
    cid = channel.get("id")
    if cid in TARGETS:
        new = ET.SubElement(result, "channel", {"id": cid})
        ET.SubElement(new, "display-name").text = TARGETS[cid]
        channel_ids.add(cid)
counts = {cid: 0 for cid in TARGETS}
for programme in source.findall("programme"):
    cid = programme.get("channel")
    if cid in channel_ids:
        result.append(programme)
        counts[cid] += 1
if set(TARGETS) != channel_ids or any(not counts[cid] for cid in TARGETS):
    raise RuntimeError(f"Five-channel EPG incomplete: found={channel_ids}, programmes={counts}")
ET.indent(result, space="  ")
ET.ElementTree(result).write(DEST, encoding="utf-8", xml_declaration=True)
ET.parse(DEST)
print(f"IBO test EPG: {DEST.stat().st_size} bytes, 5 channels, {sum(counts.values())} programmes")
