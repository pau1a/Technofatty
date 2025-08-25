from __future__ import annotations

from urllib.parse import urlparse, urljoin


def ensure_absolute(url: str, base: str) -> str | None:
    """Return an absolute URL or ``None`` if one cannot be formed.

    ``url`` may already be absolute, in which case it is returned unchanged.
    Relative URLs are resolved against ``base``. If ``url`` cannot be
    resolved to an absolute URL (for example when ``base`` is empty or the
    resulting URL still lacks a scheme/netloc), ``None`` is returned.
    """
    if not url:
        return None

    parsed = urlparse(url)
    if parsed.scheme and parsed.netloc:
        return url

    if not base:
        return None

    absolute = urljoin(base, url)
    parsed_absolute = urlparse(absolute)
    if parsed_absolute.scheme and parsed_absolute.netloc:
        return absolute
    return None
