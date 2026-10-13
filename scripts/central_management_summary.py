#!/usr/bin/env python3
"""Mevcut merkezi raporlari tek, kanita dayali yonetim ozetinde topla."""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "madsc_merkezi_denetim"
OUT.mkdir(exist_ok=True)
SOURCES = {
    "sekiz_gorev": "sekiz_gorev_tek_merkezi_rapor.json",
    "kaynak_mutabakati": "kaynak_hedef_mutabakati.json",
    "tekrar_test": "tekrar_test_analizi.json",
    "hata_asamalari": "hata_asama_raporu.json",
    "korunan_dosyalar_yedek": "yedek_ve_korunan_dosyalar_kanit.json",
    "logo_epg_kimlik": "logo_epg_kimlik_gecmis_tek_rapor.json",
    "otomasyon_durumu": "is_akisi_son_durum_siniflandirma.json",
    "kalan_isler": "kalan_isler_tek_kosu_karar_tablosu.json",
    "yabanci_arsiv_koruma": "yabanci_arsiv_koruma_denetimi.json",
    "kesif_kaynaklari": "kesif_ve_yabanci_kaynak_toplu_ozet.json",
    "son_kontrol": "son_kontrol_birikimli_ozet.json",
}

def build(folder):
    sections = {}
    for key, filename in SOURCES.items():
        path = folder / filename
        if not path.is_file():
            sections[key] = {"status": "KANIT_YOK", "file": filename}
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            sections[key] = {"status": "RAPOR_VAR", "file": filename, "data": data}
        except (ValueError, UnicodeError):
            sections[key] = {"status": "GECERSIZ_RAPOR", "file": filename}
    missing = [key for key, row in sections.items() if row["status"] != "RAPOR_VAR"]
    # Kritik sinyalleri buyuk raporu acmadan gorunur kil; veri yoksa sifir varsayma.
    source_data = sections["kaynak_mutabakati"].get("data", {})
    repeat_data = sections["tekrar_test"].get("data", {})
    indicators = {
        "source_defined": source_data.get("defined"),
        "source_target": source_data.get("target"),
        "source_target_difference": source_data.get("difference"),
        "duplicate_source_endpoints": len(source_data["duplicate_endpoints"]) if isinstance(source_data.get("duplicate_endpoints"), list) else None,
        "historical_tested_urls": repeat_data.get("tested_urls"),
        "historical_repeated_urls": repeat_data.get("urls_tested_more_than_once"),
        "historical_repeat_rate": repeat_data.get("repeat_rate_among_tested_urls"),
        "invalid_history_records": repeat_data.get("invalid_history_records"),
        "evidence_complete": not missing,
        "ibo_device_verification": "NOT_VERIFIED",
    }
    # Raporun varligi gorevin tamamlandigini tek basina kanitlamaz.
    evidence_assessment = {}
    for key, section in sections.items():
        if section["status"] != "RAPOR_VAR":
            evidence_assessment[key] = "KANIT_EKSIK"
        elif key == "kaynak_mutabakati":
            difference = section["data"].get("difference")
            evidence_assessment[key] = "HEDEF_FARKI_VAR" if isinstance(difference, int) and difference != 0 else "CANLI_DOGRULAMA_BEKLIYOR"
        else:
            evidence_assessment[key] = "RAPOR_VAR_TAMAMLANMA_DOGRULANMADI"
    blockers = []
    if source_data.get("difference") not in (None, 0):
        blockers.append({"code": "SOURCE_TARGET_MISMATCH", "status": "INCELEME_GEREKLI",
                         "evidence": SOURCES["kaynak_mutabakati"]})
    if repeat_data.get("invalid_history_records", 0) and isinstance(repeat_data.get("invalid_history_records"), int):
        blockers.append({"code": "INVALID_TEST_HISTORY", "status": "INCELEME_GEREKLI",
                         "evidence": SOURCES["tekrar_test"]})
    if missing:
        blockers.append({"code": "MISSING_AUDIT_EVIDENCE", "status": "KANIT_EKSIK",
                         "sections": missing})
    blockers.append({"code": "IBO_DEVICE_VERIFICATION", "status": "KAPSAM_DISI",
                     "note": "Kullanici talebi geregi cihaz testi yapilmaz."})
    return {
        "evidence_assessment": evidence_assessment,
        "open_blockers": blockers,
        "key_indicators": indicators,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "section_count": len(sections),
        "missing_evidence": missing,
        "sections": sections,
        "device_ibo_approval": "NOT_VERIFIED",
        "playlist_change": False,
        "limitations": "Bu rapor tek dosyada kanit toplar; eksik dosya basari sayilmaz. Canli interaktif panel, cihaz testi veya kanal onayi degildir."
    }

report = build(OUT)
(OUT / "madsc_tek_yonetim_ozeti.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"{report['section_count']} baslik tek raporda; eksik kanit: {len(report['missing_evidence'])}.")
