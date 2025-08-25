from __future__ import annotations

import json
from django.utils.safestring import SafeString, mark_safe


def render_jsonld(data: dict | list) -> SafeString:
    """Return a minified JSON-LD <script> tag from ``data``.

    Keys are sorted to ensure deterministic output. Whitespace is stripped by
    using compact separators.
    """
    json_text = json.dumps(data, sort_keys=True, separators=(",", ":"))
    return mark_safe(f'<script type="application/ld+json">{json_text}</script>')
