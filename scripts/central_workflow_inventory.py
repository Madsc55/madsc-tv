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
