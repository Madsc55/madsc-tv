"""Cuma denetimi için kanalları değiştirmeyen görünür uyarı özeti."""
import json
import os
from pathlib import Path

def main():
    path = Path("madsc_ana_liste_denetimi/rapor.json")
    if not path.exists():
        print("::warning title=Cuma denetimi::Rapor üretilemedi; çalışma günlüklerini kontrol edin.")
        return
    report = json.loads(path.read_text(encoding="utf-8"))
    rows = report.get("channels", [])
    failures = [r for r in rows if r.get("status") != "TEKNIK_ERISIM_VAR"]
    epg_missing = [r for r in rows if r.get("epg") == "PROGRAM_ESLESMEDI"]
    duplicates = report.get("duplicate_stream_groups", [])
    epg = report.get("epg", {})
    lines = [
        "# Cuma ana kanal denetimi",
        f"Kontrol edilen: {len(rows)}",
        f"Teknik erişimi doğrulanamayan: {len(failures)}",
        f"EPG programı eşleşmeyen: {len(epg_missing)}",
        f"Aynı yayın bağlantısını kullanan gruplar: {len(duplicates)}",
        f"EPG kaynağı: {epg.get('status', 'BELIRSIZ')}",
        "",
        "Kanal kimliği ve canlı yayın–EPG içerik eşleşmesi bu testte kesin doğrulanamaz.",
        "Ana listedeki kanalların hiçbirine müdahale edilmez.",
    ]
    for heading, selected in (("Teknik erişim sorunu", failures), ("EPG kaydı eşleşmeyen", epg_missing)):
        if selected:
            lines.extend(("", f"## {heading}"))
            lines.extend(f"- {r.get('name', 'Bilinmeyen')}" for r in selected[:100])
            if len(selected) > 100:
                lines.append(f"- ve {len(selected) - 100} kanal daha (rapor.json dosyasında)")
    summary = "\n".join(lines) + "\n"
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as out:
            out.write(summary)
    else:
        print(summary)
    if failures or epg_missing or duplicates or epg.get("status") != "EPG_OK":
        print("::warning title=Cuma kanal denetimi::Sorun veya doğrulanamayan yayınlar var; Actions özetini ve raporu inceleyin.")
    else:
        print("::notice title=Cuma kanal denetimi::Teknik kontrollerde sorun bulunmadı; kimlik doğrulaması ayrıca gerekir.")

if __name__ == "__main__":
    main()
