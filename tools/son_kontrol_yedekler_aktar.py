"""Son kontrol kanıtlarından güvenli YEDEKLER adaylarını hazırla.

Kimlik veya cihaz onayı yoksa otomatik olarak boş aday listesi üretir.
"""
import json
import pathlib
from tools.yedekler_guvenli_ekle import update

RESULTS = pathlib.Path("madsc_son_kontrol/results.json")
PLAYLIST = pathlib.Path("CALISANLAR.m3u")
OUTPUT = pathlib.Path("onaylanmis_adaylar.json")

def main():
    results = json.loads(RESULTS.read_text(encoding="utf-8"))
    if not isinstance(results, list):
        raise ValueError("Son kontrol raporu liste değil")
    approved = []
    for item in results:
        if not isinstance(item, dict):
            continue
        # Test raporunda kimlik açıkça doğrulanmadan otomatik ekleme yasaktır.
        if (item.get("status") != "READY_FOR_PLAYLIST"
                or item.get("station_identity") != "VERIFIED"
                or item.get("ibo_sweden") != "VERIFIED"
                or item.get("three_stage_passed") is not True):
            continue
        if not item.get("url") or not item.get("label"):
            continue
        approved.append({"name": item["label"], "url": item["url"],
                         "logo": item.get("logo", ""), "three_stage_passed": True,
                         "identity_verified": True})
    original = PLAYLIST.read_text(encoding="utf-8-sig")
    changed, count = update(original, approved)
    OUTPUT.write_text(json.dumps(approved, ensure_ascii=False, indent=2), encoding="utf-8")
    if count:
        PLAYLIST.write_text(changed, encoding="utf-8")
    print(f"Son kontrolden YEDEKLER'e güvenle eklenen: {count}")

if __name__ == "__main__":
    main()
