import pytest
from django.urls import reverse
from django.utils import timezone
from coresite.models import KnowledgeCategory, KnowledgeArticle, KnowledgeTag, StatusChoices


@pytest.mark.django_db
def test_related_articles_by_category(client):
    cat = KnowledgeCategory.objects.create(title="Cat", slug="cat", status=StatusChoices.PUBLISHED)
    art1 = KnowledgeArticle.objects.create(
        category=cat,
        title="A1",
        slug="a1",
        status=StatusChoices.PUBLISHED,
        content="text",
        published_at=timezone.now(),
    )
    art2 = KnowledgeArticle.objects.create(
        category=cat,
        title="A2",
        slug="a2",
        status=StatusChoices.PUBLISHED,
        content="text",
        published_at=timezone.now(),
    )
    response = client.get(reverse("knowledge_article", args=[cat.slug, art1.slug]))
    assert art2 in response.context["related_articles"]


@pytest.mark.django_db
def test_related_articles_by_tags(client):
    cat1 = KnowledgeCategory.objects.create(title="Cat1", slug="cat1", status=StatusChoices.PUBLISHED)
    cat2 = KnowledgeCategory.objects.create(title="Cat2", slug="cat2", status=StatusChoices.PUBLISHED)
    tag = KnowledgeTag.objects.create(name="Tag1", slug="tag1")
    art1 = KnowledgeArticle.objects.create(
        category=cat1,
        title="A1",
        slug="a1",
        status=StatusChoices.PUBLISHED,
        content="text",
        published_at=timezone.now(),
    )
    art1.tags.add(tag)
    art2 = KnowledgeArticle.objects.create(
        category=cat2,
        title="A2",
        slug="a2",
        status=StatusChoices.PUBLISHED,
        content="text",
        published_at=timezone.now(),
    )
    art2.tags.add(tag)
    response = client.get(reverse("knowledge_article", args=[cat1.slug, art1.slug]))
    assert art2 in response.context["related_articles"]
