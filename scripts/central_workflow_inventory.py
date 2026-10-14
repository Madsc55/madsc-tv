#!/usr/bin/env python3
"""Salt okunur GitHub Actions envanteri; hiçbir iş akışını tetiklemez."""
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
items = []
for path in sorted((root / ".github/workflows").glob("*")):
    if path.suffix not in (".yml", ".yaml"):
        continue
    raw = path.read_text(encoding="utf-8")
    cron = re.findall(r"^\s*-\s*cron:\s*['\"]?([^'\"\n#]+)", raw, re.M)
    items.append({
        "file": path.name,
        "name": next((x.strip().strip("'\"") for x in re.findall(r"^name:\s*(.+)$", raw, re.M)), path.name),
        "schedule_utc": [x.strip() for x in cron],
        "manual": bool(re.search(r"^\s*workflow_dispatch\s*:", raw, re.M)),
        "push": bool(re.search(r"^\s*push\s*:", raw, re.M)),
        "workflow_run": bool(re.search(r"^\s*workflow_run\s*:", raw, re.M)),
        "writes_contents": bool(re.search(r"^\s*contents:\s*write\s*$", raw, re.M)),
        "has_concurrency": bool(re.search(r"^concurrency\s*:", raw, re.M)),
        "concurrency_group": next(iter(re.findall(r"^\s*group:\s*(.+)$", raw, re.M)), "").strip().strip("\'\\\""),
    })
out = root / "madsc_merkezi_denetim"
out.mkdir(exist_ok=True)
(out / "otomasyon_haritasi.json").write_text(
    json.dumps({"workflow_count": len(items), "scheduled_count": sum(bool(x["schedule_utc"]) for x in items),
                "workflows": items, "note": "Statik envanterdir; etkinlik, başarı ve çakışma kanıtı değildir."},
               ensure_ascii=False, indent=2), encoding="utf-8")
print(f"{len(items)} workflow envantere alındı; hiçbiri değiştirilmedi veya tetiklenmedi.")

# Sadece olasi cakismalari raporla; zamanlama degistirme.
from collections import defaultdict

cron_groups = defaultdict(list)
for item in items:
    for cron in item["schedule_utc"]:
        cron_groups[cron].append(item["file"])
