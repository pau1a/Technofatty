import json
import re
import shutil
import subprocess
import textwrap
from types import SimpleNamespace

import pytest
from django.template.loader import render_to_string
from django.utils import timezone


@pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")
def test_blog_post_view_event():
    post = SimpleNamespace(
        title="Test Post",
        slug="test-post",
        date=timezone.now(),
        updated=timezone.now(),
        category_title="General",
        category_slug="general",
        category=SimpleNamespace(slug="general", title="General"),
        tags=[SimpleNamespace(slug="tag", title="Tag")],
        meta_title="Test Post",
        meta_description="Desc",
        excerpt="Excerpt",
        canonical_url="/blog/test-post/",
        og_image_url="https://example.com/og.png",
        twitter_image_url="https://example.com/tw.png",
    )
    html = render_to_string(
        "coresite/blog_detail.html",
        {
            "post": post,
            "page_id": "post",
            "page_title": post.title,
            "breadcrumbs": [],
            "blog_label": "Blog",
            "related_discussions": [],
            "canonical_url": post.canonical_url,
        },
    )
    script = next(
        m.group(1)
        for m in re.finditer(r"<script>(.*?)</script>", html, re.S)
        if "blog_post_view" in m.group(1)
    )
    node_script = textwrap.dedent(
        f"""
        var calls=[];
        var window={{tfSend:function(n,m){{calls.push([n,m]);}}}};
        var document={{events:{{}},addEventListener:function(n,f){{this.events[n]=f;if(n==='DOMContentLoaded')f();}},querySelector:function(){{return null;}}}};
        var location={{search:''}};
        {script}
        console.log(JSON.stringify(calls));
        """
    )
    result = subprocess.run(["node", "-e", node_script], capture_output=True, text=True, check=True)
    calls = json.loads(result.stdout.strip())
    assert calls[0][0] == "blog_post_view"
    assert calls[0][1]["post"] == post.slug
