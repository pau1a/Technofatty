import pytest
from django.urls import reverse
from coresite.models import CaseStudy


@pytest.mark.django_db
def test_case_studies_page(client):
    CaseStudy.objects.create(title="Alpha", is_published=True)
    res = client.get(reverse("case_studies"))
    html = res.content.decode()
    assert res["X-Robots-Tag"] == "noindex,nofollow"
    assert '<h1 id="case-studies-heading">Case Studies</h1>' in html
    assert '"@type": "BreadcrumbList"' in html


@pytest.mark.django_db
def test_case_study_detail_page(client):
    study = CaseStudy.objects.create(title="Alpha", summary="Summary", is_published=True)
    res = client.get(reverse("case_study_detail", kwargs={"slug": study.slug}))
    html = res.content.decode()
    assert res["X-Robots-Tag"] == "noindex,nofollow"
    assert f'<h1 id="case-study-detail-heading">{study.title}</h1>' in html
    assert '"@type": "Article"' in html
