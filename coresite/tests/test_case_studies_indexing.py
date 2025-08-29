import re
import pytest
from django.urls import reverse
from django.test import override_settings
from django.conf import settings
from coresite.models import CaseStudy


@pytest.mark.django_db
def test_case_studies_view_not_indexable(client):
    res = client.get(reverse("case_studies"))
    assert res["X-Robots-Tag"] == "noindex,nofollow"
    assert re.search(
        r'<meta\s+name="robots"\s+content="noindex,nofollow"\s*/?>',
        res.content.decode(),
        re.I,
    )


@override_settings(CASE_STUDIES_INDEXABLE=True)
@pytest.mark.django_db
def test_case_studies_view_indexable(client):
    res = client.get(reverse("case_studies"))
    assert res["X-Robots-Tag"] == "index,follow"
    assert re.search(
        r'<meta\s+name="robots"\s+content="index,follow"\s*/?>',
        res.content.decode(),
        re.I,
    )


@pytest.mark.django_db
def test_case_study_detail_view_not_indexable(client):
    study = CaseStudy.objects.create(title="Alpha", summary="Summary", is_published=True)
    res = client.get(study.get_absolute_url())
    assert res["X-Robots-Tag"] == "noindex,nofollow"
    assert re.search(
        r'<meta\s+name="robots"\s+content="noindex,nofollow"\s*/?>',
        res.content.decode(),
        re.I,
    )


@override_settings(CASE_STUDIES_INDEXABLE=True)
@pytest.mark.django_db
def test_case_study_detail_view_indexable(client):
    study = CaseStudy.objects.create(title="Alpha", summary="Summary", is_published=True)
    res = client.get(study.get_absolute_url())
    assert res["X-Robots-Tag"] == "index,follow"
    assert re.search(
        r'<meta\s+name="robots"\s+content="index,follow"\s*/?>',
        res.content.decode(),
        re.I,
    )


@pytest.mark.django_db
def test_sitemap_excludes_case_studies_when_not_indexable(client, settings):
    study = CaseStudy.objects.create(title="Alpha", summary="Summary", is_published=True)
    res = client.get(reverse("sitemap_xml"))
    xml = res.content.decode()
    assert f"{settings.SITE_BASE_URL}/case-studies/" not in xml
    assert f"{settings.SITE_BASE_URL}{study.get_absolute_url()}" not in xml


@override_settings(CASE_STUDIES_INDEXABLE=True)
@pytest.mark.django_db
def test_sitemap_includes_case_studies_when_indexable(client, settings):
    study = CaseStudy.objects.create(title="Alpha", summary="Summary", is_published=True)
    res = client.get(reverse("sitemap_xml"))
    xml = res.content.decode()
    assert f"{settings.SITE_BASE_URL}/case-studies/" in xml
    assert f"{settings.SITE_BASE_URL}{study.get_absolute_url()}" in xml
