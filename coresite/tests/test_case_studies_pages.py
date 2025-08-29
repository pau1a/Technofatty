import pytest
from django.conf import settings
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
