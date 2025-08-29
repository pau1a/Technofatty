import pytest
from django.urls import reverse
from coresite.models import CaseStudy


@pytest.mark.django_db
def test_homepage_featured_grid_has_case_studies(client):
    CaseStudy.objects.create(title="Alpha", summary="Summary", is_published=True)
    res = client.get(reverse("home"))
    html = res.content.decode()
    assert 'data-analytics-event="case_study_card_click"' in html
    assert 'data-analytics-event="cta.case_studies.open"' in html
