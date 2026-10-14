#!/usr/bin/env python3
"""3. aşama: Ana listedeki yayınları değiştirmeden dönüşümlü teknik kontrol."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

def entries(path):
    rows = []
    pending = None
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if line.startswith("#EXTINF:"):
            pending = line
        elif pending and line and not line.startswith("#"):
            match = re.search(r'group-title="([^"]*)"', pending)
            rows.append({"sira": len(rows) + 1, "kanal": pending.rsplit(",", 1)[-1].strip(),
                         "kategori": match.group(1) if match else "", "url": line})
            pending = None
    return rows

def batch(rows, date, size):
    if size < 1:
        raise ValueError("Grup boyutu pozitif olmalı")
    groups = (len(rows) + size - 1) // size
    if not groups:
        return [], 0, 0
    # Her gün sıradaki grup; tüm ana liste gruplar boyunca kapsanır.
    number = date.toordinal() % groups
    return rows[number * size:(number + 1) * size], number + 1, groups

def probe(row, timeout=15):
    url = row["url"]
    result = {k: row[k] for k in ("sira", "kanal", "kategori")}
    result["url_kimligi"] = hashlib.sha256(url.encode()).hexdigest()[:16]
    result["teknik_durum"] = "DOGRULANAMADI"
    result["gerekce"] = "Test başlamadı"
    if not url.startswith(("http://", "https://")):
        result["gerekce"] = "Desteklenmeyen bağlantı türü"
        return result
    cmd = ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type",
           "-of", "json", "-rw_timeout", str(timeout * 1000000), url]
    try:
        done = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 3)
        if done.returncode:
            result["gerekce"] = "Bağlantı veya erişim hatası; cihazda çalışmıyor demek değildir"
        else:
            streams = json.loads(done.stdout).get("streams", [])
            kinds = {s.get("codec_type") for s in streams}
            if "video" in kinds and "audio" in kinds:
                result["teknik_durum"] = "SES_GORUNTU_BULUNDU"
                result["gerekce"] = "Kısa teknik örnek; uzun süreklilik ve IBO onayı değildir"
            elif kinds:
                result["teknik_durum"] = "KISMI_YAYIN"
                result["gerekce"] = "Ses veya görüntü akışlarından biri bulunamadı"
            else:
                result["gerekce"] = "Yayın akışı tespit edilemedi"
    except (subprocess.TimeoutExpired, OSError, ValueError):
        result["gerekce"] = "Zaman aşımı, araç eksikliği veya geçersiz yanıt"
    return result

def run(playlist, output, date, size, timeout):
    rows = entries(playlist)
    selected, group, groups = batch(rows, date, size)
    results = [probe(row, timeout) for row in selected]
    summary = {"tarih": date.isoformat(), "asama": 3, "ana_liste_toplam": len(rows),
               "bu_kosuda_test_edilen": len(results), "grup": group,
               "toplam_grup": groups, "tum_liste_bu_kosuda_test_edildi": len(results) == len(rows),
               "otomatik_kanal_degisikligi": False, "ibo_onayi_verildi": False,
               "uyari": "Teknik hata kanalı silme, taşıma veya değiştirme izni değildir.",
               "sonuclar": results}
    output.mkdir(parents=True, exist_ok=True)
    (output / "ana_liste_saglik.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# 3. Aşama — Ana liste sağlık raporu",
             f"- Tarih: {date.isoformat()}",
             f"- Ana liste kanalı: {len(rows)}",
             f"- Bu koşuda incelenen: {len(results)}",
             f"- Grup: {group}/{groups}",
             "- Ana liste, yedekler ve kanal kararları değiştirilmedi.",
             "- Başarısız teknik deneme IBO Player'da çalışmıyor kanıtı değildir.", "",
             "| Sıra | Kanal | Teknik sonuç | Açıklama |", "|---|---|---|---|"]
    for item in results:
        clean = lambda v: str(v).replace("|", "/").replace("\n", " ")
        lines.append(f"| {item['sira']} | {clean(item['kanal'])} | {item['teknik_durum']} | {clean(item['gerekce'])} |")
    (output / "ana_liste_saglik.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--playlist", default="CALISANLAR.m3u")
    parser.add_argument("--output", default="madsc_ana_liste_saglik")
    parser.add_argument("--batch-size", type=int, default=50)
    parser.add_argument("--timeout", type=int, default=15)
    args = parser.parse_args()
    today = dt.datetime.now(dt.timezone.utc).date()
    report = run(Path(args.playlist), Path(args.output), today, args.batch_size, args.timeout)
    print(f"Ana liste {report['ana_liste_toplam']}; bu koşuda {report['bu_kosuda_test_edilen']}; grup {report['grup']}/{report['toplam_grup']}. Yalnız rapor.")
