"""Prepare discovery artwork separately; never edit or approve a playlist."""
import hashlib
import json
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]


PUBLIC_IMAGE_HOSTS = {'raw.githubusercontent.com', 'upload.wikimedia.org',
                      'i.imgur.com', 'iptv-org.github.io', 'static.wikia.nocookie.net'}

def public_artwork_url(url):
    try:
        parsed = urllib.parse.urlsplit(url)
        return (parsed.scheme == 'https' and parsed.hostname in PUBLIC_IMAGE_HOSTS
                and not parsed.username and not parsed.password and not parsed.query
                and parsed.port in (None, 443))
    except ValueError:
        return False

def prepare(candidates, previous, converter=None, limit=240):
    saved = {r['stream_sha256']: r for r in previous}
    used = 0
    for candidate in candidates:
        key = candidate['stream_sha256']
        source = candidate.get('logo_url', '').strip()
        old = saved.get(key)
        # A successful unchanged preparation is not repeated.
        if (old and old.get('source_logo') == source and old.get('status') == 'PNG_READY_REVIEW_PENDING'
                and (ROOT / old.get('png_file', '')).is_file()
                and hashlib.sha256((ROOT / old['png_file']).read_bytes()).hexdigest() == old.get('png_sha256')):
            continue
        row = {k: candidate.get(k, '') for k in ('channel', 'stream_sha256', 'channel_id', 'source')}
        row.update(source_logo=source if public_artwork_url(source) else '', visual_match='NOT_VERIFIED', playlist_approved=False)
        if candidate.get('logo_source_review_required'):
            row['status'] = 'PUBLIC_LOGO_SOURCE_REVIEW_REQUIRED'
        elif not source:
            row['status'] = 'MISSING_SOURCE_LOGO_SEARCH_REQUIRED'
        elif not public_artwork_url(source):
            row['status'] = 'PUBLIC_LOGO_SOURCE_REVIEW_REQUIRED'
        elif used >= limit:
            row['status'] = 'PREPARATION_PENDING'
        else:
            used += 1
            if converter is None:
                try:
                    from .automatic_png_logos import convert
                except ImportError:
                    from automatic_png_logos import convert
                converter = convert
            _, png, status = converter(source, output_dir=ROOT / 'madsc_kesif/candidate_pngs')
            row.update(status='PNG_READY_REVIEW_PENDING' if status in ('png_ready', 'already_local') else 'SOURCE_LOGO_FAILED', conversion=status)
            if status in ('png_ready', 'already_local'):
                path = ROOT / ('logos/auto' if status == 'already_local' else 'madsc_kesif/candidate_pngs') / png.rsplit('/', 1)[-1]
                if path.is_file():
                    destination = ROOT / 'madsc_kesif/candidate_pngs' / path.name
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    if path != destination:
                        destination.write_bytes(path.read_bytes())
                    row.update(png_file=str(destination.relative_to(ROOT)), png_sha256=hashlib.sha256(destination.read_bytes()).hexdigest())
                else:
                    row['status'] = 'PNG_FILE_UNAVAILABLE'
        saved[key] = row
    return list(saved.values())


def main():
    folder = ROOT / 'madsc_kesif'
    source = folder / 'logo_candidates.json'
    if not source.exists():
        print('No source artwork metadata yet; historical VAR is not a logo URL.')
        return
    report = folder / 'candidate_logos.json'
    previous = json.loads(report.read_text()).get('results', []) if report.exists() else []
    rows = prepare(json.loads(source.read_text()), previous)
    report.write_text(json.dumps({'checked_utc': datetime.now(timezone.utc).isoformat(), 'results': rows,
        'limits': 'Source artwork and PNG decoding do not prove station identity. No playlist writes or automatic approvals.'}, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'candidate_artwork_records': len(rows), 'png_ready': sum(r['status']=='PNG_READY_REVIEW_PENDING' for r in rows)}))


if __name__ == '__main__':
    main()
