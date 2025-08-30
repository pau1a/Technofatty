import tempfile
from urllib.parse import urlparse

from django.test import TestCase, override_settings
from django.conf import settings
from django.core.files.storage import default_storage
from PIL import Image

from coresite.models import BlogPost, PrimaryGoalChoices


@override_settings(
    DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage",
    MEDIA_ROOT=tempfile.mkdtemp(),
    MEDIA_URL="/media/",
    SITE_BASE_URL="https://example.com",
)
class SocialImageGenerationTests(TestCase):
    def _rel_path(self, url: str) -> str:
        parsed = urlparse(url)
        return parsed.path.replace(settings.MEDIA_URL, "", 1)

    def test_images_created_on_save(self):
        post = BlogPost.objects.create(
            title="My Branded Post", primary_goal=PrimaryGoalChoices.NEWSLETTER
        )
        rel = self._rel_path(post.og_image_url)
        assert post.og_image_url.startswith("https://example.com/media/social/")
        assert post.twitter_image_url.startswith("https://example.com/media/social/")
        assert default_storage.exists(rel)
        with default_storage.open(rel, "rb") as f:
            img = Image.open(f)
            assert img.size == (1200, 630)

    def test_regenerates_on_meta_title_change(self):
        post = BlogPost.objects.create(
            title="Title", meta_title="One", primary_goal=PrimaryGoalChoices.NEWSLETTER
        )
        first_url = post.og_image_url
        post.meta_title = "Two"
        post.save()
        assert post.og_image_url != first_url
