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

def render(workflows, tasks, errors, management=None):
    counts = workflows.get("classifications", {}) if isinstance(workflows, dict) else {}
    task_list = tasks.get("tasks", []) if isinstance(tasks, dict) else []
    if not isinstance(task_list, list):
        task_list = []
    error_runs = errors.get("runs", []) if isinstance(errors, dict) else []
    if not isinstance(error_runs, list):
        error_runs = []
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
        lines.append(f"- Takip gerektiren: {sum(bool(x.get('eksikler')) for x in task_list if isinstance(x, dict))} / {len(task_list)}")
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
    if isinstance(management, dict):
        indicators = management.get("key_indicators", {})
        lines.extend(["", "## Ana liste canlı sağlık takibi"])
        lines.append(f"- Son iş akışı: {indicators.get('main_playlist_health_run', 'KOSU_KANITI_YOK')}")
        lines.append("- Kanal bazlı teknik sonuçlar ayrı sağlık raporundadır; otomatik değişiklik yapılmaz.")
        lines.extend(["", "## 18 geliştirme görevi"])
        lines.append(f"- Haritalanan: {indicators.get('eighteen_tasks_mapped', 'KANIT_YOK')}")
        lines.append(f"- Kod kanıtı eksik: {indicators.get('eighteen_tasks_code_evidence_missing', 'KANIT_YOK')}")
        lines.append(f"- Canlı doğrulama bekleyen: {indicators.get('eighteen_tasks_live_evidence_pending', 'KANIT_YOK')}")
        lines.extend(["", "## Beş aşamalı toplu denetim"])
        for stage in management.get("five_stage_results", []):
            label = "Kanıt eksik" if stage.get("missing_evidence") else "Rapor mevcut; sonuç doğrulaması gerekli"
            lines.append(f"- {stage.get('number')}. {stage.get('name')}: {label}")
        actionable = [x for x in management.get("open_blockers", []) if x.get("status") != "KAPSAM_DISI"]
        lines.append(f"- İnceleme gerektiren engel: {len(actionable)}")
        for blocker in actionable[:12]:
            lines.append(f"  - {blocker.get('code', 'BİLİNMİYOR')}")
    lines.extend(["", "## Guvenlik ve kapsam",
                  "- Kanal listeleri, yedekler ve cron bu raporla degistirilmez.",
                  "- Isvec IBO cihaz testi ve kullanici onayi bu rapordan cikarilmaz.",
                  "- Eksik veya son 100 disinda kalan kanit basari sayilmaz.", ""])
    return "\n".join(lines)

summary = render(read("is_akisi_son_durum_siniflandirma.json"),
                 read("sekiz_gorev_tek_merkezi_rapor.json"),
                 read("hata_asama_raporu.json"),
                 read("madsc_tek_yonetim_ozeti.json"))
(OUT / "madsc_kisa_durum_ozeti.md").write_text(summary, encoding="utf-8")
print("Kisa durum ozeti mevcut merkezi raporlardan olusturuldu.")
