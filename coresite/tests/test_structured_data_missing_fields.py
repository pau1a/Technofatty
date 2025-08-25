import pytest


def _render(template_str: str, context: dict | None = None) -> str:
    django = pytest.importorskip("django")
    from django.conf import settings
    from django.template import Context, Template

    if not settings.configured:
        settings.configure(TEMPLATES=[{"BACKEND": "django.template.backends.django.DjangoTemplates"}])
        django.setup()

    template = Template(template_str)
    return template.render(Context(context or {}))


def test_article_schema_missing_image_renders_empty():
    html = _render(
        """
        {% load jsonld %}
        {% if headline and image %}
        {% jsonld %}{"@type": "Article", "headline": "{{ headline }}", "image": "{{ image }}"}{% endjsonld %}
        {% endif %}
        """,
        {"headline": "Test headline"},
    )
    assert "<script" not in html.strip()


def test_organization_schema_missing_name_renders_empty():
    html = _render(
        """
        {% load jsonld %}
        {% if name and url %}
        {% jsonld %}{"@type": "Organization", "name": "{{ name }}", "url": "{{ url }}"}{% endjsonld %}
        {% endif %}
        """,
        {"url": "https://example.com"},
    )
    assert "<script" not in html.strip()


def test_faqpage_schema_missing_entities_renders_empty():
    html = _render(
        """
        {% load jsonld %}
        {% if main_entity %}
        {% jsonld %}{"@type": "FAQPage", "mainEntity": {{ main_entity }}}{% endjsonld %}
        {% endif %}
        """,
        {"main_entity": None},
    )
    assert "<script" not in html.strip()
