import pytest
from django.urls import reverse
from django.utils import timezone

from coresite.models import (
    BlogPost,
    KnowledgeArticle,
    KnowledgeCategory,
    StatusChoices,
)


@pytest.mark.django_db
def test_blog_rss_feed(client):
    BlogPost.objects.create(
        title="Test Post",
        slug="test-post",
        status=StatusChoices.PUBLISHED,
        published_at=timezone.now(),
    )
    response = client.get(reverse("blog_rss"))
    assert response.status_code == 200
    assert b"<rss" in response.content
    assert b"<channel" in response.content


@pytest.mark.django_db
def test_blog_atom_feed(client):
    BlogPost.objects.create(
        title="Atom Post",
        slug="atom-post",
        status=StatusChoices.PUBLISHED,
        published_at=timezone.now(),
    )
    response = client.get(reverse("blog_atom"))
    assert response.status_code == 200
    assert b"<feed" in response.content


@pytest.mark.django_db
def test_blog_json_feed(client):
    BlogPost.objects.create(
        title="JSON Post",
        slug="json-post",
        status=StatusChoices.PUBLISHED,
        published_at=timezone.now(),
    )
    response = client.get(reverse("blog_json"))
    assert response.status_code == 200
    assert "items" in response.json()


@pytest.mark.django_db
def test_knowledge_rss_feed(client):
    category = KnowledgeCategory.objects.create(
        title="Cat",
        slug="cat",
        status=StatusChoices.PUBLISHED,
    )
    KnowledgeArticle.objects.create(
        category=category,
        title="Art",
        slug="art",
        status=StatusChoices.PUBLISHED,
        published_at=timezone.now(),
    )
    response = client.get(reverse("knowledge_rss"))
    assert response.status_code == 200
    assert b"<rss" in response.content


@pytest.mark.django_db
def test_knowledge_atom_feed(client):
    category = KnowledgeCategory.objects.create(
        title="AtomCat",
        slug="atomcat",
        status=StatusChoices.PUBLISHED,
    )
    KnowledgeArticle.objects.create(
        category=category,
        title="AtomArt",
        slug="atomart",
        status=StatusChoices.PUBLISHED,
        published_at=timezone.now(),
    )
    response = client.get(reverse("knowledge_atom"))
    assert response.status_code == 200
    assert b"<feed" in response.content


@pytest.mark.django_db
def test_knowledge_json_feed(client):
    category = KnowledgeCategory.objects.create(
        title="JsonCat",
        slug="jsoncat",
        status=StatusChoices.PUBLISHED,
    )
    KnowledgeArticle.objects.create(
        category=category,
        title="JsonArt",
        slug="jsonart",
        status=StatusChoices.PUBLISHED,
        published_at=timezone.now(),
    )
    response = client.get(reverse("knowledge_json"))
    assert response.status_code == 200
    assert "items" in response.json()
