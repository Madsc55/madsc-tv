#!/usr/bin/env python3
"""Isolated five-channel EPG preparation; never writes production playlists or EPG."""
import argparse, copy, gzip, hashlib, json, re, urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

SOURCE = 'https://raw.githubusercontent.com/trology85/iptv-epg-turkey/main/epg/turksat_epg.xml.gz'
GUIDE = 'https://raw.githubusercontent.com/Madsc55/madsc-tv/main/epg_deneme/rehber.xml'
CHANNELS = [('TRT 1', 'TRT.1'), ('TRT HABER', 'TRT.Haber'), ('TRT ÇOCUK', 'TRT.Çocuk'), ('TRT AVAZ', 'TRT.Avaz'), ('TRT TÜRK', 'TRT.Türk')]

def stamp(value):
    # Explicit numeric offset required for this controlled test.
    if not re.fullmatch(r'\d{14} [+-]\d{4}', value):
        raise ValueError('Missing or invalid XMLTV timezone')
    return datetime.strptime(value, '%Y%m%d%H%M%S %z').astimezone(timezone.utc)

def attr(line, name):
    found = re.search(r'\b' + re.escape(name) + r'="([^"]*)"', line)
    return found.group(1) if found else ''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--playlist', type=Path, default=Path(__file__).resolve().parents[1] / 'CALISANLAR.m3u')
    parser.add_argument('--source-file', type=Path)
    args = parser.parse_args()
    before = args.playlist.read_bytes()
    if args.source_file:
        data = args.source_file.read_bytes()
    else:
        with urllib.request.urlopen(SOURCE, timeout=60) as response:
            data = response.read(20_000_000)
    if data[:2] == b'\x1f\x8b':
        data = gzip.decompress(data)
    source = ET.fromstring(data)
    assert source.tag == 'tv'
    now = datetime.now(timezone.utc)
    zone = ZoneInfo('Europe/Stockholm')
    lines = before.decode('utf-8-sig').splitlines()
    result = ET.Element('tv', {'generator-info-name': 'MADSC isolated EPG pilot'})
    playlist = [f'#EXTM3U url-tvg="{GUIDE}" x-tvg-url="{GUIDE}"']
    report = {'checked_utc': now.isoformat(), 'source': SOURCE, 'source_sha256': hashlib.sha256(data).hexdigest(), 'playlist_sha256': hashlib.sha256(before).hexdigest(), 'timezone': 'Europe/Stockholm', 'ibo_device_visibility': 'NOT_VERIFIED', 'media_playback': 'NOT_RETESTED', 'channels': []}
    for name, source_id in CHANNELS:
        entries = []
        for i, line in enumerate(lines[:-1]):
            tvname = attr(line, 'tvg-name')
            if (tvname == name or tvname.startswith(name + ' ')) and '.medya.trt.com.tr/' in lines[i+1]:
                entries.append((line, lines[i+1]))
        if not entries:
            raise RuntimeError('No existing public TRT stream for ' + name)
        line, url = entries[0]
        target = attr(line, 'tvg-id')
        if not target:
            raise RuntimeError('Missing existing tvg-id for ' + name)
        ET.SubElement(ET.SubElement(result, 'channel', {'id': target}), 'display-name').text = name
        playlist += [re.sub(r'group-title="[^"]*"', 'group-title="EPG DENEME — 5 KANAL"', line), url]
        seen, programmes, invalid = set(), [], 0
        for p in source.findall('programme'):
            if p.get('channel') != source_id:
                continue
            try:
                start, stop = stamp(p.get('start', '')), stamp(p.get('stop', ''))
                if stop <= start or not p.findtext('title'):
                    raise ValueError('Invalid duration/title')
            except ValueError:
                invalid += 1
                continue
            signature = (start, stop, p.findtext('title'))
            if signature in seen:
                continue
            seen.add(signature)
            if stop <= now:
                continue
            programmes.append((start, stop, p))
        programmes.sort(key=lambda item: (item[0], item[1]))
        overlaps = sum(a[1] > b[0] for a, b in zip(programmes, programmes[1:]))
        current = [p for start, stop, p in programmes if start <= now < stop]
        for start, stop, p in programmes:
            new = copy.deepcopy(p)
            new.set('channel', target)
            new.set('start', start.strftime('%Y%m%d%H%M%S +0000'))
            new.set('stop', stop.strftime('%Y%m%d%H%M%S +0000'))
            result.append(new)
        report['channels'].append({'name': name, 'playlist_id': target, 'source_id': source_id, 'id_match': True, 'programmes': len(programmes), 'rejected_source_entries': invalid, 'overlaps': overlaps, 'current_programme_count': len(current), 'current_title': current[0].findtext('title') if len(current) == 1 else None, 'current_start_stockholm': stamp(current[0].get('start')).astimezone(zone).isoformat() if len(current) == 1 else None, 'current_stop_stockholm': stamp(current[0].get('stop')).astimezone(zone).isoformat() if len(current) == 1 else None, 'coverage_end_stockholm': max((stop for _, stop, _ in programmes), default=now).astimezone(zone).isoformat(), 'metadata_pass': len(current) == 1 and overlaps == 0})
    assert args.playlist.read_bytes() == before, 'Protected playlist changed'
    out = Path(__file__).resolve().parent
    ET.indent(result)
    ET.ElementTree(result).write(out / 'rehber.xml', encoding='utf-8', xml_declaration=True)
    (out / 'liste.m3u').write_text('\n'.join(playlist) + '\n', encoding='utf-8')
    report['all_five_metadata_pass'] = all(ch['metadata_pass'] for ch in report['channels'])
    (out / 'rapor.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
