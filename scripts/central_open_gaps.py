#!/usr/bin/env python3
"""Sekiz gorevde gercek tamamlanma ve kanit eksikligini ayri raporla."""
import json
from pathlib import Path
try:
    from scripts.evidence_reader import read_json_evidence
except ModuleNotFoundError:
    from evidence_reader import read_json_evidence

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "madsc_merkezi_denetim"
OUT.mkdir(exist_ok=True)

def read(name):
    state, data = read_json_evidence(OUT / name)
    return data if state == "present" else None

def build(tasks, management):
    records = tasks.get("tasks", []) if isinstance(tasks, dict) else []
    sections = management.get("sections", {}) if isinstance(management, dict) else {}
    result = []
    for task in records:
        blockers = task.get("eksikler", [])
        result.append({"no": task.get("no"), "gorev": task.get("gorev"),
                       "durum": "TAKIP_GEREKIYOR" if blockers else "KOD_KAPSAMI_VAR_TAMAMLANDI_KANITI_GEREKIR",
                       "acik_eksikler": blockers,
                       "user_ibo_approval": "NOT_VERIFIED"})
    missing = [key for key, item in sections.items() if item.get("status") != "RAPOR_VAR"]
    return {"task_count": len(result), "open_task_count": sum(bool(x["acik_eksikler"]) for x in result),
            "tasks": result, "missing_or_invalid_reports": missing,
            "management_report_present": isinstance(management, dict),
            "task_report_present": isinstance(tasks, dict),
            "limitations": "Rapor dosyasi varligi, is tamamlandi demek degildir. IBO, lisans, geri yukleme ve dis yedek ayri kanit ister.",
            "safety": "Salt okunur; playlist, yedek, cron ve kullanici onaylari degistirilmez."}

report = build(read("sekiz_gorev_tek_merkezi_rapor.json"),
               read("madsc_tek_yonetim_ozeti.json"))
(OUT / "acik_isler_ve_eksik_kanitlar.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Acik gorev: {report['open_task_count']} / {report['task_count']}; eksik rapor: {len(report['missing_or_invalid_reports'])}.")
