#!/usr/bin/env python3
"""Read-only longitudinal evidence; repeated measurements are never retimed."""
import csv
import datetime as dt
import json
from pathlib import Path

FIELDS = ['KANAL', 'GRUP', 'YAYIN_URL', 'SON_DURUM', 'GOZLEM_SAYISI',
          'BASARILI_VIDEO_SES_GOZLEMI', 'BASARILI_ARALIK_SAAT', '24_SAAT_KARARLI',
          'IBO_ONAYI', 'ANA_LISTEYE_EKLENEBILIR']


def timestamp(value, now):
    try:
        result = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
        if result.tzinfo is None or result > now + dt.timedelta(minutes=5):
            raise ValueError('timestamp')
        return result
    except (ValueError, TypeError, AttributeError):
        raise ValueError('Gecersiz gozlem zamani; gecmis korunuyor') from None


def validate(history, now):
    if not isinstance(history, dict):
        raise ValueError('Kararlilik gecmisi nesne olmali; sifirlanmadi')
    for url, observations in history.items():
        if not isinstance(url, str) or not isinstance(observations, list):
            raise ValueError('Gecersiz gozlem dizisi; gecmis korunuyor')
        seen = {}
        for item in observations:
            if not isinstance(item, dict) or not isinstance(item.get('state'), str) or not item['state']:
                raise ValueError('Gecersiz gozlem; gecmis korunuyor')
            stamp = timestamp(item.get('at'), now)
            if stamp in seen and seen[stamp] != item['state']:
                raise ValueError('Ayni zamanda celisen medya kaniti')
            seen[stamp] = item['state']
    return history


def track(current, history, now=None, require_measurement_time=False):
    now = now or dt.datetime.now(dt.timezone.utc)
    validate(history, now)
    result = json.loads(json.dumps(history))
    added = repeated = 0
    rows = []
    for row in current:
        url = row.get('YAYIN_URL', '').strip()
        if not url:
            continue
        state = row.get('TEKNIK_MEDYA', '')
        if not state or state == 'TEST_EDILMEDI':
            raise ValueError('Test edilmemis satir gozlem olamaz')
        raw_time = row.get('OLCUM_ZAMANI')
        if require_measurement_time and not raw_time:
            raise ValueError('Gercek olcum zamani yok; yeni gozlem uretilmedi')
        stamp = timestamp(raw_time or now.isoformat(), now)
        old = result.setdefault(url, [])
        matching = [item for item in old if timestamp(item['at'], now) == stamp]
        if matching:
            if any(item['state'] != state for item in matching):
                raise ValueError('Ayni zamanda celisen medya kaniti')
            repeated += 1
        else:
            old.append({'at': stamp.isoformat(), 'state': state})
            added += 1
        old.sort(key=lambda item: timestamp(item['at'], now))
        # Preserve the complete audit history; stability is evaluated only in a 7-day window.
        window = [item for item in old if dt.timedelta(0) <= now - timestamp(item['at'], now) <= dt.timedelta(days=7)]
        good = sorted({timestamp(item['at'], now) for item in window if item['state'] == 'VIDEO_SES_VAR'})
        span = (good[-1] - good[0]).total_seconds() / 3600 if len(good) >= 2 else 0
        latest = window[-1] if window else None
        fresh = latest is not None and now - timestamp(latest['at'], now) <= dt.timedelta(hours=24)
        stable = (len(good) >= 2 and span >= 24 and fresh
                  and all(item['state'] == 'VIDEO_SES_VAR' for item in window))
        rows.append({'KANAL': row.get('KANAL', ''), 'GRUP': row.get('GRUP', ''), 'YAYIN_URL': url,
                     'SON_DURUM': latest['state'] if latest else 'GUNCEL_GOZLEM_YOK',
                     'GOZLEM_SAYISI': len(window), 'BASARILI_VIDEO_SES_GOZLEMI': len(good),
                     'BASARILI_ARALIK_SAAT': round(span, 1), '24_SAAT_KARARLI': 'EVET' if stable else 'HAYIR',
                     'IBO_ONAYI': 'YOK', 'ANA_LISTEYE_EKLENEBILIR': 'HAYIR'})
    validate(result, now)
    return result, rows, {'new_observations': added, 'reused_measurements_not_added': repeated}


def main():
    history_file = Path('KARARLILIK_GECMISI.json')
    try:
        history = json.loads(history_file.read_text(encoding='utf-8')) if history_file.exists() else {}
        with Path('ONCELIKLI_KANAL_TEK_NIK_RAPOR.csv').open(encoding='utf-8-sig', newline='') as handle:
            current = list(csv.DictReader(handle))
        history, rows, counts = track(current, history)
    except (ValueError, OSError) as exc:
        raise SystemExit('Kararlilik kaydi degistirilmeden durduruldu: ' + str(exc)) from None
    history_file.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding='utf-8')
    with Path('KARARLILIK_RAPORU.csv').open('w', encoding='utf-8-sig', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    summary = {'aday': len(rows), '24_saat_kararli': sum(r['24_SAAT_KARARLI'] == 'EVET' for r in rows),
               **counts, 'window_days': 7, 'history_preserved': True,
               'not': 'Yalniz teknik gozlem; IBO/kimlik onayi degil. Otomatik liste degisikligi yok.'}
    Path('KARARLILIK_OZET.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == '__main__':
    main()
