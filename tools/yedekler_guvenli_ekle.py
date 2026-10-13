"""Yalnızca açıkça doğrulanmış kanalları mevcut YEDEKLER kategorisine ekle.

Girdi: onaylanmis_adaylar.json: [{name,url,logo,three_stage_passed,identity_verified}]
Başka kategoriye, mevcut satıra veya sıralamaya dokunmaz.
"""
import json
import pathlib
import re
import sys

PLAYLIST = pathlib.Path("CALISANLAR.m3u")
INPUT = pathlib.Path("onaylanmis_adaylar.json")
GROUP = re.compile(r'group-title="(📦 YEDEKLER \\(\\d+\\))"')
URL = re.compile(r'^https?://', re.I)


def update(original, candidates):
    lines = original.splitlines(keepends=True)
    existing = {s.strip() for s in lines if URL.match(s.strip())}
    backup_indexes = [i for i, s in enumerate(lines) if s.startswith("#EXTINF:") and 'group-title="📦 YEDEKLER (' in s]
    if not backup_indexes:
        raise ValueError("YEDEKLER kategorisi bulunamadı; dosya korunuyor")
    counts = {int(re.search(r'📦 YEDEKLER \\((\\d+)\\)', lines[i]).group(1)) for i in backup_indexes}
    if len(counts) != 1 or next(iter(counts)) != len(backup_indexes):
        raise ValueError("YEDEKLER sayısı tutarsız; dosya korunuyor")
    accepted = []
    for item in candidates:
        if item.get("three_stage_passed") is not True or item.get("identity_verified") is not True:
            continue
        url = str(item.get("url", "")).strip()
        name = str(item.get("name", "")).strip()
        if not URL.match(url) or not name or url in existing:
            continue
        if any(c in name for c in '\\r\\n') or any(c in url for c in '\\r\\n'):
            continue
        logo = str(item.get("logo", "")).strip().replace('"', "")
        name = name.replace(",", " ")
        accepted.append((name, url, logo))
        existing.add(url)
    if not accepted:
        return original, 0
    old_count = next(iter(counts))
    new_group = f"📦 YEDEKLER ({old_count + len(accepted)})"
    for i in backup_indexes:
        lines[i] = re.sub(r'group-title="📦 YEDEKLER \\(\\d+\\)"', f'group-title="{new_group}"', lines[i])
    # Kategori dosyanın sonunda bulunmalı; diğer satırların yeri korunur.
    last = backup_indexes[-1]
    if any(s.startswith("#EXTINF:") for s in lines[last + 1:]):
        raise ValueError("YEDEKLER son kategori değil; dosya korunuyor")
    ending = "\\r\\n" if "\\r\\n" in original else "\\n"
    for name, url, logo in accepted:
        lines.append(f'#EXTINF:-1 tvg-name="{name}" tvg-logo="{logo}" group-title="{new_group}",{name}{ending}')
        lines.append(url + ending)
    return "".join(lines), len(accepted)


if __name__ == "__main__":
    if not INPUT.exists():
        sys.exit("Doğrulanmış aday dosyası yok: hiçbir değişiklik yapılmadı")
    original = PLAYLIST.read_text(encoding="utf-8-sig")
    changed, count = update(original, json.loads(INPUT.read_text(encoding="utf-8")))
    if count:
        PLAYLIST.write_text(changed, encoding="utf-8")
    print(f"YEDEKLER'e eklenen doğrulanmış kanal: {count}")
