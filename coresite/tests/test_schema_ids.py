import json
import re
import pytest
from django.utils import timezone

from coresite.models import BlogPost, StatusChoices, PrimaryGoalChoices


def _extract_jsonld(html: str):
    match = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    assert match, "No JSON-LD script found"
    return json.loads(match.group(1))


def test_blog_post_schema_ids(client, db):
    BlogPost.objects.create(
        title="Test Post",
        slug="test-post",
        status=StatusChoices.PUBLISHED,
        published_at=timezone.now(),
        meta_title="Test Post",
        meta_description="Desc",
        og_image_url="https://example.com/og.png",
        twitter_image_url="https://example.com/tw.png",
        primary_goal=PrimaryGoalChoices.NEWSLETTER,
    )
    resp = client.get("/blog/test-post/")
    assert resp.status_code == 200
    data = _extract_jsonld(resp.content.decode())
    graph = data["@graph"]
    article = next(item for item in graph if item.get("@type") == "BlogPosting")
    assert article["@id"] == "https://technofatty.com/blog/test-post/#article"
    breadcrumb = next(item for item in graph if item.get("@type") == "BreadcrumbList")
    assert breadcrumb["@id"] == "https://technofatty.com/blog/test-post/#breadcrumb"


def test_case_studies_breadcrumb_id(client):
    resp = client.get("/case-studies/")
    assert resp.status_code == 200
    data = _extract_jsonld(resp.content.decode())
    assert data["@id"] == "https://technofatty.com/case-studies/#breadcrumb"


def test_support_faqpage_id(client):
    resp = client.get("/support/")
    assert resp.status_code == 200
    data = _extract_jsonld(resp.content.decode())
    assert data["@id"] == "https://technofatty.com/support/#webpage"
    assert data["@type"] == "FAQPage"

