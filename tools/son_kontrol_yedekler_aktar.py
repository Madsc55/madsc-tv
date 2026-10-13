"""Teknik olarak geçen yeni yayınları sadece YEDEKLER'e cihaz testi için hazırla.

Kimlik/IBO onayı vermez. Yalnızca 3/3 ve 5 dakika süreklilik kanıtı
olan, inceleme olayı bulunmayan akışları TEST etiketiyle ekler.
"""
import hashlib
import json
import pathlib
try:
    from .yedekler_guvenli_ekle import update
except ImportError:
    from yedekler_guvenli_ekle import update

RESULTS = pathlib.Path("madsc_son_kontrol/results.json")
STATE = pathlib.Path("madsc_dogrulama/state.json")
PLAYLIST = pathlib.Path("CALISANLAR.m3u")
OUTPUT = pathlib.Path("onaylanmis_adaylar.json")


def prepare(results, state):
    channels = state.get("channels", {})
    if not isinstance(channels, dict):
        raise ValueError("Üç aşama kanal kayıtları beklenen biçimde değil")
    by_id = {}
    for record in channels.values():
        if not isinstance(record, dict):
            continue
        url = record.get("url", "")
        checks = record.get("checks", [])
        if (not isinstance(url, str) or not url.startswith(("http://", "https://"))
                or not isinstance(checks, list) or len(checks) != 3
                or not all(isinstance(c, dict) and c.get("passed") is True for c in checks)):
            continue
        by_id[hashlib.sha256(url.encode()).hexdigest()[:20]] = record
    staged = []
    for item in results:
        if not isinstance(item, dict) or item.get("status") != "TECHNICAL_PASS_IDENTITY_PENDING":
            continue
        continuity = item.get("continuity", {})
        if not isinstance(continuity, dict) or continuity.get("passed") is not True:
            continue
        if any(item.get("review_events", {}).values()):
            continue
        record = by_id.get(item.get("candidate_id"))
        if not record:
            continue
        label = str(item.get("label") or record.get("channel") or "").strip()
        if not label or any(ch in label for ch in "\r\n"):
            continue
        # Yalnız teknik aday: gerçek kanal kimliği ve İsveç IBO henüz onaylı değil.
        staged.append({"name": label + " [TEST]", "url": record["url"],
                       "logo": "", "three_stage_passed": True,
                       "technical_staging": True, "identity_verified": False})
    return staged


def main():
    results = json.loads(RESULTS.read_text(encoding="utf-8"))
    if not isinstance(results, list):
        raise ValueError("Son kontrol raporu liste değil")
    state = json.loads(STATE.read_text(encoding="utf-8"))
    approved = prepare(results, state)
    original = PLAYLIST.read_text(encoding="utf-8-sig")
    changed, count = update(original, approved)
    OUTPUT.write_text(json.dumps(approved, ensure_ascii=False, indent=2), encoding="utf-8")
    if count:
        PLAYLIST.write_text(changed, encoding="utf-8")
    print(f"Yalnız YEDEKLER'e cihaz testi için hazırlanan teknik aday: {count}")


if __name__ == "__main__":
    main()
