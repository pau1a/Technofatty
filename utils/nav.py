"""Navigation helper utilities."""

from __future__ import annotations


def _normalize(path: str) -> str:
    """Ensure path starts and ends with a slash.

    The root path `/` is returned unchanged.
    """
    if not path:
        return "/"
    if not path.startswith("/"):
        path = "/" + path
    if path != "/" and not path.endswith("/"):
        path += "/"
    return path


def is_active(request_path: str, nav_url: str) -> bool:
    """Return ``True`` if ``request_path`` falls under ``nav_url``.

    Both arguments may be provided with or without leading/trailing slashes.
    The function normalises them and performs a prefix match so that child
    pages are considered active for their parent nav item.
    """
    req = _normalize(request_path)
    url = _normalize(nav_url)
    return req.startswith(url)
