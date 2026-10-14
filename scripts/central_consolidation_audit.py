#!/usr/bin/env python3
"""Tek değişiklikte yinelenen push koşularını ve beş aşama kabul kanıtını ölç."""
from fnmatch import fnmatchcase
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "madsc_merkezi_denetim"
SCENARIOS = {
    "Kanal silme veya ekleme": ["CALISANLAR.m3u", "DEVAM_NOTU.md"],
    "Kanal listesi": ["CALISANLAR.m3u"],
    "Proje notu": ["DEVAM_NOTU.md"],
    "Merkezi kod değişikliği": ["scripts/central_management_summary.py"],
    "Logo hazırlığı": ["scripts/candidate_logo_report.py"],
    "Ana liste ve logo birlikte": ["CALISANLAR.m3u", "scripts/candidate_logo_report.py"],
    "Korunan liste ve belge birlikte": ["CALISANLAR.m3u", "AGENTS.md", "DEVAM_NOTU.md"],
}

def push_rules(raw):
    # YAML'in en üst seviyesindeki on: bölümünü, push alt bölümünü ayır.
    event = re.search(r"(?m)^on:\s*\n(.*?)(?=^[^\s#][^\n]*:\s*(?:\n|$)|\Z)", raw, re.S)
    if not event:
        return None
    push = re.search(r"(?m)^  push:\s*(?:\n(.*?)(?=^  [a-zA-Z_][^\n]*:\s*(?:\n|$)|\Z))", event.group(1), re.S)
    if not push:
        return None
    section = push.group(1) or ""
    found = []
    within_paths = False
    for line in section.splitlines():
        if re.match(r"^    paths:\s*$", line):
            within_paths = True
            continue
        if re.match(r"^    [\w-]+:", line):
            within_paths = False
        if within_paths:
            match = re.match(r"^      -\s*['\"]?([^'\"\s]+)", line)
            if match:
                found.append(match.group(1))
    if not found:
        ignored = []
        inside_ignore = False
        for line in section.splitlines():
            if re.match(r"^    paths-ignore:\s*$", line):
                inside_ignore = True
                continue
            if re.match(r"^    [\w-]+:", line):
                inside_ignore = False
            if inside_ignore:
                match = re.match(r"^      -\s*['\"]?([^'\"\s]+)", line)
                if match:
                    ignored.append("!" + match.group(1))
        return ["**"] + ignored
    return found

def matches(path, rules):
    state = False
    for pattern in rules:
        negative = pattern.startswith("!")
        glob = pattern[1:] if negative else pattern
        if glob == "**" or fnmatchcase(path, glob):
            state = not negative
    return state

def analyze(workflows, scenarios=SCENARIOS):
    rules = {}
    for name, content in workflows.items():
        selected = push_rules(content)
        if selected is not None:
            rules[name] = selected
    cases = []
    for label, paths in scenarios.items():
        triggered = sorted(name for name, patterns in rules.items()
                           if any(matches(path, patterns) for path in paths))
        cases.append({"islem": label, "dosyalar": paths, "push_is_akislari": triggered,
                      "ayri_kosu_sayisi": len(triggered),
                      "tek_merkez_hedefi_saglandi": len(triggered) <= 1})
    return {"incelenen_is_akisi": len(workflows), "push_tetikleyicili": len(rules),
            "senaryolar": cases, "tekrarli_senaryolar": [c["islem"] for c in cases if not c["tek_merkez_hedefi_saglandi"]],
            "sinir": "Dosya ve push filtresi statik analizi; workflow_run, schedule ve manuel koşular ayrı değerlendirilmelidir.",
            "otomatik_kanal_degisikligi": False}

