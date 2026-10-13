#!/usr/bin/env python3
"""Kesif gecmisinden tekrar test riskini salt okunur raporla."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "madsc_merkezi_denetim"
OUT.mkdir(exist_ok=True)
history_path = ROOT / "madsc_kesif/gecmis.json"

def inspect(history):
    records = []
    tested = 0
    repeated = 0
    missing = 0
    invalid_examples = []
    zero_run_records = 0
    for key, entry in history.items():
        if not isinstance(entry, dict):
            missing += 1
            if len(invalid_examples) < 30:
                invalid_examples.append({"url_key": key, "reason": "NOT_OBJECT"})
            continue
        runs = entry.get("runs", 0)
        try:
            runs = int(runs)
        except (ValueError, TypeError):
            missing += 1
            if len(invalid_examples) < 30:
                invalid_examples.append({"url_key": key, "reason": "INVALID_RUN_COUNT"})
            continue
        if runs < 0:
            missing += 1
            if len(invalid_examples) < 30:
                invalid_examples.append({"url_key": key, "reason": "NEGATIVE_RUN_COUNT"})
            continue
        if runs == 0:
            zero_run_records += 1
        if runs:
            tested += 1
        if runs > 1:
            repeated += 1
            records.append({"url_key": key, "runs": runs,
                            "last_test": entry.get("last_test", ""),
                            "channel": entry.get("channel", "")})
    return {"historical_entries": len(history), "tested_urls": tested,
            "urls_tested_more_than_once": repeated,
            "excess_test_runs": sum(row["runs"] - 1 for row in records),
            "invalid_history_records": missing,
            "invalid_examples": invalid_examples,
            "zero_run_records": zero_run_records,
            "repeat_rate_among_tested_urls": round(repeated / tested, 4) if tested else None,
            "total_recorded_test_runs": tested + sum(row["runs"] - 1 for row in records),
            "repeated_examples": sorted(records, key=lambda row: -row["runs"])[:30]}

if history_path.is_file():
    raw = json.loads(history_path.read_text(encoding="utf-8"))
    if not isinstance(raw.get("history"), dict):
        raise ValueError("Kesif gecmisi gecersiz; kayitlar korunuyor.")
    result = inspect(raw["history"])
    result["evidence"] = "madsc_kesif/gecmis.json"
else:
    result = {"status": "GECMIS_DOSYASI_YOK", "evidence": str(history_path.relative_to(ROOT)),
              "limitations": "Gecmis olmadan tekrar orani hesaplanamaz."}
result["safety"] = "Salt okunur; testler, gecmis, listeler ve kaynaklar degistirilmez."
(OUT / "tekrar_test_analizi.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print("Tekrar test gecmisi raporu olusturuldu.")
