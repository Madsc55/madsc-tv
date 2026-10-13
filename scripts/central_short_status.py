#!/usr/bin/env python3
"""Merkezi kanittan kisa okunabilir durum ozeti; cron degistirmez."""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "madsc_merkezi_denetim"
OUT.mkdir(exist_ok=True)

def read(filename):
    path = OUT / filename
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeError):
        return None

def render(workflows, tasks, errors):
    counts = workflows.get("classifications", {}) if isinstance(workflows, dict) else {}
    task_list = tasks.get("tasks", []) if isinstance(tasks, dict) else []
    error_runs = errors.get("runs", []) if isinstance(errors, dict) else []
    lines = [
        "# MADSC - Kisa Durum Ozeti",
        "",
        "Bu ozet merkezi denetim kosusu sirasinda uretilir; gunluk otomatik calisma ayarlandigi anlamina gelmez.",
        "",
        "## Otomasyonlar (son 100 kosu ornegi)",
    ]
    for key, label in (("BASARILI", "Basarili"), ("BASARISIZ", "Basarisiz"),
                       ("DEVAM_EDIYOR", "Devam eden"), ("DIGER_SONUC", "Diger sonuc"),
                       ("SON_100_KOSUDA_YOK", "Kaniti bulunmayan")):
        lines.append(f"- {label}: {counts.get(key, 'BILINMIYOR')}")
    lines.extend(["", "## Gorevler"])
    if task_list:
        lines.append(f"- Takip gerektiren: {sum(bool(x.get('eksikler')) for x in task_list)} / {len(task_list)}")
    else:
        lines.append("- Gorev kaniti: BULUNAMADI")
    lines.extend(["", "## Basarisiz kosu asamalari"])
    if not isinstance(errors, dict):
        lines.append("- Hata raporu: BULUNAMADI")
    elif not error_runs:
        lines.append("- Bu ornekte basarisiz kosu raporlanmadi.")
    else:
        for item in error_runs[:10]:
            jobs = item.get("failed_jobs", [])
            stage = ", ".join(
                f"{j.get('job', '?')}: " + (", ".join(s.get("name", "?") for s in j.get("failed_steps", [])) or "ADIM_BILINMIYOR")
                for j in jobs) or "JOB_KANITI_YOK"
            lines.append(f"- #{item.get('run_id', '?')} {item.get('workflow', '?')}: {stage}; kok neden icin log gerekir.")
    lines.extend(["", "## Guvenlik ve kapsam",
                  "- Kanal listeleri, yedekler ve cron bu raporla degistirilmez.",
                  "- Isvec IBO cihaz testi ve kullanici onayi bu rapordan cikarilmaz.",
                  "- Eksik veya son 100 disinda kalan kanit basari sayilmaz.", ""])
    return "\n".join(lines)

summary = render(read("is_akisi_son_durum_siniflandirma.json"),
                 read("sekiz_gorev_tek_merkezi_rapor.json"),
                 read("hata_asama_raporu.json"))
(OUT / "madsc_kisa_durum_ozeti.md").write_text(summary, encoding="utf-8")
print("Kisa durum ozeti mevcut merkezi raporlardan olusturuldu.")
