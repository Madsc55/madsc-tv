#!/usr/bin/env python3
"""Actions durumunu salt okunur siniflandir; eksik kaniti basari sayma."""
import json
from datetime import datetime, timezone
from pathlib import Path

folder = Path("madsc_merkezi_denetim")
workflows = [json.loads(line) for line in (folder / "github_workflow_durumlari.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
runs = json.loads((folder / "son_100_kosu.json").read_text(encoding="utf-8"))
latest = {}
for run in sorted(runs, key=lambda x: x.get("created_at") or "", reverse=True):
    key = run.get("workflow_id")
    if key is not None and key not in latest:
        latest[key] = run
rows = []
for flow in workflows:
    last = latest.get(flow["id"])
    status = "SON_100_KOSUDA_YOK"
    if last:
        if last.get("status") != "completed":
            status = "DEVAM_EDIYOR"
        elif last.get("conclusion") == "success":
            status = "BASARILI"
        elif last.get("conclusion") in ("failure", "timed_out", "action_required", "startup_failure"):
            status = "BASARISIZ"
        else:
            status = "DIGER_SONUC"
    rows.append({"name": flow["name"], "path": flow["path"], "workflow_state": flow["state"],
                 "classification": status, "last_run": last,
                 "note": "Son 100 kosu disinda kalan islerin durumu bilinmiyor." if not last else ""})
result = {"generated_at_utc": datetime.now(timezone.utc).isoformat(), "sample_size": len(runs),
          "workflow_count": len(rows), "classifications": {
              name: sum(x["classification"] == name for x in rows)
              for name in ("BASARILI", "BASARISIZ", "DEVAM_EDIYOR", "DIGER_SONUC", "SON_100_KOSUDA_YOK")},
          "workflows": rows, "limitations": "Son 100 kosu ile sinirli; gorunmeyen workflow bozuk demek degildir."}
(folder / "is_akisi_son_durum_siniflandirma.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"{len(rows)} is akisi son 100 kosuya gore siniflandirildi.")
