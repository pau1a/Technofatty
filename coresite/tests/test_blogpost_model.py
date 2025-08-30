import pytest

from coresite.models import BlogPost


@pytest.mark.django_db
def test_blogpost_slug_autogenerates_and_uniquifies():
    p1 = BlogPost.objects.create(title="My Post")
    p2 = BlogPost.objects.create(title="My Post")
    assert p1.slug == "my-post"
    assert p2.slug == "my-post-1"


@pytest.mark.django_db
def test_blogpost_manual_slug_normalised_and_uniquified():
    p1 = BlogPost.objects.create(title="First", slug="Custom Slug")
    p2 = BlogPost.objects.create(title="Second", slug="Custom Slug")
    assert p1.slug == "custom-slug"
    assert p2.slug == "custom-slug-1"
