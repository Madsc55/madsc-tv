"""Development 16: bounded retries, rate limits and safe URL logging."""
import re
import time
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

SENSITIVE = {"token", "key", "apikey", "api_key", "auth", "authorization", "password", "pass", "sig", "signature", "secret", "access_token", "jwt"}
CREDENTIAL = re.compile(r"(?i)(bearer\s+)[^\s]+")
ASSIGNMENT = re.compile(r"(?i)\b(token|api_key|apikey|authorization|password|secret|access_token)\s*[:=]\s*([^\s&,;]+)")

def redact(value):
    """Remove credentials from URL query, userinfo and common log text."""
    value = str(value)
    def url_replacer(match):
        raw = match.group(0)
        try:
            p = urlsplit(raw)
            host = p.hostname or ""
            if p.port:
                host += ":" + str(p.port)
            query = urlencode([(k, "[REDACTED]" if k.lower() in SENSITIVE else v) for k, v in parse_qsl(p.query, keep_blank_values=True)])
            return urlunsplit((p.scheme, host, p.path, query, ""))  # fragments may contain secrets
        except ValueError:
            return "[REDACTED_URL]"
    value = re.sub(r"https?://[^\s<>\"']+", url_replacer, value)
    value = CREDENTIAL.sub(r"\1[REDACTED]", value)
    value = ASSIGNMENT.sub(lambda m: m.group(1) + "=[REDACTED]", value)
    return value

def bounded_retry(operation, *, attempts=3, delay_seconds=1, sleep=time.sleep):
    """Limit requests and retry count; caller handles HTTP timeouts."""
    if not 1 <= attempts <= 5 or not 0 <= delay_seconds <= 60:
        raise ValueError("unsafe retry settings")
    for i in range(attempts):
        try:
            return operation()
        except (TimeoutError, ConnectionError):
            if i == attempts - 1:
                raise
            sleep(delay_seconds * (i + 1))
