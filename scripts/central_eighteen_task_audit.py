#!/usr/bin/env python3
"""Sekiz temel ve on ek gelistirmeyi tek kanit tablosunda denetle."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "madsc_merkezi_denetim"
OUT.mkdir(exist_ok=True)
EIGHT = [
    ("Yayin ses goruntu surekliligi", 3, ["gelismis_medya_testi.py"]),
    ("Alternatif yayin kesfi", 2, ["yeni_kanal_tara.py"]),
    ("Kanal kimligi", 4, ["scripts/ibo_epg_kimlik_denetimi.py"]),
    ("Logo ve EPG", 4, ["scripts/candidate_epg_logo_join.py"]),
    ("Kaynak guven puani", 2, ["kaynak_guven_puani.py"]),
    ("Eksik kanal kesfi", 2, ["madsc_akilli_kesif.py"]),
    ("Gunluk saglik", 5, ["scripts/central_run_status.py"]),
    ("Ariza ve aday uyarilari", 5, ["scripts/central_run_status.py"]),
]
TEN = [
    ("Akilli tekrar test zamanlamasi", 3, ["scripts/central_duplicate_test_audit.py"]),
    ("Yanlis negatif ve pozitif ayrimi", 3, ["scripts/central_all_remaining_tasks.py"]),
    ("Ayni kanal alternatiflerini gruplama", 2, ["aday_tekrar_raporu.py"]),
    ("Cografi engel token gecici hata ayrimi", 3, ["gelismis_medya_testi.py"]),
    ("Degisiklik gecmisi", 5, ["DEVAM_NOTU.md"]),
    ("Yedi ve otuz gun egilimleri", 5, ["scripts/central_duplicate_test_audit.py"]),
    ("Logo EPG kimlik dogrulamasi", 4, ["scripts/central_identity_epg_logo_audit.py"]),
    ("Actions eszamanlilik sure izin guvenligi", 1, ["scripts/central_workflow_inventory.py"]),
    ("Tek yonetim panosu", 5, ["scripts/central_management_summary.py"]),
    ("Simulasyon ve geri alma", 1, ["scripts/central_isolated_git_restore.py"]),
]

def build(root=ROOT):
    records = []
    for issue, offset, entries in ((2, 0, EIGHT), (3, 8, TEN)):
        for number, (title, stage, paths) in enumerate(entries, offset + 1):
            existing = [p for p in paths if (root / p).is_file()]
            records.append({
                "no": number, "gorev": title, "asama": stage,
                "issue": issue, "kod_kaniti": existing,
                "eksik_dosyalar": [p for p in paths if p not in existing],
                "durum": "KOD_VAR_CANLI_DOGRULAMA_YOK" if len(existing) == len(paths) else "KOD_KANITI_EKSIK",
                "canli_dogrulandi": False, "ibo_onaylandi": False,
            })
    assert len(records) == 18 and {x["no"] for x in records} == set(range(1, 19))
    missing = [x["no"] for x in records if x["eksik_dosyalar"]]
    return {
        "eksik_kod_gorevleri": missing,
        "canli_kanit_bekleyen_gorevler": [x["no"] for x in records],
        "tamamlanmis_gorev_sayisi": 0,
        "toplam": 18, "sekiz_taban": 8, "on_ek": 10,
        "bes_asama": {str(n): sum(x["asama"] == n for x in records) for n in range(1, 6)},
        "kod_kaniti_eksik": sum(bool(x["eksik_dosyalar"]) for x in records),
        "tamamlandi": False, "gorevler": records,
        "sinir": "Dosya varligi calisan yayin, dogru kanal kimligi, uyarinin teslimi, tarihsel kapsam veya IBO onayi degildir.",
        "koruma": "Salt okunur; listeler, yedekler, cron ve onaylar degistirilmez.",
    }

if __name__ == "__main__":
    result = build()
    (OUT / "on_sekiz_gorev_bes_asama_kanit.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"18 gorev 5 asamada siniflandirildi; kod kaniti eksik: {result['kod_kaniti_eksik']}.")
