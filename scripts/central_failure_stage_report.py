#!/usr/bin/env python3
"""GitHub Actions hata asamasini job/step kanitindan ozetle; log kok nedeni uydurma."""
import json
from pathlib import Path

OUT = Path("madsc_merkezi_denetim")
runs = json.loads((OUT / "son_100_kosu.json").read_text(encoding="utf-8"))
jobs = json.loads((OUT / "basarisiz_kosu_isleri.json").read_text(encoding="utf-8"))
by_id = {str(item["run_id"]): item for item in jobs}
records = []
for run in runs:
    if run.get("conclusion") not in ("failure", "timed_out", "startup_failure", "action_required"):
        continue
    run_id = str(run.get("run_id"))
    evidence = by_id.get(run_id, {})
    failed = []
    for job in evidence.get("jobs", []):
        if job.get("conclusion") not in ("failure", "timed_out", "startup_failure", "action_required"):
            continue
        steps = [{"name": step.get("name"), "conclusion": step.get("conclusion")}
                 for step in job.get("steps", []) if step.get("conclusion") in ("failure", "timed_out")]
        failed.append({"job": job.get("name"), "conclusion": job.get("conclusion"), "failed_steps": steps})
    records.append({"run_id": run.get("run_id"), "workflow": run.get("name"),
                    "conclusion": run.get("conclusion"), "url": run.get("html_url"),
                    "failed_jobs": failed,
                    "evidence_status": evidence.get("status", "JOB_KANITI_YOK"),
                    "root_cause": "LOG_INCELEMESI_GEREKLI"})
report = {"failed_runs_in_sample": len(records), "runs": records,
          "limitations": "Job ve step bilgisi hatanin asamasini verir; log incelenmeden kok neden tespit edilmez. Son 100 kosu ornegidir."}
(OUT / "hata_asama_raporu.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"{len(records)} basarisiz kosunun hata asamalari raporlandi.")
