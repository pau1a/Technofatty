import json
import re
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime

FIXTURES = Path(__file__).parent / "fixtures"
JSON_LD_RE = re.compile(
    r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>',
    re.IGNORECASE | re.DOTALL,
)


def _extract_jsonld(html: str):
    for match in JSON_LD_RE.finditer(html):
        try:
            yield json.loads(match.group(1))
        except json.JSONDecodeError as exc:
            raise AssertionError(f"Invalid JSON-LD: {exc}") from exc


def _looks_like_url(value: str) -> bool:
    parsed = urlparse(value)
    return bool(parsed.scheme or parsed.netloc or value.startswith("/"))


def _assert_absolute_urls(node):
    if isinstance(node, dict):
        for value in node.values():
            _assert_absolute_urls(value)
    elif isinstance(node, list):
        for item in node:
            _assert_absolute_urls(item)
    elif isinstance(node, str) and _looks_like_url(node):
        parsed = urlparse(node)
        if not (parsed.scheme and parsed.netloc):
            raise AssertionError(f"URL is not absolute: {node}")


def _assert_iso_dates(node):
    if isinstance(node, dict):
        for key, value in node.items():
            if isinstance(value, str) and "date" in key.lower():
                candidate = value.replace("Z", "+00:00")
                try:
                    datetime.fromisoformat(candidate)
                except ValueError as exc:
                    raise AssertionError(
                        f"Invalid ISO-8601 date for '{key}': {value}"
                    ) from exc
            _assert_iso_dates(value)
    elif isinstance(node, list):
        for item in node:
            _assert_iso_dates(item)


def _validate_file(name: str):
    html = (FIXTURES / name).read_text()
    for data in _extract_jsonld(html):
        _assert_absolute_urls(data)
        _assert_iso_dates(data)


def test_blog_post():
    _validate_file("blog_post.html")


def test_case_study():
    _validate_file("case_study.html")


def test_faq():
    _validate_file("faq.html")
