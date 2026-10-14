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
    restore_state = backups.get("restore_test") if isinstance(backups, dict) else None
    historical = backups.get("historical_recovery_verified") is True if isinstance(backups, dict) else False
    external = backups.get("off_github_copy") == "DOGRULANDI" if isinstance(backups, dict) else False
    full_backup = restore_state == "GIT_HEAD_IZOLE_ESLESME_DOGRULANDI" and historical and external
    add(3, "Yedek geri yukleme",
        "YEDEK_KANITLARI_DOGRULANDI" if full_backup else
        "GIT_HEAD_IZOLE_ESLESME_VAR_HARICI_YEDEK_DOGRULANMADI" if restore_state == "GIT_HEAD_IZOLE_ESLESME_DOGRULANDI" else "GERI_YUKLEME_KANITI_EKSIK",
        {"protected_missing": backups.get("protected_missing") if isinstance(backups, dict) else None,
         "restore_test": restore_state,
         "historical_recovery_verified": historical,
         "off_github_copy_verified": external},
        "Bagimsiz kopya ve izole geri yukleme kanitini dogrula.", "HARICI_YEDEK_ERISIMI")
    add(4, "Logo EPG kanal kimligi", "KIMLIK_KANITI_BEKLIYOR_CIHAZ_TESTI_KAPSAM_DISI",
        {"report_present": isinstance(identity, dict), "ibo_device_retest": False,
         "ibo_user_field_observation": "Kullanıcı cihazında doğrulanmış tekil kanal kanıtı bu raporda yok",
         "technical_false_negative_possible": True},
        "Kanal kimligi ve logo EPG eslesmesini cihaz testi istemeden eldeki kanitlarla incele.", "KANAL_KIMLIK_KANITI")
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
            "limitations": "Tek kosu kalan islerin kanitini ve bagimliliklarini toplar; cihaz testi kapsam disidir. Teknik fail IBO fail demek degildir; eksik kimlik, lisans, harici yedek veya gercek testleri bitmis saymaz."}

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
            # EXTINF sonrasi IPTV seceneklerini atla; sonraki kanala gecme.
            url = ""
            for j in range(i + 1, len(lines)):
                candidate = lines[j].strip()
                if candidate.startswith("#EXTINF:"):
                    break
                if candidate and not candidate.startswith("#"):
                    url = candidate
                    break
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
    "backup_count_is_snapshot_only": True,
    "archive_urls_missing": sum(not e["url"] for e in foreign_archive["entries"]),
    "archive_duplicate_records": foreign_archive["count"] - len(set(archive_pairs)),
    "main_playlist_present": main_playlist["present"],
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
                "device_approval_not_inferred": True,
                "ibo_device_retest_out_of_scope": True,
                "technical_failure_does_not_prove_ibo_failure": True},
               ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
if not foreign_report["archive_present"] or foreign_report["archive_urls_missing"]:
    raise SystemExit("Yabanci kanal arsivi eksik veya URL kaydi bos.")
if not foreign_report["main_playlist_present"]:
    raise SystemExit("Ana kanal listesi bulunamadi; korunan dosya degistirilmedi.")
# Korunan yedekler icin sabit sayi/isim varsayimi yapma; yalnizca salt okunur raporla.
# Gercek liste icerigi degistirilmez.
print("Yabanci arsiv, yedekler ve birikimli aday ozeti tek merkezi denetimde kontrol edildi.")

# Tek pakette kesif kaynaklari, bos aday kuyrugu ve yabanci arsiv
# adaylarini ayristir. Salt okunur: hicbir akisa baglanmaz.
import csv
from urllib.parse import urlsplit

def csv_rows(path):
    if not path.is_file():
        return []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))

access_rows = csv_rows(ROOT / "madsc_kesif" / "kaynak_erisim_raporu.csv")
candidate_rows = csv_rows(ROOT / "madsc_kesif" / "adaylar.csv")
alternative_rows = csv_rows(ROOT / "madsc_kesif" / "alternatifler.csv")
unreachable = [{"source": row.get("kaynak"), "error": row.get("hata")}
               for row in access_rows if row.get("durum") != "ERISILDI"]
