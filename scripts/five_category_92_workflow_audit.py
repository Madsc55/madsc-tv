#!/usr/bin/env python3
"""Read-only 92-workflow task inventory; never dispatches, edits, or disables workflows."""
from __future__ import annotations
import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {
    1: ("Guvenlik", ("guvenlik", "safety", "protected", "write-gate", "write-path", "rule24", "security", "butunluk")),
    2: ("Kanal kesfi", ("kesif", "arama", "tarama", "kaynak", "discovery", "source", "candidate", "aday")),
    3: ("Kanal testleri", ("ffprobe", "ffmpeg", "stream", "kanal", "test", "epg", "logo", "png", "ibo", "kalite", "quality", "playback")),
    4: ("Arsiv ve yedek", ("yedek", "backup", "arsiv", "archive", "restore", "kurtarma", "geri-yukle")),
    5: ("Genel bakim", ("rapor", "report", "denetim", "audit", "kontrol", "maintenance", "otomatik-devam", "vod", "guncelle")),
}
# Prefer a workflow's explicit subject; preserve cross-category dependencies as secondary tags.
def classify(filename, commands):
    title = filename.lower()
    if any(k in title for k in ("yedek", "arsiv", "kurtarma", "restore", "backup")):
        primary = 4
    elif any(k in title for k in ("guvenlik", "safety", "protected", "write-", "rule24", "butunluk")):
        primary = 1
    elif any(k in title for k in ("kesif", "arama", "tarama", "kaynak")):
        primary = 2
    elif any(k in title for k in ("epg", "logo", "png", "kanal", "aday", "test", "ibo", "kararlilik")):
        primary = 3
    else:
        primary = 5
    text = (title + " " + " ".join(commands)).lower()
    tags = sorted(set([primary] + [n for n, (_, keys) in CATEGORIES.items() if any(k in text for k in keys)]))
    return primary, tags

