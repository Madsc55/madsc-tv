#!/usr/bin/env python3
"""10. geliştirme: aday HLS yayınları için yanlış pozitif koruması."""
import time
import urllib.parse
import urllib.request

def verify_hls(url, samples=2, pause=2, timeout=12):
    """Ayrı zamanlarda playlist ve medya parçası doğrula; hata halinde güvenli reddet."""
    if not url.startswith(("http://", "https://")):
        return False, "Gecersiz URL"
    seen = []
    for index in range(samples):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "MADSC-TV-Scanner/2.0"})
            with urllib.request.urlopen(req, timeout=timeout) as response:
                body = response.read(512_000).decode("utf-8", "replace")
                final_url = response.geturl()
            if not body.lstrip().startswith("#EXTM3U"):
                return False, "HLS oynatma listesi degil"
            lines = [s.strip() for s in body.splitlines() if s.strip() and not s.startswith("#")]
            if not lines:
                return False, "HLS segmenti bulunamadi"
            if "#EXT-X-STREAM-INF" in body:
                return False, "Master playlist: medya listesi dogrulanmadi"
            segment = urllib.parse.urljoin(final_url, lines[-1])
            if not segment.startswith(("http://", "https://")):
                return False, "Gecersiz segment URL"
            with urllib.request.urlopen(urllib.request.Request(segment, headers={"User-Agent": "MADSC-TV-Scanner/2.0", "Range": "bytes=0-4095"}), timeout=timeout) as response:
                data = response.read(4096)
            if len(data) < 188:
                return False, "Medya parcasi cok kisa"
            seen.append(segment)
        except Exception as exc:
            return False, "HLS dogrulama hatasi: " + type(exc).__name__
        if index + 1 < samples:
            time.sleep(pause)
    if len(set(seen)) < samples:
        return False, "Farkli zamanlarda yeni segment gorulmedi"
    return True, "Iki ayri zamanda HLS segmenti dogrulandi"
