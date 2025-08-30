import pytest
from django.urls import reverse
from django.utils import timezone
from django.core.management import call_command

from coresite.models import BlogPost, StatusChoices, PrimaryGoalChoices


@pytest.mark.django_db
def test_blog_post_renders_related_content(client):
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
        primary_goal=PrimaryGoalChoices.NEWSLETTER,
    )
    res = client.get(reverse("blog_post", args=[post.slug]))
    content = res.content.decode()
    assert "Related across TF" in content
    assert "From Knowledge" in content


@pytest.mark.django_db
def test_backfill_related_content_command():
    post = BlogPost.objects.create(
        title="Old Post",
        slug="old-post",
        status=StatusChoices.PUBLISHED,
        excerpt="excerpt",
        content="hello",
        published_at=timezone.now(),
        category_slug="general",
        category_title="General",
        tags=[{"slug": "deployment", "title": "Deployment"}],
        meta_title="Old Post",
        meta_description="Desc",
        og_image_url="https://example.com/og.png",
        twitter_image_url="https://example.com/tw.png",
        primary_goal=PrimaryGoalChoices.NEWSLETTER,
    )
    call_command("backfill_related_content")
    post.refresh_from_db()
    assert "<!-- related-content -->" in post.content
