import pytest
from django.urls import reverse

from coresite.models import KnowledgeCategory, KnowledgeArticle, StatusChoices


@pytest.mark.django_db
def test_knowledge_index_renders_featured_and_pagination(client):
    category = KnowledgeCategory.objects.create(
        title="General", slug="general", status=StatusChoices.PUBLISHED
    )
    for i in range(7):
        KnowledgeArticle.objects.create(
            category=category,
            title=f"Article {i}",
            slug=f"article-{i}",
            status=StatusChoices.PUBLISHED,
            blurb="blurb",
        )
    response = client.get(reverse("knowledge"))
    assert response.status_code == 200
    content = response.content.decode()
    assert "Article 6" in content
    assert "Article 5" in content
    assert f"/knowledge/{category.slug}/" in content
    assert "?page=2" in content


@pytest.mark.django_db
def test_knowledge_index_second_page_has_no_featured(client):
    category = KnowledgeCategory.objects.create(
        title="General", slug="general", status=StatusChoices.PUBLISHED
    )
    for i in range(7):
        KnowledgeArticle.objects.create(
            category=category,
            title=f"Article {i}",
            slug=f"article-{i}",
            status=StatusChoices.PUBLISHED,
            blurb="blurb",
        )
    response = client.get(reverse("knowledge") + "?page=2")
    assert response.status_code == 200
    content = response.content.decode()
    assert "knowledge-featured" not in content
    assert "Article 0" in content


@pytest.mark.django_db
def test_knowledge_index_empty_state(client):
    response = client.get(reverse("knowledge"))
    assert response.status_code == 200
    content = response.content.decode()
    assert "No articles published yet." in content
    assert "knowledge-grid" not in content


@pytest.mark.django_db
def test_knowledge_category_no_results(client):
    category = KnowledgeCategory.objects.create(
        title="General", slug="general", status=StatusChoices.PUBLISHED
    )
    response = client.get(reverse("knowledge_category", args=[category.slug]))
    assert response.status_code == 200
    content = response.content.decode()
    assert "No articles found for your selection." in content
    assert "knowledge-grid" not in content
