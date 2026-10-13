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
