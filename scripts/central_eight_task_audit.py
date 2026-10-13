#!/usr/bin/env python3
"""Sekiz is basligi icin tek salt-okunur denetim ve eylem listesi."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "madsc_merkezi_denetim"
OUT.mkdir(exist_ok=True)

def present(*names):
    return {name: (ROOT / name).is_file() for name in names}

def task(number, name, evidence, blockers):
    return {"no": number, "gorev": name, "kanit": evidence,
            "eksikler": blockers, "durum": "TAKIP_GEREKIYOR" if blockers else "KOD_KAPSAMI_MEVCUT"}

workflows = sorted((ROOT / ".github/workflows").glob("*.yml"))
tests = sorted(ROOT.glob("test_*.py"))
protected = ["CALISANLAR.m3u", "GUVENLIK_KURALLARI.md", "AGENTS.md"]
records = [
    task(1, "Merkezi otomasyon ve hata kok nedeni",
         present("scripts/central_run_status.py", "scripts/central_workflow_inventory.py"),
         ["Canli Actions hatalari ve loglari ayrica incelenmeli; tek kosu tum isleri calistirmaz."]),
    task(2, "Kaynak taramasi ve tekrar azaltma",
         present("madsc_akilli_kesif.py", ".github/workflows/madsc-birlesik-kesif.yml"),
         ["URL bazli tekrar/test maliyeti olculmeden optimizasyon tamamlanmis sayilmaz."]),
    task(3, "156 kaynak 155 hedef mutabakati",
         present("madsc_akilli_kesif.py"),
         ["Kaynak/hedef gercek AST mutabakat raporunda olculur; fark sifirlanmadikca acik kalir."]),
    task(4, "Butun dosyalar otomasyonlar ve yedekler",
         {"workflow_count": len(workflows), "python_test_count": len(tests),
          "protected_files": present(*protected),
          "backup_workflows": [p.name for p in workflows if "yedek" in p.name.lower() or "backup" in p.name.lower()]},
         ["GitHub disi bagimsiz yedek ve gercek geri yukleme kaniti eksik."]),
    task(5, "Logo EPG kimlik ve test gecmisi",
         present("scripts/candidate_logo_report.py", "scripts/candidate_epg_logo_join.py",
                 "scripts/build_epg.py", "scripts/ibo_epg_kimlik_denetimi.py"),
         ["IBO Isvec cihazinda logo/EPG/kimlik dogrulamasi eksik."]),
    task(6, "Guvenli IBO aday denemesi",
         {"protected_files": present(*protected), "device_result": "NOT_VERIFIED"},
         ["Kullanici onayli ayri cihaz denemesi ve aday secimi gerekiyor; otomatik aktarim yasak."]),
    task(7, "Tek yonetim paneli",
         present("scripts/central_six_area_audit.py", "scripts/central_run_status.py"),
         ["Canli panel ve kalici IBO kullanici karar arayuzu henuz yok."]),
    task(8, "Gunluk kisa ozet ve hata nedenleri",
         {"workflow_status_script": present("scripts/central_run_status.py"),
          "report_frequency": "MERKEZI_AYDA_IKI_KEZ"},
         ["Gunluk otomatik kisa ozet ve log tabanli kok neden raporu tamamlanmadi."]),
]
tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, text=True,
                         capture_output=True, check=False)
report = {"version": 1, "total": len(records), "workflow_count": len(workflows),
          "tracked_file_count": len(tracked.stdout.splitlines()) if tracked.returncode == 0 else None,
          "tasks": records,
          "summary": {"needs_followup": sum(bool(x["eksikler"]) for x in records),
                      "fully_completed": sum(not x["eksikler"] for x in records)},
          "safety": {"playlists_modified": False, "backups_modified": False,
                     "cron_modified": False, "device_test_claimed": False},
          "limitations": "Kod envanteri ve eksik kanit raporu; sekiz isin bitirilmesi veya cihaz testi degildir."}
(OUT / "sekiz_gorev_tek_merkezi_rapor.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print("Sekiz gorev tek merkezi raporda toplandi; eksikler acik birakildi.")
