import re
import pytest
from django.urls import reverse


def test_tools_page_has_content(client):
    res = client.get(reverse("tools"))
    html = res.content.decode()
    assert "Get AI Growth Tips" in html
    assert 'aria-label="Open ROI Calculator"' in html
    assert 'aria-label="Open Content Ideator"' in html
    assert "Learn" in html
    assert "From the Blog" in html


def test_tools_page_section_has_no_region_role(client):
    res = client.get(reverse("tools"))
    html = res.content.decode()
    scaffold = re.search(r'<section class="section section--scaffold"[^>]*>', html)
    assert scaffold is not None
    assert "role=" not in scaffold.group(0)


def test_tool_button_has_analytics(client):
    res = client.get(reverse("tools"))
    html = res.content.decode()
    assert 'data-analytics-event="cta.tools.open"' in html
    assert 'data-analytics-meta="{\"tool\":\"roi-calculator\"}"' in html


def test_focus_style_exists_in_css():
    sass = pytest.importorskip("sass")
    css = sass.compile(filename="coresite/static/coresite/scss/main.scss")
    assert ".tools__link:focus-visible" in css
