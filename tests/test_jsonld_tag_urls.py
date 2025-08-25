import json
import re
import pathlib
import sys
import pytest

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))


def _render(template_str: str, base: str | None = None) -> str:
    django = pytest.importorskip("django")
    from django.conf import settings
    from django.template import Context, Template

    if not settings.configured:
        settings.configure(
            TEMPLATES=[{"BACKEND": "django.template.backends.django.DjangoTemplates"}]
        )
        django.setup()

    if base is not None:
        settings.SITE_BASE_URL = base
    elif hasattr(settings, "SITE_BASE_URL"):
        delattr(settings, "SITE_BASE_URL")

    template = Template(template_str)
    return template.render(Context({}))


def _extract_json(html: str) -> dict:
    match = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    assert match, "No JSON-LD script found"
    return json.loads(match.group(1))


def test_relative_urls_become_absolute():
    html = _render(
        """
        {% load jsonld %}
        {% jsonld %}{"@type": "Thing", "url": "/foo", "image": {"url": "/img.png"}, "sameAs": [{"url": "/bar"}]}{% endjsonld %}
        """,
        base="https://example.com",
    )
    data = _extract_json(html)
    assert data["url"] == "https://example.com/foo"
    assert data["image"]["url"] == "https://example.com/img.png"
    assert data["sameAs"][0]["url"] == "https://example.com/bar"


def test_invalid_relative_url_skips_output():
    html = _render(
        """
        {% load jsonld %}
        {% jsonld %}{"@type": "Thing", "url": "/foo"}{% endjsonld %}
        """,
        base=None,
    )
    assert html.strip() == ""
