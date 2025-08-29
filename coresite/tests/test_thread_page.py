import json
import re
import pytest
from django.test import override_settings


@override_settings(SITE_BASE_URL="https://technofatty.com")
def test_thread_page_has_qapage_schema(client):
    res = client.get("/community/t/deploy-technofatty/")
    html = res.content.decode()
    assert '<link rel="canonical" href="/community/t/deploy-technofatty/">' in html
    match = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    assert match
    data = json.loads(match.group(1))
    types = {item["@type"] for item in data["@graph"]}
    assert "QAPage" in types


def test_thread_page_404(client):
    res = client.get("/community/t/does-not-exist/")
    assert res.status_code == 404


def test_no_accepted_answer_state(client):
    res = client.get("/community/t/api-authentication-options/")
    html = res.content.decode()
    assert "No accepted answer yet" in html
    match = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    assert match
    data = json.loads(match.group(1))
    qapage = next(item for item in data["@graph"] if item["@type"] == "QAPage")
    question = qapage["mainEntity"]
    assert question["acceptedAnswer"] is None
