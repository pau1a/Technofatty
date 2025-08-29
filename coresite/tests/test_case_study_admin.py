import tempfile

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, override_settings
from django.urls import reverse

from coresite.models import CaseStudy


@pytest.fixture
def admin_client(db):
    User = get_user_model()
    User.objects.create_superuser("admin", "admin@example.com", "password")
    client = Client()
    assert client.login(username="admin", password="password")
    return client


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
def test_image_widget_preview(admin_client):
    image = SimpleUploadedFile(
        "test.jpg",
        b"\xff\xd8\xff\xd9",
        content_type="image/jpeg",
    )
    cs = CaseStudy.objects.create(title="Alpha", image=image)
    url = reverse("admin:coresite_casestudy_change", args=[cs.pk])
    resp = admin_client.get(url)
    assert cs.image.url in resp.content.decode()


def test_slug_prepopulated(admin_client):
    url = reverse("admin:coresite_casestudy_add")
    resp = admin_client.get(url)
    html = resp.content.decode()
    assert "data-source-field" in html


def test_preview_link(admin_client, settings):
    settings.STAGING_BASE_URL = "https://staging.example.com/"
    cs = CaseStudy.objects.create(title="Alpha", slug="alpha")
    url = reverse("admin:coresite_casestudy_change", args=[cs.pk])
    resp = admin_client.get(url)
    html = resp.content.decode()
    assert "https://staging.example.com/case-studies/alpha/?preview=1" in html

