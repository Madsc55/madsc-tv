#!/usr/bin/env python3
"""Beş aşamanın bütün kanıtlarını tek ekranda toplayan salt okunur rapor."""
import json
from pathlib import Path
OUT = Path(__file__).resolve().parents[1] / "madsc_merkezi_denetim"
FILES = {
 "güvenlik": ["protected-write-gate-report.json", "yedek_ve_korunan_dosyalar_kanit.json"],
 "keşif": ["kesif_ve_yabanci_kaynak_toplu_ozet.json", "kaynak_hedef_mutabakati.json"],
 "kanal testleri": ["ana_liste_saglik_kosu_kaniti.json", "tekrar_test_analizi.json"],
 "logo ve EPG": ["logo_epg_kimlik_gecmis_tek_rapor.json", "aday_logo_eksik_raporu.json"],
 "arşiv ve kabul": ["bes_asama_kabul_kapisi.json", "on_sekiz_gorev_bes_asama_kanit.json", "kalan_isler_tek_kosu_karar_tablosu.json"],
}
def read(folder, name):
    try:
        return json.loads((folder / name).read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return None
def build(folder):
    stages = []
    missing = []
    for stage, names in FILES.items():
        absent = [name for name in names if read(folder, name) is None]
        missing.extend(absent)
        stages.append({"asama": stage, "eksik": absent,
                       "durum": "KANIT_EKSIK" if absent else "RAPOR_VAR_CIHAZ_KABULU_AYRI"})
    push = read(folder, "tek_islem_coklu_push_analizi.json") or {}
    jobs = read(folder, "kalan_isler_tek_kosu_karar_tablosu.json") or {}
    problems = [{"tur": "RAPOR_EKSIK", "aciklama": name} for name in missing]
    problems += [{"tur": "GEREKSIZ_TEKRAR", "aciklama": name} for name in push.get("tekrarli_senaryolar", [])]
    problems += [{"tur": "MERKEZ_TETIKLEME_EKSIK", "aciklama": name} for name in push.get("merkezi_denetime_ulasamayan_senaryolar", [])]
    problems += [{"tur": "KALAN_IS", "aciklama": item.get("name", "?") + ": " + item.get("status", "?")}
                 for item in jobs.get("jobs", []) if item.get("status") not in ("TAMAMLANDI", "ONAYLANDI")]
    problems += [{"tur": "CIHAZ_ONAYI", "aciklama": "IBO Player kanal ve EPG görünümü"},
                 {"tur": "HARICI_YEDEK", "aciklama": "Bağımsız yedek ve gerçek geri yükleme kanıtı"}]
    return {"genel_kabul": "HENUZ_ONAYLANMADI", "bes_asama": stages, "eksik_rapor": len(missing),
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
