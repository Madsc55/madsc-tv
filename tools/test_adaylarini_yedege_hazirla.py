"""Güvenli kanal araması çıktılarından yalnızca teknik testi geçenleri ayrı yedeğe hazırlar."""
import csv
import hashlib
import pathlib

ROOT = pathlib.Path("indirilen_adaylar")
OUT = pathlib.Path("yedekler/otomatik_test_adaylari")
OUT.mkdir(parents=True, exist_ok=True)
existing = pathlib.Path("CALISANLAR.m3u").read_text(encoding="utf-8-sig")
existing_urls = {line.strip() for line in existing.splitlines() if line.strip().startswith(("http://", "https://"))}
selected = {}
for path in sorted(ROOT.rglob("YENILER_TARAMA_RAPORU.csv")):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.DictReader(stream):
            url = (row.get("YAYIN_URL") or "").strip()
            if (row.get("TEKNIK_TEST") != "TEKNIK_AKIS_VAR"
                    or row.get("MEDYA_TEST") != "VIDEO_SES_VAR"
                    or not url.startswith(("http://", "https://"))
                    or url in existing_urls):
                continue
            selected.setdefault(url, row)
lines = ["#EXTM3U"]
for url, row in sorted(selected.items(), key=lambda item: (item[1]["KANAL"].casefold(), item[0])):
    name = row["KANAL"].replace("\n", " ").replace(",", " ").strip()
    logo = (row.get("LOGO_ADAY_URL") or "").strip().replace('"', "")
    kind = row.get("ADAY_TURU", "")
    lines.append(f'#EXTINF:-1 tvg-logo="{logo}" group-title="OTOMATIK TEST YEDEGI",{name}')
    lines.append(url)
(OUT / "TEKNIK_TESTI_GECEN_ADAYLAR.m3u").write_text("\n".join(lines) + "\n", encoding="utf-8")
(OUT / "OZET.txt").write_text(
    f"Teknik testi gecen benzersiz aday: {len(selected)}\n"
    "Yalnizca teknik akisin ve video/ses izlerinin varligi denetlendi.\n"
    "Kanal kimligi, dogru canli yayin, IBO Player ve Isvec erisimi dogrulanmadi.\n"
    "Ana listeye veya YENILER listesine otomatik eklenmez.\n", encoding="utf-8")
print(f"Test yedegine hazirlanan aday: {len(selected)}")
