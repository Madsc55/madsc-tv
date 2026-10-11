#!/usr/bin/env python3
"""Read-only playlist logo audit. Does not change playlists, backups or workflows."""
import concurrent.futures, hashlib, io, json, re, time, urllib.error, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
LIMIT = 4_000_000

def attr(line, name):
    match = re.search(r'\b' + re.escape(name) + r'="([^"]*)"', line)
    return match.group(1) if match else ''

def safe_url(url):
    p = urllib.parse.urlsplit(url)
    host = p.hostname or ''
    if p.port:
        host += ':' + str(p.port)
    return urllib.parse.urlunsplit((p.scheme, host, p.path, '[MASKED]' if p.query else '', ''))

def inspect(url):
    started = time.monotonic()
    result = {'logo': safe_url(url), 'status': 'ERROR', 'format': None, 'width': None, 'height': None, 'ibo_device_compatibility': 'NOT_VERIFIED'}
    try:
        # Non-ASCII URL paths are encoded without rewriting existing % escapes.
        p = urllib.parse.urlsplit(url)
        if p.scheme not in ('http', 'https') or p.username or p.password:
            result['status'] = 'UNSUPPORTED_URL'
            return result
        request_url = urllib.parse.urlunsplit((p.scheme, p.netloc, urllib.parse.quote(p.path, safe='/%:@!$&\'()*+,;=-._~'), urllib.parse.quote(p.query, safe='=&%+:;/?,@!$\'()*-._~'), ''))
        request = urllib.request.Request(request_url, headers={'User-Agent': 'MADSC-logo-audit/1.0'})
        with urllib.request.urlopen(request, timeout=12) as response:
            result['http'] = response.status
            result['content_type'] = response.headers.get('Content-Type', '').split(';')[0]
            result['final_logo'] = safe_url(response.url)
            data = response.read(LIMIT + 1)
        result['bytes'] = len(data)
        if len(data) > LIMIT:
            result['status'] = 'TOO_LARGE'
            return result
        if not data:
            result['status'] = 'EMPTY'
            return result
        try:
            with Image.open(io.BytesIO(data)) as im:
                result.update(format=im.format, width=im.width, height=im.height)
                im.verify()
            with Image.open(io.BytesIO(data)) as im:
                im.load()
            result['status'] = 'IMAGE_OK'
        except Exception:
            try:
                root = ET.fromstring(data)
                if root.tag.split('}')[-1] != 'svg':
                    raise ValueError('Not SVG')
                result.update(status='SVG_XML_OK', format='SVG')
            except Exception:
                result['status'] = 'NOT_DECODABLE_IMAGE'
        result['transport'] = 'HTTPS' if urllib.parse.urlsplit(result['final_logo']).scheme == 'https' else 'HTTP'
    except urllib.error.HTTPError as exc:
        result.update(status='HTTP_ERROR', http=exc.code)
    except Exception:
        result['status'] = 'NETWORK_OR_TLS_ERROR'
    finally:
        result['elapsed_seconds'] = round(time.monotonic() - started, 3)
    return result

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--playlist', type=Path, default=ROOT / 'CALISANLAR.m3u')
    args = parser.parse_args()
    raw = args.playlist.read_bytes()
    entries = [{'name': line.rsplit(',', 1)[-1], 'id': attr(line, 'tvg-id'), 'logo': attr(line, 'tvg-logo')} for line in raw.decode('utf-8-sig').splitlines() if line.startswith('#EXTINF')]
    urls = sorted({e['logo'] for e in entries if e['logo']})
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        jobs = {pool.submit(inspect, url): url for url in urls}
        for job in concurrent.futures.as_completed(jobs):
            results[jobs[job]] = job.result()
    counts = {}
    for result in results.values():
        counts[result['status']] = counts.get(result['status'], 0) + 1
    formats = {}
    for result in results.values():
        if result['format']:
            formats[result['format']] = formats.get(result['format'], 0) + 1
    rows = []
    for entry in entries:
        row = {'name': entry['name'], 'id': entry['id']}
        row.update(results[entry['logo']] if entry['logo'] else {'logo': '', 'status': 'MISSING_LOGO'})
        row['station_identity'] = 'NOT_VERIFIED'
        rows.append(row)
    summary = {'checked_utc': datetime.now(timezone.utc).isoformat(), 'playlist_sha256': hashlib.sha256(raw).hexdigest(), 'entries': len(entries), 'unique_logo_urls': len(urls), 'missing_logo_entries': sum(not e['logo'] for e in entries), 'unique_url_statuses': counts, 'formats': formats, 'image_ok_entries': sum(r['status'] == 'IMAGE_OK' for r in rows), 'svg_entries': sum(r['status'] == 'SVG_XML_OK' for r in rows), 'problem_entries': sum(r['status'] not in ('IMAGE_OK', 'SVG_XML_OK') for r in rows), 'limits': ['Image decode does not prove the correct station logo or IBO device support.', 'Failures may be temporary or runner/location dependent.', 'No image or playlist was replaced.']}
    assert args.playlist.read_bytes() == raw
    out = Path(__file__).resolve().parent
    (out / 'rapor.json').write_text(json.dumps({'summary': summary, 'entries': rows}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (out / 'ozet.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
