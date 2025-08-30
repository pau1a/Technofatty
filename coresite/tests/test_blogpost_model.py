import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from coresite.models import BlogPost, StatusChoices, PrimaryGoalChoices


@pytest.mark.django_db
def test_blogpost_slug_autogenerates_and_uniquifies():
    p1 = BlogPost.objects.create(title="My Post", primary_goal=PrimaryGoalChoices.NEWSLETTER)
    p2 = BlogPost.objects.create(title="My Post", primary_goal=PrimaryGoalChoices.NEWSLETTER)
    assert p1.slug == "my-post"
    assert p2.slug == "my-post-1"


@pytest.mark.django_db
def test_blogpost_manual_slug_normalised_and_uniquified():
    p1 = BlogPost.objects.create(title="First", slug="Custom Slug", primary_goal=PrimaryGoalChoices.NEWSLETTER)
    p2 = BlogPost.objects.create(title="Second", slug="Custom Slug", primary_goal=PrimaryGoalChoices.NEWSLETTER)
    assert p1.slug == "custom-slug"
    assert p2.slug == "custom-slug-1"


@pytest.mark.django_db
def test_published_blogpost_requires_meta_fields():
    post = BlogPost(
        title="Needs Meta",
        status=StatusChoices.PUBLISHED,
        published_at=timezone.now(),
        primary_goal=PrimaryGoalChoices.NEWSLETTER,
    )
    with pytest.raises(ValidationError) as excinfo:
        post.full_clean()
    assert "meta_title" in excinfo.value.message_dict
    assert "meta_description" in excinfo.value.message_dict
    assert "og_image_url" in excinfo.value.message_dict
    assert "twitter_image_url" in excinfo.value.message_dict


@pytest.mark.django_db
def test_blogpost_requires_primary_goal():
    post = BlogPost(title="No Goal")
    post.primary_goal = ""
    with pytest.raises(ValidationError):
        post.full_clean()
