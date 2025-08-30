import pytest
from django.urls import reverse
from django.utils import timezone
from coresite.models import BlogPost, StatusChoices


@pytest.mark.django_db
def test_blog_tag_page_renders_description_cta_and_related(client, settings):
    settings.SITE_BASE_URL = "https://technofatty.com"
    BlogPost.objects.create(
        title="Tag Post",
        slug="tag-post",
        status=StatusChoices.PUBLISHED,
        excerpt="excerpt",
        content="content",
        published_at=timezone.now(),
        category_slug="general",
        category_title="General",
        tags=[
            {
                "slug": "deployment",
                "title": "Deployment",
                "description": "About deployment",
            }
        ],
        meta_title="Tag Post",
        meta_description="Desc",
        og_image_url="https://example.com/og.png",
        twitter_image_url="https://example.com/tw.png",
    )

    response = client.get(reverse("blog_tag", args=["deployment"]))
    assert response.status_code == 200
    content = response.content.decode()
    assert "About deployment" in content
    assert "Subscribe for short, useful tech & music tips" in content
    assert "Related across TF" in content
    assert '"@type": "ItemList"' in content
    assert '<link rel="canonical" href="http://testserver/blog/tag/deployment/">' in content
