from __future__ import annotations

import json
from django import template
from utils.jsonld import render_jsonld

register = template.Library()


class JsonLDNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        raw = self.nodelist.render(context).strip()
        if not raw:
            return ""
        data = json.loads(raw)
        return render_jsonld(data)


@register.tag(name="jsonld")
def do_jsonld(parser, token):
    nodelist = parser.parse(("endjsonld",))
    parser.delete_first_token()
    return JsonLDNode(nodelist)
