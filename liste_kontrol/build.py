#!/usr/bin/env python3
"""Prepare read-only list status; never writes a playlist or changes workflows."""
import argparse, hashlib, json, re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from channel_name_normalization import normalize_channel_name

def attribute(line, name):
    match = re.search(r'\b' + re.escape(name) + r'="([^"]*)"', line)
    return match.group(1) if match else ''

def name_key(name):
    return normalize_channel_name(name, profile="list_control")

def parse(text):
    entries, pending = [], None
    for line in text.splitlines():
        if line.startswith('#EXTINF'):
            if pending:
                raise ValueError('Channel entry has no stream URL')
            pending = {'name': attribute(line, 'tvg-name') or line.rsplit(',', 1)[-1], 'display': line.rsplit(',', 1)[-1], 'id': attribute(line, 'tvg-id'), 'group': attribute(line, 'group-title')}
        elif pending and line.strip() and not line.startswith('#'):
            pending['stream_key'] = hashlib.sha256(line.strip().encode()).hexdigest()
            entries.append(pending)
            pending = None
    if pending:
        raise ValueError('Final channel entry has no stream URL')
    return entries

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--playlist', type=Path, default=Path(__file__).resolve().parents[1] / 'CALISANLAR.m3u')
    args = parser.parse_args()
    data = args.playlist.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    entries = parse(data.decode('utf-8-sig'))
    counts = Counter(e['group'] for e in entries)
    categories = []
    for group, count in counts.items():
        label = re.search(r'\((\d+)\)', group)
        advertised = int(label.group(1)) if label else None
        categories.append({'name': group, 'actual_entries': count, 'label_count': advertised, 'count_matches': advertised is None or advertised == count})
    national = {e['stream_key'] for e in entries if 'ULUSAL' in e['group']}
    missing = [e for e in entries if 'ULUSAL' not in e['group'] and 'YEDEKLER' not in e['group'] and e['stream_key'] not in national]
    missing_unique = {}
    for e in missing:
        row = missing_unique.setdefault(e['stream_key'], {'name': e['display'], 'stream_key': e['stream_key'], 'categories': []})
        if e['group'] not in row['categories']:
            row['categories'].append(e['group'])
    f1 = [e for e in entries if 'FAVORİLER 1' in e['group']]
    f2 = [e for e in entries if 'FAVORİLER 2' in e['group']]
    overlaps = []
    for e in f2:
        matches = [a for a in f1 if a['stream_key'] == e['stream_key'] or (e['id'] and a['id'] == e['id']) or name_key(a['name']) == name_key(e['name'])]
        if matches:
            overlaps.append({'favorite2': e['display'], 'favorite1': sorted({a['display'] for a in matches}), 'status': 'REVIEW_NAME_OR_ID_MATCH'})
    report = {'checked_utc': datetime.now(timezone.utc).isoformat(), 'source': 'CALISANLAR.m3u', 'source_git_blob': blob, 'source_sha256': digest, 'version_label': blob[:12], 'ibo_loaded_version': 'NOT_OBSERVED', 'total_category_entries': len(entries), 'unique_stream_urls': len({e['stream_key'] for e in entries}), 'categories': categories, 'national_missing_unique_streams': len(missing_unique), 'national_missing': list(missing_unique.values()), 'favorite1_entries': len(f1), 'favorite2_entries': len(f2), 'favorite1_2_overlap': overlaps, 'changes_to_playlist': 0, 'limits': ['Category entries and stream URLs are not counts of distinct stations or working stations.', 'IBO loaded playlist version cannot be observed from GitHub.', 'Name/ID comparisons require review before deleting a favorite.']}
    assert args.playlist.read_bytes() == data
    out = Path(__file__).resolve().parent
    (out / 'rapor.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    table = '\n'.join(f"| {c['name']} | {c['actual_entries']} | {'Uyumlu' if c['count_matches'] else 'Etiket farklı'} |" for c in categories)
    md = f"# MADSC liste durumu\n\nKontrol: {report['checked_utc']}\n\nGitHub liste sürümü: **{blob[:12]}**. Tam Git blob: `{blob}`. Bu rapor statiktir; liste değişirse yeniden hazırlanmalıdır.\n\nToplam kategori kaydı: {len(entries)}. Farklı yayın bağlantısı: {report['unique_stream_urls']}. Bu rakamlar farklı/çalışan kanal sayısı değildir.\n\n| Kategori | Gerçek kayıt | Sayı etiketi |\n|---|---:|---|\n{table}\n\nUlusal'da bulunmayan farklı bağlantı: {len(missing_unique)}. Yedekler onay beklediği için bu karşılaştırmanın dışında tutulur. İsimler ayrıntılı JSON raporundadır; yayının gizli URL bilgileri rapora alınmaz.\n\nFavoriler 1: {len(f1)}, Favoriler 2: {len(f2)}. Bu iki kategori arasında inceleme gerektiren eşleşme: {len(overlaps)}. Boş kategoriler M3U'da görünmeyebilir.\n\nIBO'nun yüklediği sürüm **gözlenmedi**. Buradaki sürüm GitHub dosyasına aittir; uygulamada sürüm göstergesi kurulduğu anlamına gelmez. Ekran görüntüsü veya cihaz erişimi olmadan IBO'nun güncel listeyi yüklediği doğrulanamaz.\n\nAna liste, kategori sırası, yayınlar, logolar, yedekler ve test iş akışları değiştirilmedi. Eksikler otomatik eklenmedi.\n"
    (out / 'README.md').write_text(md, encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k not in ('national_missing', 'favorite1_2_overlap', 'limits')}, ensure_ascii=False))

if __name__ == '__main__':
    main()
