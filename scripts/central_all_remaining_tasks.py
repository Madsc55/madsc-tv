#!/usr/bin/env python3
"""Kalan isleri tek kanit tablosunda, onay gerektirenleri ayirarak yonet."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "madsc_merkezi_denetim"
OUT.mkdir(exist_ok=True)

def load(name):
    path = OUT / name
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeError):
        return None

def assemble(source, duplicate, backups, identity, failures, tasks):
    jobs = []
    def add(code, name, status, evidence, next_action, dependency):
        jobs.append({"id": code, "name": name, "status": status,
                     "evidence": evidence, "next_action": next_action,
                     "dependency": dependency})
    if isinstance(source, dict):
        diff = source.get("difference")
        dup = source.get("duplicate_endpoints", [])
        invalid = source.get("invalid_endpoint_definitions", [])
        status = "TANIM_ESIT_KANIT_KISITLI" if diff == 0 and not dup and not invalid else "INCELEME_GEREKLI"
        add(1, "Kaynak hedef mutabakati", status,
            {"defined": source.get("defined"), "target": source.get("target"), "difference": diff,
             "duplicate_count": len(dup), "invalid_count": len(invalid)},
            "Kaynaklari canli erisilebilirlik ve lisans acisindan dogrula; sayilari rastgele degistirme.",
            "CANLI_KAYNAK_KANITI")
    else:
        add(1, "Kaynak hedef mutabakati", "KANIT_YOK", {}, "Kaynak denetimini yeniden calistir.", "RAPOR")
    add(2, "Tekrar test optimizasyonu",
        "OLCUM_VAR_KESIN_OPTIMIZASYON_YOK" if isinstance(duplicate, dict) and duplicate.get("status") != "GECMIS_DOSYASI_YOK" and isinstance(duplicate.get("excess_test_runs"), int) else "GECMIS_KANITI_YOK",
        {"excess_test_runs": duplicate.get("excess_test_runs") if isinstance(duplicate, dict) else None},
        "Gercek gecmisle tekrar maliyetini dogrula; test guvenlik kurallarini bozma.", "GECMIS")
    add(3, "Yedek geri yukleme", "GERI_YUKLEME_BU_KOSUDA_YOK",
        {"protected_missing": backups.get("protected_missing") if isinstance(backups, dict) else None},
        "Bagimsiz kopya ve izole geri yukleme kanitini dogrula.", "HARICI_YEDEK_ERISIMI")
    add(4, "Logo EPG kanal kimligi", "CIHAZ_ONAYI_YOK",
        {"report_present": isinstance(identity, dict)},
        "IBO Isvec cihazinda goruntu ve EPG dogrula.", "KULLANICI_CIHAZI")
    add(5, "Actions hata analizi", "IS_ADIM_KANITI_VAR" if isinstance(failures, dict) else "KANIT_YOK",
        {"failed_runs_in_sample": failures.get("failed_runs_in_sample") if isinstance(failures, dict) else None},
        "Gercek kok neden icin ilgili loglari incele.", "GITHUB_LOG")
    add(6, "IBO onay ve liste aktarimi", "ONAY_BEKLIYOR", {},
        "Yalniz kullanici onayli adaylari ayri listede degerlendir; otomatik aktarim yapma.", "KULLANICI_ONAYI")
    add(7, "Tek yonetim", "OKUNABILIR_RAPOR_VAR_PANEL_YOK", {},
        "Kalici cihaz onay arayuzu ayri izin ve tasarim gerektirir.", "ARAYUZ")
    add(8, "Gunluk ozet", "MERKEZI_KOSUDA_RAPOR_VAR_GUNLUK_TETIK_YOK", {},
        "Gunluk otomatik calisma icin ayrica zamanlama onayi gerekir.", "CRON_ONAYI")
    return {"total": len(jobs), "jobs": jobs,
            "prior_task_report_present": isinstance(tasks, dict),
            "all_done": False, "requires_user_or_external_evidence": [x["id"] for x in jobs if x["dependency"] in
            ("HARICI_YEDEK_ERISIMI", "KULLANICI_CIHAZI", "KULLANICI_ONAYI", "CRON_ONAYI")],
            "safety": "Kanal listesi, yedek, cron, onay, kesif ve test esikleri degistirilmedi.",
            "limitations": "Tek kosu kalan islerin kanitini ve bagimliliklarini toplar; eksik cihaz, lisans, harici yedek veya gercek testleri bitmis saymaz."}

result = assemble(load("kaynak_hedef_mutabakati.json"), load("tekrar_test_analizi.json"),
                  load("yedek_ve_korunan_dosyalar_kanit.json"),
                  load("logo_epg_kimlik_gecmis_tek_rapor.json"),
                  load("hata_asama_raporu.json"), load("sekiz_gorev_tek_merkezi_rapor.json"))
(OUT / "kalan_isler_tek_kosu_karar_tablosu.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"{result['total']} is tek kosuda siniflandirildi; tamamlandi iddiasi yok.")

# Yabanci kanal arsivi ve son kontrol ilerlemesini ayni merkezi kosuda denetle.
# Bu inceleme yayini acmaz, kanal kimligi onaylamaz ve playlist degistirmez.
def inspect_m3u(path):
    if not path.is_file():
        return {"present": False, "count": 0, "entries": []}
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    entries = []
    for i, line in enumerate(lines):
        if line.startswith("#EXTINF:"):
            url = lines[i + 1].strip() if i + 1 < len(lines) else ""
            entries.append({"meta": line, "url": url})
    return {"present": True, "count": len(entries), "entries": entries}

main_playlist = inspect_m3u(ROOT / "CALISANLAR.m3u")
foreign_archive = inspect_m3u(ROOT / "YABANCI_KANALLAR.m3u")
backup_entries = [e for e in main_playlist["entries"] if 'group-title="📦 YEDEKLER' in e["meta"]]
archive_pairs = [(e["meta"], e["url"]) for e in foreign_archive["entries"]]
backup_names = [e["meta"].rsplit(",", 1)[-1] for e in backup_entries]
foreign_report = {
    "archive_present": foreign_archive["present"],
    "archive_count": foreign_archive["count"],
    "archive_distinct_records": len(set(archive_pairs)),
    "backup_count": len(backup_entries),
    "backup_names": backup_names,
    "backup_only_trt1_dha": len(backup_entries) == 2 and
        any("TRT 1" in n for n in backup_names) and any("DHA" in n for n in backup_names),
    "archive_urls_missing": sum(not e["url"] for e in foreign_archive["entries"]),
    "new_ibo_category_created": False,
    "live_streams_tested": False,
    "note": "Arsiv kanal kimligi, ulke ve canlilik kaniti degildir; orijinal metadata korunur."
}
(OUT / "yabanci_arsiv_koruma_denetimi.json").write_text(
    json.dumps(foreign_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
last_control = ROOT / "madsc_son_kontrol" / "summary.json"
try:
    last_summary = json.loads(last_control.read_text(encoding="utf-8")) if last_control.exists() else {}
except (OSError, ValueError):
    last_summary = {}
(OUT / "son_kontrol_birikimli_ozet.json").write_text(
    json.dumps({"checked_utc": last_summary.get("checked_utc"),
                "completed": last_summary.get("completed"),
                "remaining": last_summary.get("remaining"),
                "ready_for_playlist": last_summary.get("ready_for_playlist"),
                "status_counts": last_summary.get("status_counts", {}),
                "snapshot_only": True,
                "device_approval_not_inferred": True},
               ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
if not foreign_report["backup_only_trt1_dha"] or foreign_report["archive_count"] != 740 or foreign_report["archive_urls_missing"]:
    raise SystemExit("Yabanci kanal arsivi veya korunan yedekler beklenen durumda degil.")
print("Yabanci arsiv, yedekler ve birikimli aday ozeti tek merkezi denetimde kontrol edildi.")