def acceptance(folder):
    def load(name):
        try:
            return json.loads((folder / name).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
    stages = load("bes_asama_tum_workflow_eslestirmesi.json") or {}
    health = load("ana_liste_saglik_kosu_kaniti.json") or {}
    runs = load("son_100_kosu.json")
    protected = load("protected-write-gate-report.json")
    duplicates = load("tek_islem_coklu_push_analizi.json")
    criteria = [
        {"alan": "Beş aşama workflow envanteri", "kanit": "bes_asama_tum_workflow_eslestirmesi.json",
         "durum": "ENVANTER_VAR_KAPSAM_ONAYSIZ" if stages.get("mapped_count") and not stages.get("unmapped") else "KANIT_EKSIK"},
        {"alan": "Ana liste canlı yayın kontrolü", "kanit": "ana_liste_saglik_kosu_kaniti.json",
         "durum": "KOSU_BASARILI_TUM_KANALLAR_ONAYSIZ" if health.get("durum") == "IS_AKISI_BASARILI_KANAL_SONUCU_INCELENMELI" else "KANIT_EKSIK"},
        {"alan": "GitHub çalışma geçmişi", "kanit": "son_100_kosu.json",
         "durum": "SON_100_KOSU_VAR" if isinstance(runs, list) and runs else "KANIT_EKSIK"},
        {"alan": "Korunan liste yazma kapısı", "kanit": "protected-write-gate-report.json",
         "durum": ("DENETIM_VAR_MANUEL_INCELEME_GEREKLI"
                   if isinstance(protected, dict) and protected.get("workflows_scanned", 0) > 0
                   and not protected.get("errors") else "KANIT_EKSIK_VEYA_HATALI")},
        {"alan": "Tek işlem / tek merkezi push hedefi", "kanit": "tek_islem_coklu_push_analizi.json",
         "durum": ("TEKRARLI_PUSH_VAR" if isinstance(duplicates, dict)
                   and duplicates.get("tekrarli_senaryolar")
                   else "STATIK_KONTROL_TEMIZ_KAPSAM_ONAYSIZ" if isinstance(duplicates, dict)
                   and isinstance(duplicates.get("senaryolar"), list)
                   and duplicates["senaryolar"] else "KANIT_EKSIK")},
        {"alan": "IBO Player gerçek cihaz kabulü", "kanit": "Kullanıcının IBO test sonuçları", "durum": "KULLANICI_ONAYI_BEKLENIYOR"},
        {"alan": "18 geliştirme ve 26 kuralın uçtan uca doğrulanması", "kanit": "Tam uygulama ve güvenlik testleri", "durum": "UCA_UCA_KANIT_EKSIK"},
    ]
    return {"genel_kabul": "HENUZ_ONAYLANMADI", "kriterler": criteria,
            "aciklama": "Yeşil Actions testi, tüm IPTV sisteminin çalıştığına veya kullanıcının cihazda onayladığına eşit değildir."}

def main():
    workflows = {p.name: p.read_text(encoding="utf-8") for p in
                 (ROOT / ".github/workflows").glob("*.y*ml")}
    OUT.mkdir(exist_ok=True)
    overlap = analyze(workflows)
    (OUT / "tek_islem_coklu_push_analizi.json").write_text(
        json.dumps(overlap, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    result = acceptance(OUT)
    (OUT / "bes_asama_kabul_kapisi.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["## Tek işlem / çoklu test denetimi",
             f"- İncelenen workflow: {overlap['incelenen_is_akisi']}",
             f"- Birden fazla push açabilecek senaryo: {len(overlap['tekrarli_senaryolar'])}",
             "| İşlem | Ayrı push koşusu | Durum |", "|---|---:|---|"]
    for case in overlap["senaryolar"]:
        lines.append(f"| {case['islem']} | {case['ayri_kosu_sayisi']} | {'TEKRAR VAR' if not case['tek_merkez_hedefi_saglandi'] else 'UYGUN'} |")
    lines.extend(["", "### Tetiklenen ayrı workflow dosyaları"])
    for case in overlap["senaryolar"]:
        if not case["tek_merkez_hedefi_saglandi"]:
            lines.append("- " + case["islem"] + ": " + ", ".join(case["push_is_akislari"]))
    lines.extend(["", "## Beş aşama genel kabul", "- Durum: HENUZ_ONAYLANMADI"])
    for item in result["kriterler"]:
        lines.append(f"- {item[\'alan\']}: {item[\'durum\']}")
    lines.extend(["",
                  "- Kabul için gerçek yayın, geçmiş, güvenlik ve IBO cihaz kanıtları gereklidir.",
                  "- Hiçbir kanal otomatik değiştirilmedi."])
    (OUT / "toplu_tetikleme_ve_kabul_ozeti.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))

if __name__ == "__main__":
    main()
