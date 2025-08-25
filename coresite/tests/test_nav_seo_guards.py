import json
import re
from pathlib import Path

import pytest

TEMPLATE_ROOT = Path(__file__).resolve().parents[1] / "templates"
NAV_PARTIAL = TEMPLATE_ROOT / "coresite" / "partials" / "global" / "nav_links.html"
PILLAR_HREF_PATTERN = re.compile(r'href="/(knowledge|tools|case-studies|community|blog)/"')

SD_SENTINEL = "<!-- sd:canonical -->"

ROUTES = [
    ("/", 200),
    ("/blog/", 200),
    ("/case-studies/", 200),
    ("/nonexistent-page/", 404),
]


def _iter_templates():
    for path in TEMPLATE_ROOT.rglob("*.html"):
        if "partials" in path.parts or path.name.startswith("_"):
            continue
        yield path


def test_structured_data_block_presence():
    base = TEMPLATE_ROOT / "coresite" / "base.html"
    base_text = base.read_text()
    assert "{% block structured_data %}" in base_text, "base template missing structured_data block"

    missing = []
    for tpl in _iter_templates():
        text = tpl.read_text()
        if "{% block structured_data %}" in text:
            continue
        if "{% extends \"coresite/base.html\" %}" in text or "{% extends 'coresite/base.html' %}" in text:
            continue  # inherits from base
        missing.append(str(tpl.relative_to(TEMPLATE_ROOT)))
    assert not missing, f"Templates missing structured_data block: {missing}"


def test_no_pillar_links_outside_nav():
    offenders = []
    for tpl in TEMPLATE_ROOT.rglob("*.html"):
        if tpl == NAV_PARTIAL:
            continue
        text = tpl.read_text()
        for match in PILLAR_HREF_PATTERN.finditer(text):
            offenders.append(f"{tpl}:{match.group(0)}")
    assert not offenders, "Pillar links found outside nav_links.html:\n" + "\n".join(offenders)


@pytest.mark.parametrize("path,status", ROUTES)
def test_jsonld_single_and_centralised(path, status):
    django = pytest.importorskip("django")
    from django.test import Client
    from django.conf import settings
    settings.DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
    client = Client()
    resp = client.get(path)
    assert resp.status_code == status
    html = resp.content.decode()
    assert html.count(SD_SENTINEL) == 1, f"Sentinel missing or duplicated in {path}"
    scripts = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    assert len(scripts) == 1, f"Expected 1 JSON-LD script in {path}, found {len(scripts)}"
    json.loads(scripts[0])
