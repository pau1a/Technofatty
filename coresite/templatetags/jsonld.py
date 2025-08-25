from __future__ import annotations

import json
from django import template
from django.conf import settings

from utils.jsonld import render_jsonld
from utils.urls import ensure_absolute

register = template.Library()


class JsonLDNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        raw = self.nodelist.render(context).strip()
        if not raw:
            return ""
        data = json.loads(raw)

        request = context.get("request")
        base = request.build_absolute_uri("/") if request else getattr(
            settings, "SITE_BASE_URL", ""
        )

        if not _absolutize_urls(data, base):
            return ""
        return render_jsonld(data)


def _absolutize_urls(value, base: str) -> bool:
    """Ensure all ``url`` fields within ``value`` are absolute.

    The ``value`` structure is modified in-place. ``True`` is returned when all
    URLs could be converted to absolute form, otherwise ``False``.
    """
    if isinstance(value, dict):
        for key, val in value.items():
            if key == "url" and isinstance(val, str):
                absolute = ensure_absolute(val, base)
                if absolute is None:
                    return False
                value[key] = absolute
            else:
                if not _absolutize_urls(val, base):
                    return False
    elif isinstance(value, list):
        for item in value:
            if not _absolutize_urls(item, base):
                return False
    return True


@register.tag(name="jsonld")
def do_jsonld(parser, token):
    nodelist = parser.parse(("endjsonld",))
    parser.delete_first_token()
    return JsonLDNode(nodelist)
