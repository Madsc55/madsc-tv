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
# Onayli is listesi: GitHub issue #2. Bu rapor yalnizca kod varligini
# ve eksik dogrulama kanitini raporlar; basarili cihaz/yayin testi iddia etmez.
records = [
    task(1, "Gelismis yayin kontrolu: goruntu/ses, kesinti ve donma",
         present("gelismis_medya_testi.py"),
         ["Gercek yayin ornekleri ve kesinti/donma sonuclari dogrulanmali."]),
    task(2, "Alternatif yayin baglantisi kesfi ve aday raporu",
         present("yeni_kanal_tara.py", "aday_tekrar_raporu.py"),
         ["Alternatif kaynaklarin canli erisimi ve tekilligi dogrulanmali."]),
    task(3, "Kanal kimligi dogrulama ve yanlis eslesme onleme",
         present("scripts/ibo_epg_kimlik_denetimi.py"),
         ["Kanal kimligi kaniti olmadan otomatik onay verilmez."]),
    task(4, "Eksik logo ve EPG kontrolu",
         present("scripts/candidate_logo_report.py", "scripts/candidate_epg_logo_join.py",
                 "scripts/build_epg.py"),
         ["Logo ve EPG eslesme dogrulama kaniti eksik."]),
    task(5, "Kaynak guvenilirlik puani",
         present("kaynak_guven_puani.py"),
         ["Puanlarin gercek gecmis verileriyle dogrulanmasi gerekiyor."]),
    task(6, "Eksik kanal kesfi",
         present("madsc_akilli_kesif.py", "yeni_kanal_tara.py"),
         ["Kesif adaylari kullanici onayi olmadan listeye aktarilmaz."]),
    task(7, "Gunluk kanal saglik raporu",
         present("scripts/central_run_status.py"),
         ["Gunluk zamanlama ve saglik raporu ciktisi dogrulanmali."]),
    task(8, "Onemli ariza ve guvenilir yeni aday uyarilari",
         present("scripts/central_run_status.py"),
         ["Uyari esikleri ve gercek bildirim teslimi dogrulanmali."]),
]

tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, text=True,
                         capture_output=True, check=False)
report = {"version": 2, "source_issue": "https://github.com/Madsc55/madsc-tv/issues/2", "total": len(records), "workflow_count": len(workflows),
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
