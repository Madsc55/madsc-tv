#!/usr/bin/env python3
"""Summarize playlist inventory and optimization suggestions as Markdown.

Read-only with respect to IPTV playlists; writes only the requested report.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return data


def cell(value: object) -> str:
    return str(value if value is not None else "—").replace("|", "\\|").replace("\n", " ")


def render(inventory: dict, optimizer: dict) -> str:
    rows = inventory.get("playlists", [])
    proposals = optimizer.get("reports", [])
    if not isinstance(rows, list) or not isinstance(proposals, list):
        raise ValueError("Invalid inventory/optimizer report format")
    by_file = {r.get("file"): r for r in proposals if isinstance(r, dict)}
    out = [
        "# MADSC TV — Kanal Listesi Sağlık Raporu", "",
        f"Oluşturulma (UTC): {datetime.now(timezone.utc).isoformat()}", "",
        "**Kapsam:** Salt okunur analiz; kanallar silinmez, taşınmaz veya değiştirilmez.", "",
        "## Genel durum", "",
        "| Liste | Durum | Kanal | Kategori | Tekrar URL | Öneri | Envanter eşleşmesi |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    total_channels = total_suggestions = 0
    for item in rows:
        if not isinstance(item, dict):
            continue
        name = item.get("file", "Bilinmiyor")
        suggestion = by_file.get(name, {})
        count = item.get("channels", 0)
        proposed = suggestion.get("suggestion_count", len(suggestion.get("suggestions", [])))
        total_channels += count if isinstance(count, int) else 0
        total_suggestions += proposed if isinstance(proposed, int) else 0
        match = suggestion.get("inventory_sha256_matches")
        match_text = "Evet" if match is True else "Hayır — güncel envanter oluşturun" if match is False else "Kontrol edilmedi"
        out.append("| " + " | ".join(map(cell, [
            name, "Mevcut" if item.get("exists") else "Eksik",
            count if item.get("exists") else "—",
            len(item.get("groups", {})),
            item.get("duplicate_url_count", len(item.get("duplicate_urls", []))),
            proposed, match_text,
        ])) + " |")
    out += ["", f"**Toplam:** {total_channels} kanal, {total_suggestions} öneri.", ""]
    out += ["## Liste ayrıntıları", ""]
    for item in rows:
        if not isinstance(item, dict):
            continue
        name = str(item.get("file", "Bilinmiyor"))
        out += [f"### {name}", ""]
        if not item.get("exists"):
            out += ["Dosya bulunamadı.", ""]
            continue
        out += [
            f"- M3U başlığı geçerli: {'Evet' if item.get('header_valid') else 'Hayır'}",
            f"- Eşleşmeyen EXTINF satırı: {item.get('unpaired_metadata', 0)}",
            f"- URL/metadata hatası: {len(item.get('invalid_entries', []))}",
        ]
        for group, count in sorted(item.get("groups", {}).items()):
            out.append(f"- Kategori: {cell(group)} — {count} kanal")
        for title, matches in item.get("important_channels", {}).items():
            out.append(f"- Önemli kanal {cell(title)}: {len(matches)} eşleşme")
        for group, count in item.get("protected_groups", {}).items():
            out.append(f"- Korunan grup {cell(group)}: {count} kayıt")
        out.append("")
        suggestion = by_file.get(name, {})
        entries = suggestion.get("suggestions", [])
        if entries:
            out += ["| EXTINF satırı | Öneri türü | Mevcut | Önerilen / Not |",
                    "| ---: | --- | --- | --- |"]
            for entry in entries:
                for kind, change in entry.get("changes", {}).items():
                    if isinstance(change, dict):
                        current = change.get("current", "")
                        proposed = change.get("suggested", "")
                    else:
                        current, proposed = "", change
                    out.append("| " + " | ".join(map(cell, [
                        entry.get("extinf_line", "?"), kind, current, proposed
                    ])) + " |")
            out.append("")
        else:
            out += ["Bu liste için biçimlendirme önerisi yok.", ""]
    unknown = [r.get("file") for r in proposals if isinstance(r, dict)
               and r.get("file") not in {i.get("file") for i in rows if isinstance(i, dict)}]
    if unknown:
        out += ["## Envanterde bulunmayan optimizer girdileri", "",
                ", ".join(map(cell, unknown)), ""]
    out += ["## Güvenlik notu", "",
            "Bu rapor otomatik düzenleme onayı değildir. Öneriler manuel incelenmelidir.",
            "Kaynak M3U dosyaları bu betik tarafından açılıp değiştirilmez.", ""]
    return "\n".join(out)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, default=Path("playlist_inventory.json"))
    parser.add_argument("--suggestions", type=Path, default=Path("playlist_optimizer_suggestions.json"))
    parser.add_argument("--output", type=Path, default=Path("reports/playlist_health_report.md"))
    parser.add_argument("--stdout-only", action="store_true", help="Print without creating report file")
    args = parser.parse_args()
    report = render(load_json(args.inventory), load_json(args.suggestions))
    if not args.stdout_only:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
        print(f"Markdown report: {args.output}")
    print(report)


if __name__ == "__main__":
    main()
