#!/usr/bin/env python3
"""Mevcut merkezi raporlari tek, kanita dayali yonetim ozetinde topla."""
import json
from datetime import datetime, timezone
from pathlib import Path
try:
    from scripts.evidence_reader import read_json_evidence
except ModuleNotFoundError:
    from evidence_reader import read_json_evidence

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "madsc_merkezi_denetim"
OUT.mkdir(exist_ok=True)
SOURCES = {
    "sekiz_gorev": "sekiz_gorev_tek_merkezi_rapor.json",
    "on_sekiz_gorev": "on_sekiz_gorev_bes_asama_kanit.json",
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
    "ana_liste_saglik": "ana_liste_saglik_kosu_kaniti.json",
    "bes_asama": "bes_asama_tum_workflow_eslestirmesi.json",
    "actions_dogrulama": "actions_otomatik_sonuc_dogrulama.json",
}

def build(folder):
    sections = {}
    for key, filename in SOURCES.items():
        state, data = read_json_evidence(folder / filename)
        if state == "missing":
            sections[key] = {"status": "KANIT_YOK", "file": filename}
        elif state == "invalid":
            sections[key] = {"status": "GECERSIZ_RAPOR", "file": filename}
        else:
            sections[key] = {"status": "RAPOR_VAR", "file": filename, "data": data}
    missing = [key for key, row in sections.items() if row["status"] != "RAPOR_VAR"]
    # Kritik sinyalleri buyuk raporu acmadan gorunur kil; veri yoksa sifir varsayma.
    source_data = sections["kaynak_mutabakati"].get("data", {})
    repeat_data = sections["tekrar_test"].get("data", {})
    indicators = {
        "eighteen_tasks_mapped": sections["on_sekiz_gorev"].get("data", {}).get("toplam"),
        "eighteen_tasks_code_evidence_missing": sections["on_sekiz_gorev"].get("data", {}).get("kod_kaniti_eksik"),
        "eighteen_tasks_live_evidence_pending": len(sections["on_sekiz_gorev"].get("data", {}).get("canli_kanit_bekleyen_gorevler", [])) if isinstance(sections["on_sekiz_gorev"].get("data", {}).get("canli_kanit_bekleyen_gorevler"), list) else None,
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
        "main_playlist_health_run": sections["ana_liste_saglik"].get("data", {}).get("durum", "KOSU_KANITI_YOK"),
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
    # Bes asama kapsami ve gercek Actions sonucunu ayri tut.
    stage_data = sections["bes_asama"].get("data", {})
    actions_data = sections["actions_dogrulama"].get("data", {})
    mapped = stage_data.get("mapped_count")
    total = stage_data.get("workflow_count")
    indicators["five_stage_workflows_mapped"] = mapped
    indicators["five_stage_workflows_total"] = total
    indicators["five_stage_unreviewed_ownership"] = len(stage_data.get("manual_scope_review_required", [])) if isinstance(stage_data.get("manual_scope_review_required"), list) else None
    indicators["actions_successful_latest_seen"] = actions_data.get("successful")
    indicators["actions_failed_latest_seen"] = len(actions_data.get("failed", [])) if isinstance(actions_data.get("failed"), list) else None
    indicators["historical_coverage_verified"] = stage_data.get("complete_historical_coverage_verified") is True
    # Bes asamanin her birini ayri kanit ve engel durumuyla tek rapora ekle.
    stage_evidence = {
        1: ("korunan_dosyalar_yedek", "otomasyon_durumu"),
        2: ("kaynak_mutabakati", "kesif_kaynaklari"),
        3: ("tekrar_test", "son_kontrol", "ana_liste_saglik"),
        4: ("logo_epg_kimlik",),
        5: ("hata_asamalari", "kalan_isler", "actions_dogrulama"),
    }
    stage_results = []
    for stage in stage_data.get("stages", []):
        number = stage.get("number")
        expected = stage_evidence.get(number, ())
        absent = [key for key in expected if sections[key]["status"] != "RAPOR_VAR"]
        stage_results.append({
            "number": number,
            "name": stage.get("name"),
            "workflow_count": len(stage.get("workflows", [])),
            "evidence_reports": list(expected),
            "missing_evidence": absent,
            "status": "KANIT_EKSIK" if absent else "RAPOR_VAR_SONUC_DOGRULAMASI_GEREKIR",
        })
    indicators["five_stage_evidence_status"] = stage_results
    indicators["actions_current_run_verified"] = False
    blockers = []
    eighteen = sections["on_sekiz_gorev"].get("data", {})
    if eighteen.get("eksik_kod_gorevleri"):
        blockers.append({"code": "EIGHTEEN_TASK_CODE_GAPS", "status": "INCELEME_GEREKLI",
                         "tasks": eighteen["eksik_kod_gorevleri"]})
    if eighteen.get("canli_kanit_bekleyen_gorevler"):
        blockers.append({"code": "EIGHTEEN_TASK_LIVE_EVIDENCE_PENDING", "status": "KANIT_EKSIK",
                         "tasks": eighteen["canli_kanit_bekleyen_gorevler"]})
    if indicators["main_playlist_health_run"] in ("KOSU_KANITI_YOK", "IS_AKISI_BASARISIZ"):
        blockers.append({"code": "MAIN_PLAYLIST_HEALTH_RUN_NOT_VERIFIED", "status": "KANIT_EKSIK",
                         "evidence": SOURCES["ana_liste_saglik"]})
    if source_data.get("difference") not in (None, 0):
        blockers.append({"code": "SOURCE_TARGET_MISMATCH", "status": "INCELEME_GEREKLI",
                         "evidence": SOURCES["kaynak_mutabakati"]})
    if repeat_data.get("invalid_history_records", 0) and isinstance(repeat_data.get("invalid_history_records"), int):
        blockers.append({"code": "INVALID_TEST_HISTORY", "status": "INCELEME_GEREKLI",
                         "evidence": SOURCES["tekrar_test"]})
    if stage_data.get("manual_scope_review_required"):
        blockers.append({"code": "UNREVIEWED_WORKFLOW_OWNERSHIP", "status": "INCELEME_GEREKLI",
                         "workflows": stage_data["manual_scope_review_required"]})
    if stage_results and any(row["missing_evidence"] for row in stage_results):
        blockers.append({"code": "FIVE_STAGE_MISSING_EVIDENCE", "status": "KANIT_EKSIK",
                         "stages": [row["number"] for row in stage_results if row["missing_evidence"]]})
    if mapped is not None and total is not None and mapped != total:
        blockers.append({"code": "FIVE_STAGE_MAPPING_INCOMPLETE", "status": "INCELEME_GEREKLI"})
    if isinstance(actions_data.get("failed"), list) and actions_data["failed"]:
        blockers.append({"code": "LATEST_ACTIONS_FAILURES", "status": "INCELEME_GEREKLI", "runs": actions_data["failed"]})
    if missing:
        blockers.append({"code": "MISSING_AUDIT_EVIDENCE", "status": "KANIT_EKSIK",
                         "sections": missing})
    blockers.append({"code": "IBO_DEVICE_VERIFICATION", "status": "KAPSAM_DISI",
                     "note": "Kullanici talebi geregi cihaz testi yapilmaz."})
    return {
        "five_stage_results": stage_results,
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
