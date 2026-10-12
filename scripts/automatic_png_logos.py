"""Fill empty playlist logo attributes using exact IPTV-org channel matches."""
import concurrent.futures
import hashlib
import io
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PREFIX = 'https://raw.githubusercontent.com/Madsc55/madsc-tv/main/logos/auto/'
LIMIT = 4_000_000

def convert(url, output_dir=None):
    filename = hashlib.sha256(url.encode()).hexdigest()[:24] + '.png'
    output = (Path(output_dir) if output_dir is not None else ROOT / 'logos/auto') / filename
    if url.startswith(PREFIX):
        return url, url, 'already_local'
    try:
        parsed = urllib.parse.urlsplit(url)
        if parsed.scheme not in ('http', 'https') or parsed.username or parsed.password:
            raise ValueError('unsupported_url')
        request_url = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc,
            urllib.parse.quote(parsed.path, safe='/%:@!$&\'()*+,;=-._~'),
            urllib.parse.quote(parsed.query, safe='=&%+:;/?,@!$\'()*-._~'), ''))
        with urllib.request.urlopen(urllib.request.Request(request_url, headers={'User-Agent':'MADSC-logo-PNG/1.0'}), timeout=12) as response:
            data = response.read(LIMIT + 1)
        if not data or len(data) > LIMIT:
            raise ValueError('size_limit')
        if b'<svg' in data[:1000]:
            # Keep relative/remote resources disabled: convert self-contained SVG only.
            if re.search(rb'(?:href\s*=|<!ENTITY|<!DOCTYPE|url\s*\()', data, re.I):
                raise ValueError('svg_external_resource')
            import cairosvg
            data = cairosvg.svg2png(bytestring=data)
        with Image.open(io.BytesIO(data)) as image:
            if image.width * image.height > 16_000_000:
                raise ValueError('pixel_limit')
            image.load()
            image = image.convert('RGBA')
            image.thumbnail((640,640))
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
        output.parent.mkdir(parents=True, exist_ok=True)
        png = buffer.getvalue()
        if not output.exists() or output.read_bytes() != png:
            output.write_bytes(png)
        return url, PREFIX + filename, 'png_ready'
    except Exception as error:
        return url, url, type(error).__name__

def main():
    playlist = ROOT / 'CALISANLAR.m3u'
    raw = playlist.read_text(encoding='utf-8')
    def download_json(name):
        with urllib.request.urlopen('https://iptv-org.github.io/api/'+name+'.json', timeout=20) as response:
            return json.load(response)
    lines = raw.splitlines(keepends=True)
    missing = [i for i,line in enumerate(lines) if line.startswith('#EXTINF') and
               not re.search(r'tvg-logo="[^"\s][^"]*"',line)]
    audit_path = ROOT / 'logo_deneme/rapor.json'
    audit = json.loads(audit_path.read_text()) if audit_path.exists() else {'entries':[]}
    problems = [r for r in audit['entries'] if r['status'] not in ('IMAGE_OK','SVG_XML_OK')]
    config_path = ROOT / 'logo_deneme/verified_sources.json'
    verified = json.loads(config_path.read_text()) if config_path.exists() else {}
    channels = download_json('channels') if missing else []
    logos = download_json('logos') if missing else []
    by_id = {c['id']:c for c in channels}
    by_name = {}
    for channel in channels:
        for name in [channel['name']]+channel.get('alt_names',[]):
            by_name.setdefault(name.casefold().strip(),set()).add(channel['id'])
    artwork = {}
    for logo in logos:
        artwork.setdefault(logo['channel'],[]).append(logo['url'])
    selected = {}
    unresolved = []
    for i in missing:
        line = lines[i]
        identity = re.search(r'tvg-id="([^"]*)"',line)
        name = re.search(r'tvg-name="([^"]*)"',line)
        label = name[1] if name else line.rsplit(',',1)[-1].strip()
        cid = identity[1].split('@')[0] if identity else ''
        if cid not in by_id:
            candidates = by_name.get(label.casefold().strip(),set())
            cid = next(iter(candidates)) if len(candidates)==1 else ''
        options = artwork.get(cid,[])
        if options:
            options.sort(key=lambda url: (not urllib.parse.urlsplit(url).path.lower().endswith('.png'),url))
            selected[i] = options
        else:
            unresolved.append(label)
    urls = sorted({url for options in selected.values() for url in options})
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        results = list(pool.map(convert, urls))
    replacements = {old:new for old,new,status in results if status in ('png_ready','already_local')}
    for i,options in selected.items():
        # Exact names alone do not prove the on-air artwork. Require a saved review.
        label = lines[i].rsplit(',',1)[-1].strip()
        review = verified.get(label, {})
        url = next((url for url in options if url in replacements and
                    review.get('source') == url and review.get('visual_match') is True and
                    review.get('png_sha256') == hashlib.sha256((ROOT/'logos/auto'/replacements[url].rsplit('/',1)[-1]).read_bytes()).hexdigest()), None)
        if url is None:
            continue
        if 'tvg-logo="' in lines[i]:
            lines[i] = re.sub(r'tvg-logo="[^"]*"','tvg-logo="'+replacements[url]+'"',lines[i])
        else:
            lines[i] = lines[i].replace(' group-title=', ' tvg-logo="'+replacements[url]+'" group-title=',1)
    updated = ''.join(lines)
    # All order, names, stream URLs, categories and other metadata remain exact.
    strip = lambda text: re.sub(r' ?tvg-logo="[^"]*"','',text)
    assert strip(updated) == strip(raw)
    if playlist.read_text(encoding='utf-8') != raw:
        raise RuntimeError('playlist_changed_during_conversion')
    playlist.write_text(updated,encoding='utf-8')
    report = {'missing_logo_entries':len(missing),'unresolved':unresolved,'unique_logos':len(urls),'png_ready':sum(s=='png_ready' for _,_,s in results),
        'already_local':sum(s=='already_local' for _,_,s in results),
        'failed':sum(s not in ('png_ready','already_local') for _,_,s in results),
        'identity':'Existing logos untouched; automatic insertion requires a saved visual review and unchanged PNG hash.',
        'problem_channels':[{'name':r['name'],'status':r['status'],'http':r.get('http'),'visual_match':'NOT_VERIFIED'} for r in problems],
        'pending_visual_review':[lines[i].rsplit(',',1)[-1].strip() for i in missing if not re.search(r'tvg-logo="[^"\s][^"]*"',lines[i])],
        'results':[{'source_sha256':hashlib.sha256(u.encode()).hexdigest(),'png':n if s in ('png_ready','already_local') else None,'status':s} for u,n,s in results]}
    (ROOT/'logo_deneme/png_automation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='results'}))

if __name__ == '__main__':
    main()
