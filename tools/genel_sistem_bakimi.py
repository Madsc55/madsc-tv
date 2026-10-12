#!/usr/bin/env python3
"""Non-destructive weekly system health check."""
import json
from datetime import datetime, timezone
from pathlib import Path

paths={
 "discovery":"madsc_kesif/ozet.json",
 "triple_verification":"madsc_dogrulama/summary.json",
 "final_verification":"madsc_son_kontrol/summary.json",
 "wide_scan_state":"madsc_genis_tarama/state.json",
}
checks={}
for key,name in paths.items():
    p=Path(name)
    try:
        data=json.loads(p.read_text(encoding="utf-8"))
        checks[key]={"status":"OK","path":name,"bytes":p.stat().st_size,"snapshot":data.get("zaman",data.get("generated_utc","")) if isinstance(data,dict) else ""}
    except FileNotFoundError:
        checks[key]={"status":"MISSING","path":name}
    except (ValueError,OSError) as exc:
        checks[key]={"status":"INVALID","path":name,"error":str(exc)[:120]}
required=["AGENTS.md","DEVAM_NOTU.md","CALISANLAR.m3u","madsc_akilli_kesif.py"]
for name in required:
    checks[name]={"status":"OK" if Path(name).is_file() else "MISSING"}
report={"generated_utc":datetime.now(timezone.utc).isoformat(),"mode":"READ_ONLY","checks":checks,"problems":[name for name,v in checks.items() if v["status"]=="INVALID" or (v["status"]=="MISSING" and name!="wide_scan_state")],"note":"No playlists, logos, EPG, test state or channel URLs were changed."}
out=Path("madsc_bakim");out.mkdir(exist_ok=True)
(out/"weekly_health.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,ensure_ascii=False))
