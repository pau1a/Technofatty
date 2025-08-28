import json
import pathlib
import re
import sys

import pytest
from django.utils.safestring import SafeString

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from utils.jsonld import render_jsonld


def test_render_jsonld_minified_and_deterministic():
    data1 = {"b": 2, "a": 1}
    data2 = {"a": 1, "b": 2}
    out1 = render_jsonld(data1)
    out2 = render_jsonld(data2)
    expected = '<script type="application/ld+json">{"a":1,"b":2}</script>'
    assert isinstance(out1, SafeString)
    assert out1 == expected
    assert out1 == out2
    # ensure minified: no unnecessary whitespace
    inner = out1.split('>', 1)[1].rsplit('<', 1)[0]
    assert '\n' not in inner and ' ' not in inner


def _render(template_str: str, context: dict) -> str:
    django = pytest.importorskip("django")
    from django.conf import settings
    from django.template import Context, Template

    if not settings.configured:
        settings.configure(
            TEMPLATES=[{"BACKEND": "django.template.backends.django.DjangoTemplates"}]
        )
        django.setup()

    template = Template(template_str)
    return template.render(Context(context))


def _extract_json(html: str) -> dict:
    match = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    assert match, "No JSON-LD script found"
    return json.loads(match.group(1))


TOOLS_TEMPLATE = """
{% load jsonld %}
{% jsonld %}
{
  "@context": "https://schema.org",
  "@graph": [
    {% for tool in tools %}
    {
      "@type": "{% if tool.schema_kind == 'software' %}SoftwareApplication{% else %}CreativeWork{% endif %}",
      "name": "{{ tool.title|escapejs }}",
      "description": "{{ tool.description|escapejs }}",
      "url": "{{ tool.url|escapejs }}"{% if tool.image %},
      "image": "{{ tool.image|escapejs }}"{% endif %}{% if tool.schema_kind == 'software' %},
      "operatingSystem": "Web"{% endif %}
    }{% if not forloop.last %},{% endif %}
    {% endfor %}
  ]
}
{% endjsonld %}
"""


def test_tools_jsonld_handles_schema_kinds():
    tools = [
        {"title": "App", "description": "A", "url": "/app/", "schema_kind": "software"},
        {"title": "Guide", "description": "G", "url": "/guide/", "schema_kind": "guide"},
    ]
    html = _render(TOOLS_TEMPLATE, {"tools": tools})
    data = _extract_json(html)
    app, guide = data["@graph"]
    assert app["@type"] == "SoftwareApplication"
    assert app["operatingSystem"] == "Web"
    assert guide["@type"] == "CreativeWork"
    assert "operatingSystem" not in guide


TOOL_DETAIL_TEMPLATE = """
{% load jsonld %}
{% jsonld %}
{
  "@context": "https://schema.org",
  "@type": "{% if tool.schema_kind == 'software' %}SoftwareApplication{% else %}CreativeWork{% endif %}",
  "name": "{{ tool.title|escapejs }}",
  "description": "{{ tool.description|escapejs }}",
  "url": "{{ tool.url|escapejs }}"{% if tool.image %},
  "image": "{{ tool.image|escapejs }}"{% endif %}{% if tool.schema_kind == 'software' %},
  "operatingSystem": "Web"{% endif %}
}
{% endjsonld %}
"""


def test_tool_detail_jsonld_handles_schema_kinds():
    tool = {"title": "App", "description": "A", "url": "/app/", "schema_kind": "software"}
    html = _render(TOOL_DETAIL_TEMPLATE, {"tool": tool})
    data = _extract_json(html)
    assert data["@type"] == "SoftwareApplication"
    assert data["operatingSystem"] == "Web"

    tool = {"title": "Guide", "description": "G", "url": "/guide/", "schema_kind": "guide"}
    html = _render(TOOL_DETAIL_TEMPLATE, {"tool": tool})
    data = _extract_json(html)
    assert data["@type"] == "CreativeWork"
    assert "operatingSystem" not in data
