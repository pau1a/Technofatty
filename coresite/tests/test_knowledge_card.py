import pytest
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.formats import date_format

from coresite.models import KnowledgeCategory, KnowledgeArticle, StatusChoices


@pytest.mark.django_db
def test_card_meta_and_placeholder_rendering():
    category = KnowledgeCategory.objects.create(
        title="General", slug="general", status=StatusChoices.PUBLISHED
    )
    article = KnowledgeArticle.objects.create(
        category=category,
        title="Sample",
        slug="sample",
        status=StatusChoices.PUBLISHED,
        published_at=timezone.now(),
        content="First paragraph."
    )
    html = render_to_string("coresite/knowledge/_card.html", {"article": article})
    assert "knowledge-card__image--placeholder" in html
    assert category.title in html
    assert date_format(article.published_at, "F j, Y") in html


@pytest.mark.django_db
def test_blurb_auto_generation_from_first_paragraph():
    category = KnowledgeCategory.objects.create(
        title="General", slug="general", status=StatusChoices.PUBLISHED
    )
    content = "First paragraph.\n\nSecond paragraph."
    article = KnowledgeArticle.objects.create(
        category=category,
        title="Auto",
        slug="auto",
        status=StatusChoices.DRAFT,
        content=content,
    )
    assert article.blurb == "First paragraph."
