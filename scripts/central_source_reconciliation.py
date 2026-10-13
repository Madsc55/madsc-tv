#!/usr/bin/env python3
"""Gercek kesif kaynak sozlugunu ve hedefini statik olarak karsilastir."""
import ast
import json
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
source = ast.parse((ROOT / "madsc_akilli_kesif.py").read_text(encoding="utf-8"))
assignments = {}
for node in source.body:
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in ("SOURCES", "SOURCE_TARGET"):
                assignments[target.id] = ast.literal_eval(node.value)
sources = assignments["SOURCES"]
# AST sozluk anahtarlarini incele: Python yinelenen isimleri sessizce ezer.
source_nodes = [node.value for node in source.body if isinstance(node, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == "SOURCES" for t in node.targets)]
source_keys = [ast.literal_eval(key) for key in source_nodes[-1].keys] if source_nodes and isinstance(source_nodes[-1], ast.Dict) else []
name_counts = defaultdict(int)
for name in source_keys:
    name_counts[name] += 1
duplicate_names = sorted(name for name, count in name_counts.items() if count > 1)
target = assignments["SOURCE_TARGET"]
by_url = defaultdict(list)
for name, url in sources.items():
    normalized = url.strip().rstrip("/")
    by_url[normalized].append(name)
duplicate_urls = [{"url": url, "names": names} for url, names in sorted(by_url.items()) if len(names) > 1]
# Ayni URL birden cok isimle tanimlandiysa, hedef farki icin guvenli inceleme adayi.
# Bu bir silme karari degildir; isimler ve aktif kullanim bagimsiz dogrulanmalidir.
review_candidates = [
    {"endpoint": row["url"], "names": row["names"], "redundant_definitions": len(row["names"]) - 1,
     "decision": "MANUEL_INCELEME_GEREKLI"}
    for row in duplicate_urls
]
reviewable_surplus = sum(row["redundant_definitions"] for row in review_candidates)
invalid = [{"name": name, "url": url} for name, url in sources.items()
           if urlsplit(url).scheme not in ("http", "https") or not urlsplit(url).netloc]
# Hedef farkini tek basina kopya kaynaklara baglama; karar icin somut kanit ayir.
gap = len(sources) - target
gap_diagnosis = {
    "gap": gap,
    "exact_url_duplicate_surplus": reviewable_surplus,
    "duplicate_name_overwrites": len(source_keys) - len(sources),
    "invalid_url_definitions": len(invalid),
    "explanation": (
        "AYNI_URL_FAZLASI_FARKI_ACIKLAYABILIR_AMA_SILME_ONAYI_DEGIL"
        if gap > 0 and reviewable_surplus >= gap
        else "FARK_TEK_BASINA_URL_TEKRARIYLA_ACIKLANAMIYOR"
        if gap > 0 else "HEDEF_FARKI_YOK_VEYA_EKSIK"
    ),
    "next_action": "Kaynak tanimlarinin kullanimi ve canli erisimi dogrulanmadan hedef degistirilmez.",
}
# Kesifte otomatik secilen kaynaklar koddan okunur; isim listesi canli erisim kaniti degildir.
active_names = []
for node in ast.walk(source):
    if isinstance(node, ast.FunctionDef) and node.name == "turkish_feed":
        for child in ast.walk(node):
            if isinstance(child, ast.Compare) and any(isinstance(op, ast.In) for op in child.ops):
                for candidate in child.comparators:
                    if isinstance(candidate, (ast.Set, ast.Tuple, ast.List)):
                        try:
                            values = ast.literal_eval(candidate)
                            if all(isinstance(value, str) for value in values):
                                active_names = sorted(set(values))
                        except (ValueError, TypeError):
                            pass
configured_active = sorted(set(active_names) & set(sources))
unconfigured_active = sorted(set(active_names) - set(sources))
inactive_configured = sorted(set(sources) - set(active_names))
report = {"defined": len(sources), "target": target, "difference": len(sources) - target,
          "target_is_declared_config_not_verified_active_feed_count": True,
          "action_required": ("Tanimlar hedefi asiyor; kaynaklari silmeden once canli erisim ve kaynak secimi incelenmeli."
                              if len(sources) > target else "Tanim sayisi hedefe esit veya dusuk; canli erisim ayrica dogrulanmali."),
          "unique_endpoint_count": len(by_url), "duplicate_endpoints": duplicate_urls,
          "gap_diagnosis": gap_diagnosis,
          "automatic_discovery_selection": {"selection_found_in_code": bool(active_names),
              "selected_configured_count": len(configured_active),
              "selected_configured_names": configured_active,
              "selected_missing_from_definitions": unconfigured_active,
              "configured_but_not_auto_selected_count": len(inactive_configured),
              "configured_but_not_auto_selected_names": inactive_configured,
              "limitations": "Statik kod secimi; gercek HTTP erisimi veya calisan yayin kaniti degildir."},
          "duplicate_endpoint_review_candidates": review_candidates,
          "duplicate_endpoint_definition_surplus": reviewable_surplus,
          "target_gap_explainable_by_exact_endpoint_duplicates": bool(len(sources) > target and reviewable_surplus >= len(sources) - target),
          "safe_next_step": "Tekrarli URL tanimlarini kullanan is akislari incelenmeli; otomatik silme veya hedef sayisi degisikligi yapilmaz.",
          "duplicate_source_names": duplicate_names,
          "raw_source_entry_count": len(source_keys),
          "overwritten_source_definitions": len(source_keys) - len(sources),
          "invalid_endpoint_definitions": invalid,
          "all_sources": [{"name": name, "url": url} for name, url in sorted(sources.items())],
          "conclusion": "TANIM_FAZLASI" if len(sources) > target else
                        "TANIM_EKSIK" if len(sources) < target else "TANIM_SAYISI_ESIT",
          "limitations": "Yalniz gercek Python kaynak tanimlari ve URL tekrarlarini karsilastirir; erisilebilirlik ve lisans kaniti degildir. Hedef veya kaynaklar otomatik degistirilmez."}
out = ROOT / "madsc_merkezi_denetim"
out.mkdir(exist_ok=True)
(out / "kaynak_hedef_mutabakati.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Kaynak mutabakati: {len(sources)} tanim, {len(by_url)} benzersiz URL, hedef {target}, fark {len(sources)-target}.")
