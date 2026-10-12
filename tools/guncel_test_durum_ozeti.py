"""Read-only combined IPTV test progress report. Does not start tests or edit playlists."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read_json(relative):
    path = ROOT / relative
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8-sig"))

def report():
    triple = read_json("madsc_dogrulama/summary.json")
    final = read_json("madsc_son_kontrol/summary.json")
    if not isinstance(triple, dict) or not isinstance(final, dict):
        raise SystemExit("Missing three-stage or final summary; no counts inferred.")
    total = int(triple["candidates"])
    completed = int(triple["completed_three_attempts"])
    waiting = int(triple["waiting_6h"])
    if completed + waiting != total:
        raise SystemExit("Snapshot counts inconsistent; do not report stale figures as live.")
    statuses = final.get("status_counts", {})
    remaining_final = int(final.get("remaining", 0))
    if remaining_final < 0:
        raise SystemExit("Negative remaining final checks in snapshot.")
    reviewed = int(statuses.get("TECHNICAL_PASS_CONTENT_REVIEW", 0))
    identity_pending = int(statuses.get("TECHNICAL_PASS_IDENTITY_PENDING", 0))
    continuity_failed = int(statuses.get("CONTINUITY_FAILED", 0))
    timeouts = int(statuses.get("TIMEOUT", 0))
    return {
        "three_stage_snapshot_utc": triple.get("time"),
        "url_candidates_not_unique_channels": total,
        "three_attempts_completed": completed,
        "three_passes": int(triple["three_decode_passes"]),
        "waiting_for_remaining_attempts": waiting,
        "due_at_snapshot": int(triple.get("due_now", 0)),
        "final_snapshot_utc": final.get("checked_utc"),
        "final_completed": int(final["completed"]),
        "final_statuses": statuses,
        "final_remaining_at_snapshot": remaining_final,
        "final_technical_pass_identity_pending": identity_pending,
        "final_technical_pass_content_review": reviewed,
        "final_continuity_failed": continuity_failed,
        "final_timeouts": timeouts,
        "work_remaining": {
            "three_stage_missing_attempts": waiting,
            "final_checks_pending": remaining_final,
            "identity_or_content_review": identity_pending + reviewed,
            "device_confirmation": "USER_IBO_PLAYER_REQUIRED"
        },
        "ready_for_playlist": 0,
        "next_action": "Resume only due missing attempts; do not repeat completed results.",
        "caution": "Historical snapshots, not live Actions status. Technical pass is not station identity or Sweden IBO confirmation."
    }

if __name__ == "__main__":
    print(json.dumps(report(), ensure_ascii=False, indent=2))
