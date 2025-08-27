import pytest

django = pytest.importorskip("django")
from django.conf import settings
from django.template import Context, Template


def render(template_string, context=None):
    tpl = Template(template_string)
    return tpl.render(Context(context or {}))


def test_canonical_tag_without_request():
    settings.SITE_BASE_URL = "https://example.com"
    out = render("{%% load seo_tags %%}{%% canonical_url '/foo/' as url %%}{{ url }}")
    assert out == "https://example.com/foo/"


def test_canonical_tag_missing_base():
    settings.SITE_BASE_URL = ""
    settings.SITE_CANONICAL_HOST = ""
    out = render("{%% load seo_tags %%}{%% canonical_url '/foo/' as url %%}{{ url }}")
    assert out == ""


def test_canonical_tag_prefers_request_host(rf, settings):
    settings.SITE_BASE_URL = "https://example.com"
    request = rf.get("/foo/", secure=True, HTTP_HOST="staging.example.com")
    out = render(
        "{%% load seo_tags %%}{%% canonical_url '/foo/' as url %%}{{ url }}",
        {"request": request},
    )
    assert out == "https://staging.example.com/foo/"
