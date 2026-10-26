#!/usr/bin/env python3
"""Read-only Turkish TV candidate gate and official YouTube live discovery.
No playlist writes, no stream URL extraction, no promotion.
"""
import argparse
import datetime as dt
import json
import os
import pathlib
import re
import urllib.parse
import urllib.request

TV_WORDS = ("tv", "televizyon", "television", "canlı yayın", "canli yayin", "haber", "news")
RADIO = re.compile(r"(?i)(?:^|[^a-z])(?:radio|radyo|fm|am radio|podcast)(?:$|[^a-z])")
LOCKED = re.compile(r"(?i)(?:drm|widevine|playready|fairplay|premium|abonelik|subscription|encrypted|şifreli|sifreli)")
TURKISH = re.compile(r"(?i)(?:türk|turk|türkiye|turkiye|trt|\btr\b|\btur\b)")
YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}

def classify(name, language="", category="", source="", url="", is_live=False, youtube=False):
    title = str(name or "").strip()
    lang = str(language or "").strip().lower()
    kind = str(category or "").strip()
    origin = str(source or "").strip()
    if not title or not url:
        return "REJECT_MISSING_IDENTITY_OR_URL"
    if RADIO.search(" ".join((title, kind))):
        return "REJECT_RADIO"
    if LOCKED.search(" ".join((title, kind, origin, url))):
        return "REJECT_ENCRYPTED_OR_PAID"
    if lang and lang not in ("tr", "tur", "turkish", "türkçe", "turkce"):
        return "REJECT_NON_TURKISH_LANGUAGE"
    # A country/source name is NOT language or station identity evidence.
    if not (lang in ("tr", "tur", "turkish", "türkçe", "turkce") or TURKISH.search(title)):
        return "REVIEW_TURKISH_LANGUAGE_UNVERIFIED"
    if youtube:
        host = (urllib.parse.urlsplit(url).hostname or "").lower()
        if host not in YOUTUBE_HOSTS:
            return "REJECT_NOT_YOUTUBE"
        if not is_live:
            return "REJECT_NOT_CONFIRMED_LIVE"
    if not (any(w in title.lower() for w in TV_WORDS) or kind.lower() in ("tv", "television")):
        return "REVIEW_TV_IDENTITY_UNVERIFIED"
    return "REVIEW_TURKISH_TV_CANDIDATE_NOT_APPROVED"

def youtube_live(api_key, queries, max_results=25):
    if not api_key:
        return [], "YOUTUBE_API_KEY_MISSING_NO_YOUTUBE_SEARCH"
    results = []
    for query in queries:
        params = urllib.parse.urlencode({"part": "snippet", "type": "video",
                                         "eventType": "live", "q": query,
                                         "maxResults": min(max_results, 50),
                                         "relevanceLanguage": "tr", "key": api_key})
        req = urllib.request.Request("https://www.googleapis.com/youtube/v3/search?" + params,
                                     headers={"User-Agent": "MADSC-TV-readonly-discovery/1.0"})
        with urllib.request.urlopen(req, timeout=20) as response:
            data = json.load(response)
        for item in data.get("items", []):
            video_id = item.get("id", {}).get("videoId", "")
            snippet = item.get("snippet", {})
            if not re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id):
                continue
            title = snippet.get("title", "")
            channel = snippet.get("channelTitle", "")
            url = "https://www.youtube.com/watch?v=" + video_id
            results.append({"title": title, "channel": channel, "url": url,
                            "source": "YOUTUBE_DATA_API_LIVE",
                            "live_flag": snippet.get("liveBroadcastContent") == "live",
                            "status": classify(channel + " " + title, category="tv",
                                               url=url, is_live=snippet.get("liveBroadcastContent") == "live",
                                               youtube=True),
                            "identity_verified": False, "language_verified": False,
                            "drm_verified": False, "three_stage_verified": False,
                            "approved_for_playlist": False})
    return list({r["url"]: r for r in results}.values()), ""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="madsc_kesif/youtube_review.json")
    parser.add_argument("--query", action="append", default=[])
    args = parser.parse_args()
    queries = args.query or ["Türkçe televizyon canlı yayın", "Türkiye haber TV canlı",
                              "Türk televizyonu canlı yayın Avrupa"]
    try:
        candidates, error = youtube_live(os.getenv("YOUTUBE_API_KEY", ""), queries)
    except Exception as exc:
        candidates, error = [], "YOUTUBE_SEARCH_ERROR_" + type(exc).__name__
    report = {"checked_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
              "queries": queries, "candidates": candidates, "error": error,
              "publication": "DENIED_UNTIL_EXPLICIT_WRITTEN_USER_APPROVAL",
              "notes": "Search results are NOT decoded streams. Manual official-channel, Turkish-language, free-to-air, video/audio, three-stage and IBO checks are still required. No playlist writes."}
    path = pathlib.Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"youtube_candidates": len(candidates), "error": error,
                      "playlist_modified": False}, ensure_ascii=False))

if __name__ == "__main__":
    main()
