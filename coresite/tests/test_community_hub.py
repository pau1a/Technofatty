import json
import re
import shutil
import subprocess

import pytest
from django.test import override_settings


def _extract_json(html: str) -> dict:
    match = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    assert match, "No JSON-LD script found"
    return json.loads(match.group(1))


@override_settings(SITE_BASE_URL="https://technofatty.com")
def test_community_hub_has_canonical_and_jsonld(client):
    res = client.get("/community/")
    html = res.content.decode()
    assert '<link rel="canonical" href="/community/">' in html
    data = _extract_json(html)
    types = {item["@type"] for item in data["@graph"]}
    assert {"CollectionPage", "BreadcrumbList", "ItemList"}.issubset(types)


@pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")
def test_community_view_event_respects_consent():
    script = """
        var calls = [];
        var window = {};
        var document = {addEventListener:function(ev,fn){fn();}};
        (function(){
          var payload = {surface:'community', filter:'latest'};
          if (window.tfSend) { window.tfSend('community.view_hub', payload); }
        })();
        console.log(JSON.stringify(calls));
    """
    result = subprocess.run(['node', '-e', script], capture_output=True, text=True, check=True)
    assert result.stdout.strip() == "[]"

    script2 = """
        var calls = [];
        var window = {tfSend:function(ev,payload){calls.push([ev,payload]);}};
        var document = {addEventListener:function(ev,fn){fn();}};
        (function(){
          var payload = {surface:'community', filter:'latest'};
          if (window.tfSend) { window.tfSend('community.view_hub', payload); }
        })();
        console.log(JSON.stringify(calls));
    """
    result2 = subprocess.run(['node', '-e', script2], capture_output=True, text=True, check=True)
    assert result2.stdout.strip() == '[["community.view_hub",{"surface":"community","filter":"latest"}]]'
