import base64
import tempfile
import pytest
from django.conf import settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from coresite.models import CaseStudy


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
@pytest.mark.django_db
def test_case_studies_page(client):
    img_bytes = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAAAASUVORK5CYII="
    )
    image = SimpleUploadedFile("gamma.png", img_bytes, content_type="image/png")
    CaseStudy.objects.create(title="Gamma", is_published=True, image=image)
    res = client.get(reverse("case_studies"))
    html = res.content.decode()
    expected = (
        "index,follow" if settings.CASE_STUDIES_INDEXABLE else "noindex,nofollow"
    )
    assert res["X-Robots-Tag"] == expected
    assert '<h1 id="case-studies-heading">Case Studies</h1>' in html
    assert '"@type": "BreadcrumbList"' in html
    assert 'data-analytics-event="case_study_card_click"' in html
    assert 'alt="Case study: Gamma"' in html


@pytest.mark.django_db
def test_case_study_detail_page(client):
    study = CaseStudy.objects.create(title="Alpha", summary="Summary", is_published=True)
    res = client.get(study.get_absolute_url())
    html = res.content.decode()
    expected = (
        "index,follow" if settings.CASE_STUDIES_INDEXABLE else "noindex,nofollow"
    )
    assert res["X-Robots-Tag"] == expected
    assert f'<h1 id="case-study-detail-heading">{study.title}</h1>' in html
    assert '<nav class="breadcrumbs"' in html
    assert '"@type": "Article"' in html
    assert '"@type": "BreadcrumbList"' in html
    assert '"inLanguage": "en"' in html
    assert '"datePublished":' in html
    assert 'http://testserver/case-studies/' in html


@pytest.mark.django_db
def test_case_study_preview_requires_staff(client):
    study = CaseStudy.objects.create(title="Alpha", summary="Summary", is_published=False)
    res = client.get(f"{study.get_absolute_url()}?preview=1")
    assert res.status_code == 404


@pytest.mark.django_db
def test_case_study_preview_staff_client(client):
    study = CaseStudy.objects.create(title="Alpha", summary="Summary", is_published=False)
    from django.contrib.auth.models import User
    User.objects.create_user("staff", "staff@example.com", "pass", is_staff=True)
    assert client.login(username="staff", password="pass")
    res = client.get(f"{study.get_absolute_url()}?preview=1")
    assert res.status_code == 200
