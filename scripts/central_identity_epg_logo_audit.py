#!/usr/bin/env python3
"""Logo EPG kimlik ve teknik gecmis kanitlarini tek salt okunur rapora al."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "madsc_merkezi_denetim"
OUT.mkdir(exist_ok=True)

def load(relative):
    path = ROOT / relative
    if not path.is_file():
        return {"available": False, "path": relative, "data": None}
    try:
        return {"available": True, "path": relative, "data": json.loads(path.read_text(encoding="utf-8"))}
    except (ValueError, UnicodeError):
        return {"available": False, "path": relative, "error": "INVALID_JSON", "data": None}

sources = {
    "final_validation": load("madsc_son_kontrol/summary.json"),
    "discovery_history": load("madsc_kesif/gecmis.json"),
    "logo_preparation": load("madsc_kesif/candidate_logos.json"),
    "candidate_epg_join": load("madsc_kesif/candidate_epg_logo_join.json"),
}
final = sources["final_validation"]["data"]
history = sources["discovery_history"]["data"]
logo = sources["logo_preparation"]["data"]
epg = sources["candidate_epg_join"]["data"]
report = {
    "evidence": {key: {"available": v["available"], "path": v["path"]}
                 for key, v in sources.items()},
    "final_validation": {
        "status_counts": final.get("status_counts", {}) if isinstance(final, dict) else {},
        "ready_for_playlist_reported": final.get("ready_for_playlist") if isinstance(final, dict) else None,
        "identity_and_device_confirmation_required": True,
    },
    "history": {"entries": len(history.get("history", {})) if isinstance(history, dict) and isinstance(history.get("history"), dict) else None},
    "logos": {"prepared_results": len(logo.get("results", [])) if isinstance(logo, dict) and isinstance(logo.get("results"), list) else None,
              "visual_identity_verified_by_this_audit": False},
    "epg": {"candidate_results": len(epg.get("candidate_results", [])) if isinstance(epg, dict) and isinstance(epg.get("candidate_results"), list) else None,
            "sweden_ibo_verified_by_this_audit": False},
    "user_ibo_approval": "NOT_VERIFIED",
    "playlist_approved_by_this_audit": False,
    "limitations": "Teknik test, PNG ve XMLTV eslesmesi kanal kimligi, lisans veya Isvec IBO cihazinda calisma kaniti degildir. Eksik raporlar tamamlanmis sayilmaz.",
    "safety": "Salt okunur; adaylari, gecmisi, EPG'yi ve playlistleri degistirmez."
}
(OUT / "logo_epg_kimlik_gecmis_tek_rapor.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print("Logo, EPG, kimlik ve gecmis tek raporda birlestirildi; IBO onayi verilmedi.")
