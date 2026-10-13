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
duplicate_names = sorted({name for name in source_keys if source_keys.count(name) > 1})
target = assignments["SOURCE_TARGET"]
by_url = defaultdict(list)
for name, url in sources.items():
    normalized = url.strip().rstrip("/")
    by_url[normalized].append(name)
duplicate_urls = [{"url": url, "names": names} for url, names in sorted(by_url.items()) if len(names) > 1]
invalid = [{"name": name, "url": url} for name, url in sources.items()
           if urlsplit(url).scheme not in ("http", "https") or not urlsplit(url).netloc]
report = {"defined": len(sources), "target": target, "difference": len(sources) - target,
          "target_is_declared_config_not_verified_active_feed_count": True,
          "action_required": ("Tanimlar hedefi asiyor; kaynaklari silmeden once canli erisim ve kaynak secimi incelenmeli."
                              if len(sources) > target else "Tanim sayisi hedefe esit veya dusuk; canli erisim ayrica dogrulanmali."),
          "unique_endpoint_count": len(by_url), "duplicate_endpoints": duplicate_urls,
          "duplicate_source_names": duplicate_names,
          "raw_source_entry_count": len(source_keys),
          "invalid_endpoint_definitions": invalid,
          "all_sources": [{"name": name, "url": url} for name, url in sorted(sources.items())],
          "conclusion": "TANIM_FAZLASI" if len(sources) > target else
                        "TANIM_EKSIK" if len(sources) < target else "TANIM_SAYISI_ESIT",
          "limitations": "Yalniz gercek Python kaynak tanimlari ve URL tekrarlarini karsilastirir; erisilebilirlik ve lisans kaniti degildir. Hedef veya kaynaklar otomatik degistirilmez."}
out = ROOT / "madsc_merkezi_denetim"
out.mkdir(exist_ok=True)
(out / "kaynak_hedef_mutabakati.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Kaynak mutabakati: {len(sources)} tanim, {len(by_url)} benzersiz URL, hedef {target}, fark {len(sources)-target}.")
