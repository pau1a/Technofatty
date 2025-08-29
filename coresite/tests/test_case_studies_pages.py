import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from coresite.models import CaseStudy


@pytest.mark.django_db
def test_case_studies_page(client):
    CaseStudy.objects.create(title="Alpha", is_published=True)
    res = client.get(reverse("case_studies"))
    html = res.content.decode()
    expected = (
        "index,follow" if settings.CASE_STUDIES_INDEXABLE else "noindex,nofollow"
    )
    assert res["X-Robots-Tag"] == expected
    assert '<h1 id="case-studies-heading">Case Studies</h1>' in html
    assert '"@type": "BreadcrumbList"' in html
    assert 'data-analytics-event="case_study_card_click"' in html


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
    assert '"@type": "Article"' in html


@pytest.mark.django_db
def test_case_study_preview_requires_staff(client):
    study = CaseStudy.objects.create(title="Alpha", summary="Summary", is_published=False)
    res = client.get(f"{study.get_absolute_url()}?preview=1")
    assert res.status_code == 404


@pytest.mark.django_db
def test_case_study_preview_staff_client(client):
    study = CaseStudy.objects.create(title="Alpha", summary="Summary", is_published=False)
    User = get_user_model()
    User.objects.create_user("staff", "staff@example.com", "pass", is_staff=True)
    assert client.login(username="staff", password="pass")
    res = client.get(f"{study.get_absolute_url()}?preview=1")
    assert res.status_code == 200
