import json
import re

import pytest
from django.utils import timezone

from coresite.context_processors import NAV_LINKS
from coresite.models import BlogPost, StatusChoices


def _extract_jsonld(html: str):
    match = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    assert match, "No JSON-LD script found"
    return json.loads(match.group(1))


@pytest.mark.django_db
def test_blog_post_breadcrumbs(client):
    post = BlogPost.objects.create(
        title="Test Bread",
        slug="test-bread",
        status=StatusChoices.PUBLISHED,
        published_at=timezone.now(),
        category_slug="test-cat",
        category_title="Test Cat",
        meta_title="Test Bread",
        meta_description="Desc",
        canonical_url="https://technofatty.com/blog/test-bread/",
        og_image_url="https://example.com/og.png",
        twitter_image_url="https://example.com/tw.png",
    )
    resp = client.get("/blog/test-bread/")
    assert resp.status_code == 200
    html = resp.content.decode()
    assert '<nav class="breadcrumbs"' in html
    blog_label = next(l["label"] for l in NAV_LINKS if l["url"] == "blog")
    assert f">{blog_label}</a>" in html
    assert "<li aria-current=\"page\">Test Bread</li>" in html

    data = _extract_jsonld(html)
    breadcrumb = next(item for item in data["@graph"] if item.get("@type") == "BreadcrumbList")
    items = breadcrumb["itemListElement"]
    assert items[1]["name"] == blog_label
    assert items[2]["name"] == "Test Cat"
    assert items[3]["name"] == "Test Bread"

