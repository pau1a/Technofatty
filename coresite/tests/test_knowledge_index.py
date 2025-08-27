import pytest
from django.urls import reverse
from django.utils import timezone

from coresite.models import (
    KnowledgeCategory,
    KnowledgeArticle,
    KnowledgeTag,
    StatusChoices,
    SubtypeChoices,
)


@pytest.mark.django_db
def test_knowledge_index_renders_featured_and_pagination(client):
    category = KnowledgeCategory.objects.create(
        title="General", slug="general", status=StatusChoices.PUBLISHED
    )
    for i in range(10):
        KnowledgeArticle.objects.create(
            category=category,
            title=f"Article {i}",
            slug=f"article-{i}",
            status=StatusChoices.PUBLISHED,
            blurb="blurb",
            published_at=timezone.now(),
        )
    response = client.get(reverse("knowledge"))
    assert response.status_code == 200
    content = response.content.decode()
    assert "Article 9" in content
    assert "Article 8" in content
    assert f"?category={category.slug}" in content
    assert "?page=2" in content
    assert "knowledge-card--featured" in content
    assert "kn-filterbar" in content


@pytest.mark.django_db
def test_knowledge_index_second_page_has_no_featured(client):
    category = KnowledgeCategory.objects.create(
        title="General", slug="general", status=StatusChoices.PUBLISHED
    )
    for i in range(10):
        KnowledgeArticle.objects.create(
            category=category,
            title=f"Article {i}",
            slug=f"article-{i}",
            status=StatusChoices.PUBLISHED,
            blurb="blurb",
            published_at=timezone.now(),
        )
    response = client.get(reverse("knowledge") + "?page=2")
    assert response.status_code == 200
    content = response.content.decode()
    assert "knowledge-card--featured" not in content
    assert "Article 0" in content


@pytest.mark.django_db
def test_knowledge_index_empty_state(client):
    response = client.get(reverse("knowledge"))
    assert response.status_code == 200
    content = response.content.decode()
    assert "No articles published yet." in content
    assert "knowledge-grid" not in content
    assert "kn-filterbar" not in content


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


@pytest.mark.django_db
def test_published_article_auto_sets_published_at():
    category = KnowledgeCategory.objects.create(
        title="General", slug="general", status=StatusChoices.PUBLISHED
    )
    article = KnowledgeArticle.objects.create(
        category=category,
        title="Auto",
        slug="auto",
        status=StatusChoices.PUBLISHED,
    )
    assert article.published_at is not None


@pytest.mark.django_db
def test_future_articles_excluded_from_index(client):
    category = KnowledgeCategory.objects.create(
        title="General", slug="general", status=StatusChoices.PUBLISHED
    )
    KnowledgeArticle.objects.create(
        category=category,
        title="Future",
        slug="future",
        status=StatusChoices.PUBLISHED,
        published_at=timezone.now() + timezone.timedelta(days=1),
    )
    response = client.get(reverse("knowledge"))
    assert "Future" not in response.content.decode()


@pytest.mark.django_db
def test_knowledge_index_filters_combination(client):
    cat1 = KnowledgeCategory.objects.create(
        title="Cat1", slug="cat1", status=StatusChoices.PUBLISHED
    )
    cat2 = KnowledgeCategory.objects.create(
        title="Cat2", slug="cat2", status=StatusChoices.PUBLISHED
    )
    tag1 = KnowledgeTag.objects.create(name="Tag1", slug="tag1")
    tag2 = KnowledgeTag.objects.create(name="Tag2", slug="tag2")
    match = KnowledgeArticle.objects.create(
        category=cat1,
        title="Match",
        slug="match",
        status=StatusChoices.PUBLISHED,
        blurb="blurb",
        subtype=SubtypeChoices.GUIDE,
        reading_time=4,
        published_at=timezone.now(),
    )
    match.tags.add(tag1)
    other = KnowledgeArticle.objects.create(
        category=cat1,
        title="Other",
        slug="other",
        status=StatusChoices.PUBLISHED,
        blurb="blurb",
        subtype=SubtypeChoices.GUIDE,
        reading_time=10,
        published_at=timezone.now(),
    )
    other.tags.add(tag2)
    different_cat = KnowledgeArticle.objects.create(
        category=cat2,
        title="Different",
        slug="different",
        status=StatusChoices.PUBLISHED,
        blurb="blurb",
        subtype=SubtypeChoices.GUIDE,
        reading_time=4,
        published_at=timezone.now(),
    )
    different_cat.tags.add(tag1)

    url = (
        reverse("knowledge")
        + f"?category={cat1.slug}&tag={tag1.slug}&time=5&subtype=guide"
    )
    response = client.get(url)
    content = response.content.decode()
    assert "Match" in content
    assert "Other" not in content
    assert "Different" not in content


@pytest.mark.django_db
def test_knowledge_index_search_queries(client):
    category = KnowledgeCategory.objects.create(
        title="General", slug="general", status=StatusChoices.PUBLISHED
    )
    tag = KnowledgeTag.objects.create(name="Special", slug="special")
    article = KnowledgeArticle.objects.create(
        category=category,
        title="Foo Title",
        slug="foo",
        status=StatusChoices.PUBLISHED,
        blurb="Bar blurb",
        published_at=timezone.now(),
    )
    article.tags.add(tag)
    KnowledgeArticle.objects.create(
        category=category,
        title="Other",
        slug="other",
        status=StatusChoices.PUBLISHED,
        blurb="Different",
        published_at=timezone.now(),
    )

    res = client.get(reverse("knowledge") + "?q=foo")
    assert "Foo Title" in res.content.decode()
    assert "Other" not in res.content.decode()

    res = client.get(reverse("knowledge") + "?q=bar")
    assert "Foo Title" in res.content.decode()

    res = client.get(reverse("knowledge") + "?q=special")
    assert "Foo Title" in res.content.decode()


@pytest.mark.django_db
def test_filtered_results_set_noindex_header(client):
    category = KnowledgeCategory.objects.create(
        title="General", slug="general", status=StatusChoices.PUBLISHED
    )
    KnowledgeArticle.objects.create(
        category=category,
        title="Article", slug="article", status=StatusChoices.PUBLISHED,
        blurb="blurb", published_at=timezone.now(),
    )
    res = client.get(reverse("knowledge") + f"?category={category.slug}")
    assert res["X-Robots-Tag"] == "noindex,follow"
    assert '<meta name="robots" content="noindex,follow">' in res.content.decode()
