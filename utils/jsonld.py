from __future__ import annotations

import json
import hashlib
from django.core.cache import cache
from django.utils.safestring import SafeString, mark_safe


def render_jsonld(data: dict | list) -> SafeString:
    """Return a minified JSON-LD <script> tag from ``data``.

    Keys are sorted to ensure deterministic output. Whitespace is stripped by
    using compact separators.
    """
    json_text = json.dumps(data, sort_keys=True, separators=(",", ":"))
    key = "jsonld:" + hashlib.md5(json_text.encode("utf-8")).hexdigest()
    cached = cache.get(key)
    if cached is not None:
        return cached
    tag = mark_safe(f'<script type="application/ld+json">{json_text}</script>')
    cache.set(key, tag, 60 * 60)
    return tag