def inspect(root=ROOT):
    folder = root / ".github" / "workflows"
    items = []
    new_category_files = {f"madsc-0{n}-" for n in range(1, 6)}
    for path in sorted(folder.glob("*.y*ml")):
        if path.name == "k1-protected-write-tests.yml":
            continue  # New K1 security CI, not one of the original 92 legacy workflows.
        if any(path.name.startswith(prefix) for prefix in new_category_files):
            continue  # Five new category workflows are not among the original 92.
        raw = path.read_text(encoding="utf-8")
        commands = list(dict.fromkeys(re.findall(r"(?:(?:python3?|bash|sh)\s+(?:-m\s+\w+\s+)?)([\w./-]+\.(?:py|sh))", raw)))
        uses = list(dict.fromkeys(re.findall(r"^\s+-?\s*uses:\s*([^\s#]+)", raw, re.M)))
        cron = [x.strip() for x in re.findall(r"^\s+-\s*cron:\s*['\"]?([^'\"\n#]+)", raw, re.M)]
        primary, tags = classify(path.name, commands)
        push_commands = re.findall(r"\bgit\s+(?:(?:-c|--config)\s+\S+\s+|(?:-[A-Za-z]+|--[\w-]+(?:=\S+)?)\s+)*push\b[^\n;&|]*", raw)
        force_push_commands = [cmd for cmd in push_commands if re.search(r"(?:--force(?:-with-lease)?\b|\s-f(?:\s|$))", cmd)]
        push_signal_lines = [line.strip()[:240] for line in raw.splitlines() if re.search(r"\bgit\s+(?:(?:-c|--config)\s+\S+\s+|(?:-[A-Za-z]+|--[\w-]+(?:=\S+)?)\s+)*push\b", line)]
        outputs = list(dict.fromkeys(re.findall(r"(?:(?:path|name):\s*)([\w./*-]+(?:\.json|\.md|\.zip|/))", raw)))
        items.append({
            "file": path.name, "primary_category": primary, "related_categories": tags,
            "cron_utc": cron, "manual": bool(re.search(r"^\s*workflow_dispatch:", raw, re.M)),
            "push": bool(re.search(r"^\s*push:", raw, re.M)),
            "workflow_run": bool(re.search(r"^\s*workflow_run:", raw, re.M)),
            "workflow_call": bool(re.search(r"^\s*workflow_call:", raw, re.M)),
            "contents_write": bool(re.search(r"^\s*contents:\s*write\s*$", raw, re.M)),
            "commands": commands, "actions": uses, "output_hints": outputs,
            "git_push_command_count": len(push_commands),
            "push_signal_lines": push_signal_lines,
            "force_push_command_count": len(force_push_commands),
            "multiple_push_command_signal": len(push_commands) > 1,
            "requires_manual_behavior_review": True,
        })
    if len(items) != 92:
        raise SystemExit(f"Legacy inventory mismatch: expected 92, found {len(items)}; review before migration")
    category_paths = sorted(path for path in folder.glob("*.y*ml")
                            if any(path.name.startswith(prefix) for prefix in new_category_files))
    new_commands = {}
    for category_path in category_paths:
        category_raw = category_path.read_text(encoding="utf-8")
        new_commands[category_path.name] = set(re.findall(
            r"(?:(?:python3?|bash|sh)\s+(?:-m\s+\w+\s+)?)([\w./-]+\.(?:py|sh))",
            category_raw))
    for item in items:
        item["shared_script_entrypoints"] = sorted(
            cmd for cmd in item["commands"]
            if any(cmd in scripts for scripts in new_commands.values()))
        item["unmatched_script_entrypoints"] = sorted(
            set(item["commands"]) - set(item["shared_script_entrypoints"]))
        item["missing_legacy_script_files"] = sorted(cmd for cmd in item["commands"] if not (root / cmd).is_file())
        item["script_entrypoint_coverage_ratio"] = (
            round(len(item["shared_script_entrypoints"]) / len(set(item["commands"])), 3)
            if item["commands"] else None
        )
        item["possible_replacement_workflows"] = sorted(
            name for name, scripts in new_commands.items()
            if set(item["commands"]) & scripts)
        # Review triage only: this is evidence of shared entrypoints, NOT task migration.
        if not item["commands"]:
            item["integration_evidence_level"] = "NO_EXTRACTED_SCRIPT_REVIEW_INLINE_ACTIONS"
        elif item["unmatched_script_entrypoints"]:
            item["integration_evidence_level"] = "PARTIAL_OR_MISSING_SCRIPT_COVERAGE"
        else:
            item["integration_evidence_level"] = "SCRIPT_NAMES_MATCH_ONLY"
        item["unverified_trigger_behavior"] = bool(
            item["cron_utc"] or item["push"] or item["workflow_run"] or item["workflow_call"]
        )
        # Concrete migration checklist: do not mistake a script-name match for
        # trigger, write permission, or downstream publication parity.
        item["migration_gap_reasons"] = (
            (["INLINE_OR_ACTION_BEHAVIOR_UNREVIEWED"] if not item["commands"] else [])
            + (["UNMATCHED_SCRIPT_ENTRYPOINTS"] if item["unmatched_script_entrypoints"] else [])
            + (["MISSING_LEGACY_SCRIPT_FILE"] if item["missing_legacy_script_files"] else [])
            + (["AUTOMATIC_TRIGGER_NOT_REPLACED"] if item["unverified_trigger_behavior"] else [])
            + (["WRITE_SIDE_EFFECTS_UNVERIFIED"] if item["contents_write"] else [])
            + (["MULTIPLE_PUSH_COMMANDS_REVIEW"] if item["multiple_push_command_signal"] else [])
            + (["FORCE_PUSH_COMMAND_REVIEW"] if item["force_push_command_count"] else [])
            + (["ARTIFACT_OUTPUTS_UNVERIFIED"] if item["output_hints"] else [])
            + ["BEHAVIORAL_EQUIVALENCE_NOT_PROVEN"]
        )
        # Explicit, auditable comparison of legacy trigger and permission signals
        # against candidate shadow replacements. This is triage, NOT parity proof.
        replacements = item["possible_replacement_workflows"]
        replacement_raw = {
            name: (folder / name).read_text(encoding="utf-8")
            for name in replacements
        }
        trigger_signals = {
            "schedule": bool(item["cron_utc"]),
            "push": item["push"],
            "workflow_run": item["workflow_run"],
            "workflow_call": item["workflow_call"],
            "manual": item["manual"],
        }
        def has_trigger(raw, trigger):
            return bool(re.search(r"^  " + re.escape(trigger) + r":", raw, re.M))
        item["trigger_coverage_signals"] = {
            trigger: {
                "legacy": enabled,
                "replacement_declares": any(has_trigger(raw, trigger) for raw in replacement_raw.values()),
            }
            for trigger, enabled in trigger_signals.items()
        }
        # A matching trigger type is not proof that schedule expressions match.
        replacement_crons = sorted(set(
            cron.strip() for raw in replacement_raw.values()
            for cron in re.findall(r"^\s+-\s*cron:\s*['\"]?([^'\"\n#]+)", raw, re.M)
        ))
        item["legacy_cron_expressions"] = sorted(set(item["cron_utc"]))
        item["replacement_cron_expressions"] = replacement_crons
        item["unmatched_cron_expressions"] = sorted(
            set(item["legacy_cron_expressions"]) - set(replacement_crons)
        )
        item["unmatched_trigger_signals"] = [
            trigger for trigger, status in item["trigger_coverage_signals"].items()
            if status["legacy"] and not status["replacement_declares"]
        ]
        item["write_permission_parity_unverified"] = item["contents_write"]
        item["required_acceptance_checks"] = [
            "COMPARE_LEGACY_AND_REPLACEMENT_JOB_STEPS",
            "VERIFY_TRIGGER_EQUIVALENCE",
            "VERIFY_OUTPUT_AND_ARTIFACT_EQUIVALENCE",
            "VERIFY_PROTECTED_PATHS_UNCHANGED",
        ] + (["VERIFY_WRITE_AUTHORIZATION_AND_ROLLBACK"] if item["contents_write"] or item["git_push_command_count"] else []) + (["VERIFY_NO_DUPLICATE_PUSH"] if item["multiple_push_command_signal"] else [])

        if item["unmatched_trigger_signals"]:
            item["migration_gap_reasons"].append("UNMATCHED_TRIGGER_SIGNALS")
        if item["unmatched_cron_expressions"]:
            item["migration_gap_reasons"].append("UNMATCHED_CRON_EXPRESSIONS")
        item["behavioral_parity_verified"] = False
    # Explicit migration gate: static script-name matches are not production parity.
    for item in items:
        item["migration_decision"] = "BLOCKED_NEEDS_BEHAVIOR_EVIDENCE"
        item["review_priority"] = (
            "HIGH" if item["contents_write"] and
            (item["cron_utc"] or item["push"] or item["workflow_run"])
            else "HIGH" if item["workflow_run"] or item["cron_utc"]
            else "NORMAL"
        )
    counts = Counter(x["primary_category"] for x in items)
    risks = [x["file"] for x in items if x["contents_write"] and (x["cron_utc"] or x["push"] or x["workflow_run"])]
    return {
        "total": len(items), "category_counts": {CATEGORIES[n][0]: counts[n] for n in CATEGORIES},
        "scheduled": sum(bool(x["cron_utc"]) for x in items),
        "cron_entries": sum(len(x["cron_utc"]) for x in items),
        "push": sum(x["push"] for x in items), "workflow_run": sum(x["workflow_run"] for x in items),
        "manual": sum(x["manual"] for x in items), "write_enabled_with_auto_trigger": risks,
        "multiple_push_workflows": [x["file"] for x in items if x["multiple_push_command_signal"]],
        "force_push_workflows": [x["file"] for x in items if x["force_push_command_count"]],
        "legacy_workflows_with_unmatched_scripts": sum(bool(x["unmatched_script_entrypoints"]) for x in items),
        "legacy_workflows_with_no_shared_script": sum(not x["shared_script_entrypoints"] for x in items),
        "legacy_workflows_with_missing_script_file": sum(bool(x["missing_legacy_script_files"]) for x in items),
        "behavioral_parity_verified_count": 0,
        "integration_evidence_counts": dict(Counter(x["integration_evidence_level"] for x in items)),
        "migration_gap_reason_counts": dict(Counter(reason for x in items for reason in x["migration_gap_reasons"])),
        "migration_blocked_count": len(items),
        "high_priority_review_count": sum(x["review_priority"] == "HIGH" for x in items),
        "items": items,
        "limitations": [
            "Classification is preliminary, based on filename and commands; manual review of behavior is mandatory.",
            "Multiple related categories do not cause the workflow to run twice.",
            "Does not prove replacement parity, production behavior, or that all 92 workflows are enabled.",
            "No legacy workflow is disabled, deleted, or dispatched."
        ],
    }