# Etiket yalniz arsivden gelen adayin sinifidir; gercek ulke/dil iddiasi degil.
archive_candidates = []
for item in foreign_archive["entries"]:
    url = item["url"]
    parsed = urlsplit(url)
    archive_candidates.append({
        "channel": item["meta"].rsplit(",", 1)[-1],
        "origin": "YABANCI_KANALLAR.m3u",
        "classification": "YABANCI_ADAY_ARSIVI",
        "stream_url": url,
        "host": parsed.hostname or "",
        "url_scheme_valid": parsed.scheme in ("http", "https") and bool(parsed.netloc),
        "technical_test": "BU_KOSUDA_YAPILMADI",
        "identity": "DOGRULANMADI"
    })
(OUT / "yabanci_kanal_adaylari.json").write_text(
    json.dumps({"count": len(archive_candidates), "channels": archive_candidates,
                "not_a_playlist": True, "per_channel_ibo_approval_not_inferred": True,
                "user_confirmed_ibo_field_testing": False,
    "ibo_field_testing_evidence": "KANAL_BAZINDA_DOGRULAMA_YOK",
                "technical_failure_does_not_prove_ibo_failure": True},
               ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
main_urls = {e["url"].strip() for e in main_playlist["entries"]}
discovery_report = {
    "source_report_is_snapshot": True,
    "sources_in_access_report": len(access_rows),
    "accessible_in_snapshot": sum(row.get("durum") == "ERISILDI" for row in access_rows),
    "unreachable_in_snapshot": unreachable,
    "candidate_queue_count": len(candidate_rows),
    "alternative_queue_count": len(alternative_rows),
    "candidate_queue_missing_url": sum(not (row.get("url") or row.get("stream_url") or row.get("link") or "").strip() for row in candidate_rows),
    "alternative_queue_missing_url": sum(not (row.get("url") or row.get("stream_url") or row.get("link") or "").strip() for row in alternative_rows),
    "candidate_urls_already_in_main": sum((row.get("url") or row.get("stream_url") or row.get("link") or "").strip() in main_urls for row in candidate_rows if (row.get("url") or row.get("stream_url") or row.get("link") or "").strip()),
    "alternative_urls_already_in_main": sum((row.get("url") or row.get("stream_url") or row.get("link") or "").strip() in main_urls for row in alternative_rows if (row.get("url") or row.get("stream_url") or row.get("link") or "").strip()),
    "candidate_queue_with_url": sum(bool((row.get("url") or row.get("stream_url") or row.get("link") or "").strip()) for row in candidate_rows),
    "alternative_queue_with_url": sum(bool((row.get("url") or row.get("stream_url") or row.get("link") or "").strip()) for row in alternative_rows),
    "candidate_queue_names": sorted({(row.get("kanal") or row.get("channel") or row.get("name") or "").strip() for row in candidate_rows if (row.get("kanal") or row.get("channel") or row.get("name") or "").strip()}),
    "alternative_queue_names": sorted({(row.get("kanal") or row.get("channel") or row.get("name") or "").strip() for row in alternative_rows if (row.get("kanal") or row.get("channel") or row.get("name") or "").strip()}),
    "candidate_queue_empty": not candidate_rows,
    "foreign_archive_candidate_count": len(archive_candidates),
    "foreign_archive_invalid_url_count": sum(not x["url_scheme_valid"] for x in archive_candidates),
    "foreign_archive_unique_urls": len({x["stream_url"].strip() for x in archive_candidates}),
    "foreign_archive_duplicate_url_count": len(archive_candidates) - len({x["stream_url"].strip() for x in archive_candidates}),
    "foreign_archive_urls_also_in_main": sum(x["stream_url"].strip() in main_urls for x in archive_candidates),
    "main_playlist_count": main_playlist["count"],
    "main_playlist_duplicate_urls": main_playlist["count"] - len(main_urls),
    "foreign_archive_missing_url_count": foreign_report["archive_urls_missing"],
    "foreign_archive_duplicate_records": foreign_report["archive_duplicate_records"],
    "next_action": "Bos aday kuyruğu ile tarihsel son kontrol birbirine karistirilmadan kaynak ve tekrar filtreleri incelenmeli.",
    "live_sources_rechecked": False,
    "live_streams_rechecked": False
}
(OUT / "kesif_ve_yabanci_kaynak_toplu_ozet.json").write_text(
    json.dumps(discovery_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
if discovery_report["foreign_archive_invalid_url_count"]:
    raise SystemExit("Yabanci arsivde gecersiz URL semasi bulundu.")
print(f"Kaynak, aday, alternatif ve {foreign_archive['count']} arsiv kaydi tek merkezi denetimde siniflandirildi.")
