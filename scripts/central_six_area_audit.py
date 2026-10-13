#!/usr/bin/env python3
"""Alti plan basligini tek, salt okunur merkezi raporda birlestir."""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "madsc_merkezi_denetim"
OUT.mkdir(exist_ok=True)

def exists(*paths):
    return [str(p) for p in paths if (ROOT / p).exists()]

def check(title, evidence, limitations, status="DENETLENDI"):
    return {"konu": title, "durum": status, "kanit": evidence, "sinir": limitations}

workflows = list((ROOT / ".github/workflows").glob("*.y*ml"))
python_tests = list(ROOT.glob("test_*.py"))
reports = []
reports.append(check("1. Basarisiz otomasyonlar",
    {"raporlar": exists("scripts/central_run_status.py", "scripts/central_workflow_inventory.py"),
     "workflow_sayisi": len(workflows)},
    "Gercek son kosu durumlari merkezi Actions adiminda API'den eklenir; bu statik denetim tek basina basari kaniti degildir."))
discovery = exists(".github/workflows/madsc-birlesik-kesif.yml", "madsc_akilli_kesif.py")
reports.append(check("2. Tekrarli kanal taramasi",
    {"kesif_bilesenleri": discovery, "teknik_test_dosyasi_sayisi": len(python_tests)},
    "Gercek URL/test gecmisi karsilastirilip tekrar orani olculmeden tekrarlar azaltildi denemez.",
    "INCELEME_GEREKIYOR"))
sources = list(ROOT.rglob("*kaynak*"))
targets = list(ROOT.rglob("*hedef*"))
reports.append(check("3. 156 kaynak / 155 hedef farki",
    {"kaynak_adli_dosya_sayisi": len([p for p in sources if p.is_file()]),
     "hedef_adli_dosya_sayisi": len([p for p in targets if p.is_file()])},
    "156 ve 155 sayilari bu dosya adi taramasindan dogrulanamaz; ilgili gercek kaynak/hedef raporu eslestirilmeli.",
    "INCELEME_GEREKIYOR"))
reports.append(check("4. Dosya, otomasyon, yedek kapsami",
    {"workflow_sayisi": len(workflows),
     "yedek_isleri": [p.name for p in workflows if "yedek" in p.name.lower() or "backup" in p.name.lower()],
     "koruma_dosyalari": exists("AGENTS.md", "GUVENLIK_KURALLARI.md", "CALISANLAR.m3u")},
    "Yedek varligi veya workflow varligi geri yukleme testinin basarisi degildir."))
reports.append(check("5. Kanal kimligi, logo, EPG ve test gecmisi",
    {"bilesenler": exists("scripts/candidate_logo_report.py", "scripts/candidate_epg_logo_join.py",
                          "scripts/build_epg.py", "scripts/ibo_epg_kimlik_denetimi.py")},
    "Bilesen varligi, kimlik dogrulama veya IBO'da EPG calisma kaniti degildir.",
    "INCELEME_GEREKIYOR"))
reports.append(check("6. IBO icin guvenli aday deneme",
    {"onay_kurallari": exists("GUVENLIK_KURALLARI.md", "AGENTS.md"),
     "korunan_listeye_otomatik_ekleme": False},
    "Bu denetim cihazda kanal test etmez, test playlisti olusturmaz ve yedeklere kanal eklemez.",
    "KULLANICI_CIHAZ_TESTI_GEREKIR"))
summary = {"kontrol_sayisi": len(reports), "kontroller": reports,
           "degisiklik": {"kanal_listesi": False, "yedek": False, "cron": False},
           "aciklama": "Alti baslik tek raporda incelendi; eksik kanitlar tamamlandi anlamina gelmez."}
(OUT / "alti_konu_tek_denetime_rapor.json").write_text(
    json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print("Alti konu tek raporda toplandi; korunan dosyalar degistirilmedi.")