def main():
    report = inspect()
    out = ROOT / "madsc_merkezi_denetim"
    out.mkdir(exist_ok=True)
    (out / "92_workflow_gorev_ve_kategori_haritasi.json").write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    # Single, machine-readable review queue: all 92 rows, not only aggregate counts.
    with (out / "92_workflow_esdegerlik_kabul_matrisi.csv").open("w", encoding="utf-8", newline="") as f:
        columns = [
            "legacy_workflow", "primary_category", "review_priority",
            "cron_utc", "push", "workflow_run", "workflow_call", "manual",
            "contents_write", "git_push_command_count", "force_push_command_count",
            "multiple_push_command_signal", "push_signal_lines", "legacy_commands", "legacy_actions",
            "output_hints", "possible_replacement_workflows",
            "shared_script_entrypoints", "unmatched_script_entrypoints",
            "behavioral_parity_verified", "migration_decision",
            "integration_evidence_level", "unverified_trigger_behavior",
            "migration_gap_reasons", "missing_legacy_script_files",
            "unmatched_trigger_signals", "write_permission_parity_unverified",
            "required_acceptance_checks", "script_entrypoint_coverage_ratio",
            "unmatched_cron_expressions",
        ]
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for item in report["items"]:
            writer.writerow({
                "legacy_workflow": item["file"],
                "primary_category": CATEGORIES[item["primary_category"]][0],
                "review_priority": item["review_priority"],
                "cron_utc": "; ".join(item["cron_utc"]),
                "push": item["push"],
                "workflow_run": item["workflow_run"],
                "workflow_call": item["workflow_call"],
                "manual": item["manual"],
                "contents_write": item["contents_write"],
                "git_push_command_count": item["git_push_command_count"],
                "force_push_command_count": item["force_push_command_count"],
                "multiple_push_command_signal": item["multiple_push_command_signal"],
                "push_signal_lines": " || ".join(item["push_signal_lines"]),
                "legacy_commands": "; ".join(item["commands"]),
                "legacy_actions": "; ".join(item["actions"]),
                "output_hints": "; ".join(item["output_hints"]),
                "possible_replacement_workflows": "; ".join(item["possible_replacement_workflows"]),
                "shared_script_entrypoints": "; ".join(item["shared_script_entrypoints"]),
                "unmatched_script_entrypoints": "; ".join(item["unmatched_script_entrypoints"]),
                "behavioral_parity_verified": item["behavioral_parity_verified"],
                "migration_decision": item["migration_decision"],
                "integration_evidence_level": item["integration_evidence_level"],
                "unverified_trigger_behavior": item["unverified_trigger_behavior"],
                "migration_gap_reasons": "; ".join(item["migration_gap_reasons"]),
                "unmatched_trigger_signals": "; ".join(item["unmatched_trigger_signals"]),
                "write_permission_parity_unverified": item["write_permission_parity_unverified"],
                "required_acceptance_checks": "; ".join(item["required_acceptance_checks"]),
                "script_entrypoint_coverage_ratio": item["script_entrypoint_coverage_ratio"],
                "unmatched_cron_expressions": "; ".join(item["unmatched_cron_expressions"]),
                "missing_legacy_script_files": "; ".join(item["missing_legacy_script_files"]),
            })
    # Five actionable queues in one artifact; no legacy workflow is mutated.
    queues = {}
    for n in CATEGORIES:
        rows = [item for item in report["items"] if item["primary_category"] == n]
        queues[CATEGORIES[n][0]] = {
            "count": len(rows),
            "high_priority": sum(x["review_priority"] == "HIGH" for x in rows),
            "workflows": [
                {"file": x["file"], "priority": x["review_priority"],
                 "missing_scripts": x["unmatched_script_entrypoints"],
                 "gap_reasons": x["migration_gap_reasons"],
                 "replacement_candidates": x["possible_replacement_workflows"]}
                for x in rows
            ],
        }
    (out / "bes_kategori_toplu_eksik_is_kuyrugu.json").write_text(
        json.dumps(queues, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # Single actionable review order across all categories.
    priority_rows = sorted(
        report["items"],
        key=lambda item: (
            item["review_priority"] != "HIGH",
            not item["workflow_run"],
            not bool(item["cron_utc"]),
            item["file"],
        ),
    )
    priority_report = {
        "total": len(priority_rows),
        "note": "Review queue only; no migration or deletion authorized.",
        "ordered_workflows": [
            {
                "file": item["file"],
                "category": CATEGORIES[item["primary_category"]][0],
                "priority": item["review_priority"],
                "gaps": item["migration_gap_reasons"],
            }
            for item in priority_rows
        ],
    }
    # Actionable high-risk queue: no workflow changes, only review evidence.
    push_review = [
        {
            "file": item["file"],
            "category": CATEGORIES[item["primary_category"]][0],
            "git_push_command_count": item["git_push_command_count"],
            "force_push_command_count": item["force_push_command_count"],
            "push_signal_lines": item["push_signal_lines"],
            "contents_write": item["contents_write"],
            "automatic_triggers": {
                "cron_utc": item["cron_utc"],
                "push": item["push"],
                "workflow_run": item["workflow_run"],
            },
            "migration_decision": item["migration_decision"],
        }
        for item in report["items"]
        if item["git_push_command_count"] or item["contents_write"]
    ]
    push_review.sort(key=lambda item: (
        -item["force_push_command_count"],
        -item["git_push_command_count"],
        not item["contents_write"],
        item["file"],
    ))
    (out / "92_workflow_yazma_risk_inceleme_kuyrugu.json").write_text(
        json.dumps({
            "total_review_items": len(push_review),
            "review_only": True,
            "no_migration_authorized": True,
            "items": push_review,
        }, ensure_ascii=False, indent=2) + "\\n",
        encoding="utf-8",
    )
    (out / "92_workflow_oncelikli_gecis_isleri.json").write_text(
        json.dumps(priority_report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    lines = ["# MADSC — 92 Otomasyon Görev ve Kategori Haritası", "",
             f"İncelenen iş akışı: **{report['total']}** (statik kaynak kod incelemesi)", "",
             "| Kategori | Birincil workflow sayısı |", "|---|---:|"]
    lines += [f"| {CATEGORIES[n][0]} | {report['category_counts'][CATEGORIES[n][0]]} |" for n in CATEGORIES]
    lines += ["", f"Zamanlanmış: {report['scheduled']}; cron girdisi: {report['cron_entries']}; push: {report['push']}; workflow_run: {report['workflow_run']}; manuel: {report['manual']}.", "",
              "## Her eski workflow için görev, tetik ve önerilen kategori", "",
              "| Dosya | Ana kategori | İlgili kategoriler | Tetik | Betikler |", "|---|---|---|---|---|"]
    for x in report["items"]:
        triggers = ",".join(([f"cron({';'.join(x['cron_utc'])})"] if x["cron_utc"] else []) +
                            (["push"] if x["push"] else []) + (["workflow_run"] if x["workflow_run"] else []) +
                            (["manual"] if x["manual"] else [])) or "other"
        lines.append(f"| `{x['file']}` | {CATEGORIES[x['primary_category']][0]} | {', '.join(CATEGORIES[n][0] for n in x['related_categories'])} | {triggers} | {', '.join(x['commands'][:4]) or 'YAML adımları'} |")
    lines += ["", "## 92 eski workflow icin dogrudan betik karsilastirmasi", "",
              "| Eski workflow | Yeni workflow adaylari | Eslesmeyen betikler |",
              "|---|---|---|"]
    for item in report["items"]:
        replacements = ", ".join(item["possible_replacement_workflows"]) or "YOK"
        missing = ", ".join(item["unmatched_script_entrypoints"]) or "-"
        lines.append(f"| `{item['file']}` | {replacements} | {missing} |")
    lines += ["", "## Geçiş kararı", "",
              "Bu liste otomatik **ön sınıflandırmadır**. Her iş akışının gerçek etkisi, izinleri, yazdığı dosyalar, çıktıları ve bağımlılıkları ayrıca doğrulanmadan eski tetik kapatılmaz.",
              "Mevcut yayın/EPG/Pages/yedek zinciri korunur. Kullanıcı onayı olmadan playlist, logo veya arşiv değişmez.", ""]
    (out / "92_workflow_gorev_ve_kategori_haritasi.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k!="items"}, ensure_ascii=False))
    if not report["items"]:
        raise SystemExit("No workflows found")

if __name__ == "__main__":
    main()
