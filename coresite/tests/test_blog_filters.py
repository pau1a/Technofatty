import pytest
from django.urls import reverse
from django.utils import timezone

from coresite.models import BlogPost, StatusChoices, PrimaryGoalChoices


@pytest.mark.django_db
def test_blog_filters_by_category_tag_time(client, settings):
    settings.SITE_BASE_URL = "https://technofatty.com"
    now = timezone.now()
    old = now - timezone.timedelta(days=400)

    BlogPost.objects.create(
        title="Recent Post",
        slug="recent-post",
        status=StatusChoices.PUBLISHED,
        excerpt="ex",
        content="ct",
        published_at=now,
        category_slug="tech",
        category_title="Tech",
        tags=[{"slug": "django", "title": "Django"}],
        meta_title="Recent Post",
        meta_description="Desc",
        og_image_url="https://example.com/og.png",
        twitter_image_url="https://example.com/tw.png",
        primary_goal=PrimaryGoalChoices.NEWSLETTER,
    )

    BlogPost.objects.create(
        title="Old Music",
        slug="old-music",
        status=StatusChoices.PUBLISHED,
        excerpt="ex",
        content="ct",
        published_at=old,
        category_slug="music",
        category_title="Music",
        tags=[{"slug": "guitar", "title": "Guitar"}],
        meta_title="Old Music",
        meta_description="Desc",
        og_image_url="https://example.com/og.png",
        twitter_image_url="https://example.com/tw.png",
        primary_goal=PrimaryGoalChoices.NEWSLETTER,
    )

    res = client.get(reverse("blog"), {"category": "tech"})
    content = res.content.decode()
    assert "Recent Post" in content and "Old Music" not in content

    res = client.get(reverse("blog"), {"tag": "guitar"})
    content = res.content.decode()
    assert "Old Music" in content and "Recent Post" not in content

    res = client.get(reverse("blog"), {"time": str(old.year)})
    content = res.content.decode()
    assert "Old Music" in content and "Recent Post" not in content