same_cron = [{"cron": cron, "workflows": names} for cron, names in sorted(cron_groups.items()) if len(names) > 1]
write_scheduled = [x["file"] for x in items if x["writes_contents"] and x["schedule_utc"]]
analysis = {
    "identical_cron_groups": same_cron,
    "scheduled_write_workflows": write_scheduled,
    "manual_review_required": True,
    "note": "Ayni cron kesin cakisma degildir; farkli cronlar da cakisma yaratabilir. Statik on inceleme.",
}
(out / "otomasyon_cakisma_on_analizi.json").write_text(
    json.dumps(analysis, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"{len(same_cron)} ayni cron grubu ve {len(write_scheduled)} zamanlanmis yazma izinli workflow belirlendi.")

# Eszamanlilik grup adlarini ve saat/dakika bazli olasi yogunlugu incele.
concurrency_groups = defaultdict(list)
minute_groups = defaultdict(list)
for item in items:
    group = item["concurrency_group"]
    if group:
        concurrency_groups[group].append(item["file"])
    for cron in item["schedule_utc"]:
        fields = cron.split()
        if len(fields) == 5 and fields[0].isdigit() and fields[1].isdigit():
            minute_groups[(int(fields[1]), int(fields[0]))].append(item["file"])
shared_groups = [{"group": key, "workflows": names} for key, names in sorted(concurrency_groups.items()) if len(names) > 1]
same_clock = [{"utc": f"{hour:02d}:{minute:02d}", "workflows": names}
              for (hour, minute), names in sorted(minute_groups.items()) if len(names) > 1]
(out / "otomasyon_es_zamanlilik_raporu.json").write_text(
    json.dumps({"shared_concurrency_groups": shared_groups, "same_utc_clock": same_clock,
                "note": "Farkli gunlerdeki cronlar ayni saate denk gelebilir; bu sadece on incelemedir. Dinamik grup ifadeleri birebir eslesme kaniti degildir.",
                "changes_applied": False}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"{len(shared_groups)} ortak concurrency ifadesi ve {len(same_clock)} ortak UTC saat grubu raporlandi.")

# Toplu risk siralamasi ve mevcut islerin bagimlilik/koruma siniflandirmasi.
def classify(item):
    name = (item["file"] + " " + item["name"]).lower()
    # Ana liste canlı yayın sağlık kontrolü güvenlik denetimi değil, 3. aşamadır.
    if item["file"] == "madsc-ana-liste-saglik.yml":
        return "ADAY_TEST"
    if any(k in name for k in ("yedek", "kurtarma", "backup")):
        return "YEDEK_VE_KURTARMA"
    if any(k in name for k in ("saglik", "sağlık", "guvenlik", "güvenlik", "safety", "protected", "write-gate", "rule24")):
        return "GUVENLIK"
    if "epg" in name:
        return "EPG"
    if "logo" in name or "png" in name:
        return "LOGO"
    if any(k in name for k in ("kesif", "keşif", "tarama", "kaynak", "discovery")):
        return "KESIF"
    if any(k in name for k in ("dogrulama", "doğrulama", "son-kontrol", "test", "aday")):
        return "ADAY_TEST"
    return "DIGER"

priority = []
for item in items:
    category = classify(item)
    reasons = []
    if item["writes_contents"] and item["schedule_utc"]:
        reasons.append("ZAMANLANMIS_YAZMA_YETKISI")
    if item["concurrency_group"] and any(
        len(names) > 1 and item["file"] in names for names in concurrency_groups.values()
    ):
        reasons.append("ORTAK_CONCURRENCY_IFADESI")
    if any(item["file"] in x["workflows"] for x in same_cron):
        reasons.append("AYNI_CRON_IFADESI")
    if item["writes_contents"] and not item["has_concurrency"]:
        reasons.append("YAZMA_IZNI_CONCURRENCY_YOK")
    level = "YUKSEK" if ("ZAMANLANMIS_YAZMA_YETKISI" in reasons and len(reasons) > 1) else (
        "ORTA" if reasons else "BILGI")
    priority.append({"file": item["file"], "category": category, "risk": level, "reasons": reasons,
                     "review_only": True})
priority.sort(key=lambda x: ({"YUKSEK": 0, "ORTA": 1, "BILGI": 2}[x["risk"]], x["file"]))
critical = [x for x in priority if x["category"] in ("YEDEK_VE_KURTARMA", "GUVENLIK", "EPG", "KESIF")]
(out / "merkezi_oncelik_ve_koruma_raporu.json").write_text(json.dumps({
    "workflows_checked": len(priority),
    "high_risk": sum(x["risk"] == "YUKSEK" for x in priority),
    "medium_risk": sum(x["risk"] == "ORTA" for x in priority),
    "critical_existing_workflows": critical,
    "all_workflows": priority,
    "safety": {"protected_playlists_modified": False, "schedules_modified": False,
               "workflows_triggered": False},
    "limitations": ["Statik kod incelemesi; gercek eszamanlilik veya lisans/IBO testi degildir.",
                    "Workflow isimlerinden kategori tahmini yapilir; elle inceleme gerekir.",
                    "Mevcut kesif, EPG, yedek ve guvenlik otomasyonlari kapatilmaz."]
}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Merkezi oncelik raporu: {len(priority)} is akisi, {sum(x['risk']=='YUKSEK' for x in priority)} yuksek on inceleme.")

# Bes asamali ana sistem: her mevcut workflow tam bir ana asamaya baglanir.
# Bu salt okunur eslestirme; mevcut tetikleyicileri ve izinleri degistirmez.
def five_stage(item):
    category = classify(item)
    if category in ("YEDEK_VE_KURTARMA", "GUVENLIK"):
        return 1
    if category == "KESIF":
        return 2
    if category == "ADAY_TEST":
        return 3
    if category in ("LOGO", "EPG"):
        return 4
    return 5

# Kritik kaynaklar dosya adina gore yanlis siniflanabilir. Bunlari raporda
# acikca manuel kapsam denetimine isaretle; eksiksizlik iddiasi kurma.
ambiguous_workflows = [
    item["file"] for item in items
    if classify(item) == "DIGER" or (
        any(token in item["file"].lower() for token in ("epg", "logo", "kaynak", "backup", "yedek"))
        and five_stage(item) == 5
    )
]

stage_names = {
    1: "Guvenlik ve sistem sagligi",
    2: "Kanal kesfi ve kaynak guvenilirligi",
    3: "Toplu yayin testleri",
    4: "Logo EPG ve kanal kimligi",
    5: "Sonuclar saglik raporlari ve uyarilar",
}
stage_workflows = {str(n): [] for n in range(1, 6)}
for item in items:
    stage_workflows[str(five_stage(item))].append(item["file"])
mapped = sorted(name for names in stage_workflows.values() for name in names)
expected = sorted(item["file"] for item in items)
if mapped != expected or len(mapped) != len(set(mapped)):
    raise RuntimeError("Bes asama eslestirmesinde eksik veya tekrar eden workflow var.")
(out / "bes_asama_tum_workflow_eslestirmesi.json").write_text(
    json.dumps({
        "version": 1,
        "workflow_count": len(items),
        "mapped_count": len(mapped),
        "unmapped": [],
        "manual_scope_review_required": ambiguous_workflows,
        "complete_historical_coverage_verified": False,
        "stages": [{"number": n, "name": stage_names[n],
                    "workflows": stage_workflows[str(n)]} for n in range(1, 6)],
        "limitations": [
            "Dosya adi ve mevcut kategoriye gore otomatik eslestirme; elle kapsam kontrolu gerekir.",
            "Eski workflowlar kapatilmadi veya birlestirilmedi.",
            "Gercek Actions basarisi, gecmis is kapsami veya cihaz testi kaniti degildir."
        ]
    }, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"{len(mapped)} workflow bes asamaya eksiksiz ve tekrarsiz eslestirildi; tetikleyici degismedi.")

# Kullanici icin tek ekranda kesin tetikleyici sayimi. Her tetikleyici
# bagimsiz sayilir: bir workflow hem schedule hem push icerebilir.
trigger_counts = {
    "total_workflow_files": len(items),
    "scheduled_workflows": sum(bool(x["schedule_utc"]) for x in items),
    "cron_entries": sum(len(x["schedule_utc"]) for x in items),
    "push_workflows": sum(x["push"] for x in items),
    "workflow_run_workflows": sum(x["workflow_run"] for x in items),
    "manual_workflows": sum(x["manual"] for x in items),
    "scheduled_and_push": sum(bool(x["schedule_utc"]) and x["push"] for x in items),
    "not_scheduled": sum(not x["schedule_utc"] for x in items),
}
(out / "otomasyon_kesin_tetikleyici_sayimi.json").write_text(
    json.dumps({"counts": trigger_counts,
                "scheduled": [{"file": x["file"], "cron_utc": x["schedule_utc"]}
                              for x in items if x["schedule_utc"]],
                "push": [x["file"] for x in items if x["push"]],
                "workflow_run": [x["file"] for x in items if x["workflow_run"]],
                "notes": ["Bir dosyada birden cok tetikleyici olabilir; sayilar toplanmaz.",
                          "Bu dosya statik envanterdir, Actions run sayisi degildir.",
                          "Mevcut dosyalarin hicbiri silinmedi veya calistirilmadi."]},
               ensure_ascii=False, indent=2), encoding="utf-8")
print("MADSC tetikleyici envanteri:", trigger_counts)

