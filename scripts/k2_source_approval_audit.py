#!/usr/bin/env python3
"""K2 source-approval gate. Never infer approval from reachability."""
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "k2_kaynak_onaylari.json"
SCANNER = ROOT / "madsc_akilli_kesif.py"

def declared_sources():
    tree = ast.parse(SCANNER.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "SOURCES" for t in node.targets):
            sources = ast.literal_eval(node.value)
            if not isinstance(sources, dict):
                raise ValueError("SOURCES must be a mapping")
            return sources
    raise ValueError("SOURCES not found")

def audit():
    sources = declared_sources()
    doc = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if doc.get("schema_version") != 1:
        raise ValueError("unsupported schema_version")
    entries = doc.get("sources", {})
    if not isinstance(entries, dict):
        raise ValueError("sources must be a mapping")
    approved = []
    pending = []
    errors = []
    for source_id, url in sources.items():
        entry = entries.get(source_id)
        if entry is None:
            pending.append(source_id)
            continue
        if not isinstance(entry, dict):
            errors.append(source_id + ": invalid entry")
            continue
        if entry.get("url") != url:
            errors.append(source_id + ": URL mismatch")
            continue
        if entry.get("status") == "ONAYLI":
            if not all(isinstance(entry.get(k), str) and entry[k].strip() for k in ("approved_by", "approved_at", "evidence")):
                errors.append(source_id + ": approval evidence missing")
            else:
                approved.append(source_id)
        elif entry.get("status") == "BEKLIYOR":
            pending.append(source_id)
        else:
            errors.append(source_id + ": invalid status")
    for source_id in entries.keys() - sources.keys():
        errors.append(source_id + ": no longer declared")
    return {"declared": len(sources), "approved": len(approved), "pending": len(pending),
            "approved_ids": sorted(approved), "pending_ids": sorted(pending),
            "errors": sorted(errors), "approval_complete": not pending and not errors}

if __name__ == "__main__":
    result = audit()
    print(json.dumps({k: v for k, v in result.items() if k != "pending_ids"}, ensure_ascii=False, indent=2))
    if result["errors"]:
        raise SystemExit(1)
