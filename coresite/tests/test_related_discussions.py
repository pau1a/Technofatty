import pytest
from django.urls import reverse
from django.utils import timezone
from coresite.models import (
    KnowledgeCategory,
    KnowledgeTag,
    KnowledgeArticle,
    Tool,
    CaseStudy,
    BlogPost,
    StatusChoices,
)


@pytest.mark.django_db
def test_related_discussions_on_knowledge_article(client):
    cat = KnowledgeCategory.objects.create(title="Cat", slug="cat", status=StatusChoices.PUBLISHED)
    tag = KnowledgeTag.objects.create(name="Deployment", slug="deployment")
    art = KnowledgeArticle.objects.create(
        category=cat,
        title="Article",
        slug="article",
        status=StatusChoices.PUBLISHED,
        content="body",
        published_at=timezone.now(),
    )
    art.tags.add(tag)
    res = client.get(reverse("knowledge_article", args=[cat.slug, art.slug]))
    assert "Related discussions" in res.content.decode()


@pytest.mark.django_db
def test_related_discussions_on_tool_detail(client):
    tool = Tool.objects.create(title="TF CLI", slug="tf-cli", is_published=True)
    res = client.get(reverse("tool_detail", args=[tool.slug]))
    assert "Related discussions" in res.content.decode()


@pytest.mark.django_db
def test_related_discussions_on_case_study_detail(client):
    cs = CaseStudy.objects.create(title="ACME", slug="acme", is_published=True)
    res = client.get(reverse("case_study_detail", args=[cs.slug]))
    assert "Related discussions" in res.content.decode()


@pytest.mark.django_db
def test_related_discussions_on_blog_post(client):
    post = BlogPost.objects.create(
        title="Tag Post",
        slug="tag-post",
        status=StatusChoices.PUBLISHED,
        excerpt="excerpt",
        content="content",
        published_at=timezone.now(),
        category_slug="general",
        category_title="General",
        tags=[{"slug": "deployment", "title": "Deployment"}],
        meta_title="Tag Post",
        meta_description="Desc",
        og_image_url="https://example.com/og.png",
        twitter_image_url="https://example.com/tw.png",
    )
    res = client.get(reverse("blog_post", args=[post.slug]))
    assert "Related discussions" in res.content.decode()
