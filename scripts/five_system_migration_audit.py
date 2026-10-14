#!/usr/bin/env python3
"""MADSC five-workflow migration audit. Read-only; never edits playlists or workflows."""
import argparse
import json
import re
from pathlib import Path

CATEGORIES = ("guvenlik", "kesif", "test", "arsiv", "bakim")
PROTECTED = ("CALISANLAR.m3u", "YABANCI_KANALLAR.m3u", "DEVAM_NOTU.md")
def inspect(root):
    paths = sorted((root / ".github" / "workflows").glob("*.y*ml"))
    rows = []
    for p in paths:
        s = p.read_text(encoding="utf-8")
        name = re.search(r"^name:\s*(.+)$", s, re.M)
        cron = re.findall(r"^\s*-\s*cron:\s*['\"]?([^'\"\n#]+)", s, re.M)
        triggers = [k for k in ("schedule", "push", "workflow_run", "workflow_dispatch", "repository_dispatch", "workflow_call") if re.search(r"^\s*"+k+r"\s*:", s, re.M)]
        rows.append({"file":p.name, "name":name.group(1).strip() if name else p.name,
                     "triggers":triggers, "cron":cron,
                     "contents_write":bool(re.search(r"^\s*contents:\s*write\s*$",s,re.M)),
                     "actions_write":bool(re.search(r"^\s*actions:\s*write\s*$",s,re.M)),
                     "dispatch_targets":sorted(set(re.findall(r"actions/workflows/([^/\s\"']+)/dispatches",s))),
                     "references_protected": [x for x in PROTECTED if x in s]})
    names = {r["file"] for r in rows}
    unresolved = [{"source":r["file"],"target":t} for r in rows for t in r["dispatch_targets"] if t not in names]
    scheduled = [r for r in rows if "schedule" in r["triggers"]]
    return {"workflow_count":len(rows), "scheduled_count":len(scheduled),
            "scheduled_files":[r["file"] for r in scheduled],
            "push_count":sum("push" in r["triggers"] for r in rows),
            "workflow_run_count":sum("workflow_run" in r["triggers"] for r in rows),
            "manual_count":sum("workflow_dispatch" in r["triggers"] for r in rows),
            "write_permission_count":sum(r["contents_write"] for r in rows),
            "unresolved_dispatch_targets":unresolved,
            "workflows":rows, "migration_complete":False,
            "note":"Static evidence only. Five workflows alone do not prove feature parity, safe backups, live channels, or IBO approval."}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[1])
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    report=inspect(args.root)
    result=json.dumps(report,ensure_ascii=False,indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(result+"\n",encoding="utf-8")
    print(result)
    # Static inventory cannot certify behavior parity.
if __name__=="__main__":
    main()
