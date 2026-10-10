#!/usr/bin/env python3
"""Report duplicate URLs in scan results without modifying playlists."""
import csv
from collections import defaultdict
from pathlib import Path

source = Path('YENILER_TARAMA_RAPORU.csv')
if not source.exists():
    raise SystemExit('Tarama raporu bulunamadi')
with source.open(encoding='utf-8-sig', newline='') as f:
    records = list(csv.DictReader(f))
groups = defaultdict(list)
for record in records:
    url = (record.get('YAYIN_URL') or '').strip()
    if url:
        groups[url].append(record)
output = Path('aday_bekletme/TEKRAR_EDEN_ADAYLAR.csv')
output.parent.mkdir(parents=True, exist_ok=True)
with output.open('w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['YAYIN_URL', 'TEKRAR_SAYISI', 'KANAL_ADLARI', 'KAYNAKLAR'])
    for url, entries in sorted(groups.items()):
        if len(entries) > 1:
            writer.writerow([url, len(entries), ' | '.join(sorted({e.get('KANAL', '') for e in entries})), ' | '.join(sorted({e.get('KAYNAK', '') for e in entries}))])
print('Tekrar raporu hazir; ana liste degismedi')
