#!/usr/bin/env python3
"""Beş aşamanın bütün kanıtlarını tek ekranda toplayan salt okunur rapor."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "madsc_merkezi_denetim"
FILES = {
 "güvenlik": ["protected-write-gate-report.json", "yedek_ve_korunan_dosyalar_kanit.json"],
 "keşif": ["kesif_ve_yabanci_kaynak_toplu_ozet.json", "kaynak_hedef_mutabakati.json"],
 "kanal testleri": ["ana_liste_saglik_kosu_kaniti.json", "tekrar_test_analizi.json"],
 "logo ve EPG": ["logo_epg_kimlik_gecmis_tek_rapor.json"],
 "arşiv ve kabul": ["bes_asama_kabul_kapisi.json", "on_sekiz_gorev_bes_asama_kanit.json", "kalan_isler_tek_kosu_karar_tablosu.json"],
}
def read(folder, name):
    try:
        return json.loads((folder / name).read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return None
def build(folder, discovery_folder=None):
    discovery_folder = discovery_folder if discovery_folder is not None else ROOT / "madsc_kesif"
    logo_report = read(discovery_folder, "candidate_logo_missing_report.json")
    if not isinstance(logo_report, dict):
        logo_report = None
    logo_status = ("ADAY_LOGO_KANITI_YOK" if logo_report is None else
                   "ADAY_LOGO_KAYDI_GECERSIZ" if not isinstance(logo_report.get("total_candidates"), int) else
                   "ADAY_LOGO_KANITI_VAR_KIMLIK_ONAYSIZ")
    stages = []
    missing = []
    for stage, names in FILES.items():
        absent = [name for name in names if read(folder, name) is None]
        missing.extend(absent)
        stages.append({"asama": stage, "eksik": absent,
                       "durum": "KANIT_EKSIK" if absent else "RAPOR_VAR_CIHAZ_KABULU_AYRI"})
    if logo_report is None:
        missing.append("madsc_kesif/candidate_logo_missing_report.json")
        for row in stages:
            if row["asama"] == "logo ve EPG":
                row["eksik"].append("madsc_kesif/candidate_logo_missing_report.json")
                row["durum"] = "KANIT_EKSIK"
    push = read(folder, "tek_islem_coklu_push_analizi.json") or {}
    jobs = read(folder, "kalan_isler_tek_kosu_karar_tablosu.json") or {}
    backup = read(folder, "yedek_ve_korunan_dosyalar_kanit.json") or {}
    identity = read(folder, "logo_epg_kimlik_gecmis_tek_rapor.json") or {}
    channel = read(folder, "ana_liste_saglik_kosu_kaniti.json") or {}
    sources = identity.get("evidence", {})
    sources = sources if isinstance(sources, dict) else {}
    missing_sources = [key for key, item in sources.items() if not isinstance(item, dict) or item.get("available") is not True]
    channel_status = channel.get("durum", "KOSU_KANITI_YOK")
    backup_restore = backup.get("restore_test", "KANIT_YOK")
    backup_historical = backup.get("historical_recovery_verified") is True
    backup_external = backup.get("off_github_copy")
    backup_status = ("TAM_DOGRULANDI" if backup_restore == "GIT_HEAD_IZOLE_ESLESME_DOGRULANDI" and backup_historical and backup_external == "DOGRULANDI" else "EKSIK_KANIT")
    problems = [{"tur": "RAPOR_EKSIK", "aciklama": name} for name in missing]
    problems += [{"tur": "KIMLIK_KAYNAGI_EKSIK", "aciklama": name} for name in missing_sources]
    if channel_status != "IS_AKISI_BASARILI_KANAL_SONUCU_INCELENMELI":
        problems.append({"tur": "KANAL_KOSU_KANITI", "aciklama": str(channel_status)})
    if logo_report is not None and logo_status == "ADAY_LOGO_KAYDI_GECERSIZ":
        problems.append({"tur": "LOGO_RAPORU_HATALI", "aciklama": "Aday logo raporunun sayısal kanıtı geçersiz"})
    if logo_report is not None and isinstance(logo_report.get("category_counts"), dict):
        for category, count in sorted(logo_report["category_counts"].items()):
            if count and category != "PNG_HAZIR_KIMLIK_ONAYI_BEKLIYOR":
                problems.append({"tur": "ADAY_LOGO_INCELEME", "aciklama": "{}: {} aday".format(category, count)})
    problems += [{"tur": "GEREKSIZ_TEKRAR", "aciklama": name} for name in push.get("tekrarli_senaryolar", [])]
    problems += [{"tur": "MERKEZ_TETIKLEME_EKSIK", "aciklama": name} for name in push.get("merkezi_denetime_ulasamayan_senaryolar", [])]
    problems += [{"tur": "KALAN_IS", "aciklama": item.get("name", "?") + ": " + item.get("status", "?")}
                 for item in jobs.get("jobs", []) if item.get("status") not in ("TAMAMLANDI", "ONAYLANDI")]
    if backup_restore != "GIT_HEAD_IZOLE_ESLESME_DOGRULANDI":
        problems.append({"tur": "YEDEK_GERI_YUKLEME", "aciklama": "İzole geri yükleme kanıtı yok"})
    if not backup_historical:
        problems.append({"tur": "TARIHSEL_YEDEK", "aciklama": "Önceki sürümden geri yükleme doğrulanmadı"})
    if backup_external != "DOGRULANDI":
        problems.append({"tur": "HARICI_KOPYA", "aciklama": "GitHub dışı bağımsız kopya doğrulanmadı"})
    problems += [{"tur": "CIHAZ_ONAYI", "aciklama": "IBO Player kanal ve EPG görünümü"},
                 {"tur": "HARICI_YEDEK", "aciklama": "Bağımsız yedek ve gerçek geri yükleme kanıtı"}]
    return {"genel_kabul": "HENUZ_ONAYLANMADI", "bes_asama": stages,
            "yedek_kaniti": {"durum": backup_status, "izole_geri_yukleme": backup_restore,
                            "tarihsel_geri_yukleme": backup_historical,
                            "bagimsiz_kopya": backup_external or "DOGRULANMADI"},
            "aday_logo_durumu": logo_status,
            "eksik_kimlik_kaynaklari": missing_sources,
            "kanal_kosusu": channel_status,
            "aday_logo_sayisi": logo_report.get("total_candidates") if isinstance(logo_report, dict) else None,
            "eksik_rapor": len(missing),
            "gereksiz_tekrar": len(push.get("tekrarli_senaryolar", [])),
            "merkez_kapsam_eksigi": len(push.get("merkezi_denetime_ulasamayan_senaryolar", [])),
            "acik_isler": problems, "acik_is_sayisi": len(problems),
            "not": "Yeşil Actions canlı IBO onayı değildir; korunan dosyalara yazılmaz."}
def markdown(result):
    lines = ["# MADSC — TEK EKRANDA TOPLU SONUÇ", "",
             "**Genel kabul:** " + result["genel_kabul"], "",
             "| Aşama | Durum | Eksik raporlar |", "|---|---|---|"]
    for row in result["bes_asama"]:
        lines.append("| {} | {} | {} |".format(row["asama"], row["durum"], ", ".join(row["eksik"]) or "Yok"))
    lines += ["", "## Eksik ve fazla işler", "",
              "- Eksik rapor: " + str(result["eksik_rapor"]),
              "- Yeni aday logo kanıtı: " + result["aday_logo_durumu"],
              "- Eksik logo/EPG kimlik kaynakları: " + (", ".join(result["eksik_kimlik_kaynaklari"]) or "Yok"),
              "- Kanal sağlık koşusu: " + str(result["kanal_kosusu"]),
              "- Yedek geri yükleme: " + result["yedek_kaniti"]["izole_geri_yukleme"],
              "- Tarihsel yedek doğrulandı: " + str(result["yedek_kaniti"]["tarihsel_geri_yukleme"]),
              "- GitHub dışı kopya: " + result["yedek_kaniti"]["bagimsiz_kopya"],
              "- Yeni aday sayısı (kanıt varsa): " + str(result["aday_logo_sayisi"]),
              "- Gereksiz push tekrarı: " + str(result["gereksiz_tekrar"]),
              "- Merkeze ulaşmayan senaryo: " + str(result["merkez_kapsam_eksigi"]),
              "- Toplam açık takip maddesi: " + str(result["acik_is_sayisi"]), ""]
    lines += ["- **{}:** {}".format(item["tur"], item["aciklama"]) for item in result["acik_isler"]]
    lines += ["", result["not"], ""]
    return "\n".join(lines)
if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    result = build(OUT)
    (OUT / "TEK_EKRAN_TOPLU_SONUC.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "TEK_EKRAN_TOPLU_SONUC.md").write_text(markdown(result), encoding="utf-8")
    print("TEK EKRAN: {} açık madde".format(result["acik_is_sayisi"]))
