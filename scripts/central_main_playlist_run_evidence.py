#!/usr/bin/env python3
"""Ana liste sağlığının GitHub koşu kanıtını beş aşamalı rapora bağlar."""
import json
from pathlib import Path

WORKFLOW = "madsc-ana-liste-saglik.yml"

def build(folder):
    source = folder / "son_100_kosu.json"
    try:
        runs = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        runs = []
    if not isinstance(runs, list):
        runs = []
    matches = [r for r in runs if isinstance(r, dict) and
               ("Ana Liste Sağlık Kontrolü" in str(r.get("name", "")) or
                WORKFLOW in str(r.get("path", "")))]
    matches.sort(key=lambda r: r.get("created_at") or "", reverse=True)
    latest = matches[0] if matches else None
    status = "KOSU_KANITI_YOK"
    if latest:
        if latest.get("status") != "completed":
            status = "DEVAM_EDIYOR"
        elif latest.get("conclusion") == "success":
            status = "IS_AKISI_BASARILI_KANAL_SONUCU_INCELENMELI"
        else:
            status = "IS_AKISI_BASARISIZ"
    return {
        "asama": 3, "durum": status,
        "son_kosu": {k: latest.get(k) for k in ("run_id", "created_at", "status", "conclusion", "html_url")} if latest else None,
        "kanal_sonuclari_dogrulandi": False,
        "butun_ana_liste_test_edildi": False,
        "otomatik_degisiklik": False,
        "aciklama": "Bu rapor yalnız son 100 Actions koşusundaki iş akışı durumunu doğrular. Kanal bazlı sonuçlar sağlık koşusunun artifact dosyasındadır. Yeşil koşu bütün kanalların çalıştığını kanıtlamaz."
    }

if __name__ == "__main__":
    out = Path("madsc_merkezi_denetim")
    out.mkdir(exist_ok=True)
    report = build(out)
    (out / "ana_liste_saglik_kosu_kaniti.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Ana liste sağlık iş akışı beş aşamalı rapora bağlandı:", report["durum"])
